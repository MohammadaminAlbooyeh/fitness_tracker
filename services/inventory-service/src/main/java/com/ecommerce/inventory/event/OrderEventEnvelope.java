package com.ecommerce.inventory.event;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

/**
 * Top-level envelope of an {@code order.created} event published by the
 * order-service to Kafka topic {@code order.created}.
 *
 * <pre>{@code
 * {
 *   "event": "order.created",
 *   "order": {
 *     "order_id": 12,
 *     "user_id": 7,
 *     "status": "pending",
 *     "total_amount": 199.99,
 *     "items": [{"product_id": 3, "quantity": 2, "price": 99.995}]
 *   }
 * }
 * }</pre>
 */
@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class OrderEventEnvelope {

    @JsonProperty("event")
    private String event;

    @JsonProperty("order")
    private OrderEvent order;
}