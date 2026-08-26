"""Behavior tracking service FastAPI app."""

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.database import get_db
from shared_lib.security import get_current_user
from app import models, schemas, crud

app = FastAPI(title="Behavior Tracking Service", version="1.0.0")


@app.post("/behaviors/", response_model=schemas.UserBehavior, status_code=201)
async def create_behavior(
    behavior: schemas.UserBehaviorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.create_behavior(db, behavior)


@app.get("/behaviors/{user_id}", response_model=list[schemas.UserBehavior])
async def get_behaviors(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.get_behaviors(db, user_id)
