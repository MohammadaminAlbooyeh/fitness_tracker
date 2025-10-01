from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class ProgressPhotoBase(BaseModel):
    photo_type: str
    notes: Optional[str] = None
    measurements: Optional[dict] = None
    
class ProgressPhotoCreate(ProgressPhotoBase):
    pass

class ProgressPhoto(ProgressPhotoBase):
    id: int
    user_id: int
    photo_url: str
    date: datetime
    
    class Config:
        orm_mode = True