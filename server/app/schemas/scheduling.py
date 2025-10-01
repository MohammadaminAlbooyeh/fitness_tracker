from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, time
from enum import Enum

class RecurrenceType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"

class EventType(str, Enum):
    WORKOUT = "workout"
    CLASS = "class"
    ASSESSMENT = "assessment"
    RECOVERY = "recovery"
    CONSULTATION = "consultation"
    CUSTOM = "custom"

class AvailabilityType(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    TENTATIVE = "tentative"

# Recurrence Pattern Schemas
class RecurrencePatternBase(BaseModel):
    type: RecurrenceType
    interval: int = 1
    days_of_week: Optional[List[int]] = None
    day_of_month: Optional[int] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    max_occurrences: Optional[int] = None
    exceptions: Optional[List[datetime]] = None

class RecurrencePatternCreate(RecurrencePatternBase):
    pass

class RecurrencePatternResponse(RecurrencePatternBase):
    id: int

    class Config:
        orm_mode = True

# Event Schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: EventType
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class EventCreate(EventBase):
    created_by: int
    participants: Optional[List[int]] = None
    recurrence: Optional[RecurrencePatternCreate] = None

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[EventType] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    participants: Optional[List[int]] = None
    metadata: Optional[Dict[str, Any]] = None
    is_cancelled: Optional[bool] = None

class EventResponse(EventBase):
    id: int
    created_by: int
    recurrence_id: Optional[int] = None
    is_cancelled: bool
    participants: List[Dict[str, Any]]  # List of participant user objects
    recurrence_pattern: Optional[RecurrencePatternResponse] = None

    class Config:
        orm_mode = True

# Availability Schemas
class AvailabilityBase(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime
    availability_type: AvailabilityType
    notes: Optional[str] = None

class AvailabilityCreate(AvailabilityBase):
    recurrence: Optional[RecurrencePatternCreate] = None

class AvailabilityResponse(AvailabilityBase):
    id: int
    recurrence_pattern: Optional[RecurrencePatternResponse] = None

    class Config:
        orm_mode = True

# Schedule Preference Schemas
class TimeRange(BaseModel):
    start: time
    end: time

    @validator('end')
    def end_must_be_after_start(cls, v, values):
        if 'start' in values and v <= values['start']:
            raise ValueError('end time must be after start time')
        return v

class SchedulePreferenceBase(BaseModel):
    user_id: int
    preferred_workout_days: List[int] = Field(..., min_items=1, max_items=7)  # 0=Monday, 6=Sunday
    preferred_workout_times: List[TimeRange]
    blackout_times: Optional[List[TimeRange]] = None
    max_workouts_per_week: int = Field(..., ge=1, le=7)
    min_rest_between_workouts: int = Field(..., ge=1)  # Hours
    timezone: str
    notification_preferences: Dict[str, Any]

class SchedulePreferenceCreate(SchedulePreferenceBase):
    pass

class SchedulePreferenceResponse(SchedulePreferenceBase):
    id: int

    class Config:
        orm_mode = True

# Search and Filter Schemas
class EventSearch(BaseModel):
    start_date: datetime
    end_date: datetime
    user_id: Optional[int] = None
    event_type: Optional[EventType] = None
    location: Optional[str] = None
    expand_recurring: bool = True

# Smart Scheduling Schemas
class SchedulingConstraint(BaseModel):
    min_duration: Optional[int] = None  # minutes
    max_duration: Optional[int] = None  # minutes
    required_equipment: Optional[List[str]] = None
    preferred_time_of_day: Optional[str] = None  # morning, afternoon, evening
    intensity_level: Optional[str] = None  # low, medium, high

class SmartScheduleRequest(BaseModel):
    user_id: int
    start_date: datetime
    end_date: datetime
    event_types: List[EventType]
    constraints: Optional[SchedulingConstraint] = None

class ConflictDetail(BaseModel):
    event_id: int
    title: str
    start_time: datetime
    end_time: datetime
    event_type: EventType

class ConflictCheckResponse(BaseModel):
    has_conflicts: bool
    conflicts: Optional[List[ConflictDetail]] = None

# Reminder Schemas
class ReminderBase(BaseModel):
    event_id: int
    user_id: int
    reminder_time: datetime
    notification_type: str

class ReminderCreate(ReminderBase):
    pass

class ReminderResponse(ReminderBase):
    id: int
    is_sent: bool

    class Config:
        orm_mode = True