from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database.database import Base

class AIModel(Base):
    __tablename__ = "ai_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    version = Column(String)
    type = Column(String)  # workout_recommender, form_checker, etc.
    parameters = Column(JSON)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkoutRecommendation(Base):
    __tablename__ = "workout_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model_id = Column(Integer, ForeignKey("ai_models.id"))
    workout_plan = Column(JSON)
    confidence_score = Column(Float)
    accepted = Column(Boolean, default=False)
    feedback = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="workout_recommendations")
    model = relationship("AIModel")

class FormCheck(Base):
    __tablename__ = "form_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    model_id = Column(Integer, ForeignKey("ai_models.id"))
    video_url = Column(String)
    analysis = Column(JSON)  # Joint angles, posture metrics, etc.
    feedback = Column(JSON)  # Specific feedback points
    score = Column(Float)  # Overall form score
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="form_checks")
    exercise = relationship("Exercise", back_populates="form_checks")
    model = relationship("AIModel")

class SmartAdjustment(Base):
    __tablename__ = "smart_adjustments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model_id = Column(Integer, ForeignKey("ai_models.id"))
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    original_plan = Column(JSON)
    adjusted_plan = Column(JSON)
    adjustment_reason = Column(String)
    applied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="smart_adjustments")
    model = relationship("AIModel")
    workout = relationship("Workout")