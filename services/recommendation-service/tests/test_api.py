"""Tests for recommendation-service API endpoints."""
import pytest


@pytest.mark.asyncio
async def test_create_recommendation_endpoint(client):
    response = await client.post("/recommendations/", json={
        "user_id": 1,
        "product_id": 100,
        "score": 0.95,
        "reason": "frequently_bought_together"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["product_id"] == 100
    assert data["score"] == 0.95


@pytest.mark.asyncio
async def test_get_recommendations_endpoint(client):
    await client.post("/recommendations/", json={
        "user_id": 5,
        "product_id": 10,
        "score": 0.8,
        "reason": "trending"
    })
    response = await client.get("/recommendations/5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
