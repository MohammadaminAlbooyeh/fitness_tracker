from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database.database import Base
from datetime import datetime

class BodyMeasurement(Base):
    __tablename__ = "body_measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    
    # Basic measurements
    weight = Column(Float)  # in kg
    height = Column(Float)  # in cm
    
    # Body composition
    body_fat = Column(Float)  # percentage
    muscle_mass = Column(Float)  # in kg
    
    # Circumference measurements
    chest = Column(Float)  # in cm
    waist = Column(Float)  # in cm
    hips = Column(Float)  # in cm
    biceps_left = Column(Float)  # in cm
    biceps_right = Column(Float)  # in cm
    thigh_left = Column(Float)  # in cm
    thigh_right = Column(Float)  # in cm
    
    # Relationships
    user = relationship("User", back_populates="body_measurements")