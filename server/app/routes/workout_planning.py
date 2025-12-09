from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..database.database import get_db
from ..models.workout_planning import WorkoutTemplate, ScheduledWorkout, WorkoutReminder
from ..models.user import User
from ..schemas.workout_planning import (
    WorkoutTemplateCreate,
    WorkoutTemplateResponse,
    ScheduledWorkoutCreate,
    ScheduledWorkoutResponse,
    ReminderCreate,
    ReminderResponse
)
from ..utils.auth import get_current_user
from ..services.reminder_service import schedule_reminder

router = APIRouter()

# Workout Template endpoints
@router.post("/templates", response_model=WorkoutTemplateResponse)
async def create_workout_template(
    template: WorkoutTemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_template = WorkoutTemplate(
        user_id=current_user.id,
        **template.dict(exclude={'exercises'})
    )
    
    for idx, exercise in enumerate(template.exercises):
        db_template.exercises.append({
            'exercise_id': exercise.exercise_id,
            'order': idx,
            'sets': exercise.sets,
            'reps': exercise.reps,
            'rest_time': exercise.rest_time
        })
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.get("/templates", response_model=List[WorkoutTemplateResponse])
async def get_workout_templates(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    include_public: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(WorkoutTemplate)
    
    if include_public:
        query = query.filter(
            (WorkoutTemplate.user_id == current_user.id) |
            (WorkoutTemplate.is_public == True)
        )
    else:
        query = query.filter(WorkoutTemplate.user_id == current_user.id)
    
    if category:
        query = query.filter(WorkoutTemplate.category == category)
    if difficulty:
        query = query.filter(WorkoutTemplate.difficulty == difficulty)
    
    return query.all()

# Scheduled Workout endpoints
@router.post("/schedule", response_model=ScheduledWorkoutResponse)
async def schedule_workout(
    workout: ScheduledWorkoutCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create the scheduled workout
    db_scheduled = ScheduledWorkout(
        user_id=current_user.id,
        **workout.dict(exclude={'reminder'})
    )
    db.add(db_scheduled)
    db.commit()
    db.refresh(db_scheduled)
    
    # Create reminder if requested
    if workout.reminder:
        reminder = WorkoutReminder(
            user_id=current_user.id,
            scheduled_workout_id=db_scheduled.id,
            reminder_time=workout.reminder.reminder_time,
            notification_type=workout.reminder.notification_type
        )
        db.add(reminder)
        db.commit()
        
        # Schedule the reminder in the background task
        schedule_reminder(reminder)
    
    return db_scheduled

@router.get("/schedule", response_model=List[ScheduledWorkoutResponse])
async def get_scheduled_workouts(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(ScheduledWorkout).filter(ScheduledWorkout.user_id == current_user.id)
    
    if start_date:
        query = query.filter(ScheduledWorkout.scheduled_date >= start_date)
    if end_date:
        query = query.filter(ScheduledWorkout.scheduled_date <= end_date)
    if status:
        query = query.filter(ScheduledWorkout.status == status)
    
    return query.order_by(ScheduledWorkout.scheduled_date).all()

@router.put("/schedule/{workout_id}/complete")
async def complete_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workout = db.query(ScheduledWorkout).filter(
        ScheduledWorkout.id == workout_id,
        ScheduledWorkout.user_id == current_user.id
    ).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Scheduled workout not found")
    
    workout.status = 'completed'
    workout.completed_date = datetime.utcnow()
    db.commit()
    
    return {"message": "Workout marked as completed"}

@router.put("/schedule/{workout_id}/reschedule")
async def reschedule_workout(
    workout_id: int,
    new_date: datetime,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workout = db.query(ScheduledWorkout).filter(
        ScheduledWorkout.id == workout_id,
        ScheduledWorkout.user_id == current_user.id
    ).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Scheduled workout not found")
    
    workout.scheduled_date = new_date
    if workout.reminder_enabled:
        # Update reminder
        reminder = db.query(WorkoutReminder).filter(
            WorkoutReminder.scheduled_workout_id == workout_id
        ).first()
        if reminder:
            reminder.reminder_time = new_date - timedelta(hours=1)  # Default 1 hour before
            schedule_reminder(reminder)
    
    db.commit()
    return {"message": "Workout rescheduled successfully"}