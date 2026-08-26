"""Product service FastAPI app."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from subprocess import run

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.database import get_db
from shared_lib.security import get_current_user
from app import models, schemas, crud

logger = logging.getLogger("product-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_migrations()
    yield


app = FastAPI(title="Product Service", version="1.0.0", lifespan=lifespan)


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
    return {"status": "healthy", "service": "product-service"}


@app.post("/products/", response_model=schemas.Product, status_code=201)
async def create_product(
    product: schemas.ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.create_product(db, product)


@app.get("/products/", response_model=list[schemas.Product])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.get_products(db, skip=skip, limit=limit)


@app.get("/products/{product_id}", response_model=schemas.Product)
async def read_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    product = await crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/categories/", response_model=schemas.Category, status_code=201)
async def create_category(
    category: schemas.CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.create_category(db, category)


@app.get("/categories/", response_model=list[schemas.Category])
async def read_categories(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.get_categories(db)
