from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Table, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from typing import Optional

from app.db.base_class import Base

# Many-to-many relationship tables
professional_specializations = Table(
    'professional_specializations',
    Base.metadata,
    Column('professional_id', Integer, ForeignKey('professionals.id'), primary_key=True),
    Column('specialization_id', Integer, ForeignKey('specializations.id'), primary_key=True)
)

professional_certifications = Table(
    'professional_certifications',
    Base.metadata,
    Column('professional_id', Integer, ForeignKey('professionals.id'), primary_key=True),
    Column('certification_id', Integer, ForeignKey('certifications.id'), primary_key=True)
)

class ProfessionalStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"

class ProfessionalType(str, enum.Enum):
    TRAINER = "trainer"
    NUTRITIONIST = "nutritionist"
    PHYSIOTHERAPIST = "physiotherapist"
    COACH = "coach"
    OTHER = "other"

class ConsultationType(str, enum.Enum):
    IN_PERSON = "in_person"
    VIRTUAL = "virtual"
    BOTH = "both"

class Professional(Base):
    __tablename__ = "professionals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    professional_type = Column(Enum(ProfessionalType))
    status = Column(Enum(ProfessionalStatus), default=ProfessionalStatus.PENDING)
    consultation_type = Column(Enum(ConsultationType), default=ConsultationType.BOTH)
    bio = Column(Text)
    experience_years = Column(Integer)
    hourly_rate = Column(Float)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
    verification_date = Column(DateTime, nullable=True)
    insurance_info = Column(String, nullable=True)
    website = Column(String, nullable=True)
    consultation_url = Column(String, nullable=True)
    max_clients = Column(Integer, default=0)
    current_clients = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="professional_profile")
    specializations = relationship("Specialization", secondary=professional_specializations)
    certifications = relationship("Certification", secondary=professional_certifications)
    availability = relationship("ProfessionalAvailability", back_populates="professional")
    clients = relationship("ClientProfessional", back_populates="professional")
    appointments = relationship("ProfessionalAppointment", back_populates="professional")
    reviews = relationship("ProfessionalReview", back_populates="professional")
    services = relationship("ProfessionalService", back_populates="professional")

class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("specializations.id"), nullable=True)
    
    # Self-referential relationship for hierarchical specializations
    sub_specializations = relationship("Specialization")

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    issuing_organization = Column(String)
    description = Column(Text, nullable=True)
    verification_url = Column(String, nullable=True)
    expiry_required = Column(Boolean, default=False)

class ProfessionalAvailability(Base):
    __tablename__ = "professional_availability"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    day_of_week = Column(Integer)  # 0-6 for Monday-Sunday
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    available = Column(Boolean, default=True)
    recurrence = Column(Boolean, default=True)
    
    # Relationships
    professional = relationship("Professional", back_populates="availability")

class ClientProfessional(Base):
    __tablename__ = "client_professionals"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    client = relationship("User", foreign_keys=[client_id])
    professional = relationship("Professional", back_populates="clients")
    progress_notes = relationship("ClientProgressNote", back_populates="client_professional")

class ProfessionalAppointment(Base):
    __tablename__ = "professional_appointments"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    client_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    consultation_type = Column(Enum(ConsultationType))
    status = Column(String)  # scheduled, completed, cancelled, etc.
    notes = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    meeting_url = Column(String, nullable=True)
    payment_status = Column(String)
    amount = Column(Float)
    
    # Relationships
    professional = relationship("Professional", back_populates="appointments")
    client = relationship("User")

class ProfessionalReview(Base):
    __tablename__ = "professional_reviews"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    client_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Float)
    review = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verified = Column(Boolean, default=False)
    
    # Relationships
    professional = relationship("Professional", back_populates="reviews")
    client = relationship("User")

class ProfessionalService(Base):
    __tablename__ = "professional_services"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    name = Column(String)
    description = Column(Text)
    duration = Column(Integer)  # in minutes
    price = Column(Float)
    active = Column(Boolean, default=True)
    
    # Relationships
    professional = relationship("Professional", back_populates="services")

class ClientProgressNote(Base):
    __tablename__ = "client_progress_notes"

    id = Column(Integer, primary_key=True, index=True)
    client_professional_id = Column(Integer, ForeignKey("client_professionals.id"))
    note_type = Column(String)  # assessment, progress, plan, etc.
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    private = Column(Boolean, default=True)  # Whether the note is visible to the client
    
    # Relationships
    client_professional = relationship("ClientProfessional", back_populates="progress_notes")