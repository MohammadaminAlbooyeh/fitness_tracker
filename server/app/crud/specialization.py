from sqlalchemy.orm import Session
from app.models.professional import Specialization
from app.schemas.professional import SpecializationCreate, SpecializationUpdate
from app.crud.base import CRUDBase
from typing import List
from fastapi import HTTPException

class CRUDSpecialization(CRUDBase[Specialization, SpecializationCreate, SpecializationUpdate]):
    def create_specialization(
        self,
        db: Session,
        specialization: SpecializationCreate
    ) -> Specialization:
        """Create a new specialization."""
        db_specialization = Specialization(**specialization.dict())
        db.add(db_specialization)
        db.commit()
        db.refresh(db_specialization)
        return db_specialization

    def get_specializations(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Specialization]:
        """Get all specializations."""
        return (
            db.query(Specialization)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_specialization(
        self,
        db: Session,
        specialization_id: int,
        specialization: SpecializationUpdate
    ) -> Specialization:
        """Update a specialization."""
        db_specialization = self.get(db, specialization_id)
        if not db_specialization:
            raise HTTPException(
                status_code=404,
                detail="Specialization not found"
            )

        update_data = specialization.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_specialization, field, value)

        db.add(db_specialization)
        db.commit()
        db.refresh(db_specialization)
        return db_specialization

specialization = CRUDSpecialization(Specialization)