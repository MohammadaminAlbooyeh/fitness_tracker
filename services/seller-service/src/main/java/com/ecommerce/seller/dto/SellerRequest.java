package com.ecommerce.seller.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class SellerRequest {
    private Long userId;
    private String storeName;
    private String description;
}
