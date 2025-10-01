from sqlalchemy.orm import Session
from app.models.professional import Certification
from app.schemas.professional import CertificationCreate, CertificationUpdate
from app.crud.base import CRUDBase
from typing import List
from fastapi import HTTPException

class CRUDCertification(CRUDBase[Certification, CertificationCreate, CertificationUpdate]):
    def create_certification(
        self,
        db: Session,
        certification: CertificationCreate
    ) -> Certification:
        """Create a new certification."""
        db_certification = Certification(**certification.dict())
        db.add(db_certification)
        db.commit()
        db.refresh(db_certification)
        return db_certification

    def get_certifications(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Certification]:
        """Get all certifications."""
        return (
            db.query(Certification)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_certification(
        self,
        db: Session,
        certification_id: int,
        certification: CertificationUpdate
    ) -> Certification:
        """Update a certification."""
        db_certification = self.get(db, certification_id)
        if not db_certification:
            raise HTTPException(
                status_code=404,
                detail="Certification not found"
            )

        update_data = certification.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_certification, field, value)

        db.add(db_certification)
        db.commit()
        db.refresh(db_certification)
        return db_certification

certification = CRUDCertification(Certification)