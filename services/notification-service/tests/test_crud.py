"""Tests for notification-service CRUD operations."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas


@pytest.mark.asyncio
async def test_create_notification(db_session: AsyncSession):
    notif_data = schemas.NotificationCreate(
        user_id=1,
        title="Test Notification",
        message="This is a test notification",
        notification_type="order"
    )
    notification = await crud.create_notification(db_session, notif_data)
    assert notification.id is not None
    assert notification.user_id == 1
    assert notification.title == "Test Notification"
    assert notification.is_read is False


@pytest.mark.asyncio
async def test_get_notifications(db_session: AsyncSession):
    notif1 = schemas.NotificationCreate(
        user_id=1, title="Notif 1", message="Message 1", notification_type="system"
    )
    notif2 = schemas.NotificationCreate(
        user_id=1, title="Notif 2", message="Message 2", notification_type="order"
    )
    notif3 = schemas.NotificationCreate(
        user_id=2, title="Notif 3", message="Message 3", notification_type="system"
    )
    await crud.create_notification(db_session, notif1)
    await crud.create_notification(db_session, notif2)
    await crud.create_notification(db_session, notif3)

    user1_notifs = await crud.get_notifications(db_session, user_id=1)
    assert len(user1_notifs) == 2

    user2_notifs = await crud.get_notifications(db_session, user_id=2)
    assert len(user2_notifs) == 1


@pytest.mark.asyncio
async def test_get_notifications_empty(db_session: AsyncSession):
    result = await crud.get_notifications(db_session, user_id=99999)
    assert len(result) == 0
