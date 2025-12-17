from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.database import Base
import enum

class MeasurementType(str, enum.Enum):
    WEIGHT = 'weight'
    BODY_FAT = 'body_fat'
    CHEST = 'chest'
    WAIST = 'waist'
    HIPS = 'hips'
    BICEPS = 'biceps'
    THIGHS = 'thighs'
    CUSTOM = 'custom'

class Measurement(Base):
    __tablename__ = 'user_measurements'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    measurement_type = Column(String(20), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(10), nullable=False)  # kg, cm, %, etc.
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String(500))
    custom_name = Column(String(50))  # For custom measurements

    # Relationships
    user = relationship("User", back_populates="measurements")

# Note: Achievement and UserAchievement models are defined in achievements.py
# Note: ProgressPhoto model is defined in progress_photos.py

class PerformanceMetric(Base):
    __tablename__ = 'performance_metrics'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    metric_type = Column(String(50), nullable=False)  # strength, endurance, power, etc.
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    notes = Column(String(500))
    context = Column(JSON)  # Additional context like weight used, reps, etc.

    # Relationships
    user = relationship("User", back_populates="performance_metrics")
    exercise = relationship("Exercise")