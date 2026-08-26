package com.ecommerce.inventory.event;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;
import java.util.List;

/**
 * The {@code order} object embedded in an {@code order.created} event.
 */
@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class OrderEvent {

    @JsonProperty("order_id")
    private Long orderId;

    @JsonProperty("user_id")
    private Long userId;

    @JsonProperty("status")
    private String status;

    @JsonProperty("total_amount")
    private BigDecimal totalAmount;

    @JsonProperty("items")
    private List<OrderItemEvent> items;
}