package com.ecommerce.inventory.service;

import com.ecommerce.inventory.dto.InventoryRequest;
import com.ecommerce.inventory.dto.InventoryResponse;
import com.ecommerce.inventory.entity.Inventory;
import com.ecommerce.inventory.event.InventoryEventPublisher;
import com.ecommerce.inventory.repository.InventoryRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class InventoryService {

    private final InventoryRepository repository;
    private final InventoryEventPublisher eventPublisher;

    public InventoryService(InventoryRepository repository, InventoryEventPublisher eventPublisher) {
        this.repository = repository;
        this.eventPublisher = eventPublisher;
    }

    public InventoryResponse createInventory(InventoryRequest request) {
        Optional<Inventory> existing = repository.findByProductId(request.getProductId());
        if (existing.isPresent()) {
            throw new RuntimeException("Inventory for product already exists");
        }

        Inventory inventory = new Inventory();
        inventory.setProductId(request.getProductId());
        inventory.setQuantity(request.getQuantity());
        inventory.setReservedQuantity(0);
        inventory.setPrice(request.getPrice());
        inventory.setCreatedAt(LocalDateTime.now());
        inventory.setUpdatedAt(LocalDateTime.now());

        Inventory saved = repository.save(inventory);
        return mapToResponse(saved);
    }

    public InventoryResponse getInventoryByProductId(Long productId) {
        Inventory inventory = repository.findByProductId(productId)
                .orElseThrow(() -> new RuntimeException("Inventory not found for product"));
        return mapToResponse(inventory);
    }

    public List<InventoryResponse> getAllInventory() {
        return repository.findAll().stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    public InventoryResponse updateQuantity(Long productId, Integer quantityChange) {
        Inventory inventory = repository.findByProductId(productId)
                .orElseThrow(() -> new RuntimeException("Inventory not found for product"));

        int newQuantity = inventory.getQuantity() + quantityChange;
        if (newQuantity < 0) {
            throw new RuntimeException("Insufficient inventory quantity");
        }

        inventory.setQuantity(newQuantity);
        inventory.setUpdatedAt(LocalDateTime.now());
        Inventory updated = repository.save(inventory);
        eventPublisher.publishInventoryUpdated(updated);
        return mapToResponse(updated);
    }

    public InventoryResponse reserveStock(Long productId, Integer quantity) {
        Inventory inventory = repository.findByProductId(productId)
                .orElseThrow(() -> new RuntimeException("Inventory not found for product"));

        int availableQuantity = inventory.getQuantity() - inventory.getReservedQuantity();
        if (availableQuantity < quantity) {
            throw new RuntimeException("Insufficient available stock to reserve");
        }

        inventory.setReservedQuantity(inventory.getReservedQuantity() + quantity);
        inventory.setUpdatedAt(LocalDateTime.now());
        Inventory updated = repository.save(inventory);
        eventPublisher.publishInventoryUpdated(updated);
        return mapToResponse(updated);
    }

    public InventoryResponse releaseStock(Long productId, Integer quantity) {
        Inventory inventory = repository.findByProductId(productId)
                .orElseThrow(() -> new RuntimeException("Inventory not found for product"));

        if (inventory.getReservedQuantity() < quantity) {
            throw new RuntimeException("Cannot release more stock than reserved");
        }

        inventory.setReservedQuantity(inventory.getReservedQuantity() - quantity);
        inventory.setUpdatedAt(LocalDateTime.now());
        Inventory updated = repository.save(inventory);
        eventPublisher.publishInventoryUpdated(updated);
        return mapToResponse(updated);
    }

    private InventoryResponse mapToResponse(Inventory inventory) {
        InventoryResponse response = new InventoryResponse();
        response.setId(inventory.getId());
        response.setProductId(inventory.getProductId());
        response.setQuantity(inventory.getQuantity());
        response.setReservedQuantity(inventory.getReservedQuantity());
        response.setPrice(inventory.getPrice());
        response.setCreatedAt(inventory.getCreatedAt());
        response.setUpdatedAt(inventory.getUpdatedAt());
        return response;
    }
}
