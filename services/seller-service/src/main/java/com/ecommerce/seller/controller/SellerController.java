package com.ecommerce.seller.controller;

import com.ecommerce.seller.dto.SellerRequest;
import com.ecommerce.seller.dto.SellerResponse;
import com.ecommerce.seller.service.SellerService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/sellers")
public class SellerController {

    private final SellerService service;

    public SellerController(SellerService service) {
        this.service = service;
    }

    @GetMapping("/health")
    public java.util.Map<String, String> health() {
        return java.util.Map.of("status", "healthy", "service", "seller-service");
    }

    @GetMapping
    public List<SellerResponse> getAllActive() {
        return service.getAllActiveSellers();
    }

    @GetMapping("/{id}")
    public SellerResponse getById(@PathVariable Long id) {
        return service.getSellerById(id);
    }

    @GetMapping("/user/{userId}")
    public SellerResponse getByUserId(@PathVariable Long userId) {
        return service.getSellerByUserId(userId);
    }

    @PostMapping
    public SellerResponse create(@RequestBody SellerRequest request) {
        return service.createSeller(request);
    }

    @PutMapping("/{id}")
    public SellerResponse update(@PathVariable Long id, @RequestBody SellerRequest request) {
        return service.updateSeller(id, request);
    }

    @DeleteMapping("/{id}")
    public SellerResponse deactivate(@PathVariable Long id) {
        return service.deactivateSeller(id);
    }
}
