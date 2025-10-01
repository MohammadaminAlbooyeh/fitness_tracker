from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from typing import List, Optional

from app.models.professional import (
    Professional,
    Specialization,
    Certification,
    ProfessionalService,
    Availability,
    ClientProgressNote
)
from app.schemas.professional import (
    ProfessionalCreate,
    ProfessionalUpdate,
    ProfessionalSearchParams,
    ProfessionalStats,
    ProfessionalServiceCreate,
    ProfessionalServiceUpdate,
    AvailabilityCreate,
    AvailabilityUpdate,
    ClientProgressNoteCreate,
    ClientProgressNoteUpdate
)
from app.crud.base import CRUDBase
from fastapi import HTTPException

class CRUDProfessional(CRUDBase[Professional, ProfessionalCreate, ProfessionalUpdate]):
    def create_professional(
        self, 
        db: Session, 
        professional: ProfessionalCreate,
        user_id: int
    ) -> Professional:
        """Create a new professional profile."""
        # Check if professional already exists
        if db.query(Professional).filter(Professional.user_id == user_id).first():
            raise HTTPException(
                status_code=400,
                detail="Professional profile already exists for this user"
            )

        # Create professional instance
        db_professional = Professional(
            user_id=user_id,
            **professional.dict(exclude={'specialization_ids', 'certification_ids'})
        )

        # Add specializations
        specializations = (
            db.query(Specialization)
            .filter(Specialization.id.in_(professional.specialization_ids))
            .all()
        )
        if len(specializations) != len(professional.specialization_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more specialization IDs are invalid"
            )
        db_professional.specializations = specializations

        # Add certifications
        certifications = (
            db.query(Certification)
            .filter(Certification.id.in_(professional.certification_ids))
            .all()
        )
        if len(certifications) != len(professional.certification_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more certification IDs are invalid"
            )
        db_professional.certifications = certifications

        db.add(db_professional)
        db.commit()
        db.refresh(db_professional)
        return db_professional

    def update_professional(
        self,
        db: Session,
        professional_id: int,
        professional: ProfessionalUpdate
    ) -> Professional:
        """Update a professional profile."""
        db_professional = self.get(db, professional_id)
        if not db_professional:
            raise HTTPException(
                status_code=404,
                detail="Professional not found"
            )

        update_data = professional.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_professional, field, value)

        db.add(db_professional)
        db.commit()
        db.refresh(db_professional)
        return db_professional

    def create_service(
        self,
        db: Session,
        service: ProfessionalServiceCreate,
        professional_id: int
    ) -> ProfessionalService:
        """Create a new professional service."""
        db_service = ProfessionalService(**service.dict(), professional_id=professional_id)
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return db_service

    def get_services(
        self,
        db: Session,
        professional_id: int
    ) -> List[ProfessionalService]:
        """Get all services for a professional."""
        return (
            db.query(ProfessionalService)
            .filter(ProfessionalService.professional_id == professional_id)
            .all()
        )

    def update_service(
        self,
        db: Session,
        service_id: int,
        service: ProfessionalServiceUpdate,
        professional_id: int
    ) -> ProfessionalService:
        """Update a professional service."""
        db_service = (
            db.query(ProfessionalService)
            .filter(
                and_(
                    ProfessionalService.id == service_id,
                    ProfessionalService.professional_id == professional_id
                )
            )
            .first()
        )
        if not db_service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        update_data = service.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_service, field, value)

        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return db_service

    def create_availability(
        self,
        db: Session,
        availability: AvailabilityCreate,
        professional_id: int
    ) -> Availability:
        """Create a new availability slot."""
        db_availability = Availability(
            **availability.dict(),
            professional_id=professional_id
        )
        db.add(db_availability)
        db.commit()
        db.refresh(db_availability)
        return db_availability

    def get_availability(
        self,
        db: Session,
        professional_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Availability]:
        """Get availability slots for a professional."""
        query = db.query(Availability).filter(
            Availability.professional_id == professional_id
        )

        if start_date:
            query = query.filter(Availability.start_time >= start_date)
        if end_date:
            query = query.filter(Availability.end_time <= end_date)

        return query.all()

    def update_availability(
        self,
        db: Session,
        availability_id: int,
        availability: AvailabilityUpdate,
        professional_id: int
    ) -> Availability:
        """Update an availability slot."""
        db_availability = (
            db.query(Availability)
            .filter(
                and_(
                    Availability.id == availability_id,
                    Availability.professional_id == professional_id
                )
            )
            .first()
        )
        if not db_availability:
            raise HTTPException(
                status_code=404,
                detail="Availability slot not found"
            )

        update_data = availability.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_availability, field, value)

        db.add(db_availability)
        db.commit()
        db.refresh(db_availability)
        return db_availability

    def create_client_note(
        self,
        db: Session,
        note: ClientProgressNoteCreate,
        professional_id: int,
        client_id: int
    ) -> ClientProgressNote:
        """Create a new client progress note."""
        db_note = ClientProgressNote(
            **note.dict(),
            professional_id=professional_id,
            client_id=client_id
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note

    def get_client_notes(
        self,
        db: Session,
        professional_id: int,
        client_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[ClientProgressNote]:
        """Get all progress notes for a client."""
        return (
            db.query(ClientProgressNote)
            .filter(
                and_(
                    ClientProgressNote.professional_id == professional_id,
                    ClientProgressNote.client_id == client_id
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_client_note(
        self,
        db: Session,
        note_id: int,
        note: ClientProgressNoteUpdate,
        professional_id: int
    ) -> ClientProgressNote:
        """Update a client progress note."""
        db_note = (
            db.query(ClientProgressNote)
            .filter(
                and_(
                    ClientProgressNote.id == note_id,
                    ClientProgressNote.professional_id == professional_id
                )
            )
            .first()
        )
        if not db_note:
            raise HTTPException(
                status_code=404,
                detail="Note not found"
            )

        update_data = note.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_note, field, value)

        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note

    def search_professionals(
        self,
        db: Session,
        search_params: ProfessionalSearchParams,
        skip: int = 0,
        limit: int = 100
    ) -> List[Professional]:
        """Search for professionals based on various criteria."""
        query = db.query(Professional)

        if search_params.professional_type:
            query = query.filter(
                Professional.professional_type == search_params.professional_type
            )

        if search_params.specialization_ids:
            query = query.filter(
                Professional.specializations.any(
                    Specialization.id.in_(search_params.specialization_ids)
                )
            )

        if search_params.max_hourly_rate:
            query = query.filter(
                Professional.hourly_rate <= search_params.max_hourly_rate
            )

        if search_params.consultation_type:
            query = query.filter(
                Professional.consultation_type == search_params.consultation_type
            )

        if search_params.rating_min:
            query = query.filter(Professional.rating >= search_params.rating_min)

        if search_params.available_on:
            # Find professionals with availability on the specified date
            query = query.filter(
                Professional.availability.any(
                    and_(
                        Availability.start_time <= search_params.available_on,
                        Availability.end_time >= search_params.available_on,
                        Availability.available == True
                    )
                )
            )

        return query.offset(skip).limit(limit).all()

    def get_professional_stats(
        self,
        db: Session,
        professional_id: int
    ) -> ProfessionalStats:
        """Get statistics for a professional."""
        # Implementation depends on additional models (sessions, payments, etc.)
        # This is a placeholder implementation
        return ProfessionalStats(
            total_clients=0,
            total_sessions=0,
            average_rating=0.0,
            total_earnings=0.0,
            client_retention_rate=0.0,
            completion_rate=0.0
        )

professional = CRUDProfessional(Professional)