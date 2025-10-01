from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum

class TimePreference(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"

class IntensityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class EventType(str, Enum):
    WORKOUT = "workout"
    ASSESSMENT = "assessment"

class SchedulingConstraints(BaseModel):
    min_duration: int
    max_duration: int
    preferred_time_of_day: TimePreference
    intensity_level: IntensityLevel

class SmartScheduleRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    event_types: List[EventType]
    constraints: SchedulingConstraints

    class Config:
        use_enum_values = True