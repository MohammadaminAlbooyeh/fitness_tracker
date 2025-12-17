from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class FormCheckStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FeedbackSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class FormFeedbackItem(BaseModel):
    message: str
    suggestion: str
    severity: FeedbackSeverity

class FormCheckResult(BaseModel):
    id: str
    user_id: int
    exercise_id: int
    video_url: str
    status: FormCheckStatus
    score: Optional[float] = None
    analysis: Optional[dict] = None
    feedback: Optional[List[FormFeedbackItem]] = None
    error: Optional[str] = None

class RecommendationFilter(BaseModel):
    difficulty: Optional[str] = None
    duration: Optional[int] = None
    equipment: Optional[List[str]] = None

class AIModelBase(BaseModel):
    name: str
    version: str
    type: str
    parameters: dict
    active: bool = True

class AIModelCreate(AIModelBase):
    pass

class AIModel(AIModelBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class WorkoutRecommendationBase(BaseModel):
    workout_plan: dict
    confidence_score: float
    feedback: Optional[str] = None

class WorkoutRecommendationCreate(WorkoutRecommendationBase):
    pass

class WorkoutRecommendation(WorkoutRecommendationBase):
    id: int
    user_id: int
    model_id: int
    accepted: bool
    created_at: datetime

    class Config:
        orm_mode = True

class FormCheckBase(BaseModel):
    video_url: str
    analysis: dict
    feedback: dict
    score: float

class FormCheckCreate(FormCheckBase):
    exercise_id: int

class FormCheck(FormCheckBase):
    id: int
    user_id: int
    exercise_id: int
    model_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SmartAdjustmentBase(BaseModel):
    original_plan: dict
    adjusted_plan: dict
    adjustment_reason: str
    applied: bool = False

class SmartAdjustmentCreate(SmartAdjustmentBase):
    workout_id: int

class SmartAdjustment(SmartAdjustmentBase):
    id: int
    user_id: int
    model_id: int
    workout_id: int
    created_at: datetime

    class Config:
        orm_mode = True