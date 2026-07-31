"""Tests for user-service CRUD operations."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from shared_lib.security import get_password_hash


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    user_data = schemas.UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="securepassword123"
    )
    user = await crud.create_user(db_session, user_data)
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.hashed_password != "securepassword123"


@pytest.mark.asyncio
async def test_get_user(db_session: AsyncSession):
    user_data = schemas.UserCreate(
        email="getuser@example.com",
        full_name="Get User",
        password="password123"
    )
    created = await crud.create_user(db_session, user_data)
    fetched = await crud.get_user(db_session, created.id)
    assert fetched is not None
    assert fetched.email == "getuser@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(db_session: AsyncSession):
    result = await crud.get_user(db_session, 99999)
    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession):
    user_data = schemas.UserCreate(
        email="byemail@example.com",
        full_name="Email User",
        password="password123"
    )
    created = await crud.create_user(db_session, user_data)
    fetched = await crud.get_user_by_email(db_session, "byemail@example.com")
    assert fetched is not None
    assert fetched.id == created.id


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(db_session: AsyncSession):
    result = await crud.get_user_by_email(db_session, "nonexistent@example.com")
    assert result is None
