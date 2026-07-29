"""Notification service schemas."""

from pydantic import BaseModel, ConfigDict


class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    notification_type: str = "general"


class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_read: bool
