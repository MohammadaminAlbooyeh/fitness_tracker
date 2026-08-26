"""Tests for the notification-service Kafka event handlers."""
import json

import pytest

from app import events


class FakeSession:
    def __init__(self, create_fn):
        self._create_fn = create_fn

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeAsyncSessionLocal:
    def __init__(self, create_fn):
        self._create_fn = create_fn

    def __call__(self):
        return FakeSession(self._create_fn)


@pytest.mark.asyncio
async def test_handle_order_created_creates_notification(monkeypatch):
    captured = {}

    async def fake_create(db, notification):
        captured["notification"] = notification

    monkeypatch.setattr(events.crud, "create_notification", fake_create)
    monkeypatch.setattr(events, "AsyncSessionLocal", FakeAsyncSessionLocal(fake_create))

    payload = json.dumps(
        {
            "event": "order.created",
            "order": {"order_id": 12, "user_id": 7, "total_amount": 49.5, "items": []},
        }
    )
    await events.handle_message(payload)

    n = captured["notification"]
    assert n.user_id == 7
    assert n.notification_type == "order"
    assert n.title == "Order confirmed"


@pytest.mark.asyncio
async def test_handle_order_created_missing_user_id(monkeypatch):
    async def fake_create(db, notification):
        raise AssertionError("should not create a notification without user_id")

    monkeypatch.setattr(events.crud, "create_notification", fake_create)
    # No user_id -> handler returns early, fake_create must not be called.
    await events.handle_message(json.dumps({"event": "order.created", "order": {}}))


@pytest.mark.asyncio
async def test_handle_message_ignores_unknown_event():
    # Unrecognized event types are logged and skipped without raising.
    await events.handle_message(json.dumps({"event": "unknown.event", "order": {}}))