"""Recommendation service schemas."""

from pydantic import BaseModel, ConfigDict


class RecommendationBase(BaseModel):
    user_id: int
    product_id: int
    score: float
    reason: str | None = None


class RecommendationCreate(RecommendationBase):
    pass


class Recommendation(RecommendationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
