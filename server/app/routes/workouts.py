from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter()

# Exercise endpoints
@router.get("/exercises", response_model=List[schemas.Exercise])
def get_exercises(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    exercises = db.query(models.Exercise).offset(skip).limit(limit).all()
    return exercises

@router.post("/exercises", response_model=schemas.Exercise)
def create_exercise(
    exercise: schemas.ExerciseCreate,
    db: Session = Depends(get_db)
):
    db_exercise = models.Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

# Workout endpoints
@router.get("/workouts", response_model=List[schemas.Workout])
def get_workouts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    workouts = db.query(models.Workout).offset(skip).limit(limit).all()
    return workouts

@router.post("/workouts", response_model=schemas.Workout)
def create_workout(
    workout: schemas.WorkoutCreate,
    db: Session = Depends(get_db)
):
    # Create workout
    db_workout = models.Workout(
        name=workout.name,
        description=workout.description
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    
    # Add exercises to workout
    for exercise in workout.exercises:
        db_workout_exercise = models.WorkoutExercise(
            workout_id=db_workout.id,
            **exercise.dict()
        )
        db.add(db_workout_exercise)
    
    db.commit()
    db.refresh(db_workout)
    return db_workout

# Workout log endpoints
@router.post("/workout-logs", response_model=schemas.WorkoutLog)
def log_workout(
    log: schemas.WorkoutLogCreate,
    db: Session = Depends(get_db)
):
    db_log = models.WorkoutLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/workout-logs", response_model=List[schemas.WorkoutLog])
def get_workout_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    logs = db.query(models.WorkoutLog).offset(skip).limit(limit).all()
    return logs