"""Order service FastAPI app."""
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
from shared_lib.messaging import publish_order_created, publish_order_shipped, publish_order_cancelled
from app import models, schemas, crud
from app.models import OrderStatus

logger = logging.getLogger("order-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_migrations()
    consumer_task = None
    if settings.kafka_consumer_enabled:
        from app.events import consume_forever

        consumer_task = asyncio.create_task(consume_forever())
        logger.info("payment.completed Kafka consumer started")
    yield
    if consumer_task is not None:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="Order Service", version="1.0.0", lifespan=lifespan)


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
    return {"status": "healthy", "service": "order-service"}


@app.post("/orders/", response_model=schemas.Order, status_code=201)
async def create_order(
    order: schemas.OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_order = await crud.create_order(db, order)
    # Publish the canonical order.created event -> inventory reserves stock,
    # notification-service notifies the user. Best-effort: a transient Kafka
    # outage must not fail the order that is already persisted.
    try:
        await publish_order_created(
            order_id=db_order.id,
            user_id=db_order.user_id,
            status=db_order.status.value if hasattr(db_order.status, "value") else str(db_order.status),
            total_amount=db_order.total_amount,
            items=[
                {"product_id": i.product_id, "quantity": i.quantity, "price": i.price}
                for i in order.items
            ],
        )
    except Exception:  # noqa: BLE001
        logger.warning("Failed to publish order.created event for order %s", db_order.id, exc_info=True)
    return db_order


@app.get("/orders/", response_model=list[schemas.Order])
async def read_orders(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return await crud.get_orders(db, user_id=user_id, skip=skip, limit=limit)


@app.get("/orders/{order_id}", response_model=schemas.Order)
async def read_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    order = await crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.patch("/orders/{order_id}/status", response_model=schemas.Order)
async def update_order_status(
    order_id: int,
    status_update: schemas.OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        new_status = OrderStatus(status_update.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status_update.status}")

    order = await crud.update_order_status(db, order_id, new_status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Best-effort: notify downstream consumers of the status transition.
    # A transient Kafka outage must not fail a status update that already
    # persisted successfully.
    try:
        if new_status == OrderStatus.SHIPPED:
            await publish_order_shipped(order.id, order.user_id, new_status.value)
        elif new_status == OrderStatus.CANCELLED:
            await publish_order_cancelled(order.id, order.user_id, new_status.value)
    except Exception:  # noqa: BLE001
        logger.warning("Failed to publish status event for order %s", order.id, exc_info=True)
    return order
