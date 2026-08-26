package com.ecommerce.inventory.event;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

/**
 * One line item from an {@code order.created} event.
 */
@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class OrderItemEvent {

    @JsonProperty("product_id")
    private Long productId;

    @JsonProperty("quantity")
    private Integer quantity;

    @JsonProperty("price")
    private BigDecimal price;
}