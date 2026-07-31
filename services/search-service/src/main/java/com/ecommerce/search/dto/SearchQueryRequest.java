package com.ecommerce.search.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class SearchQueryRequest {
    private String query;
    private Long userId;
}
