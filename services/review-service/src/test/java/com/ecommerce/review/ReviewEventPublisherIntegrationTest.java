package com.ecommerce.review.service;

import com.ecommerce.review.entity.Review;
import com.ecommerce.review.event.ReviewEventPublisher;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.junit.jupiter.api.Test;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.listener.ContainerProperties;
import org.springframework.kafka.listener.KafkaMessageListenerContainer;
import org.springframework.kafka.listener.MessageListener;
import org.springframework.kafka.support.serializer.JsonDeserializer;
import org.testcontainers.containers.KafkaContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.DockerImageName;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

@Testcontainers
class ReviewEventPublisherIntegrationTest {

    @Container
    static final KafkaContainer KAFKA = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:latest"));

    @Test
    void publishReviewCreated_sendsEventToKafka() throws Exception {
        Map<String, Object> producerProps = new HashMap<>();
        producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, KAFKA.getBootstrapServers());
        producerProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        producerProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, org.springframework.kafka.support.serializer.JsonSerializer.class);

        DefaultKafkaProducerFactory<String, Object> producerFactory = new DefaultKafkaProducerFactory<>(producerProps);
        KafkaTemplate<String, Object> template = new KafkaTemplate<>(producerFactory);
        template.setDefaultTopic("review.created");

        ReviewEventPublisher publisher = new ReviewEventPublisher(template);

        Review review = new Review();
        review.setId(1L);
        review.setProductId(200L);
        review.setUserId(50L);
        review.setRating(5);

        publisher.publishReviewCreated(review);
        template.flush();

        Map<String, Object> consumerProps = new HashMap<>();
        consumerProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, KAFKA.getBootstrapServers());
        consumerProps.put(ConsumerConfig.GROUP_ID_CONFIG, "test-group");
        consumerProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        consumerProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        consumerProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
        consumerProps.put(JsonDeserializer.TRUSTED_PACKAGES, "*");

        DefaultKafkaConsumerFactory<String, Object> consumerFactory = new DefaultKafkaConsumerFactory<>(consumerProps);
        ContainerProperties containerProps = new ContainerProperties("review.created");

        BlockingQueue<ConsumerRecord<String, Object>> records = new LinkedBlockingQueue<>();
        containerProps.setMessageListener((MessageListener<String, Object>) record -> records.add(record));

        KafkaMessageListenerContainer<String, Object> container = new KafkaMessageListenerContainer<>(consumerFactory, containerProps);
        container.start();

        ConsumerRecord<String, Object> record = records.poll(5, TimeUnit.SECONDS);
        assertNotNull(record);
        assertNotNull(record.value());

        @SuppressWarnings("unchecked")
        Map<String, Object> event = (Map<String, Object>) record.value();
        assertEquals("review.created", event.get("event"));
        assertEquals(1L, event.get("reviewId"));
        assertEquals(200L, event.get("productId"));
        assertEquals(50L, event.get("userId"));
        assertEquals(5, event.get("rating"));

        container.stop();
    }
}
