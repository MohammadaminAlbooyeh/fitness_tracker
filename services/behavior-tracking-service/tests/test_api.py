"""Tests for behavior-tracking-service API endpoints."""
import pytest


@pytest.mark.asyncio
async def test_create_behavior_endpoint(client):
    response = await client.post("/behaviors/", json={
        "user_id": 1,
        "product_id": 100,
        "event_type": "view",
        "metadata": "page_duration=30s"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["product_id"] == 100
    assert data["event_type"] == "view"


@pytest.mark.asyncio
async def test_get_behaviors_endpoint(client):
    await client.post("/behaviors/", json={
        "user_id": 5,
        "product_id": 1,
        "event_type": "click",
        "metadata": None
    })
    response = await client.get("/behaviors/5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
