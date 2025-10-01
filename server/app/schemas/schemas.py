from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Exercise schemas
class ExerciseBase(BaseModel):
    name: str
    description: str
    category: str

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    id: int

    class Config:
        from_attributes = True

# Workout Exercise schemas
class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[int] = None
    duration: Optional[int] = None

class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass

class WorkoutExercise(WorkoutExerciseBase):
    id: int
    workout_id: int
    exercise: Exercise

    class Config:
        from_attributes = True

# Workout schemas
class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseCreate]

class Workout(WorkoutBase):
    id: int
    user_id: int
    created_at: datetime
    exercises: List[WorkoutExercise]

    class Config:
        from_attributes = True

# Workout Log schemas
class WorkoutLogBase(BaseModel):
    workout_id: int
    notes: Optional[str] = None

class WorkoutLogCreate(WorkoutLogBase):
    pass

class WorkoutLog(WorkoutLogBase):
    id: int
    user_id: int
    completed_at: datetime
    workout: Workout

    class Config:
        from_attributes = True