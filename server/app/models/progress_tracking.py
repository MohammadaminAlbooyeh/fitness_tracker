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

class UserMeasurement(Base):
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

class ProgressPhoto(Base):
    __tablename__ = 'progress_photos'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    photo_url = Column(String(255), nullable=False)
    photo_type = Column(String(20), nullable=False)  # front, side, back
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(String(500))
    measurements = Column(JSON)  # Optional associated measurements

    # Relationships
    user = relationship("User", back_populates="progress_photos")

class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    icon_url = Column(String(255))
    category = Column(String(50))  # workout, progress, nutrition, etc.
    criteria = Column(JSON)  # Achievement criteria in JSON format
    points = Column(Integer, default=0)

class UserAchievement(Base):
    __tablename__ = 'user_achievements'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), nullable=False)
    earned_date = Column(DateTime, default=datetime.utcnow)
    progress = Column(JSON)  # Current progress towards achievement

    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement")

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