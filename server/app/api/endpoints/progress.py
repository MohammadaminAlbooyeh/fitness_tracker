import os
from typing import List
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.api import deps
from app.core.config import settings
from app.models.user import User
from app.models.progress_photos import ProgressPhoto
from app.schemas.progress_photos import ProgressPhotoCreate, ProgressPhoto as ProgressPhotoSchema

router = APIRouter()

@router.post("/photos", response_model=ProgressPhotoSchema)
async def create_progress_photo(
    photo: UploadFile = File(...),
    data: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Parse the form data
    photo_data = json.loads(data)
    
    # Create photo filename with timestamp to ensure uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"progress_photo_{current_user.id}_{timestamp}{os.path.splitext(photo.filename)[1]}"
    
    # Save photo to filesystem
    file_path = os.path.join(settings.MEDIA_ROOT, "progress_photos", filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        content = await photo.read()
        buffer.write(content)
    
    # Create database record
    photo_url = f"{settings.MEDIA_URL}/progress_photos/{filename}"
    db_photo = ProgressPhoto(
        user_id=current_user.id,
        photo_url=photo_url,
        photo_type=photo_data["photo_type"],
        notes=photo_data.get("notes"),
        measurements=photo_data.get("measurements", {})
    )
    
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    
    return db_photo

@router.get("/photos", response_model=List[ProgressPhotoSchema])
def get_progress_photos(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Get all progress photos for the current user"""
    return db.query(ProgressPhoto).filter(
        ProgressPhoto.user_id == current_user.id
    ).order_by(ProgressPhoto.date.desc()).all()