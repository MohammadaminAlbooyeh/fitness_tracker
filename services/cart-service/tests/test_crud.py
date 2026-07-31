"""Tests for cart-service CRUD operations."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas


@pytest.mark.asyncio
async def test_create_cart(db_session: AsyncSession):
    cart = await crud.create_cart(db_session, user_id=1)
    assert cart.id is not None
    assert cart.user_id == 1
    assert cart.is_active is True


@pytest.mark.asyncio
async def test_get_cart(db_session: AsyncSession):
    created = await crud.create_cart(db_session, user_id=2)
    fetched = await crud.get_cart(db_session, user_id=2)
    assert fetched is not None
    assert fetched.user_id == 2


@pytest.mark.asyncio
async def test_get_cart_not_found(db_session: AsyncSession):
    result = await crud.get_cart(db_session, user_id=99999)
    assert result is None


@pytest.mark.asyncio
async def test_add_item(db_session: AsyncSession):
    cart = await crud.create_cart(db_session, user_id=3)
    item_data = schemas.CartItemCreate(product_id=10, quantity=2, price=19.99)
    item = await crud.add_item(db_session, cart.id, item_data)
    assert item.id is not None
    assert item.product_id == 10
    assert item.quantity == 2
    assert item.price == 19.99


@pytest.mark.asyncio
async def test_get_cart_items(db_session: AsyncSession):
    cart = await crud.create_cart(db_session, user_id=4)
    item1 = schemas.CartItemCreate(product_id=1, quantity=1, price=10.0)
    item2 = schemas.CartItemCreate(product_id=2, quantity=3, price=20.0)
    await crud.add_item(db_session, cart.id, item1)
    await crud.add_item(db_session, cart.id, item2)
    items = await crud.get_cart_items(db_session, cart.id)
    assert len(items) == 2
