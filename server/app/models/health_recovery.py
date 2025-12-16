from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database.database import Base

class SleepQuality(str, enum.Enum):
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"

class RecoveryStatus(str, enum.Enum):
    NEEDS_REST = "needs_rest"
    MODERATE = "moderate"
    GOOD = "good"
    OPTIMAL = "optimal"

class SleepData(Base):
    __tablename__ = "sleep_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    sleep_start = Column(DateTime, nullable=False)
    sleep_end = Column(DateTime, nullable=False)
    duration = Column(Float, nullable=False)  # in hours
    quality = Column(Enum(SleepQuality), nullable=False)
    deep_sleep = Column(Float)  # in hours
    rem_sleep = Column(Float)  # in hours
    light_sleep = Column(Float)  # in hours
    awake_time = Column(Float)  # in hours
    sleep_score = Column(Integer)  # 0-100
    heart_rate_avg = Column(Float)
    heart_rate_min = Column(Float)
    heart_rate_max = Column(Float)
    respiratory_rate = Column(Float)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="sleep_data")

class RecoveryMetrics(Base):
    __tablename__ = "recovery_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    hrv_score = Column(Float)  # Heart Rate Variability
    resting_heart_rate = Column(Float)
    readiness_score = Column(Integer)  # 0-100
    recovery_status = Column(Enum(RecoveryStatus), nullable=False)
    muscle_strain = Column(Float)  # 0-100
    stress_level = Column(Float)  # 0-100
    recovery_time = Column(Float)  # recommended recovery time in hours
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="recovery_metrics")

class HealthMetrics(Base):
    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    steps = Column(Integer)
    distance = Column(Float)  # in kilometers
    calories_active = Column(Float)
    calories_basal = Column(Float)
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    blood_oxygen = Column(Float)  # SpO2 percentage
    body_temperature = Column(Float)  # in Celsius
    hydration = Column(Float)  # percentage
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="health_metrics")

class HealthDevice(Base):
    __tablename__ = "health_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_type = Column(String, nullable=False)  # e.g., "fitbit", "apple_watch", "oura_ring"
    device_id = Column(String, nullable=False)
    device_name = Column(String)
    last_synced = Column(DateTime)
    access_token = Column(String)
    refresh_token = Column(String)
    token_expires = Column(DateTime)
    settings = Column(JSON)  # device-specific settings
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="health_devices")