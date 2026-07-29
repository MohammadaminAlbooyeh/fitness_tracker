"""Analytics service FastAPI app."""

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared_lib.database import get_db
from app import models, schemas, crud

app = FastAPI(title="Analytics Service", version="1.0.0")


@app.get("/analytics/sales/", response_model=list[schemas.SalesAnalytics])
async def read_sales_analytics(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_sales_analytics(db, skip=skip, limit=limit)


@app.post("/analytics/sales/", response_model=schemas.SalesAnalytics, status_code=201)
async def create_sales_analytics(analytics: schemas.SalesAnalyticsCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_sales_analytics(db, analytics)
