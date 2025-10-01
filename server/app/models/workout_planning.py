from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any
from .base import Base

# Association table for workout templates and exercises
template_exercises = Table(
    'template_exercises',
    Base.metadata,
    Column('template_id', Integer, ForeignKey('workout_templates.id'), primary_key=True),
    Column('exercise_id', Integer, ForeignKey('exercises.id'), primary_key=True),
    Column('order', Integer),
    Column('sets', Integer),
    Column('reps', String),  # Can be "12" or "8-12" for rep ranges
    Column('rest_time', Integer),  # Rest time in seconds
)

class WorkoutTemplate(Base):
    __tablename__ = 'workout_templates'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(50))  # strength, cardio, flexibility, etc.
    difficulty = Column(String(20))  # beginner, intermediate, advanced
    estimated_duration = Column(Integer)  # Duration in minutes
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)  # For storing additional template data

    # Relationships
    user = relationship("User", back_populates="workout_templates")
    exercises = relationship(
        "Exercise",
        secondary=template_exercises,
        order_by=template_exercises.c.order
    )
    scheduled_workouts = relationship("ScheduledWorkout", back_populates="template")

class ScheduledWorkout(Base):
    __tablename__ = 'scheduled_workouts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    template_id = Column(Integer, ForeignKey('workout_templates.id'))
    scheduled_date = Column(DateTime, nullable=False)
    completed_date = Column(DateTime)
    status = Column(String(20), default='scheduled')  # scheduled, completed, skipped
    notes = Column(String(500))
    reminder_enabled = Column(Boolean, default=True)
    reminder_time = Column(DateTime)  # When to send the reminder
    recurrence_rule = Column(String(100))  # iCal format recurrence rule

    # Relationships
    user = relationship("User", back_populates="scheduled_workouts")
    template = relationship("WorkoutTemplate", back_populates="scheduled_workouts")

class WorkoutReminder(Base):
    __tablename__ = 'workout_reminders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    scheduled_workout_id = Column(Integer, ForeignKey('scheduled_workouts.id'), nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    notification_type = Column(String(20))  # email, push, sms
    status = Column(String(20), default='pending')  # pending, sent, failed
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User")
    scheduled_workout = relationship("ScheduledWorkout")