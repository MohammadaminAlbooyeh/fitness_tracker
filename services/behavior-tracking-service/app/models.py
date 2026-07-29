"""Behavior tracking service models."""

from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from shared_lib.base_model import Base, TimestampMixin


class UserBehavior(Base, TimestampMixin):
    __tablename__ = "user_behaviors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    product_id: Mapped[int] = mapped_column(nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    metadata: Mapped[str | None] = mapped_column(Text, nullable=True)
