"""Tests for order-service CRUD operations."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas


@pytest.mark.asyncio
async def test_create_order(db_session: AsyncSession):
    order_data = schemas.OrderCreate(
        user_id=1,
        total_amount=99.99,
        shipping_address="123 Main St, City, Country",
        items=[
            schemas.OrderItemCreate(product_id=10, quantity=2, price=49.99)
        ]
    )
    order = await crud.create_order(db_session, order_data)
    assert order.id is not None
    assert order.user_id == 1
    assert order.total_amount == 99.99
    assert order.status.value == "pending"


@pytest.mark.asyncio
async def test_get_order(db_session: AsyncSession):
    order_data = schemas.OrderCreate(
        user_id=2,
        total_amount=50.00,
        shipping_address="456 Oak Ave",
        items=[
            schemas.OrderItemCreate(product_id=20, quantity=1, price=50.00)
        ]
    )
    created = await crud.create_order(db_session, order_data)
    fetched = await crud.get_order(db_session, created.id)
    assert fetched is not None
    assert fetched.user_id == 2


@pytest.mark.asyncio
async def test_get_order_not_found(db_session: AsyncSession):
    result = await crud.get_order(db_session, 99999)
    assert result is None


@pytest.mark.asyncio
async def test_get_orders(db_session: AsyncSession):
    for i in range(3):
        order_data = schemas.OrderCreate(
            user_id=3,
            total_amount=10.0 * (i + 1),
            shipping_address="Address " + str(i),
            items=[
                schemas.OrderItemCreate(product_id=i, quantity=1, price=10.0)
            ]
        )
        await crud.create_order(db_session, order_data)
    orders = await crud.get_orders(db_session, user_id=3, skip=0, limit=100)
    assert len(orders) >= 3
