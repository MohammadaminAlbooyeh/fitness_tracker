from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import numpy as np
from datetime import datetime, timedelta

from app.models.professional import Professional, Specialization, Availability
from app.models.client import Client, ClientPreferences
from app.schemas.professional import ProfessionalType, ConsultationType

class MatchingService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_specialization_score(
        self,
        professional_specializations: List[Specialization],
        client_preferences: ClientPreferences
    ) -> float:
        """Calculate match score based on specializations."""
        if not professional_specializations or not client_preferences.specialization_ids:
            return 0.0

        matched_specializations = len(
            set(s.id for s in professional_specializations) & 
            set(client_preferences.specialization_ids)
        )
        return matched_specializations / len(client_preferences.specialization_ids)

    def calculate_availability_score(
        self,
        professional_availability: List[Availability],
        preferred_times: List[Dict[str, Any]]
    ) -> float:
        """Calculate match score based on availability."""
        if not professional_availability or not preferred_times:
            return 0.0

        total_matches = 0
        for pref_time in preferred_times:
            day_of_week = pref_time["day_of_week"]
            start_hour = pref_time["start_hour"]
            end_hour = pref_time["end_hour"]

            for slot in professional_availability:
                if (slot.day_of_week == day_of_week and
                    slot.start_time.hour <= end_hour and
                    slot.end_time.hour >= start_hour and
                    slot.available):
                    total_matches += 1
                    break

        return total_matches / len(preferred_times)

    def calculate_consultation_type_score(
        self,
        professional_type: ConsultationType,
        preferred_type: ConsultationType
    ) -> float:
        """Calculate match score based on consultation type."""
        if professional_type == preferred_type:
            return 1.0
        elif professional_type == ConsultationType.BOTH:
            return 0.8
        return 0.0

    def calculate_price_score(
        self,
        professional_rate: float,
        max_budget: float
    ) -> float:
        """Calculate match score based on price."""
        if professional_rate > max_budget:
            return 0.0
        return 1.0 - (professional_rate / max_budget)

    def calculate_location_score(
        self,
        professional_location: Dict[str, float],
        client_location: Dict[str, float],
        max_distance: float = 50.0  # km
    ) -> float:
        """Calculate match score based on location (for in-person sessions)."""
        if not professional_location or not client_location:
            return 0.0

        distance = self._calculate_distance(
            professional_location["latitude"],
            professional_location["longitude"],
            client_location["latitude"],
            client_location["longitude"]
        )

        if distance > max_distance:
            return 0.0
        return 1.0 - (distance / max_distance)

    def _calculate_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """Calculate distance between two points using Haversine formula."""
        R = 6371  # Earth's radius in kilometers

        lat1_rad = np.radians(lat1)
        lon1_rad = np.radians(lon1)
        lat2_rad = np.radians(lat2)
        lon2_rad = np.radians(lon2)

        d_lat = lat2_rad - lat1_rad
        d_lon = lon2_rad - lon1_rad

        a = (np.sin(d_lat/2) ** 2 + 
             np.cos(lat1_rad) * np.cos(lat2_rad) * 
             np.sin(d_lon/2) ** 2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

        return R * c

    def find_matches(
        self,
        client_id: int,
        professional_type: Optional[ProfessionalType] = None,
        consultation_type: Optional[ConsultationType] = None,
        max_budget: Optional[float] = None,
        min_rating: Optional[float] = None,
        specialization_ids: Optional[List[int]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Find matching professionals based on client preferences."""
        # Get client preferences
        client_prefs = self.db.query(ClientPreferences).filter(
            ClientPreferences.client_id == client_id
        ).first()

        if not client_prefs:
            raise ValueError("Client preferences not found")

        # Base query
        query = self.db.query(Professional)

        # Apply filters
        if professional_type:
            query = query.filter(Professional.professional_type == professional_type)
        if consultation_type:
            query = query.filter(Professional.consultation_type.in_([consultation_type, ConsultationType.BOTH]))
        if max_budget:
            query = query.filter(Professional.hourly_rate <= max_budget)
        if min_rating:
            query = query.filter(Professional.rating >= min_rating)
        if specialization_ids:
            query = query.filter(Professional.specializations.any(Specialization.id.in_(specialization_ids)))

        # Get potential matches
        professionals = query.all()
        matches = []

        for prof in professionals:
            # Calculate individual scores
            specialization_score = self.calculate_specialization_score(
                prof.specializations,
                client_prefs
            )
            
            availability_score = self.calculate_availability_score(
                prof.availability,
                client_prefs.preferred_times
            )
            
            consultation_score = self.calculate_consultation_type_score(
                prof.consultation_type,
                client_prefs.preferred_consultation_type
            )
            
            price_score = self.calculate_price_score(
                prof.hourly_rate,
                client_prefs.max_budget
            )
            
            location_score = (
                self.calculate_location_score(
                    prof.location,
                    client_prefs.location
                ) if prof.consultation_type in [ConsultationType.IN_PERSON, ConsultationType.BOTH]
                else 1.0
            )

            # Calculate weighted total score
            weights = {
                'specialization': 0.3,
                'availability': 0.25,
                'consultation': 0.2,
                'price': 0.15,
                'location': 0.1
            }

            total_score = (
                specialization_score * weights['specialization'] +
                availability_score * weights['availability'] +
                consultation_score * weights['consultation'] +
                price_score * weights['price'] +
                location_score * weights['location']
            )

            matches.append({
                'professional': prof,
                'total_score': total_score,
                'scores': {
                    'specialization': specialization_score,
                    'availability': availability_score,
                    'consultation': consultation_score,
                    'price': price_score,
                    'location': location_score
                }
            })

        # Sort matches by total score
        matches.sort(key=lambda x: x['total_score'], reverse=True)

        return matches[:limit]