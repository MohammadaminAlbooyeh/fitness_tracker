"""Tests for notification-service API endpoints."""
import pytest


@pytest.mark.asyncio
async def test_create_notification_endpoint(client):
    response = await client.post("/notifications/", json={
        "user_id": 1,
        "title": "API Notification",
        "message": "Test message",
        "notification_type": "system"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "API Notification"
    assert data["is_read"] is False


@pytest.mark.asyncio
async def test_get_notifications_endpoint(client):
    await client.post("/notifications/", json={
        "user_id": 5,
        "title": "Test",
        "message": "Msg",
        "notification_type": "system"
    })
    response = await client.get("/notifications/5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
