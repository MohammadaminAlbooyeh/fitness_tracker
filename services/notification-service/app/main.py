"""Notification service FastAPI app."""
import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from subprocess import run

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.config import settings
from shared_lib.database import get_db
from shared_lib.security import get_current_user
from app import models, schemas, crud

logger = logging.getLogger("notification-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_migrations()
    consumer_task = None
    if settings.kafka_consumer_enabled:
        from app.events import consume_forever

        consumer_task = asyncio.create_task(consume_forever())
        logger.info("order.created Kafka consumer started")
    yield
    if consumer_task is not None:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="Notification Service", version="1.0.0", lifespan=lifespan)


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
    return {"status": "healthy", "service": "notification-service"}


@app.post("/notifications/", response_model=schemas.Notification, status_code=201)
async def create_notification(
    notification: schemas.NotificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.create_notification(db, notification)


@app.get("/notifications/{user_id}", response_model=list[schemas.Notification])
async def get_notifications(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.get_notifications(db, user_id)
