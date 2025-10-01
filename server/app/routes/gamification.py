from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models.gamification import Achievement, UserStreak, UserPoints
from ..models.user import User
from ..dependencies import get_current_user
from datetime import datetime, timedelta
import json

router = APIRouter()

# Achievement checking functions
def check_workout_count_achievement(user: User, db: Session):
    workout_count = len(user.workouts)
    achievements = []
    
    milestones = {
        5: "Workout Beginner",
        10: "Workout Enthusiast",
        25: "Workout Warrior",
        50: "Fitness Master",
        100: "Fitness Legend"
    }
    
    for count, name in milestones.items():
        if workout_count >= count:
            achievement = db.query(Achievement).filter(Achievement.name == name).first()
            if achievement and achievement not in user.achievements:
                achievements.append(achievement)
    
    return achievements

def check_streak_achievement(user: User, db: Session):
    if not user.streak:
        return []
    
    achievements = []
    streak_milestones = {
        7: "Week Warrior",
        30: "Monthly Master",
        90: "Quarterly Queen/King",
        180: "Half-Year Hero",
        365: "Year-Long Legend"
    }
    
    for days, name in streak_milestones.items():
        if user.streak.longest_streak >= days:
            achievement = db.query(Achievement).filter(Achievement.name == name).first()
            if achievement and achievement not in user.achievements:
                achievements.append(achievement)
    
    return achievements

@router.get("/achievements/", response_model=List[dict])
async def get_user_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return [
        {
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "icon": achievement.icon,
            "earned_at": next(
                (ua.earned_at for ua in achievement.users 
                 if ua.user_id == current_user.id),
                None
            )
        }
        for achievement in current_user.achievements
    ]

@router.get("/streak/")
async def get_user_streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.streak:
        current_user.streak = UserStreak(user_id=current_user.id)
        db.add(current_user.streak)
        db.commit()
        db.refresh(current_user.streak)
    
    return {
        "current_streak": current_user.streak.current_streak,
        "longest_streak": current_user.streak.longest_streak,
        "last_workout_date": current_user.streak.last_workout_date
    }

@router.post("/check-achievements/")
async def check_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check for new achievements
    new_achievements = []
    new_achievements.extend(check_workout_count_achievement(current_user, db))
    new_achievements.extend(check_streak_achievement(current_user, db))
    
    # Add new achievements to user
    for achievement in new_achievements:
        if achievement not in current_user.achievements:
            current_user.achievements.append(achievement)
            
            # Add points for achievement
            if not current_user.points:
                current_user.points = UserPoints(user_id=current_user.id)
            current_user.points.total_points += achievement.points
            
            # Check for level up
            while current_user.points.total_points >= current_user.points.points_to_next_level:
                current_user.points.level += 1
                current_user.points.points_to_next_level = current_user.points.level * 100
    
    if new_achievements:
        db.commit()
        db.refresh(current_user)
    
    return {"new_achievements": [
        {
            "name": achievement.name,
            "description": achievement.description,
            "points": achievement.points
        }
        for achievement in new_achievements
    ]}

@router.post("/update-streak/")
async def update_streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.streak:
        current_user.streak = UserStreak(user_id=current_user.id)
    
    today = datetime.utcnow().date()
    last_workout = current_user.streak.last_workout_date.date() if current_user.streak.last_workout_date else None
    
    if not last_workout or (today - last_workout).days > 1:
        # Streak broken
        current_user.streak.current_streak = 1
    else:
        # Continue streak
        current_user.streak.current_streak += 1
    
    # Update longest streak if current is higher
    if current_user.streak.current_streak > current_user.streak.longest_streak:
        current_user.streak.longest_streak = current_user.streak.current_streak
    
    current_user.streak.last_workout_date = datetime.utcnow()
    db.commit()
    
    return {
        "current_streak": current_user.streak.current_streak,
        "longest_streak": current_user.streak.longest_streak
    }