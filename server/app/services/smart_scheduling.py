from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.models.scheduling import Event, RecurrencePattern, Availability
from app.models.health import RecoveryMetrics
from sqlalchemy.orm import Session
from app.schemas.scheduling import EventCreate, SmartScheduleRequest
import numpy as np
from datetime import time

class SmartSchedulingService:
    def __init__(self, db: Session):
        self.db = db

    def _get_time_slot_score(
        self,
        slot_start: datetime,
        preferred_time: str,
        recovery_metrics: Optional[RecoveryMetrics],
        existing_events: List[Event]
    ) -> float:
        """Calculate a score for a potential time slot based on various factors."""
        score = 0.0
        
        # Time of day preference scoring
        hour = slot_start.hour
        if preferred_time == 'morning' and 5 <= hour < 12:
            score += 30
        elif preferred_time == 'afternoon' and 12 <= hour < 17:
            score += 30
        elif preferred_time == 'evening' and 17 <= hour < 22:
            score += 30
        
        # Recovery metrics scoring
        if recovery_metrics:
            readiness_score = recovery_metrics.readiness_score
            # Higher readiness score increases the slot's viability
            score += min(readiness_score / 2, 30)
            
            # Consider sleep quality if available
            if recovery_metrics.sleep_quality:
                score += min(recovery_metrics.sleep_quality * 10, 20)
        
        # Event spacing scoring
        for event in existing_events:
            time_diff = abs((slot_start - event.start_time).total_seconds() / 3600)
            if time_diff < 4:  # Less than 4 hours apart
                score -= 20
            elif time_diff < 8:  # Less than 8 hours apart
                score -= 10
        
        # Prefer slots not too early or too late
        if hour < 5 or hour >= 22:
            score -= 50
            
        return score

    def _check_slot_availability(
        self,
        slot_start: datetime,
        duration: int,
        existing_events: List[Event]
    ) -> bool:
        """Check if a time slot is available."""
        slot_end = slot_start + timedelta(minutes=duration)
        
        for event in existing_events:
            event_end = event.start_time + timedelta(minutes=event.duration)
            
            # Check for overlap
            if not (slot_end <= event.start_time or slot_start >= event_end):
                return False
                
        return True

    def _get_valid_time_slots(
        self,
        start_date: datetime,
        end_date: datetime,
        duration: int,
        existing_events: List[Event]
    ) -> List[datetime]:
        """Generate valid time slots between start and end dates."""
        valid_slots = []
        current_time = start_date
        
        while current_time < end_date:
            # Only consider slots during reasonable hours (5 AM to 10 PM)
            if 5 <= current_time.hour < 22:
                if self._check_slot_availability(current_time, duration, existing_events):
                    valid_slots.append(current_time)
            
            # Move to next slot (30-minute intervals)
            current_time += timedelta(minutes=30)
            
        return valid_slots

    def generate_smart_schedule(
        self,
        request: SmartScheduleRequest,
        user_id: int
    ) -> List[EventCreate]:
        """Generate an optimized schedule based on user preferences and constraints."""
        # Get existing events
        existing_events = self.db.query(Event).filter(
            Event.user_id == user_id,
            Event.start_time >= request.start_date,
            Event.start_time <= request.end_date
        ).all()
        
        # Get latest recovery metrics
        recovery_metrics = self.db.query(RecoveryMetrics).filter(
            RecoveryMetrics.user_id == user_id
        ).order_by(RecoveryMetrics.timestamp.desc()).first()
        
        # Calculate average duration within constraints
        duration = (request.constraints.min_duration + request.constraints.max_duration) // 2
        
        # Get all possible time slots
        valid_slots = self._get_valid_time_slots(
            request.start_date,
            request.end_date,
            duration,
            existing_events
        )
        
        # Score all valid slots
        slot_scores = [
            (
                slot,
                self._get_time_slot_score(
                    slot,
                    request.constraints.preferred_time_of_day,
                    recovery_metrics,
                    existing_events
                )
            )
            for slot in valid_slots
        ]
        
        # Sort slots by score
        slot_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Generate events based on user preferences
        generated_events = []
        events_per_week = 3  # Default to 3 workouts per week
        
        # Calculate weeks between start and end date
        weeks = ((request.end_date - request.start_date).days + 6) // 7
        total_events = weeks * events_per_week
        
        # Take the top N scored slots
        selected_slots = slot_scores[:total_events]
        
        for slot, score in selected_slots:
            event = EventCreate(
                title=f"Smart Scheduled Workout",
                start_time=slot,
                duration=duration,
                event_type="workout",
                intensity=request.constraints.intensity_level,
                description="AI-generated workout session based on your preferences and recovery metrics.",
                user_id=user_id
            )
            generated_events.append(event)
            
        return generated_events

    def adjust_schedule_for_recovery(
        self,
        events: List[EventCreate],
        recovery_metrics: RecoveryMetrics
    ) -> List[EventCreate]:
        """Adjust schedule based on recovery metrics."""
        adjusted_events = []
        
        for event in events:
            # Adjust intensity based on recovery
            if recovery_metrics.readiness_score < 60:
                event.intensity = "low"
            elif recovery_metrics.readiness_score < 80:
                event.intensity = "medium"
                
            # Adjust duration if recovery is poor
            if recovery_metrics.readiness_score < 50:
                event.duration = max(30, event.duration - 15)
                
            adjusted_events.append(event)
            
        return adjusted_events