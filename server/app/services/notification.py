from typing import Optional, Dict, Any
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from app.models.payment import Payment, ProfessionalPayout
from app.models.user import User

class NotificationService:
    def __init__(self, background_tasks: Optional[BackgroundTasks] = None):
        self.background_tasks = background_tasks
        self.mail_config = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_TLS=settings.MAIL_TLS,
            MAIL_SSL=settings.MAIL_SSL,
            USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS
        )
        self.fastmail = FastMail(self.mail_config)

    async def _send_email(
        self,
        subject: str,
        recipients: list[str],
        body: str,
        template_name: Optional[str] = None,
        template_data: Optional[Dict[str, Any]] = None
    ):
        """Send an email using FastMail."""
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            template_body=template_data or {}
        )

        if self.background_tasks:
            self.background_tasks.add_task(
                self.fastmail.send_message,
                message,
                template_name=template_name
            )
        else:
            await self.fastmail.send_message(
                message,
                template_name=template_name
            )

    def send_payment_success(self, payment: Payment):
        """Send payment success notification."""
        subject = "Payment Successful"
        template_data = {
            "payment_id": payment.id,
            "amount": payment.amount,
            "currency": payment.currency,
            "date": payment.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Notify client
        self._send_email(
            subject=subject,
            recipients=[payment.client.email],
            body="Your payment was successful",
            template_name="payment_success_client.html",
            template_data=template_data
        )

        # Notify professional
        self._send_email(
            subject=f"New Payment Received - {payment.amount} {payment.currency}",
            recipients=[payment.professional.email],
            body="You received a new payment",
            template_name="payment_success_professional.html",
            template_data=template_data
        )

    def send_payment_failure(self, payment: Payment):
        """Send payment failure notification."""
        subject = "Payment Failed"
        template_data = {
            "payment_id": payment.id,
            "amount": payment.amount,
            "currency": payment.currency,
            "date": payment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "error": payment.payment_details.get("error", "Unknown error")
        }

        # Notify client
        self._send_email(
            subject=subject,
            recipients=[payment.client.email],
            body="Your payment failed",
            template_name="payment_failure.html",
            template_data=template_data
        )

    def send_refund_processed(self, payment: Payment):
        """Send refund notification."""
        subject = "Refund Processed"
        template_data = {
            "payment_id": payment.id,
            "refund_amount": payment.refund_details["amount"],
            "currency": payment.currency,
            "date": payment.refund_details["refunded_at"],
            "reason": payment.refund_details.get("reason", "Not specified")
        }

        # Notify client
        self._send_email(
            subject=subject,
            recipients=[payment.client.email],
            body="Your refund has been processed",
            template_name="refund_processed_client.html",
            template_data=template_data
        )

        # Notify professional
        self._send_email(
            subject=f"Refund Processed - {payment.amount} {payment.currency}",
            recipients=[payment.professional.email],
            body="A refund has been processed",
            template_name="refund_processed_professional.html",
            template_data=template_data
        )

    def send_payout_initiated(self, payout: ProfessionalPayout):
        """Send payout initiated notification."""
        subject = "Payout Initiated"
        template_data = {
            "payout_id": payout.id,
            "amount": payout.amount,
            "currency": payout.currency,
            "date": payout.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "estimated_arrival": "2-3 business days"
        }

        self._send_email(
            subject=subject,
            recipients=[payout.professional.email],
            body="Your payout has been initiated",
            template_name="payout_initiated.html",
            template_data=template_data
        )

    def send_low_balance_alert(
        self,
        professional: User,
        current_balance: float,
        currency: str
    ):
        """Send low balance alert."""
        subject = "Low Balance Alert"
        template_data = {
            "current_balance": current_balance,
            "currency": currency,
            "threshold": settings.LOW_BALANCE_THRESHOLD
        }

        self._send_email(
            subject=subject,
            recipients=[professional.email],
            body="Your account balance is low",
            template_name="low_balance_alert.html",
            template_data=template_data
        )

    def send_payout_failed(self, payout: ProfessionalPayout):
        """Send payout failure notification."""
        subject = "Payout Failed"
        template_data = {
            "payout_id": payout.id,
            "amount": payout.amount,
            "currency": payout.currency,
            "date": payout.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "error": payout.payout_details.get("error", "Unknown error")
        }

        self._send_email(
            subject=subject,
            recipients=[payout.professional.email],
            body="Your payout failed",
            template_name="payout_failed.html",
            template_data=template_data
        )