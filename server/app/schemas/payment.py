from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from decimal import Decimal

class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(..., max_length=3)

class PaymentCreate(PaymentBase):
    consultation_id: int
    professional_id: int
    payment_method_id: Optional[str] = None

class PaymentResponse(BaseModel):
    payment_id: int
    client_secret: str
    amount: float
    currency: str

    class Config:
        orm_mode = True

class PaymentMethodCreate(BaseModel):
    payment_method_id: str

class PaymentMethodResponse(BaseModel):
    id: int
    type: str
    card_last4: str
    card_brand: str
    card_exp_month: int
    card_exp_year: int
    is_default: bool
    created_at: datetime

    class Config:
        orm_mode = True

class PaymentHistoryResponse(BaseModel):
    id: int
    consultation_id: int
    client_id: int
    professional_id: int
    amount: float
    platform_fee: float
    professional_share: float
    currency: str
    status: str
    payment_method: Optional[str]
    transaction_id: str
    created_at: datetime
    updated_at: datetime
    refund_details: Optional[Dict[str, Any]]

    class Config:
        orm_mode = True

class MonthlyEarnings(BaseModel):
    month: str
    earnings: float

class ProfessionalEarningsResponse(BaseModel):
    total_earnings: float
    monthly_earnings: List[MonthlyEarnings]

class RefundCreate(BaseModel):
    amount: Optional[float] = None
    reason: Optional[str] = None

class PayoutCreate(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(..., max_length=3)

class PayoutResponse(BaseModel):
    id: int
    professional_id: int
    amount: float
    currency: str
    status: str
    payout_method: str
    transaction_id: str
    created_at: datetime
    payout_details: Dict[str, Any]

    class Config:
        orm_mode = True