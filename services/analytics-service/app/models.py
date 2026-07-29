"""Analytics service models."""

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from shared_lib.base_model import Base, TimestampMixin


class SalesAnalytics(Base, TimestampMixin):
    __tablename__ = "sales_analytics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    total_revenue: Mapped[float] = mapped_column(Float, nullable=False)
    total_orders: Mapped[int] = mapped_column(Integer, nullable=False)
    average_order_value: Mapped[float] = mapped_column(Float, nullable=False)
