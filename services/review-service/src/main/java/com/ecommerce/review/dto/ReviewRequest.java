package com.ecommerce.review.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ReviewRequest {
    private Long productId;
    private Long userId;
    private Integer rating;
    private String comment;
}
