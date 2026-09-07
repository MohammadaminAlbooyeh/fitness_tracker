"""Kafka consumer logic for the notification service.

Listens on ``order.created``, ``order.shipped`` and ``order.cancelled``
(published by the order-service) and creates a ``Notification`` row for the
ordering user. The consumer is only started when
``settings.kafka_consumer_enabled`` is true (set via ``KAFKA_CONSUMER_ENABLED``)
so unit tests and broker-less local runs are unaffected.

The connect loop retries with backoff instead of giving up after a single
failed attempt, since the broker may not be reachable yet during startup.
"""

from __future__ import annotations

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer

from shared_lib.config import settings
from shared_lib.database import AsyncSessionLocal
from shared_lib.messaging import TOPIC_ORDER_CREATED, TOPIC_ORDER_SHIPPED, TOPIC_ORDER_CANCELLED
from app import crud, schemas

logger = logging.getLogger("notification-service.events")

_MAX_BACKOFF_SECONDS = 30


async def _handle_order_created(event: dict) -> None:
    order = event.get("order", {})
    user_id = order.get("user_id")
    if user_id is None:
        logger.warning("Ignoring order.created payload without user_id")
        return
    message = (
        f"Your order #{order.get('order_id')} was placed successfully "
        f"with a total of ${order.get('total_amount', 0):.2f}."
    )
    notification = schemas.NotificationCreate(
        user_id=int(user_id),
        title="Order confirmed",
        message=message,
        notification_type="order",
    )
    async with AsyncSessionLocal() as session:
        await crud.create_notification(session, notification)
    logger.info("Created order notification for user %s", user_id)


async def _handle_order_status_event(event: dict, title: str, message_template: str) -> None:
    order = event.get("order", {})
    user_id = order.get("user_id")
    if user_id is None:
        logger.warning("Ignoring %s payload without user_id", event.get("event"))
        return
    notification = schemas.NotificationCreate(
        user_id=int(user_id),
        title=title,
        message=message_template.format(order_id=order.get("order_id")),
        notification_type="order",
    )
    async with AsyncSessionLocal() as session:
        await crud.create_notification(session, notification)
    logger.info("Created %s notification for user %s", event.get("event"), user_id)


async def handle_message(payload: str) -> None:
    """Parse a raw Kafka payload and dispatch it to the right handler."""
    event = json.loads(payload)
    event_name = event.get("event")
    if event_name == "order.created":
        await _handle_order_created(event)
    elif event_name == "order.shipped":
        await _handle_order_status_event(event, "Order shipped", "Your order #{order_id} has shipped.")
    elif event_name == "order.cancelled":
        await _handle_order_status_event(event, "Order cancelled", "Your order #{order_id} was cancelled.")
    else:
        logger.warning("Ignoring unhandled event type %s", event_name)


async def consume_forever() -> None:
    """Run the consumer loop until cancelled, retrying connection with backoff."""
    backoff = 1
    while True:
        consumer = AIOKafkaConsumer(
            TOPIC_ORDER_CREATED,
            TOPIC_ORDER_SHIPPED,
            TOPIC_ORDER_CANCELLED,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id="notification-service",
            enable_auto_commit=True,
            auto_offset_reset="earliest",
        )
        try:
            await consumer.start()
        except Exception:  # noqa: BLE001
            logger.warning(
                "Could not connect to Kafka (%s); retrying in %ss",
                settings.kafka_bootstrap_servers,
                backoff,
                exc_info=True,
            )
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, _MAX_BACKOFF_SECONDS)
            continue
        backoff = 1
        try:
            async for message in consumer:
                try:
                    # message.value is the raw utf-8 JSON payload produced by the
                    # order-service; decode & dispatch it.
                    await handle_message(message.value.decode("utf-8"))
                except Exception:  # noqa: BLE001
                    logger.warning("Error handling order event message", exc_info=True)
        finally:
            await consumer.stop()