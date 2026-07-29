"""Analytics service CRUD."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import SalesAnalytics
from app.schemas import SalesAnalyticsCreate


async def get_sales_analytics(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[SalesAnalytics]:
    result = await db.execute(select(SalesAnalytics).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_sales_analytics(db: AsyncSession, analytics: SalesAnalyticsCreate) -> SalesAnalytics:
    db_analytics = SalesAnalytics(**analytics.model_dump())
    db.add(db_analytics)
    await db.commit()
    await db.refresh(db_analytics)
    return db_analytics
