from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class EquipmentStatus(str, Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    OUT_OF_ORDER = "out_of_order"

class MaintenanceType(str, Enum):
    ROUTINE = "routine"
    REPAIR = "repair"
    REPLACEMENT = "replacement"
    INSPECTION = "inspection"

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True

# Equipment Schemas
class EquipmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    model_number: Optional[str] = None
    serial_number: str
    purchase_date: Optional[datetime] = None
    location: Optional[str] = None
    max_usage_hours: Optional[float] = None
    notes: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[datetime] = None
    location: Optional[str] = None
    max_usage_hours: Optional[float] = None
    status: Optional[EquipmentStatus] = None
    notes: Optional[str] = None

class EquipmentResponse(EquipmentBase):
    id: int
    status: EquipmentStatus
    last_maintenance_date: Optional[datetime]
    next_maintenance_date: Optional[datetime]
    current_usage_hours: float
    qr_code: str
    category: CategoryResponse

    class Config:
        orm_mode = True

# Maintenance Record Schemas
class MaintenanceRecordBase(BaseModel):
    equipment_id: int
    maintenance_type: MaintenanceType
    performed_by: str
    description: str
    cost: Optional[float] = None
    next_maintenance_date: Optional[datetime] = None
    parts_replaced: Optional[str] = None

class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass

class MaintenanceRecordUpdate(BaseModel):
    maintenance_type: Optional[MaintenanceType] = None
    performed_by: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    next_maintenance_date: Optional[datetime] = None
    parts_replaced: Optional[str] = None

class MaintenanceRecordResponse(MaintenanceRecordBase):
    id: int
    date_performed: datetime

    class Config:
        orm_mode = True

# Equipment Usage Schemas
class EquipmentUsageBase(BaseModel):
    equipment_id: int
    user_id: int
    workout_id: Optional[int] = None

class EquipmentUsageCreate(EquipmentUsageBase):
    pass

class EquipmentUsageUpdate(BaseModel):
    end_time: datetime
    duration: float

class EquipmentUsageResponse(EquipmentUsageBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime]
    duration: Optional[float]

    class Config:
        orm_mode = True

# Additional Response Schemas
class EquipmentStats(BaseModel):
    total_equipment: int
    available_count: int
    in_use_count: int
    maintenance_count: int
    out_of_order_count: int
    total_usage_hours: float
    maintenance_due_count: int

class MaintenanceAlert(BaseModel):
    equipment_id: int
    equipment_name: str
    alert_type: str
    message: str
    due_date: Optional[datetime]
    current_usage_hours: float
    max_usage_hours: Optional[float]