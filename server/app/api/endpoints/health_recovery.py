from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ...database.database import get_db
from ...utils.auth import get_current_user
from ...schemas.health_recovery import (
    SleepDataCreate,
    SleepData,
    RecoveryMetricsCreate,
    RecoveryMetrics,
    HealthMetricsCreate,
    HealthMetrics,
    HealthDeviceCreate,
    HealthDeviceUpdate,
    HealthDevice,
    SleepStatistics,
    RecoveryStatistics,
    HealthStatistics
)
from ...models.health_recovery import (
    SleepData as SleepDataModel,
    RecoveryMetrics as RecoveryMetricsModel,
    HealthMetrics as HealthMetricsModel,
    HealthDevice as HealthDeviceModel
)
from ...core.health_integration import HealthDeviceManager
from ...utils.statistics import get_sleep_statistics, get_recovery_statistics, get_health_statistics
from sqlalchemy import func

router = APIRouter()
health_device_manager = HealthDeviceManager()

# Sleep tracking endpoints
@router.post("/sleep", response_model=SleepData)
async def create_sleep_data(
    sleep_data: SleepDataCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record sleep data for a user"""
    db_sleep = SleepDataModel(**sleep_data.dict(), user_id=current_user.id)
    db.add(db_sleep)
    db.commit()
    db.refresh(db_sleep)
    return db_sleep

@router.get("/sleep", response_model=List[SleepData])
async def get_sleep_data(
    start_date: datetime = None,
    end_date: datetime = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sleep data for a user within a date range"""
    query = db.query(SleepDataModel).filter(SleepDataModel.user_id == current_user.id)
    if start_date:
        query = query.filter(SleepDataModel.date >= start_date)
    if end_date:
        query = query.filter(SleepDataModel.date <= end_date)
    return query.order_by(SleepDataModel.date.desc()).all()

@router.get("/sleep/statistics", response_model=SleepStatistics)
async def get_sleep_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sleep statistics for a user"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return get_sleep_statistics(
        current_user.id, start_date, end_date, db
    )

# Recovery metrics endpoints
@router.post("/recovery", response_model=RecoveryMetrics)
async def create_recovery_metrics(
    metrics: RecoveryMetricsCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record recovery metrics for a user"""
    db_metrics = RecoveryMetricsModel(**metrics.dict(), user_id=current_user.id)
    db.add(db_metrics)
    db.commit()
    db.refresh(db_metrics)
    return db_metrics

@router.get("/recovery", response_model=List[RecoveryMetrics])
async def get_recovery_metrics(
    start_date: datetime = None,
    end_date: datetime = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recovery metrics for a user within a date range"""
    query = db.query(RecoveryMetricsModel).filter(
        RecoveryMetricsModel.user_id == current_user.id
    )
    if start_date:
        query = query.filter(RecoveryMetricsModel.date >= start_date)
    if end_date:
        query = query.filter(RecoveryMetricsModel.date <= end_date)
    return query.order_by(RecoveryMetricsModel.date.desc()).all()

@router.get("/recovery/statistics", response_model=RecoveryStatistics)
async def get_recovery_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recovery statistics for a user"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return get_recovery_statistics(
        current_user.id, start_date, end_date, db
    )

# Health metrics endpoints
@router.post("/health", response_model=HealthMetrics)
async def create_health_metrics(
    metrics: HealthMetricsCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record health metrics for a user"""
    db_metrics = HealthMetricsModel(**metrics.dict(), user_id=current_user.id)
    db.add(db_metrics)
    db.commit()
    db.refresh(db_metrics)
    return db_metrics

@router.get("/health", response_model=List[HealthMetrics])
async def get_health_metrics(
    start_date: datetime = None,
    end_date: datetime = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health metrics for a user within a date range"""
    query = db.query(HealthMetricsModel).filter(
        HealthMetricsModel.user_id == current_user.id
    )
    if start_date:
        query = query.filter(HealthMetricsModel.date >= start_date)
    if end_date:
        query = query.filter(HealthMetricsModel.date <= end_date)
    return query.order_by(HealthMetricsModel.date.desc()).all()

@router.get("/health/statistics", response_model=HealthStatistics)
async def get_health_statistics(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health statistics for a user"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return get_health_statistics(
        current_user.id, start_date, end_date, db
    )

# Health device endpoints
@router.post("/devices", response_model=HealthDevice)
async def connect_health_device(
    device: HealthDeviceCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Connect a new health device for a user"""
    # Check if device already exists
    existing_device = db.query(HealthDeviceModel).filter(
        HealthDeviceModel.user_id == current_user.id,
        HealthDeviceModel.device_type == device.device_type,
        HealthDeviceModel.device_id == device.device_id
    ).first()
    
    if existing_device:
        raise HTTPException(
            status_code=400,
            detail="Device already connected"
        )
    
    # Initialize device connection
    device_data = await health_device_manager.connect_device(
        device.device_type,
        device.device_id,
        current_user.id
    )
    
    # Create device record
    db_device = HealthDeviceModel(
        **device.dict(),
        user_id=current_user.id,
        access_token=device_data.get('access_token'),
        refresh_token=device_data.get('refresh_token'),
        token_expires=device_data.get('token_expires')
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/devices", response_model=List[HealthDevice])
async def get_connected_devices(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all connected health devices for a user"""
    return db.query(HealthDeviceModel).filter(
        HealthDeviceModel.user_id == current_user.id
    ).all()

@router.put("/devices/{device_id}", response_model=HealthDevice)
async def update_health_device(
    device_id: int,
    device_update: HealthDeviceUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update health device settings"""
    device = db.query(HealthDeviceModel).filter(
        HealthDeviceModel.id == device_id,
        HealthDeviceModel.user_id == current_user.id
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )
    
    for key, value in device_update.dict(exclude_unset=True).items():
        setattr(device, key, value)
    
    db.commit()
    db.refresh(device)
    return device

@router.delete("/devices/{device_id}")
async def disconnect_health_device(
    device_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disconnect a health device"""
    device = db.query(HealthDeviceModel).filter(
        HealthDeviceModel.id == device_id,
        HealthDeviceModel.user_id == current_user.id
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )
    
    # Revoke device access
    await health_device_manager.disconnect_device(
        device.device_type,
        device.device_id,
        current_user.id
    )
    
    db.delete(device)
    db.commit()
    return {"message": "Device disconnected successfully"}