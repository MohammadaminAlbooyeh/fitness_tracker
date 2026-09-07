"""Async Kafka (MSG/MSK) helpers for event-driven flows.

Canonical topics used across the platform:

- ``order.created``: published by order-service after an order is placed.
  Consumed by inventory-service (reserve stock) and notification-service
  (notify the user).
- ``order.shipped`` / ``order.cancelled``: published by order-service on the
  corresponding status transition. Consumed by notification-service.
- ``payment.completed``: published by payment-service (Java/Spring Kafka)
  once a payment settles. Consumed by order-service to confirm the order.
- ``inventory.updated``: published by inventory-service (Java/Spring Kafka)
  whenever stock levels change. No Python consumer yet; reserved for
  analytics-service.
- ``review.created``: published by review-service (Java/Spring Kafka) after a
  review is saved. No Python consumer yet; reserved for
  analytics-service/recommendation-service.

See docs/event-catalog.md for the full producer/consumer matrix.

The published event payload is JSON and is intentionally language-agnostic so
Python producers/consumers and Java (Spring Kafka) consumers can interoperate.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Optional

from aiokafka import AIOKafkaProducer

from shared_lib.config import settings

logger = logging.getLogger("shared_lib.messaging")

TOPIC_ORDER_CREATED = "order.created"
TOPIC_ORDER_SHIPPED = "order.shipped"
TOPIC_ORDER_CANCELLED = "order.cancelled"
TOPIC_PAYMENT_COMPLETED = "payment.completed"
TOPIC_INVENTORY_UPDATED = "inventory.updated"
TOPIC_REVIEW_CREATED = "review.created"

EVENT_ORDER_CREATED = "order.created"
EVENT_ORDER_SHIPPED = "order.shipped"
EVENT_ORDER_CANCELLED = "order.cancelled"


def build_order_created_event(
    order_id: int,
    user_id: int,
    status: str,
    total_amount: float,
    items: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build the canonical payload published to ``order.created``.

    ``items`` entries must contain at least ``product_id``, ``quantity`` and
    ``price``. Keys are camelCase to match the Java consumers' Jackson DTOs.
    """
    return {
        "event": EVENT_ORDER_CREATED,
        "order": {
            "order_id": order_id,
            "user_id": user_id,
            "status": status,
            "total_amount": total_amount,
            "items": [
                {
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                }
                for item in items
            ],
        },
    }


def build_order_status_event(event_name: str, order_id: int, user_id: int, status: str) -> dict[str, Any]:
    """Build the canonical payload for order status-transition events."""
    return {
        "event": event_name,
        "order": {
            "order_id": order_id,
            "user_id": user_id,
            "status": status,
        },
    }


class KafkaPublisher:
    """Small, best-effort async publisher wrapper around ``AIOKafkaProducer``.

    Publishing never raises: if the broker is unreachable the event is logged
    and dropped so the HTTP request that triggered it still succeeds. This keeps
    synchronous REST paths resilient while the async consumers are eventually
    consistent.
    """

    def __init__(self, bootstrap_servers: Optional[str] = None) -> None:
        self.bootstrap_servers = bootstrap_servers or settings.kafka_bootstrap_servers

    def _serializer(self, value: Any) -> bytes:
        return json.dumps(value, default=str).encode("utf-8")

    async def publish(self, topic: str, key: str, value: dict[str, Any]) -> None:
        producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=self._serializer,
        )
        try:
            await producer.start()
            await producer.send_and_wait(topic, value=value, key=key.encode("utf-8"))
        except Exception:  # noqa: BLE001 - best-effort eventing
            logger.warning("Failed to publish event to topic %s", topic, exc_info=True)
        finally:
            await producer.stop()

    async def publish_order_created(
        self,
        order_id: int,
        user_id: int,
        status: str,
        total_amount: float,
        items: list[dict[str, Any]],
    ) -> None:
        event = build_order_created_event(order_id, user_id, status, total_amount, items)
        await self.publish(
            TOPIC_ORDER_CREATED,
            key=f"order:{order_id}",
            value=event,
        )

    async def publish_order_shipped(self, order_id: int, user_id: int, status: str) -> None:
        event = build_order_status_event(EVENT_ORDER_SHIPPED, order_id, user_id, status)
        await self.publish(TOPIC_ORDER_SHIPPED, key=f"order:{order_id}", value=event)

    async def publish_order_cancelled(self, order_id: int, user_id: int, status: str) -> None:
        event = build_order_status_event(EVENT_ORDER_CANCELLED, order_id, user_id, status)
        await self.publish(TOPIC_ORDER_CANCELLED, key=f"order:{order_id}", value=event)


async def publish_order_created(
    order_id: int,
    user_id: int,
    status: str,
    total_amount: float,
    items: list[dict[str, Any]],
) -> None:
    """One-shot convenience wrapper used by order-service."""
    await KafkaPublisher().publish_order_created(order_id, user_id, status, total_amount, items)


async def publish_order_shipped(order_id: int, user_id: int, status: str) -> None:
    """One-shot convenience wrapper used by order-service."""
    await KafkaPublisher().publish_order_shipped(order_id, user_id, status)


async def publish_order_cancelled(order_id: int, user_id: int, status: str) -> None:
    """One-shot convenience wrapper used by order-service."""
    await KafkaPublisher().publish_order_cancelled(order_id, user_id, status)