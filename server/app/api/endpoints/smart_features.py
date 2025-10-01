import os
import cv2
import numpy as np
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.smart_features import (
    FormCheckResult,
    WorkoutRecommendation,
    RecommendationFilter,
    FormCheckStatus,
    FeedbackSeverity,
    FormFeedbackItem
)
from app.models.smart_features import FormCheck, WorkoutRecommendation as WorkoutRecommendationModel
from app.core.ai_model import AIModel
from app.utils.storage import save_video, get_video_url

router = APIRouter()
ai_model = AIModel()

@router.post("/form-check/upload", response_model=FormCheckResult)
async def upload_form_check_video(
    exercise_id: str,
    video: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a video for form checking"""
    if not video.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    # Save video to storage and get URL
    video_url = await save_video(video, f"form_checks/{current_user.id}")
    
    # Create form check record
    form_check = FormCheck(
        user_id=current_user.id,
        exercise_id=exercise_id,
        video_url=video_url,
        status=FormCheckStatus.PENDING
    )
    db.add(form_check)
    db.commit()
    db.refresh(form_check)
    
    return FormCheckResult(
        id=str(form_check.id),
        user_id=current_user.id,
        exercise_id=exercise_id,
        video_url=video_url,
        status=FormCheckStatus.PENDING
    )

@router.post("/form-check/{check_id}/start", response_model=FormCheckResult)
async def start_form_check(
    check_id: str,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start processing a form check video"""
    form_check = db.query(FormCheck).filter(
        FormCheck.id == check_id,
        FormCheck.user_id == current_user.id
    ).first()
    
    if not form_check:
        raise HTTPException(status_code=404, detail="Form check not found")
    
    if form_check.status != FormCheckStatus.PENDING:
        raise HTTPException(status_code=400, detail="Form check already processed or processing")
    
    # Update status to processing
    form_check.status = FormCheckStatus.PROCESSING
    db.commit()
    
    # Add form check processing to background tasks
    background_tasks.add_task(process_form_check, form_check.id, db)
    
    return FormCheckResult(
        id=str(form_check.id),
        user_id=current_user.id,
        exercise_id=form_check.exercise_id,
        video_url=form_check.video_url,
        status=FormCheckStatus.PROCESSING
    )

async def process_form_check(check_id: str, db: Session):
    """Process form check video in background"""
    form_check = db.query(FormCheck).filter(FormCheck.id == check_id).first()
    if not form_check:
        return
    
    try:
        # Get video from storage
        video_path = await get_video_url(form_check.video_url)
        
        # Process video with AI model
        results = ai_model.analyze_form(video_path)
        
        # Update form check with results
        form_check.status = FormCheckStatus.COMPLETED
        form_check.score = results['score']
        form_check.analysis = results['analysis']
        form_check.feedback = [
            FormFeedbackItem(
                message=fb['message'],
                suggestion=fb['suggestion'],
                severity=fb['severity']
            ) for fb in results['feedback']
        ]
        
    except Exception as e:
        form_check.status = FormCheckStatus.FAILED
        form_check.error = str(e)
    
    db.commit()

@router.get("/form-check/{check_id}/results", response_model=FormCheckResult)
async def get_form_check_results(
    check_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get form check results"""
    form_check = db.query(FormCheck).filter(
        FormCheck.id == check_id,
        FormCheck.user_id == current_user.id
    ).first()
    
    if not form_check:
        raise HTTPException(status_code=404, detail="Form check not found")
    
    return FormCheckResult(
        id=str(form_check.id),
        user_id=current_user.id,
        exercise_id=form_check.exercise_id,
        video_url=form_check.video_url,
        status=form_check.status,
        score=form_check.score,
        analysis=form_check.analysis,
        feedback=form_check.feedback
    )

@router.post("/workout-recommendations", response_model=List[WorkoutRecommendation])
async def get_workout_recommendations(
    filters: Optional[RecommendationFilter] = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized workout recommendations"""
    # Get user's workout history and preferences
    user_data = ai_model.get_user_data(current_user.id)
    
    # Generate recommendations based on user data and filters
    recommendations = ai_model.generate_recommendations(user_data, filters)
    
    # Save recommendations to database
    db_recommendations = []
    for rec in recommendations:
        db_rec = WorkoutRecommendationModel(
            user_id=current_user.id,
            name=rec['name'],
            description=rec['description'],
            type=rec['type'],
            intensity=rec['intensity'],
            duration=rec['duration'],
            focus=rec['focus'],
            difficulty=rec['difficulty'],
            exercises=rec['exercises'],
            factors=rec['factors']
        )
        db.add(db_rec)
        db_recommendations.append(db_rec)
    
    db.commit()
    
    return [WorkoutRecommendation.from_orm(rec) for rec in db_recommendations]

@router.post("/workout-recommendations/{recommendation_id}/feedback")
async def update_recommendation_feedback(
    recommendation_id: str,
    feedback: bool,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user feedback for a workout recommendation"""
    recommendation = db.query(WorkoutRecommendationModel).filter(
        WorkoutRecommendationModel.id == recommendation_id,
        WorkoutRecommendationModel.user_id == current_user.id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    recommendation.user_feedback = feedback
    db.commit()
    
    # Update AI model with feedback
    ai_model.update_from_feedback(recommendation_id, feedback)
    
    return {"status": "success"}

@router.post("/workout-recommendations/{recommendation_id}/alternative")
async def generate_new_recommendation(
    recommendation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate an alternative workout recommendation"""
    original = db.query(WorkoutRecommendationModel).filter(
        WorkoutRecommendationModel.id == recommendation_id,
        WorkoutRecommendationModel.user_id == current_user.id
    ).first()
    
    if not original:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    # Generate alternative recommendation
    alternative = ai_model.generate_alternative(original)
    
    # Save new recommendation
    db_rec = WorkoutRecommendationModel(
        user_id=current_user.id,
        name=alternative['name'],
        description=alternative['description'],
        type=alternative['type'],
        intensity=alternative['intensity'],
        duration=alternative['duration'],
        focus=alternative['focus'],
        difficulty=alternative['difficulty'],
        exercises=alternative['exercises'],
        factors=alternative['factors']
    )
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)
    
    return WorkoutRecommendation.from_orm(db_rec)

@router.get("/workout-recommendations/{recommendation_id}/insights")
async def get_recommendation_insights(
    recommendation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get insights about why a workout was recommended"""
    recommendation = db.query(WorkoutRecommendationModel).filter(
        WorkoutRecommendationModel.id == recommendation_id,
        WorkoutRecommendationModel.user_id == current_user.id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    return {
        "factors": recommendation.factors
    }