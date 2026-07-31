package com.ecommerce.seller.controller;

import com.ecommerce.seller.dto.SellerRequest;
import com.ecommerce.seller.dto.SellerResponse;
import com.ecommerce.seller.service.SellerService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class SellerControllerTest {

    @Mock
    private SellerService service;

    @InjectMocks
    private SellerController controller;

    @Test
    void getAllActive_shouldReturnList() {
        SellerResponse response = new SellerResponse();
        response.setId(1L);
        response.setStoreName("Test Store");
        response.setIsActive(true);

        when(service.getAllActiveSellers()).thenReturn(List.of(response));

        List<SellerResponse> result = controller.getAllActive();

        assertEquals(1, result.size());
        assertEquals("Test Store", result.get(0).getStoreName());
    }

    @Test
    void getById_shouldReturnSeller() {
        SellerResponse response = new SellerResponse();
        response.setId(1L);
        response.setStoreName("Test Store");

        when(service.getSellerById(1L)).thenReturn(response);

        SellerResponse result = controller.getById(1L);

        assertEquals(1L, result.getId());
        assertEquals("Test Store", result.getStoreName());
    }

    @Test
    void getByUserId_shouldReturnSeller() {
        SellerResponse response = new SellerResponse();
        response.setId(1L);
        response.setUserId(1L);

        when(service.getSellerByUserId(1L)).thenReturn(response);

        SellerResponse result = controller.getByUserId(1L);

        assertEquals(1L, result.getUserId());
    }

    @Test
    void create_shouldReturnResponse() {
        SellerRequest request = new SellerRequest();
        request.setUserId(1L);
        request.setStoreName("New Store");

        SellerResponse response = new SellerResponse();
        response.setId(1L);
        response.setUserId(1L);
        response.setStoreName("New Store");

        when(service.createSeller(request)).thenReturn(response);

        SellerResponse result = controller.create(request);

        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals("New Store", result.getStoreName());
    }

    @Test
    void update_shouldReturnUpdatedResponse() {
        SellerRequest request = new SellerRequest();
        request.setStoreName("Updated Store");

        SellerResponse response = new SellerResponse();
        response.setId(1L);
        response.setStoreName("Updated Store");

        when(service.updateSeller(1L, request)).thenReturn(response);

        SellerResponse result = controller.update(1L, request);

        assertEquals("Updated Store", result.getStoreName());
    }

    @Test
    void deactivate_shouldReturnDeactivatedResponse() {
        SellerResponse response = new SellerResponse();
        response.setId(1L);
        response.setIsActive(false);

        when(service.deactivateSeller(1L)).thenReturn(response);

        SellerResponse result = controller.deactivate(1L);

        assertFalse(result.getIsActive());
    }
}
