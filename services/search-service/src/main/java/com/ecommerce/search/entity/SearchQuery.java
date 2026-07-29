package com.ecommerce.search.entity;

import com.ecommerce.common.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Entity
@Table(name = "search_queries")
@Getter
@Setter
public class SearchQuery extends BaseEntity {

    @Column(nullable = false)
    private String query;

    @Column(nullable = false)
    private Long userId;
}
