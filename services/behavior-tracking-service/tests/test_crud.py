"""Tests for behavior-tracking-service CRUD operations."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas


@pytest.mark.asyncio
async def test_create_behavior(db_session: AsyncSession):
    behavior_data = schemas.UserBehaviorCreate(
        user_id=1,
        product_id=100,
        event_type="view",
        context="page_duration=30s"
    )
    behavior = await crud.create_behavior(db_session, behavior_data)
    assert behavior.id is not None
    assert behavior.user_id == 1
    assert behavior.product_id == 100
    assert behavior.event_type == "view"


@pytest.mark.asyncio
async def test_get_behaviors(db_session: AsyncSession):
    behavior1 = schemas.UserBehaviorCreate(
        user_id=1, product_id=1, event_type="view", context=None
    )
    behavior2 = schemas.UserBehaviorCreate(
        user_id=1, product_id=2, event_type="click", context="button=add_to_cart"
    )
    behavior3 = schemas.UserBehaviorCreate(
        user_id=2, product_id=1, event_type="view", context=None
    )
    await crud.create_behavior(db_session, behavior1)
    await crud.create_behavior(db_session, behavior2)
    await crud.create_behavior(db_session, behavior3)

    user1_behaviors = await crud.get_behaviors(db_session, user_id=1)
    assert len(user1_behaviors) == 2

    user2_behaviors = await crud.get_behaviors(db_session, user_id=2)
    assert len(user2_behaviors) == 1


@pytest.mark.asyncio
async def test_get_behaviors_empty(db_session: AsyncSession):
    result = await crud.get_behaviors(db_session, user_id=99999)
    assert len(result) == 0
