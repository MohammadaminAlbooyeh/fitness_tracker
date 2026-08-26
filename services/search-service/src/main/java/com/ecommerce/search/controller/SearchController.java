package com.ecommerce.search.controller;

import com.ecommerce.search.dto.SearchQueryRequest;
import com.ecommerce.search.dto.SearchQueryResponse;
import com.ecommerce.search.service.SearchService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/search")
public class SearchController {

    private final SearchService service;

    public SearchController(SearchService service) {
        this.service = service;
    }

    @GetMapping("/health")
    public java.util.Map<String, String> health() {
        return java.util.Map.of("status", "healthy", "service", "search-service");
    }

    @GetMapping("/queries")
    public List<SearchQueryResponse> getQueries(@RequestParam Long userId) {
        return service.getQueriesByUserId(userId);
    }

    @PostMapping("/queries")
    public SearchQueryResponse saveQuery(@RequestBody SearchQueryRequest request) {
        return service.saveQuery(request);
    }

    @GetMapping("/queries/all")
    public List<SearchQueryResponse> getAllQueries() {
        return service.getAllQueries();
    }
}
