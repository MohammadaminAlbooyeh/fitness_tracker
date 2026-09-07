"""Kafka consumer logic for the order service.

Listens on ``payment.completed`` (published by the Java payment-service) and
confirms the corresponding order. The consumer is only started when
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
from shared_lib.messaging import TOPIC_PAYMENT_COMPLETED
from app import crud
from app.models import OrderStatus

logger = logging.getLogger("order-service.events")

_MAX_BACKOFF_SECONDS = 30


async def _handle_payment_completed(event: dict) -> None:
    order_id = event.get("orderId") or event.get("order_id")
    if order_id is None:
        logger.warning("Ignoring payment.completed payload without orderId")
        return
    async with AsyncSessionLocal() as session:
        order = await crud.update_order_status(session, int(order_id), OrderStatus.CONFIRMED)
    if order is None:
        logger.warning("payment.completed for unknown order %s", order_id)
        return
    logger.info("Order %s confirmed after payment completion", order_id)


async def handle_message(payload: str) -> None:
    """Parse a raw Kafka payload and dispatch it to the right handler."""
    event = json.loads(payload)
    event_name = event.get("event")
    if event_name == "payment.completed":
        await _handle_payment_completed(event)
    else:
        logger.warning("Ignoring unhandled event type %s", event_name)


async def consume_forever() -> None:
    """Run the consumer loop until cancelled, retrying connection with backoff."""
    backoff = 1
    while True:
        consumer = AIOKafkaConsumer(
            TOPIC_PAYMENT_COMPLETED,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id="order-service",
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
                    await handle_message(message.value.decode("utf-8"))
                except Exception:  # noqa: BLE001
                    logger.warning("Error handling payment event message", exc_info=True)
        finally:
            await consumer.stop()
