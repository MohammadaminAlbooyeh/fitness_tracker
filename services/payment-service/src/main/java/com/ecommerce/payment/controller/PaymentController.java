package com.ecommerce.payment.controller;

import com.ecommerce.payment.dto.PaymentRequest;
import com.ecommerce.payment.dto.PaymentResponse;
import com.ecommerce.payment.service.PaymentService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/payments")
public class PaymentController {

    private final PaymentService service;

    public PaymentController(PaymentService service) {
        this.service = service;
    }

    @GetMapping("/health")
    public java.util.Map<String, String> health() {
        return java.util.Map.of("status", "healthy", "service", "payment-service");
    }

    @GetMapping
    public List<PaymentResponse> getAll() {
        return service.getPaymentsByOrderId(null);
    }

    @GetMapping("/{id}")
    public PaymentResponse getById(@PathVariable Long id) {
        return service.getPaymentById(id);
    }

    @PostMapping
    public PaymentResponse create(@RequestBody PaymentRequest request) {
        return service.createPayment(request);
    }

    @PutMapping("/{id}/status")
    public PaymentResponse updateStatus(@PathVariable Long id, @RequestParam String status) {
        return service.updatePaymentStatus(id, status);
    }

    @GetMapping("/order/{orderId}")
    public List<PaymentResponse> getByOrderId(@PathVariable Long orderId) {
        return service.getPaymentsByOrderId(orderId);
    }
}
