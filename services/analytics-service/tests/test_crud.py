"""Tests for analytics-service CRUD operations."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas


@pytest.mark.asyncio
async def test_create_sales_analytics(db_session: AsyncSession):
    analytics_data = schemas.SalesAnalyticsCreate(
        date="2024-01-15",
        total_revenue=1500.00,
        total_orders=15,
        average_order_value=100.00
    )
    analytics = await crud.create_sales_analytics(db_session, analytics_data)
    assert analytics.id is not None
    assert analytics.date == "2024-01-15"
    assert analytics.total_revenue == 1500.00
    assert analytics.total_orders == 15


@pytest.mark.asyncio
async def test_get_sales_analytics(db_session: AsyncSession):
    data1 = schemas.SalesAnalyticsCreate(
        date="2024-01-01",
        total_revenue=1000.00,
        total_orders=10,
        average_order_value=100.00
    )
    data2 = schemas.SalesAnalyticsCreate(
        date="2024-01-02",
        total_revenue=2000.00,
        total_orders=20,
        average_order_value=100.00
    )
    await crud.create_sales_analytics(db_session, data1)
    await crud.create_sales_analytics(db_session, data2)
    results = await crud.get_sales_analytics(db_session, skip=0, limit=100)
    assert len(results) >= 2
