from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException

from app.models.consultation import (
    Consultation,
    ConsultationNote,
    ConsultationAttachment,
    ConsultationGoal,
    ConsultationTemplate,
    ConsultationStatus,
    ConsultationNoteType
)
from app.schemas.professional import ConsultationType
from app.services.notification import NotificationService
from app.core.storage import StorageService

class ConsultationService:
    def __init__(
        self,
        db: Session,
        notification_service: NotificationService,
        storage_service: StorageService
    ):
        self.db = db
        self.notification_service = notification_service
        self.storage_service = storage_service

    def create_consultation(
        self,
        professional_id: int,
        client_id: int,
        appointment_id: int,
        consultation_type: ConsultationType,
        **kwargs
    ) -> Consultation:
        """Create a new consultation."""
        consultation = Consultation(
            professional_id=professional_id,
            client_id=client_id,
            appointment_id=appointment_id,
            consultation_type=consultation_type,
            status=ConsultationStatus.SCHEDULED,
            **kwargs
        )

        self.db.add(consultation)
        self.db.commit()
        self.db.refresh(consultation)

        # Send notifications
        self.notification_service.send_consultation_scheduled(consultation)

        return consultation

    def start_consultation(
        self,
        consultation_id: int,
        meeting_url: Optional[str] = None
    ) -> Consultation:
        """Start a consultation."""
        consultation = (
            self.db.query(Consultation)
            .filter(Consultation.id == consultation_id)
            .first()
        )

        if not consultation:
            raise HTTPException(
                status_code=404,
                detail="Consultation not found"
            )

        if consultation.status != ConsultationStatus.SCHEDULED:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot start consultation with status: {consultation.status}"
            )

        consultation.status = ConsultationStatus.IN_PROGRESS
        consultation.start_time = datetime.utcnow()
        if meeting_url:
            consultation.meeting_url = meeting_url

        self.db.add(consultation)
        self.db.commit()
        self.db.refresh(consultation)

        # Send notifications
        self.notification_service.send_consultation_started(consultation)

        return consultation

    def end_consultation(
        self,
        consultation_id: int,
        summary: Optional[str] = None,
        recording_url: Optional[str] = None
    ) -> Consultation:
        """End a consultation."""
        consultation = (
            self.db.query(Consultation)
            .filter(Consultation.id == consultation_id)
            .first()
        )

        if not consultation:
            raise HTTPException(
                status_code=404,
                detail="Consultation not found"
            )

        if consultation.status != ConsultationStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot end consultation with status: {consultation.status}"
            )

        consultation.status = ConsultationStatus.COMPLETED
        consultation.end_time = datetime.utcnow()
        consultation.summary = summary
        if recording_url:
            consultation.recording_url = recording_url

        # Calculate duration
        if consultation.start_time:
            duration = (consultation.end_time - consultation.start_time).total_seconds() / 60
            consultation.duration = int(duration)

        self.db.add(consultation)
        self.db.commit()
        self.db.refresh(consultation)

        # Send notifications
        self.notification_service.send_consultation_completed(consultation)

        return consultation

    def add_consultation_note(
        self,
        consultation_id: int,
        note_type: ConsultationNoteType,
        content: str,
        is_private: bool = True
    ) -> ConsultationNote:
        """Add a note to a consultation."""
        note = ConsultationNote(
            consultation_id=consultation_id,
            note_type=note_type,
            content=content,
            is_private=is_private
        )

        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)

        return note

    def add_consultation_attachment(
        self,
        consultation_id: int,
        file: Any,
        is_private: bool = True
    ) -> ConsultationAttachment:
        """Add an attachment to a consultation."""
        # Upload file to storage
        file_url = self.storage_service.upload_file(
            file,
            folder=f"consultations/{consultation_id}/attachments"
        )

        attachment = ConsultationAttachment(
            consultation_id=consultation_id,
            file_name=file.filename,
            file_type=file.content_type,
            file_size=len(file.file.read()),
            file_url=file_url,
            is_private=is_private
        )

        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)

        return attachment

    def add_consultation_goal(
        self,
        consultation_id: int,
        title: str,
        description: str,
        target_date: datetime,
        metrics: Optional[Dict[str, Any]] = None
    ) -> ConsultationGoal:
        """Add a goal to a consultation."""
        goal = ConsultationGoal(
            consultation_id=consultation_id,
            title=title,
            description=description,
            target_date=target_date,
            status="not_started",
            progress=0.0,
            metrics=metrics or {}
        )

        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)

        return goal

    def update_goal_progress(
        self,
        goal_id: int,
        progress: float,
        status: Optional[str] = None,
        metrics: Optional[Dict[str, Any]] = None
    ) -> ConsultationGoal:
        """Update progress on a consultation goal."""
        goal = (
            self.db.query(ConsultationGoal)
            .filter(ConsultationGoal.id == goal_id)
            .first()
        )

        if not goal:
            raise HTTPException(
                status_code=404,
                detail="Goal not found"
            )

        goal.progress = progress
        if status:
            goal.status = status
        if metrics:
            goal.metrics.update(metrics)

        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)

        # Send notifications if goal is completed
        if goal.status == "completed":
            self.notification_service.send_goal_completed(goal)

        return goal

    def create_consultation_template(
        self,
        professional_id: int,
        name: str,
        description: str,
        structure: Dict[str, Any],
        default_duration: int
    ) -> ConsultationTemplate:
        """Create a consultation template."""
        template = ConsultationTemplate(
            professional_id=professional_id,
            name=name,
            description=description,
            structure=structure,
            default_duration=default_duration
        )

        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)

        return template

    def get_professional_templates(
        self,
        professional_id: int
    ) -> List[ConsultationTemplate]:
        """Get all consultation templates for a professional."""
        return (
            self.db.query(ConsultationTemplate)
            .filter(ConsultationTemplate.professional_id == professional_id)
            .all()
        )

    def get_consultation_history(
        self,
        client_id: Optional[int] = None,
        professional_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[List[ConsultationStatus]] = None
    ) -> List[Consultation]:
        """Get consultation history."""
        query = self.db.query(Consultation)

        if client_id:
            query = query.filter(Consultation.client_id == client_id)
        if professional_id:
            query = query.filter(Consultation.professional_id == professional_id)
        if start_date:
            query = query.filter(Consultation.created_at >= start_date)
        if end_date:
            query = query.filter(Consultation.created_at <= end_date)
        if status:
            query = query.filter(Consultation.status.in_(status))

        return query.order_by(Consultation.created_at.desc()).all()

    def get_consultation_metrics(
        self,
        professional_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get metrics for consultations."""
        query = self.db.query(Consultation).filter(
            Consultation.professional_id == professional_id
        )

        if start_date:
            query = query.filter(Consultation.created_at >= start_date)
        if end_date:
            query = query.filter(Consultation.created_at <= end_date)

        total_consultations = query.count()
        completed_consultations = query.filter(
            Consultation.status == ConsultationStatus.COMPLETED
        ).count()
        cancelled_consultations = query.filter(
            Consultation.status == ConsultationStatus.CANCELLED
        ).count()

        avg_duration = (
            query.filter(Consultation.duration.isnot(None))
            .with_entities(func.avg(Consultation.duration))
            .scalar() or 0
        )

        return {
            "total_consultations": total_consultations,
            "completed_consultations": completed_consultations,
            "cancelled_consultations": cancelled_consultations,
            "completion_rate": (completed_consultations / total_consultations * 100
                              if total_consultations > 0 else 0),
            "average_duration": round(avg_duration, 2)
        }