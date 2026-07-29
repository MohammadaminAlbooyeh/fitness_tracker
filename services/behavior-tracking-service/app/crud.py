"""Behavior tracking service CRUD."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import UserBehavior
from app.schemas import UserBehaviorCreate


async def create_behavior(db: AsyncSession, behavior: UserBehaviorCreate) -> UserBehavior:
    db_behavior = UserBehavior(**behavior.model_dump())
    db.add(db_behavior)
    await db.commit()
    await db.refresh(db_behavior)
    return db_behavior


async def get_behaviors(db: AsyncSession, user_id: int) -> list[UserBehavior]:
    result = await db.execute(select(UserBehavior).where(UserBehavior.user_id == user_id))
    return list(result.scalars().all())
