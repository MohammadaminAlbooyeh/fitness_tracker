"""Integration tests for order-service Kafka event handlers against a real broker."""
import json
import os
import sys
from pathlib import Path

import pytest
from aiokafka import AIOKafkaProducer
from testcontainers.community.kafka import KafkaContainer

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared" / "python-common-lib"))
sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///test_svc.db"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"
os.environ["KAFKA_BOOTSTRAP_SERVERS"] = "localhost:9092"
os.environ["KAFKA_CONSUMER_ENABLED"] = "false"

from shared_lib.base_model import Base
from shared_lib.database import get_db
from app import crud, events, models
from app.models import OrderStatus
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    engine = create_async_engine("sqlite+aiosqlite:///test_svc.db", echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///test_svc.db", echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="session")
def kafka_container():
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        kafka.start()
        os.environ["KAFKA_BOOTSTRAP_SERVERS"] = kafka.get_bootstrap_server()
        yield kafka


@pytest.mark.asyncio
async def test_payment_completed_confirms_order(kafka_container, db_session):
    order = models.Order(user_id=1, total_amount=99.99, shipping_address="123 Main St", status=OrderStatus.PENDING)
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    order_id = order.id

    payload = json.dumps({
        "event": "payment.completed",
        "paymentId": 1,
        "orderId": order_id,
        "amount": 99.99,
        "currency": "USD",
        "status": "COMPLETED",
    })

    async with AIOKafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server()) as producer:
        await producer.send_and_wait("payment.completed", payload.encode("utf-8"))

    await events.handle_message(payload)

    result = await db_session.execute(
        models.Order.__table__.select().where(models.Order.id == order_id)
    )
    updated_order = result.fetchone()
    assert updated_order is not None
    assert updated_order.status == OrderStatus.CONFIRMED.value


@pytest.mark.asyncio
async def test_payment_completed_ignores_missing_order_id(kafka_container, db_session):
    payload = json.dumps({"event": "payment.completed", "orderId": None})
    result = await events.handle_message(payload)
    assert result is None
