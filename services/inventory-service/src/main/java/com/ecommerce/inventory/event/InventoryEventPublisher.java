package com.ecommerce.inventory.event;

import com.ecommerce.inventory.entity.Inventory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Publishes {@code inventory.updated} whenever stock levels change, for any
 * downstream consumer that needs to react to stock (e.g. analytics-service).
 * Publishing is best-effort: a broker outage must not fail the HTTP request
 * that triggered the stock change.
 */
@Component
public class InventoryEventPublisher {

    private static final Logger log = LoggerFactory.getLogger(InventoryEventPublisher.class);
    private static final String TOPIC_INVENTORY_UPDATED = "inventory.updated";

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public InventoryEventPublisher(KafkaTemplate<String, Object> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void publishInventoryUpdated(Inventory inventory) {
        Map<String, Object> event = new LinkedHashMap<>();
        event.put("event", "inventory.updated");
        event.put("productId", inventory.getProductId());
        event.put("quantity", inventory.getQuantity());
        event.put("reservedQuantity", inventory.getReservedQuantity());

        try {
            kafkaTemplate.send(TOPIC_INVENTORY_UPDATED, String.valueOf(inventory.getProductId()), event);
        } catch (Exception e) {
            log.warn("Failed to publish inventory.updated for product {}", inventory.getProductId(), e);
        }
    }
}
