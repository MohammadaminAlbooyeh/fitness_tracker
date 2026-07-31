"""Tests for analytics-service API endpoints."""
import pytest


@pytest.mark.asyncio
async def test_create_sales_analytics_endpoint(client):
    response = await client.post("/analytics/sales/", json={
        "date": "2024-01-15",
        "total_revenue": 1500.00,
        "total_orders": 15,
        "average_order_value": 100.00
    })
    assert response.status_code == 201
    data = response.json()
    assert data["date"] == "2024-01-15"
    assert data["total_orders"] == 15


@pytest.mark.asyncio
async def test_get_sales_analytics_endpoint(client):
    response = await client.get("/analytics/sales/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
