from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database.database import get_db
from ..utils.auth import get_current_user
from ..models.user import User
from ..models.exercise_library import Exercise, Equipment, Muscle, ExerciseProgress
from ..schemas.exercise_library import (
    Exercise as ExerciseSchema,
    ExerciseCreate,
    Equipment as EquipmentSchema,
    EquipmentCreate,
    Muscle as MuscleSchema,
    MuscleCreate,
    ExerciseProgress as ExerciseProgressSchema,
    ExerciseProgressCreate
)
from ..core.storage import upload_file
from sqlalchemy import and_, or_

router = APIRouter()

# Exercise endpoints
@router.post("/exercises/", response_model=ExerciseSchema)
async def create_exercise(
    exercise: ExerciseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_exercise = Exercise(
        **exercise.dict(exclude={'equipment_ids', 'muscle_ids'}),
        created_by=current_user.id,
        is_custom=True
    )
    
    # Add equipment
    for eq_id in exercise.equipment_ids:
        equipment = db.query(Equipment).filter(Equipment.id == eq_id).first()
        if equipment:
            db_exercise.equipment.append(equipment)
    
    # Add muscles
    for muscle_data in exercise.muscle_ids:
        muscle = db.query(Muscle).filter(Muscle.id == muscle_data['muscle_id']).first()
        if muscle:
            db_exercise.muscles.append(muscle)
    
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.get("/exercises/", response_model=List[ExerciseSchema])
async def list_exercises(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    equipment_id: Optional[int] = None,
    muscle_id: Optional[int] = None,
    custom_only: bool = False,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    query = db.query(Exercise)
    
    if category:
        query = query.filter(Exercise.category == category)
    if difficulty:
        query = query.filter(Exercise.difficulty_level == difficulty)
    if equipment_id:
        query = query.filter(Exercise.equipment.any(Equipment.id == equipment_id))
    if muscle_id:
        query = query.filter(Exercise.muscles.any(Muscle.id == muscle_id))
    if custom_only and current_user:
        query = query.filter(Exercise.created_by == current_user.id)
    
    return query.all()

@router.post("/exercises/{exercise_id}/progress", response_model=ExerciseProgressSchema)
async def log_exercise_progress(
    exercise_id: int,
    progress: ExerciseProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Check for personal records
    is_pr = False
    pr_type = None
    
    if progress.weight:
        max_weight = db.query(ExerciseProgress)\
            .filter(
                ExerciseProgress.exercise_id == exercise_id,
                ExerciseProgress.user_id == current_user.id,
                ExerciseProgress.weight.isnot(None)
            )\
            .order_by(ExerciseProgress.weight.desc())\
            .first()
        
        if not max_weight or progress.weight > max_weight.weight:
            is_pr = True
            pr_type = 'weight'
    
    db_progress = ExerciseProgress(
        user_id=current_user.id,
        exercise_id=exercise_id,
        is_personal_record=is_pr,
        pr_type=pr_type,
        **progress.dict()
    )
    
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

@router.post("/exercises/{exercise_id}/video")
async def upload_exercise_video(
    exercise_id: int,
    video: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.created_by == current_user.id
    ).first()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found or unauthorized")
    
    video_url = await upload_file(video, f"exercise_videos/{exercise_id}")
    exercise.video_url = video_url
    db.commit()
    
    return {"video_url": video_url}

# Equipment endpoints
@router.get("/equipment/", response_model=List[EquipmentSchema])
async def list_equipment(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Equipment)
    if category:
        query = query.filter(Equipment.category == category)
    return query.all()

# Muscle endpoints
@router.get("/muscles/", response_model=List[MuscleSchema])
async def list_muscles(
    body_part: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Muscle)
    if body_part:
        query = query.filter(Muscle.body_part == body_part)
    return query.all()

# Progress tracking endpoints
@router.get("/progress/{exercise_id}", response_model=List[ExerciseProgressSchema])
async def get_exercise_progress(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(ExerciseProgress)\
        .filter(
            ExerciseProgress.exercise_id == exercise_id,
            ExerciseProgress.user_id == current_user.id
        )\
        .order_by(ExerciseProgress.date.desc())\
        .all()

@router.get("/progress/personal-records", response_model=List[ExerciseProgressSchema])
async def get_personal_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(ExerciseProgress)\
        .filter(
            ExerciseProgress.user_id == current_user.id,
            ExerciseProgress.is_personal_record == True
        )\
        .order_by(ExerciseProgress.date.desc())\
        .all()