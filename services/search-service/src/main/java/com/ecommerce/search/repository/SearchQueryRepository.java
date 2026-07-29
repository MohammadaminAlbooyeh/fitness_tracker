package com.ecommerce.search.repository;

import com.ecommerce.search.entity.SearchQuery;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SearchQueryRepository extends JpaRepository<SearchQuery, Long> {
    List<SearchQuery> findByUserId(Long userId);
}
