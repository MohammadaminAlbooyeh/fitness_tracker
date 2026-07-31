package com.ecommerce.seller.repository;

import com.ecommerce.seller.entity.Seller;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface SellerRepository extends JpaRepository<Seller, Long> {
    List<Seller> findByIsActiveTrue();
    Optional<Seller> findByUserId(Long userId);
}
