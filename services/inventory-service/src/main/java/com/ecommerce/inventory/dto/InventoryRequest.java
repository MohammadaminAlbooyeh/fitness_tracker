package com.ecommerce.inventory.dto;

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter
@Setter
public class InventoryRequest {
    private Long productId;
    private Integer quantity;
    private BigDecimal price;
}
