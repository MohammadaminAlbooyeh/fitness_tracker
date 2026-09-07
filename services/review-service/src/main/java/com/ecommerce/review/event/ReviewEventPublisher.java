package com.ecommerce.review.event;

import com.ecommerce.review.entity.Review;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Publishes {@code review.created} after a review is saved, for consumers
 * such as analytics-service or recommendation-service. Publishing is
 * best-effort: a broker outage must not fail the HTTP request that created
 * the review.
 */
@Component
public class ReviewEventPublisher {

    private static final Logger log = LoggerFactory.getLogger(ReviewEventPublisher.class);
    private static final String TOPIC_REVIEW_CREATED = "review.created";

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public ReviewEventPublisher(KafkaTemplate<String, Object> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void publishReviewCreated(Review review) {
        Map<String, Object> event = new LinkedHashMap<>();
        event.put("event", "review.created");
        event.put("reviewId", review.getId());
        event.put("productId", review.getProductId());
        event.put("userId", review.getUserId());
        event.put("rating", review.getRating());

        try {
            kafkaTemplate.send(TOPIC_REVIEW_CREATED, String.valueOf(review.getProductId()), event);
        } catch (Exception e) {
            log.warn("Failed to publish review.created for product {}", review.getProductId(), e);
        }
    }
}
