package com.ecommerce.inventory.controller;

import com.ecommerce.inventory.dto.InventoryRequest;
import com.ecommerce.inventory.dto.InventoryResponse;
import com.ecommerce.inventory.service.InventoryService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class InventoryControllerTest {

    @Mock
    private InventoryService service;

    @InjectMocks
    private InventoryController controller;

    @Test
    void getAll_shouldReturnAllInventory() {
        InventoryResponse response = new InventoryResponse();
        response.setId(1L);
        response.setProductId(1L);
        response.setQuantity(100);

        when(service.getAllInventory()).thenReturn(List.of(response));

        List<InventoryResponse> result = controller.getAll();

        assertEquals(1, result.size());
        assertEquals(1L, result.get(0).getId());
    }

    @Test
    void getByProductId_shouldReturnInventory() {
        InventoryResponse response = new InventoryResponse();
        response.setId(1L);
        response.setProductId(1L);
        response.setQuantity(50);

        when(service.getInventoryByProductId(1L)).thenReturn(response);

        InventoryResponse result = controller.getByProductId(1L);

        assertEquals(1L, result.getProductId());
        assertEquals(50, result.getQuantity());
    }

    @Test
    void create_shouldReturnCreatedInventory() {
        InventoryRequest request = new InventoryRequest();
        request.setProductId(1L);
        request.setQuantity(100);
        request.setPrice(new BigDecimal("29.99"));

        InventoryResponse response = new InventoryResponse();
        response.setId(1L);
        response.setProductId(1L);
        response.setQuantity(100);

        when(service.createInventory(request)).thenReturn(response);

        InventoryResponse result = controller.create(request);

        assertNotNull(result);
        assertEquals(1L, result.getId());
    }

    @Test
    void updateQuantity_shouldReturnUpdatedInventory() {
        InventoryResponse response = new InventoryResponse();
        response.setId(1L);
        response.setQuantity(125);

        when(service.updateQuantity(1L, 25)).thenReturn(response);

        InventoryResponse result = controller.updateQuantity(1L, 25);

        assertEquals(125, result.getQuantity());
    }

    @Test
    void reserveStock_shouldReturnReservedInventory() {
        InventoryResponse response = new InventoryResponse();
        response.setId(1L);
        response.setReservedQuantity(30);

        when(service.reserveStock(1L, 30)).thenReturn(response);

        InventoryResponse result = controller.reserveStock(1L, 30);

        assertEquals(30, result.getReservedQuantity());
    }

    @Test
    void releaseStock_shouldReturnReleasedInventory() {
        InventoryResponse response = new InventoryResponse();
        response.setId(1L);
        response.setReservedQuantity(20);

        when(service.releaseStock(1L, 20)).thenReturn(response);

        InventoryResponse result = controller.releaseStock(1L, 20);

        assertEquals(20, result.getReservedQuantity());
    }
}
