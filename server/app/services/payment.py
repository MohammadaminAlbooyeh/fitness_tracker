from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException
import stripe
from decimal import Decimal

from app.models.payment import (
    Payment,
    ProfessionalPayout,
    ProfessionalBankAccount,
    PaymentMethod,
    PlatformFee,
    PaymentStatus
)
from app.core.config import settings
from app.services.notification import NotificationService

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    def __init__(self, db: Session, notification_service: NotificationService):
        self.db = db
        self.notification_service = notification_service

    def calculate_platform_fee(self, amount: float) -> float:
        """Calculate platform fee based on the amount."""
        fee = (
            self.db.query(PlatformFee)
            .filter(PlatformFee.is_active == True)
            .first()
        )

        if not fee:
            return 0.0

        if fee.fee_type == "percentage":
            calculated_fee = amount * (fee.fee_value / 100)
        else:
            calculated_fee = fee.fee_value

        if fee.min_fee and calculated_fee < fee.min_fee:
            return fee.min_fee
        if fee.max_fee and calculated_fee > fee.max_fee:
            return fee.max_fee

        return calculated_fee

    def create_payment_intent(
        self,
        consultation_id: int,
        client_id: int,
        professional_id: int,
        amount: float,
        currency: str = "USD",
        payment_method_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a payment intent."""
        try:
            platform_fee = self.calculate_platform_fee(amount)
            professional_share = amount - platform_fee

            # Create Stripe PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency.lower(),
                payment_method=payment_method_id,
                confirmation_method="manual",
                metadata={
                    "consultation_id": str(consultation_id),
                    "client_id": str(client_id),
                    "professional_id": str(professional_id)
                }
            )

            # Create payment record
            payment = Payment(
                consultation_id=consultation_id,
                client_id=client_id,
                professional_id=professional_id,
                amount=amount,
                platform_fee=platform_fee,
                professional_share=professional_share,
                currency=currency,
                status=PaymentStatus.PENDING,
                payment_method=payment_method_id,
                transaction_id=payment_intent.id,
                payment_details={
                    "stripe_payment_intent_id": payment_intent.id,
                    "client_secret": payment_intent.client_secret
                }
            )

            self.db.add(payment)
            self.db.commit()
            self.db.refresh(payment)

            return {
                "payment_id": payment.id,
                "client_secret": payment_intent.client_secret,
                "amount": amount,
                "currency": currency
            }

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error creating payment intent: {str(e)}"
            )

    def confirm_payment(
        self,
        payment_id: int,
        payment_intent_id: str
    ) -> Payment:
        """Confirm a payment."""
        payment = (
            self.db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        try:
            # Confirm the payment intent
            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)

            if payment_intent.status == "succeeded":
                payment.status = PaymentStatus.COMPLETED
                self.notification_service.send_payment_success(payment)
            else:
                payment.status = PaymentStatus.FAILED
                self.notification_service.send_payment_failure(payment)

            payment.payment_details["stripe_payment_status"] = payment_intent.status
            
            self.db.add(payment)
            self.db.commit()
            self.db.refresh(payment)

            return payment

        except stripe.error.StripeError as e:
            payment.status = PaymentStatus.FAILED
            payment.payment_details["error"] = str(e)
            self.db.add(payment)
            self.db.commit()

            raise HTTPException(
                status_code=400,
                detail=f"Error confirming payment: {str(e)}"
            )

    def process_refund(
        self,
        payment_id: int,
        amount: Optional[float] = None,
        reason: Optional[str] = None
    ) -> Payment:
        """Process a refund for a payment."""
        payment = (
            self.db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        if payment.status != PaymentStatus.COMPLETED:
            raise HTTPException(
                status_code=400,
                detail="Only completed payments can be refunded"
            )

        try:
            refund = stripe.Refund.create(
                payment_intent=payment.payment_details["stripe_payment_intent_id"],
                amount=int((amount or payment.amount) * 100),
                reason=reason
            )

            payment.status = PaymentStatus.REFUNDED
            payment.refund_details = {
                "refund_id": refund.id,
                "amount": amount or payment.amount,
                "reason": reason,
                "status": refund.status,
                "refunded_at": datetime.utcnow().isoformat()
            }

            self.db.add(payment)
            self.db.commit()
            self.db.refresh(payment)

            self.notification_service.send_refund_processed(payment)

            return payment

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing refund: {str(e)}"
            )

    def create_professional_payout(
        self,
        professional_id: int,
        amount: float,
        currency: str = "USD"
    ) -> ProfessionalPayout:
        """Create a payout for a professional."""
        try:
            bank_account = (
                self.db.query(ProfessionalBankAccount)
                .filter(
                    and_(
                        ProfessionalBankAccount.professional_id == professional_id,
                        ProfessionalBankAccount.is_default == True,
                        ProfessionalBankAccount.is_verified == True
                    )
                )
                .first()
            )

            if not bank_account:
                raise HTTPException(
                    status_code=400,
                    detail="No verified bank account found for professional"
                )

            # Create Stripe payout
            payout = stripe.Payout.create(
                amount=int(amount * 100),
                currency=currency.lower(),
                method="standard",
                metadata={
                    "professional_id": str(professional_id)
                }
            )

            # Create payout record
            professional_payout = ProfessionalPayout(
                professional_id=professional_id,
                amount=amount,
                currency=currency,
                status="pending",
                payout_method="bank_transfer",
                transaction_id=payout.id,
                payout_details={
                    "stripe_payout_id": payout.id,
                    "bank_account_id": bank_account.id,
                    "status": payout.status
                }
            )

            self.db.add(professional_payout)
            self.db.commit()
            self.db.refresh(professional_payout)

            self.notification_service.send_payout_initiated(professional_payout)

            return professional_payout

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error creating payout: {str(e)}"
            )

    def add_payment_method(
        self,
        client_id: int,
        payment_method_id: str
    ) -> PaymentMethod:
        """Add a payment method for a client."""
        try:
            # Retrieve payment method details from Stripe
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id)

            # Create payment method record
            new_payment_method = PaymentMethod(
                client_id=client_id,
                type=payment_method.type,
                provider_id=payment_method.id,
                card_last4=payment_method.card.last4,
                card_brand=payment_method.card.brand,
                card_exp_month=payment_method.card.exp_month,
                card_exp_year=payment_method.card.exp_year,
                metadata={
                    "stripe_payment_method_id": payment_method.id
                }
            )

            self.db.add(new_payment_method)
            self.db.commit()
            self.db.refresh(new_payment_method)

            return new_payment_method

        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error adding payment method: {str(e)}"
            )

    def get_payment_history(
        self,
        client_id: Optional[int] = None,
        professional_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[List[PaymentStatus]] = None
    ) -> List[Payment]:
        """Get payment history."""
        query = self.db.query(Payment)

        if client_id:
            query = query.filter(Payment.client_id == client_id)
        if professional_id:
            query = query.filter(Payment.professional_id == professional_id)
        if start_date:
            query = query.filter(Payment.created_at >= start_date)
        if end_date:
            query = query.filter(Payment.created_at <= end_date)
        if status:
            query = query.filter(Payment.status.in_(status))

        return query.order_by(Payment.created_at.desc()).all()

    def get_professional_earnings(
        self,
        professional_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get earnings statistics for a professional."""
        query = (
            self.db.query(Payment)
            .filter(
                and_(
                    Payment.professional_id == professional_id,
                    Payment.status == PaymentStatus.COMPLETED
                )
            )
        )

        if start_date:
            query = query.filter(Payment.created_at >= start_date)
        if end_date:
            query = query.filter(Payment.created_at <= end_date)

        total_earnings = (
            query.with_entities(func.sum(Payment.professional_share))
            .scalar() or 0
        )

        # Get monthly earnings
        monthly_earnings = (
            query.with_entities(
                func.date_trunc("month", Payment.created_at).label("month"),
                func.sum(Payment.professional_share).label("earnings")
            )
            .group_by("month")
            .order_by("month")
            .all()
        )

        return {
            "total_earnings": total_earnings,
            "monthly_earnings": [
                {
                    "month": entry[0].strftime("%Y-%m"),
                    "earnings": float(entry[1])
                }
                for entry in monthly_earnings
            ]
        }