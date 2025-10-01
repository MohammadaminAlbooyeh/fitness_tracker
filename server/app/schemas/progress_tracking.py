from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MeasurementType(str, Enum):
    WEIGHT = 'weight'
    BODY_FAT = 'body_fat'
    CHEST = 'chest'
    WAIST = 'waist'
    HIPS = 'hips'
    BICEPS = 'biceps'
    THIGHS = 'thighs'
    CUSTOM = 'custom'

class MeasurementBase(BaseModel):
    measurement_type: str
    value: float
    unit: str
    notes: Optional[str] = None
    custom_name: Optional[str] = None
    date: Optional[datetime] = None

class MeasurementCreate(MeasurementBase):
    pass

class Measurement(MeasurementBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True

class ProgressPhotoBase(BaseModel):
    photo_type: str = Field(..., regex='^(front|side|back)$')
    notes: Optional[str] = None
    measurements: Optional[Dict[str, Any]] = None

class ProgressPhotoCreate(ProgressPhotoBase):
    pass

class ProgressPhoto(ProgressPhotoBase):
    id: int
    user_id: int
    photo_url: HttpUrl
    date: datetime

    class Config:
        orm_mode = True

class AchievementBase(BaseModel):
    name: str
    description: str
    icon_url: Optional[HttpUrl] = None
    category: str
    criteria: Dict[str, Any]
    points: int = 0

class AchievementCreate(AchievementBase):
    pass

class Achievement(AchievementBase):
    id: int

    class Config:
        orm_mode = True

class UserAchievementBase(BaseModel):
    achievement_id: int
    progress: Optional[Dict[str, Any]] = None

class UserAchievement(UserAchievementBase):
    id: int
    user_id: int
    earned_date: datetime
    achievement: Achievement

    class Config:
        orm_mode = True

class PerformanceMetricBase(BaseModel):
    metric_type: str
    value: float
    unit: str
    exercise_id: Optional[int] = None
    notes: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    date: Optional[datetime] = None

class PerformanceMetricCreate(PerformanceMetricBase):
    pass

class PerformanceMetric(PerformanceMetricBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True

class ProgressSummary(BaseModel):
    measurements: Dict[str, List[Measurement]]
    recent_photos: List[ProgressPhoto]
    achievements: List[UserAchievement]
    performance_metrics: List[PerformanceMetric]
    stats: Dict[str, Any]  # Summary statistics