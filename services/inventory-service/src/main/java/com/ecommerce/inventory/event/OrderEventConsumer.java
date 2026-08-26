package com.ecommerce.inventory.event;

import com.ecommerce.inventory.service.InventoryService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

/**
 * Consumes {@code order.created} events published by the order-service and
 * reserves stock for each ordered product. Runs in its own consumer group so a
 * slow inventory consumer never blocks the notification consumer.
 */
@Component
public class OrderEventConsumer {

    private static final Logger log = LoggerFactory.getLogger(OrderEventConsumer.class);
    private static final String ORDER_CREATED_TOPIC = "order.created";

    private final ObjectMapper objectMapper;
    private final InventoryService inventoryService;

    public OrderEventConsumer(ObjectMapper objectMapper, InventoryService inventoryService) {
        this.objectMapper = objectMapper;
        this.inventoryService = inventoryService;
    }

    @KafkaListener(topics = ORDER_CREATED_TOPIC, groupId = "inventory-service")
    public void onOrderCreated(@Payload String payload) {
        OrderEventEnvelope envelope;
        try {
            envelope = objectMapper.readValue(payload, OrderEventEnvelope.class);
        } catch (Exception e) {
            log.error("Failed to deserialize order.created payload", e);
            return;
        }

        if (envelope.getOrder() == null || !"order.created".equals(envelope.getEvent())) {
            log.warn("Ignoring unexpected event payload: event={}", envelope.getEvent());
            return;
        }

        OrderEvent order = envelope.getOrder();
        if (order == null) {
            log.warn("order.created event with no order body; ignoring");
            return;
        }

        if (order.getItems() != null) {
            for (OrderItemEvent item : order.getItems()) {
                try {
                    inventoryService.reserveStock(item.getProductId(), item.getQuantity());
                    log.info("Reserved {} of product {} for order {}",
                            item.getQuantity(), item.getProductId(), order.getOrderId());
                } catch (RuntimeException e) {
                    log.warn("Could not reserve product {} for order {}: {}",
                            item.getProductId(), order.getOrderId(), e.getMessage());
                }
            }
        }
    }
}