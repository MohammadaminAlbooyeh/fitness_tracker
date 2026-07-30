package com.ecommerce.inventory.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class InventoryResponse {
    private Long id;
    private Long productId;
    private Integer quantity;
    private Integer reservedQuantity;
    private BigDecimal price;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
