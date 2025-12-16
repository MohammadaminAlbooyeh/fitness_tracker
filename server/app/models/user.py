from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base
from .achievements import user_achievements

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    full_name = Column(String)
    
    # Basic relationships
    workouts = relationship("Workout", back_populates="user")
    workout_logs = relationship("WorkoutLog", back_populates="user")
    
    # Gamification relationships
    achievements = relationship("Achievement", secondary=user_achievements, back_populates="users")
    streak = relationship("UserStreak", back_populates="user", uselist=False)
    points = relationship("UserPoints", back_populates="user", uselist=False)
    
    # Progress tracking relationships
    body_measurements = relationship("BodyMeasurement", back_populates="user")
    progress_photos = relationship("ProgressPhoto", back_populates="user")