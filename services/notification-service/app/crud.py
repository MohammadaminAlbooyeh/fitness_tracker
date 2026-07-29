"""Notification service CRUD."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Notification
from app.schemas import NotificationCreate


async def get_notifications(db: AsyncSession, user_id: int) -> list[Notification]:
    result = await db.execute(select(Notification).where(Notification.user_id == user_id))
    return list(result.scalars().all())


async def create_notification(db: AsyncSession, notification: NotificationCreate) -> Notification:
    db_notification = Notification(**notification.model_dump())
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification
