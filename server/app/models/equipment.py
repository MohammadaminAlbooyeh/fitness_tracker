from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from typing import Optional

from app.db.base_class import Base

class EquipmentStatus(str, enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    OUT_OF_ORDER = "out_of_order"

class MaintenanceType(str, enum.Enum):
    ROUTINE = "routine"
    REPAIR = "repair"
    REPLACEMENT = "replacement"
    INSPECTION = "inspection"

class EquipmentCategory(Base):
    __tablename__ = "equipment_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="category")

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("equipment_categories.id"))
    model_number = Column(String, nullable=True)
    serial_number = Column(String, unique=True)
    purchase_date = Column(DateTime, nullable=True)
    last_maintenance_date = Column(DateTime, nullable=True)
    next_maintenance_date = Column(DateTime, nullable=True)
    status = Column(Enum(EquipmentStatus), default=EquipmentStatus.AVAILABLE)
    location = Column(String, nullable=True)
    max_usage_hours = Column(Float, nullable=True)
    current_usage_hours = Column(Float, default=0.0)
    qr_code = Column(String, unique=True)
    notes = Column(String, nullable=True)
    
    # Relationships
    category = relationship("EquipmentCategory", back_populates="equipment")
    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment")
    usage_logs = relationship("EquipmentUsage", back_populates="equipment")

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    maintenance_type = Column(Enum(MaintenanceType))
    date_performed = Column(DateTime, default=datetime.utcnow)
    performed_by = Column(String)
    description = Column(String)
    cost = Column(Float, nullable=True)
    next_maintenance_date = Column(DateTime, nullable=True)
    parts_replaced = Column(String, nullable=True)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_records")

class EquipmentUsage(Base):
    __tablename__ = "equipment_usage"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)  # in hours
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=True)
    
    # Relationships
    equipment = relationship("Equipment", back_populates="usage_logs")
    user = relationship("User", back_populates="equipment_usage")
    workout = relationship("Workout", back_populates="equipment_used")