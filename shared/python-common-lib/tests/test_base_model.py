"""Tests for shared_lib base_model."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from shared_lib.base_model import Base, TimestampMixin


def test_base_is_declarative_base():
    assert Base is not None
    assert hasattr(Base, "metadata")


def test_timestamp_mixin_has_fields():
    assert hasattr(TimestampMixin, "created_at")
    assert hasattr(TimestampMixin, "updated_at")


def test_timestamp_mixin_can_be_subclassed():
    class TestModel(Base, TimestampMixin):
        __tablename__ = "test_models"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(100))

    assert TestModel.__tablename__ == "test_models"
    assert hasattr(TestModel, "created_at")
    assert hasattr(TestModel, "updated_at")
