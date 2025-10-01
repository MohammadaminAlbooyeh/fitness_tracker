from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class DeviceType(str, Enum):
    SMARTWATCH = "smartwatch"
    FITNESS_TRACKER = "fitness_tracker"
    SMART_SCALE = "smart_scale"
    HEART_RATE_MONITOR = "heart_rate_monitor"
    SLEEP_TRACKER = "sleep_tracker"

# Sleep Data Schemas
class SleepDataBase(BaseModel):
    duration: float = Field(..., description="Sleep duration in hours")
    quality: int = Field(..., ge=1, le=100, description="Sleep quality score (1-100)")
    deep_sleep_percentage: float = Field(..., ge=0, le=100)
    rem_sleep_percentage: float = Field(..., ge=0, le=100)
    light_sleep_percentage: float = Field(..., ge=0, le=100)
    awake_time: float = Field(..., description="Time spent awake in minutes")
    sleep_score: int = Field(..., ge=0, le=100)
    notes: Optional[str] = None

class SleepDataCreate(SleepDataBase):
    user_id: int
    date: datetime = Field(default_factory=datetime.utcnow)

class SleepDataResponse(SleepDataBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True

# Recovery Metrics Schemas
class RecoveryMetricsBase(BaseModel):
    readiness_score: int = Field(..., ge=0, le=100)
    hrv_score: int = Field(..., ge=0, le=100)
    resting_heart_rate: int = Field(..., ge=30, le=200)
    heart_rate_variability: float
    respiratory_rate: float
    body_temperature: Optional[float] = None
    stress_level: int = Field(..., ge=0, le=100)
    muscle_strain: int = Field(..., ge=0, le=100)
    recovery_status: str

class RecoveryMetricsCreate(RecoveryMetricsBase):
    user_id: int
    date: datetime = Field(default_factory=datetime.utcnow)

class RecoveryMetricsResponse(RecoveryMetricsBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True

# Health Metrics Schemas
class HealthMetricsBase(BaseModel):
    metric_type: str
    value: float
    unit: str
    notes: Optional[str] = None

class HealthMetricsCreate(HealthMetricsBase):
    user_id: int
    date: datetime = Field(default_factory=datetime.utcnow)

class HealthMetricsResponse(HealthMetricsBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        orm_mode = True

# Device Integration Schemas
class DeviceInfoBase(BaseModel):
    device_type: DeviceType
    device_id: str
    device_name: str
    status: str = "connected"
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

class DeviceInfoCreate(DeviceInfoBase):
    user_id: int

class DeviceInfoResponse(DeviceInfoBase):
    id: int
    user_id: int
    last_synced: Optional[datetime] = None

    class Config:
        orm_mode = True

# Recommendation Schema
class RecoveryRecommendation(BaseModel):
    message: str
    priority: str = Field(..., pattern="^(high|medium|low)$")
    type: str
    actions: List[str]

# Health Insights Schema
class HealthTrend(BaseModel):
    metric: str
    trend: str
    change_percentage: float
    is_positive: bool

class HealthInsight(BaseModel):
    category: str
    title: str
    description: str
    severity: str = Field(..., pattern="^(high|medium|low)$")
    recommendations: List[str]

class HealthInsightsResponse(BaseModel):
    overall_health_score: int = Field(..., ge=0, le=100)
    trends: List[HealthTrend]
    insights: List[HealthInsight]
    last_updated: datetime

# Statistics Schemas
class SleepStatistics(BaseModel):
    average_sleep_duration: float
    average_sleep_quality: float
    total_records: int
    deep_sleep_percentage: float

class RecoveryStatistics(BaseModel):
    average_readiness: float
    optimal_recovery_days: int
    needs_rest_days: int
    average_hrv: float
    recovery_trend: List[dict]

class HealthStatistics(BaseModel):
    metrics_tracked: List[str]
    completion_rate: float
    streak_days: int
    areas_of_concern: List[str]