"""Tests for user-service API endpoints."""
import pytest


@pytest.mark.asyncio
async def test_create_user_endpoint(client):
    response = await client.post("/users/", json={
        "email": "api@example.com",
        "full_name": "API User",
        "password": "securepassword123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "api@example.com"
    assert data["full_name"] == "API User"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client):
    user_data = {
        "email": "duplicate@example.com",
        "full_name": "Dup User",
        "password": "password123"
    }
    await client.post("/users/", json=user_data)
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/users/99999")
    assert response.status_code == 404
