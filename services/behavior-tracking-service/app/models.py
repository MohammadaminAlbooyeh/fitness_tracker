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
    # "context" is the Python attribute; the physical column keeps the original
    # "metadata" name so existing data is preserved. The Python name must differ
    # because "metadata" is reserved by the SQLAlchemy Declarative API.
    context: Mapped[str | None] = mapped_column("metadata", Text, nullable=True)
