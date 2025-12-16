from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from ..database.database import Base
from datetime import datetime

# Note: Achievement model is defined in achievements.py
# Importing here would cause circular dependency, so routes should import from achievements

class UserStreak(Base):
    __tablename__ = "user_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_workout_date = Column(DateTime)
    
    # Relationship
    user = relationship("User", back_populates="streak")

class UserPoints(Base):
    __tablename__ = "user_points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    points_to_next_level = Column(Integer, default=100)
    
    # Relationship
    user = relationship("User", back_populates="points")