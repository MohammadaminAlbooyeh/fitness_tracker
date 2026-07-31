package com.ecommerce.review.controller;

import com.ecommerce.review.dto.ReviewRequest;
import com.ecommerce.review.dto.ReviewResponse;
import com.ecommerce.review.service.ReviewService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ReviewControllerTest {

    @Mock
    private ReviewService service;

    @InjectMocks
    private ReviewController controller;

    @Test
    void getByProduct_shouldReturnList() {
        ReviewResponse response = new ReviewResponse();
        response.setId(1L);
        response.setProductId(1L);
        response.setRating(5);

        when(service.getReviewsByProductId(1L)).thenReturn(List.of(response));

        List<ReviewResponse> result = controller.getByProduct(1L);

        assertEquals(1, result.size());
        assertEquals(5, result.get(0).getRating());
    }

    @Test
    void getByUser_shouldReturnList() {
        ReviewResponse response = new ReviewResponse();
        response.setId(1L);
        response.setUserId(2L);

        when(service.getReviewsByUserId(2L)).thenReturn(List.of(response));

        List<ReviewResponse> result = controller.getByUser(2L);

        assertEquals(1, result.size());
        assertEquals(2L, result.get(0).getUserId());
    }

    @Test
    void create_shouldReturnResponse() {
        ReviewRequest request = new ReviewRequest();
        request.setProductId(1L);
        request.setUserId(2L);
        request.setRating(5);
        request.setComment("Great!");

        ReviewResponse response = new ReviewResponse();
        response.setId(1L);
        response.setProductId(1L);
        response.setRating(5);

        when(service.createReview(request)).thenReturn(response);

        ReviewResponse result = controller.create(request);

        assertNotNull(result);
        assertEquals(1L, result.getId());
    }

    @Test
    void delete_shouldCallService() {
        doNothing().when(service).deleteReview(1L);

        controller.delete(1L);

        verify(service).deleteReview(1L);
    }
}
