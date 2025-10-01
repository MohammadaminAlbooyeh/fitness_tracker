from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.health_recovery import SleepQuality, RecoveryStatus

class SleepDataBase(BaseModel):
    date: datetime
    sleep_start: datetime
    sleep_end: datetime
    duration: float
    quality: SleepQuality
    deep_sleep: Optional[float] = None
    rem_sleep: Optional[float] = None
    light_sleep: Optional[float] = None
    awake_time: Optional[float] = None
    sleep_score: Optional[int] = None
    heart_rate_avg: Optional[float] = None
    heart_rate_min: Optional[float] = None
    heart_rate_max: Optional[float] = None
    respiratory_rate: Optional[float] = None
    notes: Optional[str] = None

class SleepDataCreate(SleepDataBase):
    pass

class SleepData(SleepDataBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RecoveryMetricsBase(BaseModel):
    date: datetime
    hrv_score: Optional[float] = None
    resting_heart_rate: Optional[float] = None
    readiness_score: Optional[int] = Field(None, ge=0, le=100)
    recovery_status: RecoveryStatus
    muscle_strain: Optional[float] = Field(None, ge=0, le=100)
    stress_level: Optional[float] = Field(None, ge=0, le=100)
    recovery_time: Optional[float] = None

class RecoveryMetricsCreate(RecoveryMetricsBase):
    pass

class RecoveryMetrics(RecoveryMetricsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class HealthMetricsBase(BaseModel):
    date: datetime
    steps: Optional[int] = Field(None, ge=0)
    distance: Optional[float] = Field(None, ge=0)
    calories_active: Optional[float] = Field(None, ge=0)
    calories_basal: Optional[float] = Field(None, ge=0)
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    blood_oxygen: Optional[float] = Field(None, ge=0, le=100)
    body_temperature: Optional[float] = None
    hydration: Optional[float] = Field(None, ge=0, le=100)

class HealthMetricsCreate(HealthMetricsBase):
    pass

class HealthMetrics(HealthMetricsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class HealthDeviceBase(BaseModel):
    device_type: str
    device_id: str
    device_name: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

class HealthDeviceCreate(HealthDeviceBase):
    pass

class HealthDeviceUpdate(BaseModel):
    device_name: Optional[str] = None
    last_synced: Optional[datetime] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires: Optional[datetime] = None
    settings: Optional[Dict[str, Any]] = None

class HealthDevice(HealthDeviceBase):
    id: int
    user_id: int
    last_synced: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SleepStatistics(BaseModel):
    average_duration: float
    average_quality: float
    average_deep_sleep: float
    average_rem_sleep: float
    average_sleep_score: float
    best_quality_day: datetime
    worst_quality_day: datetime

class RecoveryStatistics(BaseModel):
    average_readiness: float
    average_hrv: float
    average_resting_heart_rate: float
    optimal_recovery_days: int
    needs_rest_days: int
    recovery_trend: List[Dict[str, Any]]

class HealthStatistics(BaseModel):
    average_steps: int
    average_calories_active: float
    average_blood_oxygen: float
    average_hydration: float
    steps_trend: List[Dict[str, Any]]
    calories_trend: List[Dict[str, Any]]