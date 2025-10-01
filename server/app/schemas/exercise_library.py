from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

class MuscleBase(BaseModel):
    name: str
    description: Optional[str] = None
    body_part: str
    image_url: Optional[HttpUrl] = None

class MuscleCreate(MuscleBase):
    pass

class Muscle(MuscleBase):
    id: int

    class Config:
        orm_mode = True

class EquipmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    image_url: Optional[HttpUrl] = None

class EquipmentCreate(EquipmentBase):
    pass

class Equipment(EquipmentBase):
    id: int

    class Config:
        orm_mode = True

class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    instructions: Optional[str] = None
    difficulty_level: str = Field(..., regex='^(beginner|intermediate|advanced)$')
    category: str
    video_url: Optional[HttpUrl] = None
    thumbnail_url: Optional[HttpUrl] = None
    form_tips: Optional[str] = None
    safety_warnings: Optional[str] = None
    parent_exercise_id: Optional[int] = None

class ExerciseCreate(ExerciseBase):
    equipment_ids: List[int] = []
    muscle_ids: List[dict] = Field(..., description="List of {muscle_id: int, is_primary: bool}")

class Exercise(ExerciseBase):
    id: int
    is_custom: bool
    created_by: Optional[int]
    created_at: datetime
    equipment: List[Equipment] = []
    muscles: List[Muscle] = []
    variations: List['Exercise'] = []

    class Config:
        orm_mode = True

class ExerciseProgressBase(BaseModel):
    exercise_id: int
    weight: Optional[float] = None
    reps: Optional[int] = None
    sets: Optional[int] = None
    duration: Optional[int] = None
    distance: Optional[float] = None
    notes: Optional[str] = None
    form_rating: Optional[int] = Field(None, ge=1, le=5)
    form_feedback: Optional[str] = None

class ExerciseProgressCreate(ExerciseProgressBase):
    pass

class ExerciseProgress(ExerciseProgressBase):
    id: int
    user_id: int
    date: datetime
    is_personal_record: bool
    pr_type: Optional[str]
    exercise: Exercise

    class Config:
        orm_mode = True

# Update forward references
Exercise.update_forward_refs()