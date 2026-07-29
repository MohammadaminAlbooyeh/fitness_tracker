package com.ecommerce.seller.controller;

import com.ecommerce.seller.entity.Seller;
import com.ecommerce.seller.repository.SellerRepository;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/sellers")
public class SellerController {

    private final SellerRepository repository;

    public SellerController(SellerRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<Seller> getAllActive() {
        return repository.findByIsActiveTrue();
    }

    @GetMapping("/{id}")
    public Seller getById(@PathVariable Long id) {
        return repository.findById(id).orElseThrow();
    }

    @PostMapping
    public Seller create(@RequestBody Seller seller) {
        seller.setCreatedAt(LocalDateTime.now());
        seller.setUpdatedAt(LocalDateTime.now());
        return repository.save(seller);
    }
}
