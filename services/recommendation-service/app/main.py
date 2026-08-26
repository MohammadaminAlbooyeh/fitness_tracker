"""Recommendation service FastAPI app."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from subprocess import run

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.database import get_db
from shared_lib.security import get_current_user
from app import models, schemas, crud

logger = logging.getLogger("recommendation-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_migrations()
    yield


app = FastAPI(title="Recommendation Service", version="1.0.0", lifespan=lifespan)


def _run_migrations() -> None:
    migrations_dir = Path(__file__).resolve().parent.parent / "migrations"
    result = run(
        ["python", "-m", "alembic", "upgrade", "head"],
        cwd=migrations_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.error("Alembic migration failed: %s", result.stderr)
    else:
        logger.info("Alembic migrations applied")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "recommendation-service"}


@app.get("/recommendations/{user_id}", response_model=list[schemas.Recommendation])
async def get_recommendations(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.get_recommendations(db, user_id)


@app.post("/recommendations/", response_model=schemas.Recommendation, status_code=201)
async def create_recommendation(
    recommendation: schemas.RecommendationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.create_recommendation(db, recommendation)
