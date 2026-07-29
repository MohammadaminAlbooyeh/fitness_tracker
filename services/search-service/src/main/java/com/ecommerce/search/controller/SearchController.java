package com.ecommerce.search.controller;

import com.ecommerce.search.entity.SearchQuery;
import com.ecommerce.search.repository.SearchQueryRepository;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/search")
public class SearchController {

    private final SearchQueryRepository repository;

    public SearchController(SearchQueryRepository repository) {
        this.repository = repository;
    }

    @GetMapping("/queries")
    public List<SearchQuery> getQueries(@RequestParam Long userId) {
        return repository.findByUserId(userId);
    }

    @PostMapping("/queries")
    public SearchQuery saveQuery(@RequestBody SearchQuery query) {
        query.setCreatedAt(LocalDateTime.now());
        query.setUpdatedAt(LocalDateTime.now());
        return repository.save(query);
    }
}
