package com.ecommerce.inventory.entity;

import com.ecommerce.common.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Entity
@Table(name = "inventory")
@Getter
@Setter
public class Inventory extends BaseEntity {

    @Column(nullable = false, unique = true)
    private Long productId;

    private Integer quantity;

    private Integer reservedQuantity = 0;

    private BigDecimal price;
}
