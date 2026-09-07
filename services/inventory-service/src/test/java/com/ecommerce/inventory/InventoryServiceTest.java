package com.ecommerce.inventory.service;

import com.ecommerce.inventory.dto.InventoryRequest;
import com.ecommerce.inventory.dto.InventoryResponse;
import com.ecommerce.inventory.entity.Inventory;
import com.ecommerce.inventory.event.InventoryEventPublisher;
import com.ecommerce.inventory.repository.InventoryRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class InventoryServiceTest {

    @Mock
    private InventoryRepository repository;

    @Mock
    private InventoryEventPublisher eventPublisher;

    @InjectMocks
    private InventoryService service;

    private InventoryRequest request;

    @BeforeEach
    void setUp() {
        request = new InventoryRequest();
        request.setProductId(1L);
        request.setQuantity(100);
        request.setPrice(new BigDecimal("29.99"));
    }

    @Test
    void createInventory_shouldCreateNewInventory() {
        when(repository.findByProductId(1L)).thenReturn(Optional.empty());

        Inventory saved = new Inventory();
        saved.setId(1L);
        saved.setProductId(1L);
        saved.setQuantity(100);
        saved.setReservedQuantity(0);
        saved.setPrice(new BigDecimal("29.99"));

        when(repository.save(any(Inventory.class))).thenReturn(saved);

        InventoryResponse response = service.createInventory(request);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals(1L, response.getProductId());
        assertEquals(100, response.getQuantity());
        assertEquals(0, response.getReservedQuantity());
        verify(repository).save(any(Inventory.class));
    }

    @Test
    void createInventory_shouldThrowWhenExists() {
        Inventory existing = new Inventory();
        existing.setId(99L);

        when(repository.findByProductId(1L)).thenReturn(Optional.of(existing));

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.createInventory(request));
        assertEquals("Inventory for product already exists", exception.getMessage());
    }

    @Test
    void getInventoryByProductId_shouldReturnInventory() {
        Inventory inventory = new Inventory();
        inventory.setId(1L);
        inventory.setProductId(1L);
        inventory.setQuantity(50);
        inventory.setReservedQuantity(10);
        inventory.setPrice(new BigDecimal("19.99"));

        when(repository.findByProductId(1L)).thenReturn(Optional.of(inventory));

        InventoryResponse response = service.getInventoryByProductId(1L);

        assertNotNull(response);
        assertEquals(50, response.getQuantity());
        assertEquals(10, response.getReservedQuantity());
    }

    @Test
    void getInventoryByProductId_shouldThrowWhenNotFound() {
        when(repository.findByProductId(999L)).thenReturn(Optional.empty());

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.getInventoryByProductId(999L));
        assertEquals("Inventory not found for product", exception.getMessage());
    }

    @Test
    void getAllInventory_shouldReturnAll() {
        Inventory inv1 = new Inventory();
        inv1.setId(1L);
        inv1.setProductId(1L);
        inv1.setQuantity(100);

        Inventory inv2 = new Inventory();
        inv2.setId(2L);
        inv2.setProductId(2L);
        inv2.setQuantity(200);

        when(repository.findAll()).thenReturn(List.of(inv1, inv2));

        List<InventoryResponse> responses = service.getAllInventory();

        assertEquals(2, responses.size());
    }

    @Test
    void updateQuantity_shouldUpdateQuantity() {
        Inventory inventory = new Inventory();
        inventory.setId(1L);
        inventory.setProductId(1L);
        inventory.setQuantity(50);
        inventory.setReservedQuantity(0);

        when(repository.findByProductId(1L)).thenReturn(Optional.of(inventory));
        when(repository.save(any(Inventory.class))).thenReturn(inventory);

        InventoryResponse response = service.updateQuantity(1L, 25);

        assertEquals(75, response.getQuantity());
        verify(repository).save(inventory);
    }

    @Test
    void updateQuantity_shouldThrowWhenInsufficient() {
        Inventory inventory = new Inventory();
        inventory.setId(1L);
        inventory.setProductId(1L);
        inventory.setQuantity(10);
        inventory.setReservedQuantity(0);

        when(repository.findByProductId(1L)).thenReturn(Optional.of(inventory));

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.updateQuantity(1L, -20));
        assertEquals("Insufficient inventory quantity", exception.getMessage());
    }

    @Test
    void reserveStock_shouldReserve() {
        Inventory inventory = new Inventory();
        inventory.setId(1L);
        inventory.setProductId(1L);
        inventory.setQuantity(100);
        inventory.setReservedQuantity(0);

        when(repository.findByProductId(1L)).thenReturn(Optional.of(inventory));
        when(repository.save(any(Inventory.class))).thenReturn(inventory);

        InventoryResponse response = service.reserveStock(1L, 30);

        assertEquals(30, response.getReservedQuantity());
        verify(repository).save(inventory);
    }

    @Test
    void reserveStock_shouldThrowWhenInsufficientStock() {
        Inventory inventory = new Inventory();
        inventory.setId(1L);
        inventory.setProductId(1L);
        inventory.setQuantity(20);
        inventory.setReservedQuantity(15);

        when(repository.findByProductId(1L)).thenReturn(Optional.of(inventory));

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.reserveStock(1L, 10));
        assertEquals("Insufficient available stock to reserve", exception.getMessage());
    }

    @Test
    void releaseStock_shouldRelease() {
        Inventory inventory = new Inventory();
        inventory.setId(1L);
        inventory.setProductId(1L);
        inventory.setQuantity(100);
        inventory.setReservedQuantity(50);

        when(repository.findByProductId(1L)).thenReturn(Optional.of(inventory));
        when(repository.save(any(Inventory.class))).thenReturn(inventory);

        InventoryResponse response = service.releaseStock(1L, 20);

        assertEquals(30, response.getReservedQuantity());
        verify(repository).save(inventory);
    }

    @Test
    void releaseStock_shouldThrowWhenNotEnoughReserved() {
        Inventory inventory = new Inventory();
        inventory.setId(1L);
        inventory.setProductId(1L);
        inventory.setQuantity(100);
        inventory.setReservedQuantity(10);

        when(repository.findByProductId(1L)).thenReturn(Optional.of(inventory));

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.releaseStock(1L, 20));
        assertEquals("Cannot release more stock than reserved", exception.getMessage());
    }
}
