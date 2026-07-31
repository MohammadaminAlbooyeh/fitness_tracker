"""Tests for product-service API endpoints."""
import pytest


@pytest.mark.asyncio
async def test_create_category_endpoint(client):
    response = await client.post("/categories/", json={
        "name": "API Category",
        "description": "API test category"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "API Category"


@pytest.mark.asyncio
async def test_get_categories_endpoint(client):
    response = await client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_products_endpoint(client):
    response = await client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_product_not_found(client):
    response = await client.get("/products/99999")
    assert response.status_code == 404
