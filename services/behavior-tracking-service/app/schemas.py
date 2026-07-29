"""Behavior tracking service schemas."""

from pydantic import BaseModel, ConfigDict


class UserBehaviorBase(BaseModel):
    user_id: int
    product_id: int
    event_type: str
    metadata: str | None = None


class UserBehaviorCreate(UserBehaviorBase):
    pass


class UserBehavior(UserBehaviorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
