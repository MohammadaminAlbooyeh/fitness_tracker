package com.ecommerce.seller.service;

import com.ecommerce.seller.dto.SellerRequest;
import com.ecommerce.seller.dto.SellerResponse;
import com.ecommerce.seller.entity.Seller;
import com.ecommerce.seller.repository.SellerRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class SellerServiceTest {

    @Mock
    private SellerRepository repository;

    @InjectMocks
    private SellerService service;

    private SellerRequest request;

    @BeforeEach
    void setUp() {
        request = new SellerRequest();
        request.setUserId(1L);
        request.setStoreName("Test Store");
        request.setDescription("A test store");
    }

    @Test
    void createSeller_shouldCreateNewSeller() {
        when(repository.findByUserId(1L)).thenReturn(Optional.empty());

        Seller saved = new Seller();
        saved.setId(1L);
        saved.setUserId(1L);
        saved.setStoreName("Test Store");
        saved.setDescription("A test store");
        saved.setIsActive(true);

        when(repository.save(any(Seller.class))).thenReturn(saved);

        SellerResponse response = service.createSeller(request);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals(1L, response.getUserId());
        assertEquals("Test Store", response.getStoreName());
        assertTrue(response.getIsActive());
        verify(repository).save(any(Seller.class));
    }

    @Test
    void createSeller_shouldThrowWhenSellerExists() {
        Seller existing = new Seller();
        existing.setId(99L);

        when(repository.findByUserId(1L)).thenReturn(Optional.of(existing));

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.createSeller(request));
        assertEquals("Seller already exists for user", exception.getMessage());
    }

    @Test
    void getSellerById_shouldReturnSeller() {
        Seller seller = new Seller();
        seller.setId(1L);
        seller.setUserId(1L);
        seller.setStoreName("Test Store");
        seller.setIsActive(true);

        when(repository.findById(1L)).thenReturn(Optional.of(seller));

        SellerResponse response = service.getSellerById(1L);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("Test Store", response.getStoreName());
    }

    @Test
    void getSellerById_shouldThrowWhenNotFound() {
        when(repository.findById(999L)).thenReturn(Optional.empty());

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.getSellerById(999L));
        assertEquals("Seller not found", exception.getMessage());
    }

    @Test
    void getAllActiveSellers_shouldReturnActiveOnly() {
        Seller seller1 = new Seller();
        seller1.setId(1L);
        seller1.setStoreName("Store 1");
        seller1.setIsActive(true);

        Seller seller2 = new Seller();
        seller2.setId(2L);
        seller2.setStoreName("Store 2");
        seller2.setIsActive(true);

        when(repository.findByIsActiveTrue()).thenReturn(List.of(seller1, seller2));

        List<SellerResponse> responses = service.getAllActiveSellers();

        assertEquals(2, responses.size());
        assertTrue(responses.get(0).getIsActive());
    }

    @Test
    void getSellerByUserId_shouldReturnSeller() {
        Seller seller = new Seller();
        seller.setId(1L);
        seller.setUserId(1L);
        seller.setStoreName("Test Store");

        when(repository.findByUserId(1L)).thenReturn(Optional.of(seller));

        SellerResponse response = service.getSellerByUserId(1L);

        assertNotNull(response);
        assertEquals(1L, response.getUserId());
        assertEquals("Test Store", response.getStoreName());
    }

    @Test
    void getSellerByUserId_shouldThrowWhenNotFound() {
        when(repository.findByUserId(999L)).thenReturn(Optional.empty());

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.getSellerByUserId(999L));
        assertEquals("Seller not found for user", exception.getMessage());
    }

    @Test
    void updateSeller_shouldUpdateSeller() {
        Seller seller = new Seller();
        seller.setId(1L);
        seller.setUserId(1L);
        seller.setStoreName("Old Name");
        seller.setDescription("Old description");

        when(repository.findById(1L)).thenReturn(Optional.of(seller));
        when(repository.save(any(Seller.class))).thenReturn(seller);

        SellerResponse response = service.updateSeller(1L, request);

        assertEquals("Test Store", response.getStoreName());
        assertEquals("A test store", response.getDescription());
        verify(repository).save(seller);
    }

    @Test
    void updateSeller_shouldThrowWhenNotFound() {
        when(repository.findById(999L)).thenReturn(Optional.empty());

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.updateSeller(999L, request));
        assertEquals("Seller not found", exception.getMessage());
    }

    @Test
    void deactivateSeller_shouldSetInactive() {
        Seller seller = new Seller();
        seller.setId(1L);
        seller.setUserId(1L);
        seller.setStoreName("Test Store");
        seller.setIsActive(true);

        when(repository.findById(1L)).thenReturn(Optional.of(seller));
        when(repository.save(any(Seller.class))).thenReturn(seller);

        SellerResponse response = service.deactivateSeller(1L);

        assertFalse(response.getIsActive());
        verify(repository).save(seller);
    }

    @Test
    void deactivateSeller_shouldThrowWhenNotFound() {
        when(repository.findById(999L)).thenReturn(Optional.empty());

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.deactivateSeller(999L));
        assertEquals("Seller not found", exception.getMessage());
    }
}
