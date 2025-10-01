from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean, Enum as SQLAlchemyEnum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

from app.core.database import Base
from app.schemas.professional import ConsultationType

class ConsultationStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ConsultationNoteType(str, Enum):
    PROGRESS = "progress"
    ASSESSMENT = "assessment"
    PLAN = "plan"
    FEEDBACK = "feedback"
    OTHER = "other"

class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    consultation_type = Column(SQLAlchemyEnum(ConsultationType))
    status = Column(SQLAlchemyEnum(ConsultationStatus))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)  # in minutes
    meeting_url = Column(String, nullable=True)
    recording_url = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    client_feedback = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    professional = relationship("Professional", back_populates="consultations")
    client = relationship("Client", back_populates="consultations")
    appointment = relationship("Appointment", back_populates="consultation")
    notes = relationship("ConsultationNote", back_populates="consultation")
    attachments = relationship("ConsultationAttachment", back_populates="consultation")
    goals = relationship("ConsultationGoal", back_populates="consultation")

class ConsultationNote(Base):
    __tablename__ = "consultation_notes"

    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    note_type = Column(SQLAlchemyEnum(ConsultationNoteType))
    content = Column(Text)
    is_private = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    consultation = relationship("Consultation", back_populates="notes")

class ConsultationAttachment(Base):
    __tablename__ = "consultation_attachments"

    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    file_name = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    file_url = Column(String)
    is_private = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    consultation = relationship("Consultation", back_populates="attachments")

class ConsultationGoal(Base):
    __tablename__ = "consultation_goals"

    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    title = Column(String)
    description = Column(Text)
    target_date = Column(DateTime)
    status = Column(String)  # e.g., "not_started", "in_progress", "completed"
    progress = Column(Float)
    metrics = Column(JSON)  # For tracking measurable goals
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    consultation = relationship("Consultation", back_populates="goals")

class ConsultationTemplate(Base):
    __tablename__ = "consultation_templates"

    id = Column(Integer, primary_key=True, index=True)
    professional_id = Column(Integer, ForeignKey("professionals.id"))
    name = Column(String)
    description = Column(Text)
    structure = Column(JSON)  # Template structure with sections and prompts
    default_duration = Column(Integer)  # in minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    professional = relationship("Professional", back_populates="consultation_templates")