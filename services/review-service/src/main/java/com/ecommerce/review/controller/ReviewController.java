package com.ecommerce.review.controller;

import com.ecommerce.review.dto.ReviewRequest;
import com.ecommerce.review.dto.ReviewResponse;
import com.ecommerce.review.service.ReviewService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/reviews")
public class ReviewController {

    private final ReviewService service;

    public ReviewController(ReviewService service) {
        this.service = service;
    }

    @GetMapping("/product/{productId}")
    public List<ReviewResponse> getByProduct(@PathVariable Long productId) {
        return service.getReviewsByProductId(productId);
    }

    @GetMapping("/user/{userId}")
    public List<ReviewResponse> getByUser(@PathVariable Long userId) {
        return service.getReviewsByUserId(userId);
    }

    @PostMapping
    public ReviewResponse create(@RequestBody ReviewRequest request) {
        return service.createReview(request);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        service.deleteReview(id);
    }
}
