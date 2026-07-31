package com.ecommerce.search.dto;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
public class SearchQueryResponse {
    private Long id;
    private String query;
    private Long userId;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
