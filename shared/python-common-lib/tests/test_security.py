"""Tests for shared_lib security."""
import pytest
from datetime import timedelta

from shared_lib.security import create_access_token, verify_password, get_password_hash


def test_create_access_token():
    token = create_access_token(data={"sub": "test@example.com"})
    assert token is not None
    assert len(token) > 0


def test_create_access_token_with_expiry():
    token = create_access_token(
        data={"sub": "test@example.com"},
        expires_delta=timedelta(minutes=60)
    )
    assert token is not None


def test_get_password_hash():
    password = "mySecretPassword123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert hashed is not None


def test_verify_password():
    password = "mySecretPassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongPassword", hashed) is False
