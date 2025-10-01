from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProfessionalStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"

class ProfessionalType(str, Enum):
    TRAINER = "trainer"
    NUTRITIONIST = "nutritionist"
    PHYSIOTHERAPIST = "physiotherapist"
    COACH = "coach"
    OTHER = "other"

class ConsultationType(str, Enum):
    IN_PERSON = "in_person"
    VIRTUAL = "virtual"
    BOTH = "both"

# Base Schemas
class SpecializationBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CertificationBase(BaseModel):
    name: str
    issuing_organization: str
    description: Optional[str] = None
    verification_url: Optional[str] = None
    expiry_required: bool = False

class ProfessionalServiceBase(BaseModel):
    name: str
    description: str
    duration: int
    price: float
    active: bool = True

# Create/Update Schemas
class SpecializationCreate(SpecializationBase):
    pass

class SpecializationUpdate(SpecializationBase):
    pass

class CertificationCreate(CertificationBase):
    pass

class CertificationUpdate(CertificationBase):
    pass

class ProfessionalCreate(BaseModel):
    professional_type: ProfessionalType
    consultation_type: ConsultationType
    bio: str
    experience_years: int
    hourly_rate: float
    insurance_info: Optional[str] = None
    website: Optional[str] = None
    consultation_url: Optional[str] = None
    max_clients: int = 0
    specialization_ids: List[int]
    certification_ids: List[int]

class ProfessionalUpdate(BaseModel):
    professional_type: Optional[ProfessionalType] = None
    consultation_type: Optional[ConsultationType] = None
    bio: Optional[str] = None
    experience_years: Optional[int] = None
    hourly_rate: Optional[float] = None
    insurance_info: Optional[str] = None
    website: Optional[str] = None
    consultation_url: Optional[str] = None
    max_clients: Optional[int] = None
    status: Optional[ProfessionalStatus] = None

class ProfessionalServiceCreate(ProfessionalServiceBase):
    pass

class ProfessionalServiceUpdate(ProfessionalServiceBase):
    pass

class AvailabilityCreate(BaseModel):
    day_of_week: int
    start_time: datetime
    end_time: datetime
    available: bool = True
    recurrence: bool = True

class AvailabilityUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    available: Optional[bool] = None
    recurrence: Optional[bool] = None

class ClientProgressNoteCreate(BaseModel):
    note_type: str
    content: str
    private: bool = True

class ClientProgressNoteUpdate(BaseModel):
    note_type: Optional[str] = None
    content: Optional[str] = None
    private: Optional[bool] = None

# Response Schemas
class SpecializationResponse(SpecializationBase):
    id: int
    sub_specializations: Optional[List['SpecializationResponse']] = None

    class Config:
        orm_mode = True

class CertificationResponse(CertificationBase):
    id: int

    class Config:
        orm_mode = True

class ProfessionalServiceResponse(ProfessionalServiceBase):
    id: int
    professional_id: int

    class Config:
        orm_mode = True

class AvailabilityResponse(BaseModel):
    id: int
    day_of_week: int
    start_time: datetime
    end_time: datetime
    available: bool
    recurrence: bool

    class Config:
        orm_mode = True

class ClientProgressNoteResponse(BaseModel):
    id: int
    note_type: str
    content: str
    created_at: datetime
    updated_at: datetime
    private: bool

    class Config:
        orm_mode = True

class ProfessionalResponse(BaseModel):
    id: int
    user_id: int
    professional_type: ProfessionalType
    status: ProfessionalStatus
    consultation_type: ConsultationType
    bio: str
    experience_years: int
    hourly_rate: float
    rating: float
    total_reviews: int
    verified: bool
    verification_date: Optional[datetime]
    insurance_info: Optional[str]
    website: Optional[str]
    consultation_url: Optional[str]
    max_clients: int
    current_clients: int
    specializations: List[SpecializationResponse]
    certifications: List[CertificationResponse]
    services: List[ProfessionalServiceResponse]
    availability: List[AvailabilityResponse]

    class Config:
        orm_mode = True

# Additional Schemas for specific endpoints
class ProfessionalSearchParams(BaseModel):
    professional_type: Optional[ProfessionalType] = None
    specialization_ids: Optional[List[int]] = None
    max_hourly_rate: Optional[float] = None
    consultation_type: Optional[ConsultationType] = None
    rating_min: Optional[float] = None
    available_on: Optional[datetime] = None

class ProfessionalStats(BaseModel):
    total_clients: int
    total_sessions: int
    average_rating: float
    total_earnings: float
    client_retention_rate: float
    completion_rate: float