from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database.database import Base

# Association table for user achievements
user_achievements = Table(
    'user_achievements',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('achievement_id', Integer, ForeignKey('achievements.id'), primary_key=True),
    Column('date_completed', DateTime, nullable=True)
)

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