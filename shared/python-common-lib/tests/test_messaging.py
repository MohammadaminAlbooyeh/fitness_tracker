"""Tests for shared_lib messaging (Kafka) helpers."""
import pytest

from shared_lib import messaging


class FakeProducer:
    """Records sends instead of talking to a real broker."""

    sent: list = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.started = False
        self.stopped = False

    async def start(self):
        self.started = True

    async def send_and_wait(self, topic, value=None, key=None):
        self.sent.append((topic, value, key))

    async def stop(self):
        self.stopped = True


def test_order_created_event_contract():
    """The payload must use camelCase keys matching the Java Jackson DTOs."""
    event = messaging.build_order_created_event(
        order_id=42,
        user_id=7,
        status="pending",
        total_amount=19.99,
        items=[{"product_id": 3, "quantity": 2, "price": 9.995}],
    )
    assert event["event"] == "order.created"
    order = event["order"]
    assert order["order_id"] == 42
    assert order["user_id"] == 7
    assert order["status"] == "pending"
    assert order["total_amount"] == 19.99
    item = order["items"][0]
    assert item["product_id"] == 3
    assert item["quantity"] == 2
    assert item["price"] == 9.995


@pytest.mark.asyncio
async def test_publisher_publishes_order_created(monkeypatch):
    FakeProducer.sent.clear()
    monkeypatch.setattr(messaging, "AIOKafkaProducer", FakeProducer)
    publisher = messaging.KafkaPublisher(bootstrap_servers="localhost:9092")
    await publisher.publish_order_created(
        order_id=42,
        user_id=7,
        status="pending",
        total_amount=19.99,
        items=[{"product_id": 3, "quantity": 2, "price": 9.995}],
    )
    assert len(FakeProducer.sent) == 1
    topic, value, key = FakeProducer.sent[0]
    assert topic == messaging.TOPIC_ORDER_CREATED
    assert key == b"order:42"
    assert value["event"] == "order.created"
    assert value["order"]["order_id"] == 42


@pytest.mark.asyncio
async def test_publish_is_best_effort_when_broker_down(monkeypatch):
    class BrokenProducer:
        def __init__(self, **kwargs):
            pass

        async def start(self):
            raise RuntimeError("broker unreachable")

        async def stop(self):
            pass

    monkeypatch.setattr(messaging, "AIOKafkaProducer", BrokenProducer)
    publisher = messaging.KafkaPublisher(bootstrap_servers="127.0.0.1:9999")
    # Must not raise even though the broker is unavailable.
    await publisher.publish("order.created", "order:1", {"event": "order.created"})