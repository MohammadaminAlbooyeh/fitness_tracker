from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ExerciseInTemplate(BaseModel):
    exercise_id: int
    sets: int
    reps: str
    rest_time: int

class WorkoutTemplateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: str = Field(..., min_length=1, max_length=50)
    difficulty: str = Field(..., min_length=1, max_length=20)
    estimated_duration: int
    is_public: bool = False
    exercises: List[ExerciseInTemplate]
    metadata: Optional[Dict[str, Any]]

class WorkoutTemplateResponse(WorkoutTemplateCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ReminderCreate(BaseModel):
    reminder_time: datetime
    notification_type: str = Field(..., pattern='^(email|push|sms)$')

class ScheduledWorkoutCreate(BaseModel):
    template_id: int
    scheduled_date: datetime
    notes: Optional[str] = Field(None, max_length=500)
    reminder_enabled: bool = True
    recurrence_rule: Optional[str]
    reminder: Optional[ReminderCreate]

class ScheduledWorkoutResponse(BaseModel):
    id: int
    user_id: int
    template_id: int
    scheduled_date: datetime
    completed_date: Optional[datetime]
    status: str
    notes: Optional[str]
    reminder_enabled: bool
    reminder_time: Optional[datetime]
    recurrence_rule: Optional[str]
    template: WorkoutTemplateResponse

    class Config:
        orm_mode = True

class ReminderResponse(BaseModel):
    id: int
    user_id: int
    scheduled_workout_id: int
    reminder_time: datetime
    notification_type: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True