from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from ..database.database import get_db
from ..utils.auth import get_current_user
from ..models.user import User
from ..models.progress_tracking import (
    UserMeasurement,
    ProgressPhoto,
    Achievement,
    UserAchievement,
    PerformanceMetric
)
from ..schemas.progress_tracking import (
    MeasurementCreate,
    Measurement,
    ProgressPhotoCreate,
    ProgressPhoto as ProgressPhotoSchema,
    Achievement as AchievementSchema,
    UserAchievement as UserAchievementSchema,
    PerformanceMetricCreate,
    PerformanceMetric as PerformanceMetricSchema,
    ProgressSummary
)
from ..core.storage import upload_file
from sqlalchemy import func

router = APIRouter()

# Measurements endpoints
@router.post("/measurements/", response_model=Measurement)
async def create_measurement(
    measurement: MeasurementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_measurement = UserMeasurement(
        user_id=current_user.id,
        **measurement.dict()
    )
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement

@router.get("/measurements/", response_model=List[Measurement])
async def list_measurements(
    measurement_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(UserMeasurement).filter(UserMeasurement.user_id == current_user.id)
    
    if measurement_type:
        query = query.filter(UserMeasurement.measurement_type == measurement_type)
    if start_date:
        query = query.filter(UserMeasurement.date >= start_date)
    if end_date:
        query = query.filter(UserMeasurement.date <= end_date)
    
    return query.order_by(UserMeasurement.date.desc()).all()

# Progress photos endpoints
@router.post("/photos/", response_model=ProgressPhotoSchema)
async def upload_progress_photo(
    photo_data: ProgressPhotoCreate,
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    photo_url = await upload_file(
        photo,
        f"progress_photos/{current_user.id}/{datetime.now().strftime('%Y-%m-%d')}"
    )
    
    db_photo = ProgressPhoto(
        user_id=current_user.id,
        photo_url=photo_url,
        **photo_data.dict()
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

@router.get("/photos/", response_model=List[ProgressPhotoSchema])
async def list_progress_photos(
    photo_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(ProgressPhoto).filter(ProgressPhoto.user_id == current_user.id)
    
    if photo_type:
        query = query.filter(ProgressPhoto.photo_type == photo_type)
    if start_date:
        query = query.filter(ProgressPhoto.date >= start_date)
    if end_date:
        query = query.filter(ProgressPhoto.date <= end_date)
    
    return query.order_by(ProgressPhoto.date.desc()).all()

# Achievements endpoints
@router.get("/achievements/", response_model=List[UserAchievementSchema])
async def list_user_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(UserAchievement)\
        .filter(UserAchievement.user_id == current_user.id)\
        .order_by(UserAchievement.earned_date.desc())\
        .all()

@router.get("/achievements/available", response_model=List[AchievementSchema])
async def list_available_achievements(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Achievement)
    if category:
        query = query.filter(Achievement.category == category)
    return query.all()

# Performance metrics endpoints
@router.post("/metrics/", response_model=PerformanceMetricSchema)
async def log_performance_metric(
    metric: PerformanceMetricCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_metric = PerformanceMetric(
        user_id=current_user.id,
        **metric.dict()
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/metrics/", response_model=List[PerformanceMetricSchema])
async def list_performance_metrics(
    metric_type: Optional[str] = None,
    exercise_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(PerformanceMetric).filter(PerformanceMetric.user_id == current_user.id)
    
    if metric_type:
        query = query.filter(PerformanceMetric.metric_type == metric_type)
    if exercise_id:
        query = query.filter(PerformanceMetric.exercise_id == exercise_id)
    if start_date:
        query = query.filter(PerformanceMetric.date >= start_date)
    if end_date:
        query = query.filter(PerformanceMetric.date <= end_date)
    
    return query.order_by(PerformanceMetric.date.desc()).all()

# Progress summary endpoint
@router.get("/summary", response_model=ProgressSummary)
async def get_progress_summary(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    start_date = datetime.now() - timedelta(days=days)
    
    # Get recent measurements grouped by type
    measurements = {}
    measurement_types = db.query(UserMeasurement.measurement_type)\
        .filter(UserMeasurement.user_id == current_user.id)\
        .distinct()\
        .all()
    
    for (m_type,) in measurement_types:
        measurements[m_type] = db.query(UserMeasurement)\
            .filter(
                UserMeasurement.user_id == current_user.id,
                UserMeasurement.measurement_type == m_type,
                UserMeasurement.date >= start_date
            )\
            .order_by(UserMeasurement.date.desc())\
            .all()
    
    # Get recent photos
    recent_photos = db.query(ProgressPhoto)\
        .filter(
            ProgressPhoto.user_id == current_user.id,
            ProgressPhoto.date >= start_date
        )\
        .order_by(ProgressPhoto.date.desc())\
        .all()
    
    # Get achievements
    achievements = db.query(UserAchievement)\
        .filter(
            UserAchievement.user_id == current_user.id,
            UserAchievement.earned_date >= start_date
        )\
        .order_by(UserAchievement.earned_date.desc())\
        .all()
    
    # Get performance metrics
    metrics = db.query(PerformanceMetric)\
        .filter(
            PerformanceMetric.user_id == current_user.id,
            PerformanceMetric.date >= start_date
        )\
        .order_by(PerformanceMetric.date.desc())\
        .all()
    
    # Calculate summary statistics
    stats = {
        "total_measurements": sum(len(m) for m in measurements.values()),
        "total_photos": len(recent_photos),
        "achievements_earned": len(achievements),
        "performance_records": len([m for m in metrics if m.context.get("is_record", False)]),
        "measurement_changes": {}
    }
    
    # Calculate changes in measurements
    for m_type, measures in measurements.items():
        if len(measures) >= 2:
            latest = measures[0].value
            oldest = measures[-1].value
            stats["measurement_changes"][m_type] = {
                "change": latest - oldest,
                "percent_change": ((latest - oldest) / oldest) * 100 if oldest != 0 else 0
            }
    
    return ProgressSummary(
        measurements=measurements,
        recent_photos=recent_photos,
        achievements=achievements,
        performance_metrics=metrics,
        stats=stats
    )