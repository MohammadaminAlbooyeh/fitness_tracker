from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database.database import Base

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # workout_streak, weight_goal, pr_set, etc.
    title = Column(String)
    description = Column(String)
    icon = Column(String)
    date_earned = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="achievements")
    posts = relationship("Post", back_populates="achievement")

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    progress = Column(Integer, default=0)  # For progress-based achievements
    completed = Column(Boolean, default=False)
    date_completed = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="user_achievements")
    achievement = relationship("Achievement")