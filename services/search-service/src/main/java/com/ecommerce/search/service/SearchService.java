package com.ecommerce.search.service;

import com.ecommerce.search.dto.SearchQueryRequest;
import com.ecommerce.search.dto.SearchQueryResponse;
import com.ecommerce.search.entity.SearchQuery;
import com.ecommerce.search.repository.SearchQueryRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class SearchService {

    private final SearchQueryRepository repository;

    public SearchService(SearchQueryRepository repository) {
        this.repository = repository;
    }

    public SearchQueryResponse saveQuery(SearchQueryRequest request) {
        SearchQuery query = new SearchQuery();
        query.setQuery(request.getQuery());
        query.setUserId(request.getUserId());
        query.setCreatedAt(LocalDateTime.now());
        query.setUpdatedAt(LocalDateTime.now());

        SearchQuery saved = repository.save(query);
        return mapToResponse(saved);
    }

    public List<SearchQueryResponse> getQueriesByUserId(Long userId) {
        return repository.findByUserId(userId).stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    public List<SearchQueryResponse> getAllQueries() {
        return repository.findAll().stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    private SearchQueryResponse mapToResponse(SearchQuery query) {
        SearchQueryResponse response = new SearchQueryResponse();
        response.setId(query.getId());
        response.setQuery(query.getQuery());
        response.setUserId(query.getUserId());
        response.setCreatedAt(query.getCreatedAt());
        response.setUpdatedAt(query.getUpdatedAt());
        return response;
    }
}
