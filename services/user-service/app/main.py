"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from subprocess import run

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.database import get_db
from shared_lib.security import create_access_token, get_current_user, verify_password
from app import models, schemas, crud

logger = logging.getLogger("user-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_migrations()
    yield


app = FastAPI(title="User Service", version="1.0.0", lifespan=lifespan)


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
    return {"status": "healthy", "service": "user-service"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db, user)


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user = await crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
