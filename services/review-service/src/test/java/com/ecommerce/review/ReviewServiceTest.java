package com.ecommerce.review.service;

import com.ecommerce.review.dto.ReviewRequest;
import com.ecommerce.review.dto.ReviewResponse;
import com.ecommerce.review.entity.Review;
import com.ecommerce.review.repository.ReviewRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ReviewServiceTest {

    @Mock
    private ReviewRepository repository;

    @InjectMocks
    private ReviewService service;

    private ReviewRequest request;

    @BeforeEach
    void setUp() {
        request = new ReviewRequest();
        request.setProductId(1L);
        request.setUserId(2L);
        request.setRating(5);
        request.setComment("Great product!");
    }

    @Test
    void createReview_shouldCreateAndReturnResponse() {
        Review saved = new Review();
        saved.setId(1L);
        saved.setProductId(1L);
        saved.setUserId(2L);
        saved.setRating(5);
        saved.setComment("Great product!");

        when(repository.save(any(Review.class))).thenReturn(saved);

        ReviewResponse response = service.createReview(request);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals(1L, response.getProductId());
        assertEquals(2L, response.getUserId());
        assertEquals(5, response.getRating());
        assertEquals("Great product!", response.getComment());
        verify(repository).save(any(Review.class));
    }

    @Test
    void getReviewsByProductId_shouldReturnList() {
        Review review1 = new Review();
        review1.setId(1L);
        review1.setProductId(1L);
        review1.setRating(5);

        Review review2 = new Review();
        review2.setId(2L);
        review2.setProductId(1L);
        review2.setRating(4);

        when(repository.findByProductId(1L)).thenReturn(List.of(review1, review2));

        List<ReviewResponse> responses = service.getReviewsByProductId(1L);

        assertEquals(2, responses.size());
        assertEquals(5, responses.get(0).getRating());
        assertEquals(4, responses.get(1).getRating());
    }

    @Test
    void getReviewsByUserId_shouldReturnList() {
        Review review1 = new Review();
        review1.setId(1L);
        review1.setUserId(2L);
        review1.setRating(5);

        when(repository.findByUserId(2L)).thenReturn(List.of(review1));

        List<ReviewResponse> responses = service.getReviewsByUserId(2L);

        assertEquals(1, responses.size());
        assertEquals(2L, responses.get(0).getUserId());
    }

    @Test
    void deleteReview_shouldDeleteById() {
        service.deleteReview(1L);
        verify(repository).deleteById(1L);
    }
}
