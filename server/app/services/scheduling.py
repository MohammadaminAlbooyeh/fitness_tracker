from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pytz
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY

from ..models.scheduling import Event, RecurrencePattern, Availability, SchedulePreference
from ..models.health_recovery import RecoveryMetrics
from ..schemas.scheduling import (
    EventType,
    RecurrenceType,
    SchedulingConstraint,
    ConflictDetail
)

def create_recurring_events(
    db: Session,
    event: Event,
    recurrence: RecurrencePattern
) -> List[Event]:
    """Create a series of recurring events based on the recurrence pattern."""
    events = []
    
    # Define the recurrence rule based on pattern type
    freq_map = {
        RecurrenceType.DAILY: DAILY,
        RecurrenceType.WEEKLY: WEEKLY,
        RecurrenceType.MONTHLY: MONTHLY
    }
    
    # Calculate time delta between start and end time
    duration = event.end_time - event.start_time
    
    # Generate recurrence dates
    dates = list(rrule(
        freq=freq_map[recurrence.type],
        interval=recurrence.interval,
        dtstart=recurrence.start_date,
        until=recurrence.end_date,
        count=recurrence.max_occurrences,
        byweekday=recurrence.days_of_week if recurrence.type == RecurrenceType.WEEKLY else None,
        bymonthday=recurrence.day_of_month if recurrence.type == RecurrenceType.MONTHLY else None
    ))
    
    # Create events for each recurrence date
    for date in dates:
        if date not in (recurrence.exceptions or []):
            new_event = Event(
                title=event.title,
                description=event.description,
                event_type=event.event_type,
                start_time=date,
                end_time=date + duration,
                location=event.location,
                created_by=event.created_by,
                recurrence_id=recurrence.id,
                metadata=event.metadata
            )
            events.append(new_event)
    
    return events

def check_scheduling_conflicts(
    db: Session,
    start_time: datetime,
    end_time: datetime,
    participant_ids: List[int],
    exclude_event_id: Optional[int] = None
) -> List[ConflictDetail]:
    """Check for scheduling conflicts with existing events."""
    conflicts = []
    
    # Query events that overlap with the proposed time
    for participant_id in participant_ids:
        overlapping_events = db.query(Event).filter(
            and_(
                or_(
                    Event.created_by == participant_id,
                    Event.participants.any(id=participant_id)
                ),
                Event.start_time < end_time,
                Event.end_time > start_time,
                Event.is_cancelled == False
            )
        )
        
        if exclude_event_id:
            overlapping_events = overlapping_events.filter(Event.id != exclude_event_id)
        
        for event in overlapping_events.all():
            conflicts.append(ConflictDetail(
                event_id=event.id,
                title=event.title,
                start_time=event.start_time,
                end_time=event.end_time,
                event_type=event.event_type
            ))
    
    return conflicts

def expand_recurring_events(
    events: List[Event],
    start_date: datetime,
    end_date: datetime
) -> List[Event]:
    """Expand recurring events into individual event instances."""
    expanded_events = []
    
    for event in events:
        if not event.recurrence_pattern:
            expanded_events.append(event)
            continue
        
        pattern = event.recurrence_pattern
        duration = event.end_time - event.start_time
        
        # Generate recurrence dates
        dates = list(rrule(
            freq=DAILY if pattern.type == RecurrenceType.DAILY else
                 WEEKLY if pattern.type == RecurrenceType.WEEKLY else MONTHLY,
            interval=pattern.interval,
            dtstart=max(pattern.start_date, start_date),
            until=min(pattern.end_date or end_date, end_date),
            byweekday=pattern.days_of_week if pattern.type == RecurrenceType.WEEKLY else None,
            bymonthday=pattern.day_of_month if pattern.type == RecurrenceType.MONTHLY else None
        ))
        
        # Create event instances
        for date in dates:
            if date not in (pattern.exceptions or []):
                expanded_event = Event(
                    id=event.id,
                    title=event.title,
                    description=event.description,
                    event_type=event.event_type,
                    start_time=date,
                    end_time=date + duration,
                    location=event.location,
                    created_by=event.created_by,
                    recurrence_id=event.recurrence_id,
                    metadata=event.metadata,
                    is_cancelled=event.is_cancelled
                )
                expanded_events.append(expanded_event)
    
    return expanded_events

def generate_smart_schedule(
    db: Session,
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    event_types: List[EventType],
    constraints: Optional[SchedulingConstraint] = None
) -> List[Event]:
    """Generate an optimized schedule based on user preferences and constraints."""
    # Get user preferences
    preferences = db.query(SchedulePreference).filter(
        SchedulePreference.user_id == user_id
    ).first()
    
    if not preferences:
        raise ValueError("User preferences not found")
    
    # Get user's availability
    availability = db.query(Availability).filter(
        and_(
            Availability.user_id == user_id,
            Availability.start_time >= start_date,
            Availability.end_time <= end_date,
            Availability.availability_type == "available"
        )
    ).all()
    
    # Get recovery metrics if available
    recovery_metrics = db.query(RecoveryMetrics).filter(
        and_(
            RecoveryMetrics.user_id == user_id,
            RecoveryMetrics.date >= start_date,
            RecoveryMetrics.date <= end_date
        )
    ).all()
    
    proposed_events = []
    current_date = start_date
    
    while current_date <= end_date:
        # Check if current day is a preferred workout day
        day_of_week = current_date.weekday()
        if day_of_week not in preferences.preferred_workout_days:
            current_date += timedelta(days=1)
            continue
        
        # Check recovery status
        recovery_metric = next(
            (m for m in recovery_metrics if m.date.date() == current_date.date()),
            None
        )
        
        if recovery_metric and recovery_metric.readiness_score < 60:
            # Skip if recovery score is too low
            current_date += timedelta(days=1)
            continue
        
        # Find available time slots
        for time_range in preferences.preferred_workout_times:
            slot_start = datetime.combine(current_date.date(), time_range.start)
            slot_end = datetime.combine(current_date.date(), time_range.end)
            
            # Apply constraints
            if constraints:
                if constraints.min_duration:
                    slot_end = min(
                        slot_end,
                        slot_start + timedelta(minutes=constraints.min_duration)
                    )
                if constraints.preferred_time_of_day:
                    if not is_preferred_time_of_day(slot_start, constraints.preferred_time_of_day):
                        continue
            
            # Check for conflicts
            conflicts = check_scheduling_conflicts(
                db, slot_start, slot_end, [user_id]
            )
            
            if not conflicts:
                # Create proposed event
                event = Event(
                    title=f"{event_types[0].value.title()} Session",
                    description="Auto-scheduled workout session",
                    event_type=event_types[0],
                    start_time=slot_start,
                    end_time=slot_end,
                    created_by=user_id,
                    metadata={
                        "auto_scheduled": True,
                        "intensity_level": get_recommended_intensity(recovery_metric)
                    }
                )
                proposed_events.append(event)
                break
        
        current_date += timedelta(days=1)
    
    return proposed_events

def is_preferred_time_of_day(time: datetime, preference: str) -> bool:
    """Check if a given time matches the preferred time of day."""
    hour = time.hour
    if preference == "morning":
        return 5 <= hour < 12
    elif preference == "afternoon":
        return 12 <= hour < 17
    elif preference == "evening":
        return 17 <= hour < 22
    return True

def get_recommended_intensity(recovery_metric: Optional[RecoveryMetrics]) -> str:
    """Determine recommended workout intensity based on recovery metrics."""
    if not recovery_metric:
        return "medium"
    
    if recovery_metric.readiness_score >= 80:
        return "high"
    elif recovery_metric.readiness_score >= 60:
        return "medium"
    else:
        return "low"

def calculate_schedule_score(
    events: List[Event],
    preferences: SchedulePreference,
    constraints: Optional[SchedulingConstraint]
) -> float:
    """Calculate a score for a proposed schedule based on preferences and constraints."""
    score = 0.0
    total_factors = 0
    
    for event in events:
        # Preferred day factor
        if event.start_time.weekday() in preferences.preferred_workout_days:
            score += 1
        total_factors += 1
        
        # Preferred time factor
        for time_range in preferences.preferred_workout_times:
            event_time = event.start_time.time()
            if time_range.start <= event_time <= time_range.end:
                score += 1
                break
        total_factors += 1
        
        # Rest between workouts factor
        if constraints and constraints.min_duration:
            duration = (event.end_time - event.start_time).total_seconds() / 60
            if duration >= constraints.min_duration:
                score += 1
        total_factors += 1
    
    return score / total_factors if total_factors > 0 else 0