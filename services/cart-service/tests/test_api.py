"""Tests for cart-service API endpoints."""
import pytest


@pytest.mark.asyncio
async def test_create_cart_endpoint(client):
    response = await client.post("/carts/", params={"user_id": 1})
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1


@pytest.mark.asyncio
async def test_get_cart_not_found(client):
    response = await client.get("/carts/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_item_endpoint(client):
    await client.post("/carts/", params={"user_id": 2})
    response = await client.post("/carts/2/items", json={
        "product_id": 100,
        "quantity": 2,
        "price": 29.99
    })
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == 100
    assert data["quantity"] == 2
