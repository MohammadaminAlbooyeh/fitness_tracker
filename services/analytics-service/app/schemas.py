"""Analytics service schemas."""

from pydantic import BaseModel, ConfigDict


class SalesAnalyticsBase(BaseModel):
    date: str
    total_revenue: float
    total_orders: int
    average_order_value: float


class SalesAnalyticsCreate(SalesAnalyticsBase):
    pass


class SalesAnalytics(SalesAnalyticsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
