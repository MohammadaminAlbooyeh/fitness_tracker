from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    target_muscle: str

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    id: int
    created_by: int

    class Config:
        from_attributes = True

class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[int] = None  # in kg
    duration: Optional[int] = None  # in seconds

class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass

class WorkoutExercise(WorkoutExerciseBase):
    id: int
    workout_id: int
    exercise: Exercise

    class Config:
        from_attributes = True

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseCreate]

class Workout(WorkoutBase):
    id: int
    created_at: datetime
    created_by: int
    exercises: List[WorkoutExercise]

    class Config:
        from_attributes = True