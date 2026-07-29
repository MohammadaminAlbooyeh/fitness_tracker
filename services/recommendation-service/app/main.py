"""Recommendation service FastAPI app."""

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.database import get_db
from app import models, schemas, crud

app = FastAPI(title="Recommendation Service", version="1.0.0")


@app.get("/recommendations/{user_id}", response_model=list[schemas.Recommendation])
async def get_recommendations(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_recommendations(db, user_id)


@app.post("/recommendations/", response_model=schemas.Recommendation, status_code=201)
async def create_recommendation(recommendation: schemas.RecommendationCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_recommendation(db, recommendation)
