from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from ..database.database import Base
from datetime import datetime

# Association table for user achievements
user_achievements = Table(
    'user_achievements',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('achievement_id', Integer, ForeignKey('achievements.id')),
    Column('earned_at', DateTime, default=datetime.utcnow)
)

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    icon = Column(String)  # URL or icon name
    requirement = Column(String)  # JSON string containing achievement criteria
    points = Column(Integer, default=0)
    
    # Relationships
    users = relationship("User", secondary=user_achievements, back_populates="achievements")

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