"""Tests for recommendation-service CRUD operations."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas


@pytest.mark.asyncio
async def test_create_recommendation(db_session: AsyncSession):
    rec_data = schemas.RecommendationCreate(
        user_id=1,
        product_id=100,
        score=0.95,
        reason="frequently_bought_together"
    )
    recommendation = await crud.create_recommendation(db_session, rec_data)
    assert recommendation.id is not None
    assert recommendation.user_id == 1
    assert recommendation.product_id == 100
    assert recommendation.score == 0.95


@pytest.mark.asyncio
async def test_get_recommendations(db_session: AsyncSession):
    rec1 = schemas.RecommendationCreate(
        user_id=1, product_id=10, score=0.8, reason="trending"
    )
    rec2 = schemas.RecommendationCreate(
        user_id=1, product_id=20, score=0.6, reason="similar_users"
    )
    rec3 = schemas.RecommendationCreate(
        user_id=2, product_id=30, score=0.9, reason="new_arrival"
    )
    await crud.create_recommendation(db_session, rec1)
    await crud.create_recommendation(db_session, rec2)
    await crud.create_recommendation(db_session, rec3)

    user1_recs = await crud.get_recommendations(db_session, user_id=1)
    assert len(user1_recs) == 2

    user2_recs = await crud.get_recommendations(db_session, user_id=2)
    assert len(user2_recs) == 1


@pytest.mark.asyncio
async def test_get_recommendations_empty(db_session: AsyncSession):
    result = await crud.get_recommendations(db_session, user_id=99999)
    assert len(result) == 0
