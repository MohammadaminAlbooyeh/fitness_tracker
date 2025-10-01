from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.payment import PaymentService
from app.services.notification import NotificationService
from app.models.user import User
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentMethodCreate,
    PaymentMethodResponse,
    PaymentHistoryResponse,
    ProfessionalEarningsResponse,
    RefundCreate,
    PayoutCreate,
    PayoutResponse
)

router = APIRouter()

@router.post("/payment-intent", response_model=PaymentResponse)
def create_payment_intent(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a payment intent for a consultation."""
    payment_service = PaymentService(
        db=db,
        notification_service=NotificationService()
    )

    result = payment_service.create_payment_intent(
        consultation_id=payment_data.consultation_id,
        client_id=current_user.id,
        professional_id=payment_data.professional_id,
        amount=payment_data.amount,
        currency=payment_data.currency,
        payment_method_id=payment_data.payment_method_id
    )

    return result

@router.post("/payment-methods", response_model=PaymentMethodResponse)
def add_payment_method(
    payment_method_data: PaymentMethodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new payment method for the current user."""
    payment_service = PaymentService(
        db=db,
        notification_service=NotificationService()
    )

    payment_method = payment_service.add_payment_method(
        client_id=current_user.id,
        payment_method_id=payment_method_data.payment_method_id
    )

    return payment_method

@router.post("/payments/{payment_id}/confirm")
def confirm_payment(
    payment_id: int,
    payment_intent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Confirm a payment."""
    payment_service = PaymentService(
        db=db,
        notification_service=NotificationService()
    )

    payment = payment_service.confirm_payment(
        payment_id=payment_id,
        payment_intent_id=payment_intent_id
    )

    # Verify the payment belongs to the current user
    if (
        current_user.id != payment.client_id
        and current_user.id != payment.professional_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to confirm this payment"
        )

    return {"status": "success", "payment": payment}

@router.post("/payments/{payment_id}/refund", response_model=PaymentResponse)
def refund_payment(
    payment_id: int,
    refund_data: RefundCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Process a refund for a payment."""
    payment_service = PaymentService(
        db=db,
        notification_service=NotificationService()
    )

    payment = payment_service.process_refund(
        payment_id=payment_id,
        amount=refund_data.amount,
        reason=refund_data.reason
    )

    # Verify the refund is authorized
    if (
        current_user.id != payment.client_id
        and current_user.id != payment.professional_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to refund this payment"
        )

    return payment

@router.get("/payments/history", response_model=List[PaymentHistoryResponse])
def get_payment_history(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    status: Optional[List[str]] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get payment history for the current user."""
    payment_service = PaymentService(
        db=db,
        notification_service=NotificationService()
    )

    if current_user.role == "client":
        payments = payment_service.get_payment_history(
            client_id=current_user.id,
            start_date=start_date,
            end_date=end_date,
            status=status
        )
    else:
        payments = payment_service.get_payment_history(
            professional_id=current_user.id,
            start_date=start_date,
            end_date=end_date,
            status=status
        )

    return payments

@router.get(
    "/professionals/earnings",
    response_model=ProfessionalEarningsResponse
)
def get_professional_earnings(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get earnings statistics for a professional."""
    if current_user.role != "professional":
        raise HTTPException(
            status_code=403,
            detail="Only professionals can access earnings"
        )

    payment_service = PaymentService(
        db=db,
        notification_service=NotificationService()
    )

    earnings = payment_service.get_professional_earnings(
        professional_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

    return earnings

@router.post("/professionals/payouts", response_model=PayoutResponse)
def create_payout(
    payout_data: PayoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a payout for a professional."""
    if current_user.role != "professional":
        raise HTTPException(
            status_code=403,
            detail="Only professionals can create payouts"
        )

    payment_service = PaymentService(
        db=db,
        notification_service=NotificationService()
    )

    payout = payment_service.create_professional_payout(
        professional_id=current_user.id,
        amount=payout_data.amount,
        currency=payout_data.currency
    )

    return payout