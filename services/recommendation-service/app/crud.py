"""Recommendation service CRUD."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Recommendation
from app.schemas import RecommendationCreate


async def get_recommendations(db: AsyncSession, user_id: int) -> list[Recommendation]:
    result = await db.execute(select(Recommendation).where(Recommendation.user_id == user_id))
    return list(result.scalars().all())


async def create_recommendation(db: AsyncSession, recommendation: RecommendationCreate) -> Recommendation:
    db_rec = Recommendation(**recommendation.model_dump())
    db.add(db_rec)
    await db.commit()
    await db.refresh(db_rec)
    return db_rec
