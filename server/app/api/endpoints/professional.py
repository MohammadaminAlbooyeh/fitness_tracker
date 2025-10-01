from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.professional_auth import get_current_professional
from app.schemas.professional import (
    ProfessionalCreate, ProfessionalUpdate, ProfessionalResponse,
    SpecializationCreate, SpecializationUpdate, SpecializationResponse,
    CertificationCreate, CertificationUpdate, CertificationResponse,
    ProfessionalServiceCreate, ProfessionalServiceUpdate, ProfessionalServiceResponse,
    AvailabilityCreate, AvailabilityUpdate, AvailabilityResponse,
    ClientProgressNoteCreate, ClientProgressNoteUpdate, ClientProgressNoteResponse,
    ProfessionalSearchParams, ProfessionalStats, ProfessionalType, ConsultationType
)
from app.crud import (
    professional as professional_crud,
    specialization as specialization_crud,
    certification as certification_crud
)
from app.models.professional import Professional

router = APIRouter(prefix="/professional", tags=["professional"])

# Professional Profile Management
@router.post("/register", response_model=ProfessionalResponse)
async def register_professional(
    professional: ProfessionalCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_professional)
):
    """Register a new professional profile."""
    return professional_crud.create_professional(db, professional, current_user.id)

@router.get("/me", response_model=ProfessionalResponse)
async def get_professional_profile(
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Get current professional's profile."""
    return professional_crud.get_professional(db, current_professional.id)

@router.put("/me", response_model=ProfessionalResponse)
async def update_professional_profile(
    professional: ProfessionalUpdate,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Update current professional's profile."""
    return professional_crud.update_professional(db, current_professional.id, professional)

# Specializations
@router.post("/specialization", response_model=SpecializationResponse)
async def create_specialization(
    specialization: SpecializationCreate,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Create a new specialization."""
    return specialization_crud.create_specialization(db, specialization)

@router.get("/specialization", response_model=List[SpecializationResponse])
async def list_specializations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all specializations."""
    return specialization_crud.get_specializations(db, skip=skip, limit=limit)

@router.put("/specialization/{specialization_id}", response_model=SpecializationResponse)
async def update_specialization(
    specialization_id: int,
    specialization: SpecializationUpdate,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Update a specialization."""
    return specialization_crud.update_specialization(db, specialization_id, specialization)

# Professional Services
@router.post("/service", response_model=ProfessionalServiceResponse)
async def create_service(
    service: ProfessionalServiceCreate,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Create a new professional service."""
    return professional_crud.create_service(db, service, current_professional.id)

@router.get("/service", response_model=List[ProfessionalServiceResponse])
async def list_services(
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """List all services of current professional."""
    return professional_crud.get_services(db, current_professional.id)

@router.put("/service/{service_id}", response_model=ProfessionalServiceResponse)
async def update_service(
    service_id: int,
    service: ProfessionalServiceUpdate,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Update a professional service."""
    return professional_crud.update_service(db, service_id, service, current_professional.id)

# Availability Management
@router.post("/availability", response_model=AvailabilityResponse)
async def create_availability(
    availability: AvailabilityCreate,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Create a new availability slot."""
    return professional_crud.create_availability(db, availability, current_professional.id)

@router.get("/availability", response_model=List[AvailabilityResponse])
async def list_availability(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """List all availability slots of current professional."""
    return professional_crud.get_availability(
        db, 
        current_professional.id, 
        start_date=start_date, 
        end_date=end_date
    )

@router.put("/availability/{availability_id}", response_model=AvailabilityResponse)
async def update_availability(
    availability_id: int,
    availability: AvailabilityUpdate,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Update an availability slot."""
    return professional_crud.update_availability(
        db, 
        availability_id, 
        availability, 
        current_professional.id
    )

# Client Progress Notes
@router.post("/client/{client_id}/notes", response_model=ClientProgressNoteResponse)
async def create_client_note(
    client_id: int,
    note: ClientProgressNoteCreate,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Create a new progress note for a client."""
    return professional_crud.create_client_note(
        db, 
        note, 
        current_professional.id, 
        client_id
    )

@router.get("/client/{client_id}/notes", response_model=List[ClientProgressNoteResponse])
async def list_client_notes(
    client_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """List all progress notes for a client."""
    return professional_crud.get_client_notes(
        db, 
        current_professional.id, 
        client_id, 
        skip=skip, 
        limit=limit
    )

@router.put("/client/notes/{note_id}", response_model=ClientProgressNoteResponse)
async def update_client_note(
    note_id: int,
    note: ClientProgressNoteUpdate,
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Update a client progress note."""
    return professional_crud.update_client_note(
        db, 
        note_id, 
        note, 
        current_professional.id
    )

# Search and Discovery
@router.get("/search", response_model=List[ProfessionalResponse])
async def search_professionals(
    search_params: ProfessionalSearchParams = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Search for professionals based on various criteria."""
    return professional_crud.search_professionals(
        db,
        search_params,
        skip=skip,
        limit=limit
    )

@router.get("/stats", response_model=ProfessionalStats)
async def get_professional_stats(
    db: Session = Depends(get_db),
    current_professional = Depends(get_current_professional)
):
    """Get statistics for the current professional."""
    return professional_crud.get_professional_stats(db, current_professional.id)

# Additional Endpoints
@router.get("/types", response_model=List[ProfessionalType])
async def list_professional_types():
    """List all available professional types."""
    return list(ProfessionalType)

@router.get("/consultation-types", response_model=List[ConsultationType])
async def list_consultation_types():
    """List all available consultation types."""
    return list(ConsultationType)