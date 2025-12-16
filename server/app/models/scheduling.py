from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import enum

from ..database import Base

class RecurrenceType(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"

class EventType(enum.Enum):
    WORKOUT = "workout"
    CLASS = "class"
    ASSESSMENT = "assessment"
    RECOVERY = "recovery"
    CONSULTATION = "consultation"
    CUSTOM = "custom"

class AvailabilityType(enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    TENTATIVE = "tentative"

# Association table for event participants
event_participants = Table(
    'event_participants',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    event_type = Column(Enum(EventType), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    recurrence_id = Column(Integer, ForeignKey("recurrence_patterns.id"))
    is_cancelled = Column(Boolean, default=False)
    extra_data = Column(JSONB)  # For storing event-specific data (workout details, class info, etc.)

    # Relationships
    creator = relationship("User", back_populates="created_events", foreign_keys=[created_by])
    participants = relationship("User", secondary=event_participants, back_populates="events")
    recurrence_pattern = relationship("RecurrencePattern", back_populates="events")
    reminders = relationship("Reminder", back_populates="event")

class RecurrencePattern(Base):
    __tablename__ = "recurrence_patterns"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(RecurrenceType), nullable=False)
    interval = Column(Integer, default=1)  # Every X days/weeks/months
    days_of_week = Column(JSONB)  # For weekly recurrence
    day_of_month = Column(Integer)  # For monthly recurrence
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    max_occurrences = Column(Integer)
    exceptions = Column(JSONB)  # Dates to skip

    # Relationships
    events = relationship("Event", back_populates="recurrence_pattern")

class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    availability_type = Column(Enum(AvailabilityType), nullable=False)
    recurrence_id = Column(Integer, ForeignKey("recurrence_patterns.id"))
    notes = Column(String)

    # Relationships
    user = relationship("User", back_populates="availabilities")
    recurrence_pattern = relationship("RecurrencePattern")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    is_sent = Column(Boolean, default=False)
    notification_type = Column(String)  # email, push, sms

    # Relationships
    event = relationship("Event", back_populates="reminders")
    user = relationship("User", back_populates="reminders")

class SchedulePreference(Base):
    __tablename__ = "schedule_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preferred_workout_days = Column(JSONB)  # Array of weekdays
    preferred_workout_times = Column(JSONB)  # Array of time ranges
    blackout_times = Column(JSONB)  # Times to avoid scheduling
    max_workouts_per_week = Column(Integer)
    min_rest_between_workouts = Column(Integer)  # Hours
    timezone = Column(String)
    notification_preferences = Column(JSONB)

    # Relationships
    user = relationship("User", back_populates="schedule_preferences")