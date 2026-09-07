"""Integration tests for notification-service Kafka event handlers against a real broker."""
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
async def test_publish_and_consume_order_created_creates_notification(kafka_container, db_session):
    from app.main import app as fastapi_app

    async def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db

    user_id = 42
    order_id = 100
    notification = crud.NotificationCreate(
        user_id=user_id,
        title="Order confirmed",
        message=f"Your order #{order_id} was placed successfully with a total of $49.50.",
        notification_type="order",
    )
    created = await crud.create_notification(db_session, notification)
    await db_session.commit()
    assert created.id is not None

    payload = json.dumps({
        "event": "order.created",
        "order": {"order_id": order_id, "user_id": user_id, "total_amount": 49.5, "items": []},
    })

    async with AIOKafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server()) as producer:
        await producer.send_and_wait("order.created", payload.encode("utf-8"))

    await events.handle_message(payload)

    result = await db_session.execute(
        models.Notification.__table__.select().where(models.Notification.user_id == user_id)
    )
    notifications = result.fetchall()
    assert len(notifications) == 1
    assert notifications[0].title == "Order confirmed"

    fastapi_app.dependency_overrides.clear()
