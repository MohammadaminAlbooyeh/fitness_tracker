from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.api.deps import get_db, get_current_user, get_current_active_superuser
from app.schemas.equipment import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentResponse,
    MaintenanceRecordCreate,
    MaintenanceRecordUpdate,
    MaintenanceRecordResponse,
    EquipmentUsageCreate,
    EquipmentUsageUpdate,
    EquipmentUsageResponse,
    EquipmentStats,
    MaintenanceAlert
)
from app.services.equipment import EquipmentService
from app.models.users import User

router = APIRouter()

# Category endpoints
@router.post("/categories/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new equipment category. Superuser only."""
    return EquipmentService(db).create_category(category)

@router.get("/categories/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all equipment categories."""
    return EquipmentService(db).get_categories(skip=skip, limit=limit)

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Update an equipment category. Superuser only."""
    return EquipmentService(db).update_category(category_id, category)

# Equipment endpoints
@router.post("/", response_model=EquipmentResponse)
def create_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Create new equipment. Superuser only."""
    return EquipmentService(db).create_equipment(equipment)

@router.get("/", response_model=List[EquipmentResponse])
def get_equipment(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment with optional filters."""
    return EquipmentService(db).get_equipment(
        skip=skip,
        limit=limit,
        category_id=category_id,
        status=status,
        location=location
    )

@router.get("/stats", response_model=EquipmentStats)
def get_equipment_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment usage and availability statistics."""
    return EquipmentService(db).get_equipment_stats()

@router.get("/maintenance-alerts", response_model=List[MaintenanceAlert])
def get_maintenance_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get maintenance alerts for equipment. Superuser only."""
    return EquipmentService(db).get_maintenance_alerts()

@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment_by_id(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment by ID."""
    return EquipmentService(db).get_equipment_by_id(equipment_id)

@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: int,
    equipment: EquipmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Update equipment details. Superuser only."""
    return EquipmentService(db).update_equipment(equipment_id, equipment)

# Maintenance record endpoints
@router.post("/maintenance/", response_model=MaintenanceRecordResponse)
def create_maintenance_record(
    record: MaintenanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a maintenance record. Superuser only."""
    return EquipmentService(db).create_maintenance_record(record)

@router.get("/maintenance/{equipment_id}", response_model=List[MaintenanceRecordResponse])
def get_maintenance_records(
    equipment_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get maintenance records for specific equipment."""
    return EquipmentService(db).get_maintenance_records(equipment_id, skip=skip, limit=limit)

@router.put("/maintenance/{record_id}", response_model=MaintenanceRecordResponse)
def update_maintenance_record(
    record_id: int,
    record: MaintenanceRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """Update a maintenance record. Superuser only."""
    return EquipmentService(db).update_maintenance_record(record_id, record)

# Equipment usage endpoints
@router.post("/usage/", response_model=EquipmentUsageResponse)
def start_equipment_usage(
    usage: EquipmentUsageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start equipment usage session."""
    return EquipmentService(db).start_equipment_usage(usage)

@router.put("/usage/{usage_id}", response_model=EquipmentUsageResponse)
def end_equipment_usage(
    usage_id: int,
    usage: EquipmentUsageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """End equipment usage session."""
    return EquipmentService(db).end_equipment_usage(usage_id, usage)

@router.get("/usage/user/{user_id}", response_model=List[EquipmentUsageResponse])
def get_user_equipment_usage(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get equipment usage history for a user."""
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to view other users' equipment usage")
    return EquipmentService(db).get_user_equipment_usage(user_id, skip=skip, limit=limit)

@router.get("/qr/{equipment_id}")
def get_equipment_qr_code(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get QR code for equipment."""
    return EquipmentService(db).get_equipment_qr_code(equipment_id)