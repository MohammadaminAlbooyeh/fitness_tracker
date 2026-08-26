"""Behavior tracking service FastAPI app."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from subprocess import run

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.database import get_db
from shared_lib.security import get_current_user
from app import models, schemas, crud

logger = logging.getLogger("behavior-tracking-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_migrations()
    yield


app = FastAPI(title="Behavior Tracking Service", version="1.0.0", lifespan=lifespan)


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
    return {"status": "healthy", "service": "behavior-tracking-service"}


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
