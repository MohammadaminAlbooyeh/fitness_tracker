package com.ecommerce.payment.event;

import com.ecommerce.payment.entity.Payment;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Publishes {@code payment.completed} once a payment settles, so
 * order-service (Python/aiokafka consumer) can confirm the order. Publishing
 * is best-effort: a broker outage must not fail the HTTP request that
 * triggered the status update.
 */
@Component
public class PaymentEventPublisher {

    private static final Logger log = LoggerFactory.getLogger(PaymentEventPublisher.class);
    private static final String TOPIC_PAYMENT_COMPLETED = "payment.completed";

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public PaymentEventPublisher(KafkaTemplate<String, Object> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void publishPaymentCompleted(Payment payment) {
        Map<String, Object> event = new LinkedHashMap<>();
        event.put("event", "payment.completed");
        event.put("paymentId", payment.getId());
        event.put("orderId", payment.getOrderId());
        event.put("amount", payment.getAmount());
        event.put("currency", payment.getCurrency());
        event.put("status", payment.getStatus());

        try {
            kafkaTemplate.send(TOPIC_PAYMENT_COMPLETED, String.valueOf(payment.getOrderId()), event);
        } catch (Exception e) {
            log.warn("Failed to publish payment.completed for order {}", payment.getOrderId(), e);
        }
    }
}
