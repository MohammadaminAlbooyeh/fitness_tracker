from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    profile_picture: Optional[str]
    bio: Optional[str]

    class Config:
        orm_mode = True

class ChallengeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_date: datetime
    end_date: datetime
    challenge_type: str = Field(..., min_length=1, max_length=50)
    target_value: int
    is_public: bool = True

class ChallengeResponse(ChallengeCreate):
    id: int
    creator_id: int
    status: str
    created_at: datetime
    participants: List[UserResponse]

    class Config:
        orm_mode = True

class ChallengeActivityCreate(BaseModel):
    value: int
    notes: Optional[str] = Field(None, max_length=200)

class ChallengeActivityResponse(ChallengeActivityCreate):
    id: int
    challenge_id: int
    user_id: int
    activity_date: datetime

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)
    workout_id: Optional[int]
    achievement_id: Optional[int]

class PostResponse(PostCreate):
    id: int
    user_id: int
    created_at: datetime
    likes_count: int
    comments_count: int
    user: UserResponse

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=200)

class CommentResponse(CommentCreate):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    user: UserResponse

    class Config:
        orm_mode = True

class LikeResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True