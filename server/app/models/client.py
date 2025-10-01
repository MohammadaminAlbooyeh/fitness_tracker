from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.schemas.professional import ConsultationType

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    height = Column(Float)
    weight = Column(Float)
    fitness_level = Column(String)
    health_conditions = Column(JSON)
    goals = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="client")
    preferences = relationship("ClientPreferences", back_populates="client", uselist=False)

class ClientPreferences(Base):
    __tablename__ = "client_preferences"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), unique=True)
    preferred_consultation_type = Column(SQLAlchemyEnum(ConsultationType))
    max_budget = Column(Float)
    preferred_times = Column(JSON)  # List of preferred time slots
    location = Column(JSON)  # {latitude: float, longitude: float}
    preferred_gender = Column(String, nullable=True)
    language_preferences = Column(JSON)  # List of preferred languages
    specialization_ids = Column(JSON)  # List of preferred specialization IDs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = relationship("Client", back_populates="preferences")