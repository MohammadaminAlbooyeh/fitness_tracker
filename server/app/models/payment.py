from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from typing import Optional

from app.core.database import Base

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    CRYPTO = "crypto"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    amount = Column(Float)
    platform_fee = Column(Float)
    professional_share = Column(Float)
    currency = Column(String, default="USD")
    status = Column(SQLAlchemyEnum(PaymentStatus))
    payment_method = Column(SQLAlchemyEnum(PaymentMethod))
    transaction_id = Column(String, unique=True)
    payment_details = Column(JSON)
    refund_details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    consultation = relationship("Consultation", back_populates="payment")
    client = relationship("Client", back_populates="payments")
    professional = relationship("Professional", back_populates="payments")

class ProfessionalPayout(Base):
    __tablename__ = "professional_payouts"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    amount = Column(Float)
    currency = Column(String, default="USD")
    status = Column(String)  # pending, processing, completed, failed
    payout_method = Column(String)
    transaction_id = Column(String, unique=True)
    payout_details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    professional = relationship("Professional", back_populates="payouts")

class ProfessionalBankAccount(Base):
    __tablename__ = "professional_bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    account_holder_name = Column(String)
    bank_name = Column(String)
    account_number = Column(String)
    routing_number = Column(String)
    account_type = Column(String)  # checking, savings
    currency = Column(String, default="USD")
    is_default = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    professional = relationship("Professional", back_populates="bank_accounts")

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    type = Column(SQLAlchemyEnum(PaymentMethod))
    provider_id = Column(String)  # ID from payment provider (e.g., Stripe)
    card_last4 = Column(String)
    card_brand = Column(String)
    card_exp_month = Column(Integer)
    card_exp_year = Column(Integer)
    is_default = Column(Boolean, default=False)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = relationship("Client", back_populates="payment_methods")

class PlatformFee(Base):
    __tablename__ = "platform_fees"

    id = Column(Integer, primary_key=True, index=True)
    fee_type = Column(String)  # percentage, fixed
    fee_value = Column(Float)  # percentage or fixed amount
    min_fee = Column(Float, nullable=True)
    max_fee = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)