"""Tests for order-service API endpoints."""
import pytest


@pytest.mark.asyncio
async def test_create_order_endpoint(client):
    response = await client.post("/orders/", json={
        "user_id": 1,
        "total_amount": 99.99,
        "shipping_address": "123 Main St",
        "items": [
            {"product_id": 10, "quantity": 2, "price": 49.99}
        ]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["total_amount"] == 99.99


@pytest.mark.asyncio
async def test_get_orders_endpoint(client):
    await client.post("/orders/", json={
        "user_id": 1,
        "total_amount": 50.00,
        "shipping_address": "456 Oak Ave",
        "items": [
            {"product_id": 20, "quantity": 1, "price": 50.00}
        ]
    })
    response = await client.get("/orders/", params={"user_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_order_not_found(client):
    response = await client.get("/orders/99999")
    assert response.status_code == 404
