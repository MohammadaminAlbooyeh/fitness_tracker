"""Tests for shared_lib schemas."""
from pydantic import BaseModel

from shared_lib.schemas import BaseSchema, TimestampSchema


def test_base_schema_config():
    schema = BaseSchema()
    assert schema.model_config["from_attributes"] is True


def test_timestamp_schema_fields():
    schema = TimestampSchema(created_at="2024-01-01T00:00:00", updated_at="2024-01-01T00:00:00")
    assert schema.created_at == "2024-01-01T00:00:00"
    assert schema.updated_at == "2024-01-01T00:00:00"


def test_timestamp_schema_from_orm():
    class MockModel:
        created_at = "2024-01-01T00:00:00"
        updated_at = "2024-01-01T00:00:00"

    schema = TimestampSchema.model_validate(MockModel())
    assert schema.created_at == "2024-01-01T00:00:00"
    assert schema.updated_at == "2024-01-01T00:00:00"
