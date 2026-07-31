"""Tests for shared_lib database."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.database import get_db, engine, AsyncSessionLocal


def test_engine_created():
    assert engine is not None


def test_session_local_created():
    assert AsyncSessionLocal is not None


@pytest.mark.asyncio
async def test_get_db():
    gen = get_db()
    session = await gen.__anext__()
    assert isinstance(session, AsyncSession)
    await session.close()
