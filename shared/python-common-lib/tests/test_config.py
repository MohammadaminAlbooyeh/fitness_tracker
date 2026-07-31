"""Tests for shared_lib config."""
import pytest
from shared_lib.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.algorithm == "HS256"
    assert settings.access_token_expire_minutes == 30


def test_settings_service_name():
    settings = Settings(service_name="user-service")
    assert settings.service_name == "user-service"


def test_settings_database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
    settings = Settings()
    assert "test" in settings.database_url
