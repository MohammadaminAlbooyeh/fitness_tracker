package com.ecommerce.seller.service;

import com.ecommerce.seller.dto.SellerRequest;
import com.ecommerce.seller.dto.SellerResponse;
import com.ecommerce.seller.entity.Seller;
import com.ecommerce.seller.repository.SellerRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class SellerService {

    private final SellerRepository repository;

    public SellerService(SellerRepository repository) {
        this.repository = repository;
    }

    public SellerResponse createSeller(SellerRequest request) {
        Optional<Seller> existing = repository.findByUserId(request.getUserId());
        if (existing.isPresent()) {
            throw new RuntimeException("Seller already exists for user");
        }

        Seller seller = new Seller();
        seller.setUserId(request.getUserId());
        seller.setStoreName(request.getStoreName());
        seller.setDescription(request.getDescription());
        seller.setIsActive(true);
        seller.setCreatedAt(LocalDateTime.now());
        seller.setUpdatedAt(LocalDateTime.now());

        Seller saved = repository.save(seller);
        return mapToResponse(saved);
    }

    public SellerResponse getSellerById(Long id) {
        Seller seller = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Seller not found"));
        return mapToResponse(seller);
    }

    public List<SellerResponse> getAllActiveSellers() {
        return repository.findByIsActiveTrue().stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    public SellerResponse getSellerByUserId(Long userId) {
        Seller seller = repository.findByUserId(userId)
                .orElseThrow(() -> new RuntimeException("Seller not found for user"));
        return mapToResponse(seller);
    }

    public SellerResponse updateSeller(Long id, SellerRequest request) {
        Seller seller = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Seller not found"));

        seller.setStoreName(request.getStoreName());
        seller.setDescription(request.getDescription());
        seller.setUpdatedAt(LocalDateTime.now());

        Seller updated = repository.save(seller);
        return mapToResponse(updated);
    }

    public SellerResponse deactivateSeller(Long id) {
        Seller seller = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Seller not found"));

        seller.setIsActive(false);
        seller.setUpdatedAt(LocalDateTime.now());

        Seller updated = repository.save(seller);
        return mapToResponse(updated);
    }

    private SellerResponse mapToResponse(Seller seller) {
        SellerResponse response = new SellerResponse();
        response.setId(seller.getId());
        response.setUserId(seller.getUserId());
        response.setStoreName(seller.getStoreName());
        response.setDescription(seller.getDescription());
        response.setIsActive(seller.getIsActive());
        response.setCreatedAt(seller.getCreatedAt());
        response.setUpdatedAt(seller.getUpdatedAt());
        return response;
    }
}
