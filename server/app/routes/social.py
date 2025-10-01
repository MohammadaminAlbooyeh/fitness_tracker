from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models.social import Challenge, ChallengeActivity, Post, PostLike, PostComment
from ..models.user import User
from ..schemas.social import (
    ChallengeCreate,
    ChallengeResponse,
    ChallengeActivityCreate,
    PostCreate,
    PostResponse,
    CommentCreate,
    CommentResponse,
    UserResponse
)
from ..auth import get_current_user

router = APIRouter()

# Friend system endpoints
@router.post("/friends/request/{user_id}", response_model=UserResponse)
async def send_friend_request(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send friend request to yourself")
    
    friend = db.query(User).filter(User.id == user_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="User not found")
    
    if friend in current_user.friends:
        raise HTTPException(status_code=400, detail="Already friends with this user")
    
    current_user.friends.append(friend)
    db.commit()
    return friend

@router.get("/friends", response_model=List[UserResponse])
async def get_friends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return current_user.friends

# Challenge endpoints
@router.post("/challenges", response_model=ChallengeResponse)
async def create_challenge(
    challenge: ChallengeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_challenge = Challenge(
        name=challenge.name,
        description=challenge.description,
        creator_id=current_user.id,
        start_date=challenge.start_date,
        end_date=challenge.end_date,
        challenge_type=challenge.challenge_type,
        target_value=challenge.target_value,
        is_public=challenge.is_public
    )
    db_challenge.participants.append(current_user)
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

@router.post("/challenges/{challenge_id}/join")
async def join_challenge(
    challenge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    if current_user in challenge.participants:
        raise HTTPException(status_code=400, detail="Already participating in this challenge")
    
    challenge.participants.append(current_user)
    db.commit()
    return {"message": "Successfully joined the challenge"}

@router.post("/challenges/{challenge_id}/activity")
async def log_challenge_activity(
    challenge_id: int,
    activity: ChallengeActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    if current_user not in challenge.participants:
        raise HTTPException(status_code=403, detail="Not participating in this challenge")
    
    db_activity = ChallengeActivity(
        challenge_id=challenge_id,
        user_id=current_user.id,
        value=activity.value,
        notes=activity.notes
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

# Social feed endpoints
@router.post("/posts", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_post = Post(
        user_id=current_user.id,
        content=post.content,
        workout_id=post.workout_id,
        achievement_id=post.achievement_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/feed", response_model=List[PostResponse])
async def get_feed(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get posts from friends and self
    friend_ids = [friend.id for friend in current_user.friends]
    friend_ids.append(current_user.id)
    
    posts = db.query(Post)\
        .filter(Post.user_id.in_(friend_ids))\
        .order_by(Post.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return posts

@router.post("/posts/{post_id}/like")
async def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_like = db.query(PostLike)\
        .filter(PostLike.post_id == post_id, PostLike.user_id == current_user.id)\
        .first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked this post")
    
    like = PostLike(post_id=post_id, user_id=current_user.id)
    post.likes_count += 1
    db.add(like)
    db.commit()
    return {"message": "Post liked successfully"}

@router.post("/posts/{post_id}/comment", response_model=CommentResponse)
async def comment_on_post(
    post_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = PostComment(
        post_id=post_id,
        user_id=current_user.id,
        content=comment.content
    )
    post.comments_count += 1
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment