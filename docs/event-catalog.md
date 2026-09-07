# Kafka Event Catalog

All events are JSON-encoded and keyed by the relevant entity id so partition
ordering is preserved per order/product. Python producers/consumers use
`aiokafka` via `shared_lib.messaging`; Java producers/consumers use
Spring Kafka.

| Topic | Producer | Consumer(s) | Payload shape |
|---|---|---|---|
| `order.created` | order-service | inventory-service (reserve stock), notification-service (notify user) | `{event, order: {order_id, user_id, status, total_amount, items[]}}` |
| `order.shipped` | order-service | notification-service (notify user) | `{event, order: {order_id, user_id, status}}` |
| `order.cancelled` | order-service | notification-service (notify user) | `{event, order: {order_id, user_id, status}}` |
| `payment.completed` | payment-service | order-service (confirm order) | `{event, paymentId, orderId, amount, currency, status}` |
| `inventory.updated` | inventory-service | none yet (reserved for analytics-service) | `{event, productId, quantity, reservedQuantity}` |
| `review.created` | review-service | none yet (reserved for analytics-service / recommendation-service) | `{event, reviewId, productId, userId, rating}` |

## Notes

- Publishing is always best-effort: a broker outage never fails the HTTP
  request that triggered the event. Producers log a warning and drop the
  event on failure.
- Python consumers (`order-service`, `notification-service`) only start when
  `KAFKA_CONSUMER_ENABLED=true`, and retry connecting to the broker with
  exponential backoff (capped at 30s) instead of giving up after one attempt.
- Order status transitions are driven via `PATCH /orders/{id}/status` on
  order-service, which publishes `order.shipped` / `order.cancelled`
  depending on the new status.
