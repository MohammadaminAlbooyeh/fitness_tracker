from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db, get_current_user
from app.schemas.smart_scheduling import SmartScheduleRequest
from app.schemas.scheduling import EventResponse
from app.services.smart_scheduling import SmartSchedulingService
from app.models.users import User

router = APIRouter()

@router.post("/smart-schedule", response_model=List[EventResponse])
def generate_smart_schedule(
    request: SmartScheduleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate an AI-powered schedule based on user preferences and constraints."""
    try:
        smart_scheduler = SmartSchedulingService(db)
        events = smart_scheduler.generate_smart_schedule(request, current_user.id)
        
        # Convert the generated events to response format
        return [
            EventResponse(
                id=event.id,
                title=event.title,
                start_time=event.start_time,
                duration=event.duration,
                event_type=event.event_type,
                intensity=event.intensity,
                description=event.description,
                user_id=event.user_id
            ) for event in events
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating smart schedule: {str(e)}"
        )