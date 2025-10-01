from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from typing import List, Optional
import qrcode
import io
import base64

from app.models.equipment import (
    Equipment,
    EquipmentCategory,
    MaintenanceRecord,
    EquipmentUsage,
    EquipmentStatus,
    MaintenanceType
)
from app.schemas.equipment import (
    CategoryCreate,
    CategoryUpdate,
    EquipmentCreate,
    EquipmentUpdate,
    MaintenanceRecordCreate,
    MaintenanceRecordUpdate,
    EquipmentUsageCreate,
    EquipmentUsageUpdate,
    EquipmentStats,
    MaintenanceAlert
)
from fastapi import HTTPException

class EquipmentService:
    def __init__(self, db: Session):
        self.db = db

    # Category management
    def create_category(self, category: CategoryCreate) -> EquipmentCategory:
        db_category = EquipmentCategory(**category.dict())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def get_categories(self, skip: int = 0, limit: int = 100) -> List[EquipmentCategory]:
        return self.db.query(EquipmentCategory).offset(skip).limit(limit).all()

    def update_category(self, category_id: int, category: CategoryUpdate) -> EquipmentCategory:
        db_category = self.db.query(EquipmentCategory).filter(EquipmentCategory.id == category_id).first()
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        for field, value in category.dict(exclude_unset=True).items():
            setattr(db_category, field, value)
        
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    # Equipment management
    def create_equipment(self, equipment: EquipmentCreate) -> Equipment:
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"equipment:{equipment.serial_number}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        qr_code = base64.b64encode(img_buffer.getvalue()).decode()

        db_equipment = Equipment(
            **equipment.dict(),
            qr_code=qr_code,
            status=EquipmentStatus.AVAILABLE
        )
        self.db.add(db_equipment)
        self.db.commit()
        self.db.refresh(db_equipment)
        return db_equipment

    def get_equipment(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        status: Optional[str] = None,
        location: Optional[str] = None
    ) -> List[Equipment]:
        query = self.db.query(Equipment)
        
        if category_id:
            query = query.filter(Equipment.category_id == category_id)
        if status:
            query = query.filter(Equipment.status == status)
        if location:
            query = query.filter(Equipment.location == location)
            
        return query.offset(skip).limit(limit).all()

    def get_equipment_by_id(self, equipment_id: int) -> Equipment:
        equipment = self.db.query(Equipment).filter(Equipment.id == equipment_id).first()
        if not equipment:
            raise HTTPException(status_code=404, detail="Equipment not found")
        return equipment

    def update_equipment(self, equipment_id: int, equipment: EquipmentUpdate) -> Equipment:
        db_equipment = self.get_equipment_by_id(equipment_id)
        
        for field, value in equipment.dict(exclude_unset=True).items():
            setattr(db_equipment, field, value)
            
        self.db.commit()
        self.db.refresh(db_equipment)
        return db_equipment

    # Maintenance management
    def create_maintenance_record(self, record: MaintenanceRecordCreate) -> MaintenanceRecord:
        # Update equipment status and maintenance dates
        equipment = self.get_equipment_by_id(record.equipment_id)
        equipment.status = EquipmentStatus.MAINTENANCE
        equipment.last_maintenance_date = datetime.utcnow()
        equipment.next_maintenance_date = record.next_maintenance_date

        db_record = MaintenanceRecord(**record.dict())
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def get_maintenance_records(
        self,
        equipment_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[MaintenanceRecord]:
        return self.db.query(MaintenanceRecord)\
            .filter(MaintenanceRecord.equipment_id == equipment_id)\
            .order_by(MaintenanceRecord.date_performed.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def update_maintenance_record(
        self,
        record_id: int,
        record: MaintenanceRecordUpdate
    ) -> MaintenanceRecord:
        db_record = self.db.query(MaintenanceRecord).filter(
            MaintenanceRecord.id == record_id
        ).first()
        if not db_record:
            raise HTTPException(status_code=404, detail="Maintenance record not found")

        for field, value in record.dict(exclude_unset=True).items():
            setattr(db_record, field, value)

        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    # Equipment usage management
    def start_equipment_usage(self, usage: EquipmentUsageCreate) -> EquipmentUsage:
        equipment = self.get_equipment_by_id(usage.equipment_id)
        if equipment.status != EquipmentStatus.AVAILABLE:
            raise HTTPException(
                status_code=400,
                detail=f"Equipment is not available (current status: {equipment.status})"
            )

        equipment.status = EquipmentStatus.IN_USE
        db_usage = EquipmentUsage(**usage.dict())
        self.db.add(db_usage)
        self.db.commit()
        self.db.refresh(db_usage)
        return db_usage

    def end_equipment_usage(
        self,
        usage_id: int,
        usage: EquipmentUsageUpdate
    ) -> EquipmentUsage:
        db_usage = self.db.query(EquipmentUsage).filter(
            EquipmentUsage.id == usage_id
        ).first()
        if not db_usage:
            raise HTTPException(status_code=404, detail="Usage record not found")

        equipment = self.get_equipment_by_id(db_usage.equipment_id)
        equipment.status = EquipmentStatus.AVAILABLE
        equipment.current_usage_hours += usage.duration

        db_usage.end_time = usage.end_time
        db_usage.duration = usage.duration

        self.db.commit()
        self.db.refresh(db_usage)
        return db_usage

    def get_user_equipment_usage(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[EquipmentUsage]:
        return self.db.query(EquipmentUsage)\
            .filter(EquipmentUsage.user_id == user_id)\
            .order_by(EquipmentUsage.start_time.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    # Statistics and monitoring
    def get_equipment_stats(self) -> EquipmentStats:
        stats = self.db.query(
            func.count().label('total'),
            func.sum(case([(Equipment.status == EquipmentStatus.AVAILABLE, 1)], else_=0)).label('available'),
            func.sum(case([(Equipment.status == EquipmentStatus.IN_USE, 1)], else_=0)).label('in_use'),
            func.sum(case([(Equipment.status == EquipmentStatus.MAINTENANCE, 1)], else_=0)).label('maintenance'),
            func.sum(case([(Equipment.status == EquipmentStatus.OUT_OF_ORDER, 1)], else_=0)).label('out_of_order'),
            func.sum(Equipment.current_usage_hours).label('total_usage'),
            func.count(case([(Equipment.next_maintenance_date <= datetime.utcnow(), 1)])).label('maintenance_due')
        ).first()

        return EquipmentStats(
            total_equipment=stats.total,
            available_count=stats.available,
            in_use_count=stats.in_use,
            maintenance_count=stats.maintenance,
            out_of_order_count=stats.out_of_order,
            total_usage_hours=stats.total_usage or 0.0,
            maintenance_due_count=stats.maintenance_due
        )

    def get_maintenance_alerts(self) -> List[MaintenanceAlert]:
        alerts = []
        equipment_list = self.db.query(Equipment).all()
        
        for equipment in equipment_list:
            # Check maintenance due date
            if equipment.next_maintenance_date and equipment.next_maintenance_date <= datetime.utcnow():
                alerts.append(MaintenanceAlert(
                    equipment_id=equipment.id,
                    equipment_name=equipment.name,
                    alert_type="maintenance_due",
                    message="Scheduled maintenance is due",
                    due_date=equipment.next_maintenance_date,
                    current_usage_hours=equipment.current_usage_hours,
                    max_usage_hours=equipment.max_usage_hours
                ))
            
            # Check usage hours
            if equipment.max_usage_hours and equipment.current_usage_hours >= equipment.max_usage_hours * 0.9:
                alerts.append(MaintenanceAlert(
                    equipment_id=equipment.id,
                    equipment_name=equipment.name,
                    alert_type="usage_limit",
                    message=f"Equipment has reached {round(equipment.current_usage_hours / equipment.max_usage_hours * 100)}% of maximum usage hours",
                    current_usage_hours=equipment.current_usage_hours,
                    max_usage_hours=equipment.max_usage_hours
                ))

        return alerts

    def get_equipment_qr_code(self, equipment_id: int) -> str:
        equipment = self.get_equipment_by_id(equipment_id)
        return equipment.qr_code