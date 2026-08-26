"""Tests for shared_lib security."""
import os

os.environ["SECRET_KEY"] = "test-secret-key-for-security-tests"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///test_shared_security.db"

import pytest
from datetime import timedelta

from shared_lib.security import (
    create_access_token,
    decode_token,
    get_current_user,
    verify_password,
    get_password_hash,
)


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


def test_decode_token_roundtrip():
    token = create_access_token(data={"sub": "decode@example.com"})
    payload = decode_token(token)
    assert payload["sub"] == "decode@example.com"
    assert "exp" in payload


def test_decode_token_rejects_garbage():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as excinfo:
        decode_token("not-a-valid-token")
    assert excinfo.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    token = create_access_token(data={"sub": "user@example.com"})
    user = get_current_user(token)
    assert user["sub"] == "user@example.com"


@pytest.mark.asyncio
async def test_get_current_user_missing_token():
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user("")
    assert excinfo.value.status_code == 401


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
