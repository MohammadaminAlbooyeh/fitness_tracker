from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime, timedelta

from ..database import get_db
from ..models.scheduling import Event, RecurrencePattern, Availability, SchedulePreference
from ..schemas.scheduling import (
    EventCreate,
    EventUpdate,
    EventResponse,
    RecurrencePatternCreate,
    AvailabilityCreate,
    SchedulePreferenceCreate,
    EventSearch,
    SmartScheduleRequest,
    ConflictCheckResponse
)
from ..services.scheduling import (
    create_recurring_events,
    check_scheduling_conflicts,
    generate_smart_schedule,
    expand_recurring_events
)

router = APIRouter()

# Event endpoints
@router.post("/events", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):
    # Check for scheduling conflicts
    conflicts = check_scheduling_conflicts(
        db,
        event.start_time,
        event.end_time,
        event.participants
    )
    
    if conflicts:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Scheduling conflict detected",
                "conflicts": conflicts
            }
        )
    
    # Create the event
    db_event = Event(**event.dict(exclude={'recurrence', 'participants'}))
    
    # Handle recurrence if specified
    if event.recurrence:
        recurrence_pattern = RecurrencePattern(**event.recurrence.dict())
        db.add(recurrence_pattern)
        db.flush()
        db_event.recurrence_id = recurrence_pattern.id
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event

@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db)
):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check for conflicts if time is being updated
    if event_update.start_time or event_update.end_time:
        conflicts = check_scheduling_conflicts(
            db,
            event_update.start_time or db_event.start_time,
            event_update.end_time or db_event.end_time,
            event_update.participants,
            exclude_event_id=event_id
        )
        if conflicts:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Scheduling conflict detected",
                    "conflicts": conflicts
                }
            )
    
    # Update event fields
    for field, value in event_update.dict(exclude_unset=True).items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/events/{event_id}")
async def delete_event(
    event_id: int,
    delete_series: bool = False,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if delete_series and event.recurrence_id:
        # Delete all events in the series
        db.query(Event).filter(
            Event.recurrence_id == event.recurrence_id
        ).delete()
        # Delete the recurrence pattern
        db.query(RecurrencePattern).filter(
            RecurrencePattern.id == event.recurrence_id
        ).delete()
    else:
        # Mark single event as cancelled
        event.is_cancelled = True
    
    db.commit()
    return {"message": "Event deleted successfully"}

@router.get("/events", response_model=List[EventResponse])
async def get_events(
    start_date: datetime,
    end_date: datetime,
    user_id: Optional[int] = None,
    event_type: Optional[str] = None,
    expand_recurring: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(Event).filter(
        and_(
            Event.start_time >= start_date,
            Event.end_time <= end_date,
            Event.is_cancelled == False
        )
    )
    
    if user_id:
        query = query.filter(
            or_(
                Event.created_by == user_id,
                Event.participants.any(id=user_id)
            )
        )
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    
    events = query.all()
    
    if expand_recurring:
        events = expand_recurring_events(events, start_date, end_date)
    
    return events

# Availability endpoints
@router.post("/availability", response_model=List[Availability])
async def set_availability(
    availability: List[AvailabilityCreate],
    db: Session = Depends(get_db)
):
    db_availabilities = []
    for avail in availability:
        db_avail = Availability(**avail.dict())
        db.add(db_avail)
        db_availabilities.append(db_avail)
    
    db.commit()
    for avail in db_availabilities:
        db.refresh(avail)
    
    return db_availabilities

@router.get("/availability/{user_id}")
async def get_availability(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    availability = db.query(Availability).filter(
        and_(
            Availability.user_id == user_id,
            Availability.start_time >= start_date,
            Availability.end_time <= end_date
        )
    ).all()
    return availability

# Schedule preferences endpoints
@router.post("/preferences", response_model=SchedulePreference)
async def set_schedule_preferences(
    preferences: SchedulePreferenceCreate,
    db: Session = Depends(get_db)
):
    # Update existing preferences or create new ones
    db_preferences = db.query(SchedulePreference).filter(
        SchedulePreference.user_id == preferences.user_id
    ).first()
    
    if db_preferences:
        for field, value in preferences.dict(exclude_unset=True).items():
            setattr(db_preferences, field, value)
    else:
        db_preferences = SchedulePreference(**preferences.dict())
        db.add(db_preferences)
    
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

@router.get("/preferences/{user_id}", response_model=SchedulePreference)
async def get_schedule_preferences(
    user_id: int,
    db: Session = Depends(get_db)
):
    preferences = db.query(SchedulePreference).filter(
        SchedulePreference.user_id == user_id
    ).first()
    if not preferences:
        raise HTTPException(status_code=404, detail="Schedule preferences not found")
    return preferences

# Smart scheduling endpoints
@router.post("/smart-schedule")
async def create_smart_schedule(
    request: SmartScheduleRequest,
    db: Session = Depends(get_db)
):
    schedule = generate_smart_schedule(
        db,
        request.user_id,
        request.start_date,
        request.end_date,
        request.event_types,
        request.constraints
    )
    return schedule

@router.post("/check-conflicts")
async def check_conflicts(
    event: EventCreate,
    db: Session = Depends(get_db)
) -> ConflictCheckResponse:
    conflicts = check_scheduling_conflicts(
        db,
        event.start_time,
        event.end_time,
        event.participants
    )
    return ConflictCheckResponse(has_conflicts=bool(conflicts), conflicts=conflicts)