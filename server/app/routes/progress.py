from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database.database import get_db
from ..models.progress import BodyMeasurement, ProgressPhoto
from ..models.user import User
from ..dependencies import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class BodyMeasurementCreate(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    body_fat: Optional[float] = None
    muscle_mass: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    hips: Optional[float] = None
    biceps_left: Optional[float] = None
    biceps_right: Optional[float] = None
    thigh_left: Optional[float] = None
    thigh_right: Optional[float] = None

class BodyMeasurementResponse(BodyMeasurementCreate):
    id: int
    date: datetime
    user_id: int

    class Config:
        from_attributes = True

class ProgressPhotoCreate(BaseModel):
    category: str
    notes: Optional[str] = None

class ProgressPhotoResponse(ProgressPhotoCreate):
    id: int
    date: datetime
    photo_url: str
    user_id: int

    class Config:
        from_attributes = True

@router.post("/measurements/", response_model=BodyMeasurementResponse)
async def create_measurement(
    measurement: BodyMeasurementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_measurement = BodyMeasurement(
        user_id=current_user.id,
        **measurement.dict(exclude_unset=True)
    )
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement

@router.get("/measurements/", response_model=List[BodyMeasurementResponse])
async def get_measurements(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    measurements = db.query(BodyMeasurement)\
        .filter(BodyMeasurement.user_id == current_user.id)\
        .order_by(BodyMeasurement.date.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return measurements

@router.post("/photos/", response_model=ProgressPhotoResponse)
async def create_progress_photo(
    category: str,
    notes: Optional[str] = None,
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # TODO: Implement photo upload to cloud storage
    photo_url = f"https://storage.example.com/{current_user.id}/{photo.filename}"
    
    db_photo = ProgressPhoto(
        user_id=current_user.id,
        category=category,
        notes=notes,
        photo_url=photo_url
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

@router.get("/photos/", response_model=List[ProgressPhotoResponse])
async def get_progress_photos(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    photos = db.query(ProgressPhoto)\
        .filter(ProgressPhoto.user_id == current_user.id)\
        .order_by(ProgressPhoto.date.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return photos

@router.get("/measurements/latest", response_model=BodyMeasurementResponse)
async def get_latest_measurement(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    measurement = db.query(BodyMeasurement)\
        .filter(BodyMeasurement.user_id == current_user.id)\
        .order_by(BodyMeasurement.date.desc())\
        .first()
    if not measurement:
        raise HTTPException(status_code=404, detail="No measurements found")
    return measurement

@router.get("/stats")
async def get_progress_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    first_measurement = db.query(BodyMeasurement)\
        .filter(BodyMeasurement.user_id == current_user.id)\
        .order_by(BodyMeasurement.date.asc())\
        .first()
        
    latest_measurement = db.query(BodyMeasurement)\
        .filter(BodyMeasurement.user_id == current_user.id)\
        .order_by(BodyMeasurement.date.desc())\
        .first()
        
    if not first_measurement or not latest_measurement:
        return {
            "weight_change": 0,
            "body_fat_change": 0,
            "muscle_mass_change": 0
        }
        
    return {
        "weight_change": latest_measurement.weight - first_measurement.weight if latest_measurement.weight and first_measurement.weight else 0,
        "body_fat_change": latest_measurement.body_fat - first_measurement.body_fat if latest_measurement.body_fat and first_measurement.body_fat else 0,
        "muscle_mass_change": latest_measurement.muscle_mass - first_measurement.muscle_mass if latest_measurement.muscle_mass and first_measurement.muscle_mass else 0
    }