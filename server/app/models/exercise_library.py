from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.database import Base
from typing import List

# Association table for exercise equipment
exercise_equipment = Table(
    'exercise_equipment',
    Base.metadata,
    Column('exercise_id', Integer, ForeignKey('exercises.id'), primary_key=True),
    Column('equipment_id', Integer, ForeignKey('equipment.id'), primary_key=True)
)

# Association table for exercise muscles
exercise_muscles = Table(
    'exercise_muscles',
    Base.metadata,
    Column('exercise_id', Integer, ForeignKey('exercises.id'), primary_key=True),
    Column('muscle_id', Integer, ForeignKey('muscles.id'), primary_key=True),
    Column('is_primary', Boolean, default=False)  # Primary or secondary muscle
)

class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    difficulty_level = Column(String(20))  # beginner, intermediate, advanced
    category = Column(String(50))  # strength, cardio, flexibility, etc.
    video_url = Column(String(255))
    thumbnail_url = Column(String(255))
    is_custom = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Safety and form tips
    form_tips = Column(Text)
    safety_warnings = Column(Text)
    
    # Exercise variations
    parent_exercise_id = Column(Integer, ForeignKey('exercises.id'))
    variations = relationship("Exercise")
    
    # Relationships
    equipment = relationship("Equipment", secondary=exercise_equipment)
    muscles = relationship("Muscle", secondary=exercise_muscles)
    creator = relationship("User", back_populates="custom_exercises")

class Equipment(Base):
    __tablename__ = 'equipment'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # weights, machines, cardio, etc.
    image_url = Column(String(255))

    # Relationships
    exercises = relationship("Exercise", secondary=exercise_equipment)

class Muscle(Base):
    __tablename__ = 'muscles'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    body_part = Column(String(50))  # arms, legs, core, etc.
    image_url = Column(String(255))

    # Relationships
    exercises = relationship("Exercise", secondary=exercise_muscles)

class ExerciseProgress(Base):
    __tablename__ = 'exercise_progress'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercises.id'), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    # Performance metrics
    weight = Column(Float)  # Weight used in kg
    reps = Column(Integer)
    sets = Column(Integer)
    duration = Column(Integer)  # Duration in seconds
    distance = Column(Float)  # Distance in meters if applicable
    notes = Column(Text)
    
    # Form rating and feedback
    form_rating = Column(Integer)  # 1-5 rating
    form_feedback = Column(Text)
    
    # Personal records
    is_personal_record = Column(Boolean, default=False)
    pr_type = Column(String(20))  # weight, reps, duration, etc.

    # Relationships
    user = relationship("User", back_populates="exercise_progress")
    exercise = relationship("Exercise")