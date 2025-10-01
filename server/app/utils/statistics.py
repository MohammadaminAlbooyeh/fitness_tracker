from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.health_recovery import (
    SleepData,
    RecoveryMetrics,
    HealthMetrics,
    RecoveryStatus
)

def get_sleep_statistics(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session
) -> Dict[str, Any]:
    """Calculate sleep statistics for a user"""
    query = db.query(
        func.avg(SleepData.duration).label('avg_duration'),
        func.avg(SleepData.sleep_score).label('avg_score'),
        func.avg(SleepData.deep_sleep).label('avg_deep_sleep'),
        func.avg(SleepData.rem_sleep).label('avg_rem_sleep')
    ).filter(
        SleepData.user_id == user_id,
        SleepData.date.between(start_date, end_date)
    ).first()

    # Get best and worst sleep days
    best_sleep = db.query(SleepData).filter(
        SleepData.user_id == user_id,
        SleepData.date.between(start_date, end_date)
    ).order_by(SleepData.sleep_score.desc()).first()

    worst_sleep = db.query(SleepData).filter(
        SleepData.user_id == user_id,
        SleepData.date.between(start_date, end_date)
    ).order_by(SleepData.sleep_score.asc()).first()

    return {
        "average_duration": query.avg_duration or 0,
        "average_quality": query.avg_score or 0,
        "average_deep_sleep": query.avg_deep_sleep or 0,
        "average_rem_sleep": query.avg_rem_sleep or 0,
        "average_sleep_score": query.avg_score or 0,
        "best_quality_day": best_sleep.date if best_sleep else None,
        "worst_quality_day": worst_sleep.date if worst_sleep else None
    }

def get_recovery_statistics(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session
) -> Dict[str, Any]:
    """Calculate recovery statistics for a user"""
    query = db.query(
        func.avg(RecoveryMetrics.readiness_score).label('avg_readiness'),
        func.avg(RecoveryMetrics.hrv_score).label('avg_hrv'),
        func.avg(RecoveryMetrics.resting_heart_rate).label('avg_rhr'),
        func.count(RecoveryMetrics.id).filter(
            RecoveryMetrics.recovery_status == RecoveryStatus.OPTIMAL
        ).label('optimal_days'),
        func.count(RecoveryMetrics.id).filter(
            RecoveryMetrics.recovery_status == RecoveryStatus.NEEDS_REST
        ).label('rest_days')
    ).filter(
        RecoveryMetrics.user_id == user_id,
        RecoveryMetrics.date.between(start_date, end_date)
    ).first()

    # Get recovery trend
    trend = db.query(
        RecoveryMetrics.date,
        RecoveryMetrics.readiness_score,
        RecoveryMetrics.recovery_status
    ).filter(
        RecoveryMetrics.user_id == user_id,
        RecoveryMetrics.date.between(start_date, end_date)
    ).order_by(RecoveryMetrics.date.asc()).all()

    return {
        "average_readiness": query.avg_readiness or 0,
        "average_hrv": query.avg_hrv or 0,
        "average_resting_heart_rate": query.avg_rhr or 0,
        "optimal_recovery_days": query.optimal_days or 0,
        "needs_rest_days": query.rest_days or 0,
        "recovery_trend": [
            {
                "date": t.date,
                "score": t.readiness_score,
                "status": t.recovery_status
            } for t in trend
        ]
    }

def get_health_statistics(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session
) -> Dict[str, Any]:
    """Calculate health statistics for a user"""
    query = db.query(
        func.avg(HealthMetrics.steps).label('avg_steps'),
        func.avg(HealthMetrics.calories_active).label('avg_calories'),
        func.avg(HealthMetrics.blood_oxygen).label('avg_blood_oxygen'),
        func.avg(HealthMetrics.hydration).label('avg_hydration')
    ).filter(
        HealthMetrics.user_id == user_id,
        HealthMetrics.date.between(start_date, end_date)
    ).first()

    # Get steps trend
    steps_trend = db.query(
        HealthMetrics.date,
        HealthMetrics.steps
    ).filter(
        HealthMetrics.user_id == user_id,
        HealthMetrics.date.between(start_date, end_date)
    ).order_by(HealthMetrics.date.asc()).all()

    # Get calories trend
    calories_trend = db.query(
        HealthMetrics.date,
        HealthMetrics.calories_active,
        HealthMetrics.calories_basal
    ).filter(
        HealthMetrics.user_id == user_id,
        HealthMetrics.date.between(start_date, end_date)
    ).order_by(HealthMetrics.date.asc()).all()

    return {
        "average_steps": int(query.avg_steps or 0),
        "average_calories_active": query.avg_calories or 0,
        "average_blood_oxygen": query.avg_blood_oxygen or 0,
        "average_hydration": query.avg_hydration or 0,
        "steps_trend": [
            {
                "date": t.date,
                "steps": t.steps
            } for t in steps_trend
        ],
        "calories_trend": [
            {
                "date": t.date,
                "active": t.calories_active,
                "basal": t.calories_basal
            } for t in calories_trend
        ]
    }

def get_recovery_recommendation(
    user_id: int,
    db: Session
) -> Dict[str, Any]:
    """Generate recovery recommendations based on recent metrics"""
    # Get latest metrics
    latest_sleep = db.query(SleepData).filter(
        SleepData.user_id == user_id
    ).order_by(SleepData.date.desc()).first()

    latest_recovery = db.query(RecoveryMetrics).filter(
        RecoveryMetrics.user_id == user_id
    ).order_by(RecoveryMetrics.date.desc()).first()

    latest_health = db.query(HealthMetrics).filter(
        HealthMetrics.user_id == user_id
    ).order_by(HealthMetrics.date.desc()).first()

    recommendations = []

    if latest_recovery and latest_recovery.recovery_status == RecoveryStatus.NEEDS_REST:
        recommendations.append({
            "type": "rest",
            "priority": "high",
            "message": "Your body needs rest. Consider taking a recovery day.",
            "actions": [
                "Get 8+ hours of sleep",
                "Focus on light stretching",
                "Stay hydrated"
            ]
        })

    if latest_sleep and latest_sleep.sleep_score < 70:
        recommendations.append({
            "type": "sleep",
            "priority": "medium",
            "message": "Your sleep quality could be improved.",
            "actions": [
                "Maintain a consistent sleep schedule",
                "Avoid screens before bedtime",
                "Create a relaxing bedtime routine"
            ]
        })

    if latest_health and latest_health.hydration < 60:
        recommendations.append({
            "type": "hydration",
            "priority": "medium",
            "message": "Your hydration levels are low.",
            "actions": [
                "Drink water regularly throughout the day",
                "Monitor urine color",
                "Increase electrolyte intake"
            ]
        })

    return {
        "recommendations": recommendations,
        "based_on": {
            "sleep_data": bool(latest_sleep),
            "recovery_data": bool(latest_recovery),
            "health_data": bool(latest_health)
        }
    }