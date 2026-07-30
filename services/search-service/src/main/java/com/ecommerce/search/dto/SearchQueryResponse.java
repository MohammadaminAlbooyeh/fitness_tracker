package com.ecommerce.search.dto;

import java.time.LocalDateTime;

public class SearchQueryResponse {
    private Long id;
    private String query;
    private Long userId;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
