package com.ecommerce.inventory.controller;

import com.ecommerce.inventory.dto.InventoryRequest;
import com.ecommerce.inventory.dto.InventoryResponse;
import com.ecommerce.inventory.service.InventoryService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/inventory")
public class InventoryController {

    private final InventoryService service;

    public InventoryController(InventoryService service) {
        this.service = service;
    }

    @GetMapping
    public List<InventoryResponse> getAll() {
        return service.getAllInventory();
    }

    @GetMapping("/product/{productId}")
    public InventoryResponse getByProductId(@PathVariable Long productId) {
        return service.getInventoryByProductId(productId);
    }

    @PostMapping
    public InventoryResponse create(@RequestBody InventoryRequest request) {
        return service.createInventory(request);
    }

    @PutMapping("/{productId}/quantity")
    public InventoryResponse updateQuantity(@PathVariable Long productId, @RequestParam Integer quantityChange) {
        return service.updateQuantity(productId, quantityChange);
    }

    @PostMapping("/{productId}/reserve")
    public InventoryResponse reserveStock(@PathVariable Long productId, @RequestParam Integer quantity) {
        return service.reserveStock(productId, quantity);
    }

    @PostMapping("/{productId}/release")
    public InventoryResponse releaseStock(@PathVariable Long productId, @RequestParam Integer quantity) {
        return service.releaseStock(productId, quantity);
    }
}
