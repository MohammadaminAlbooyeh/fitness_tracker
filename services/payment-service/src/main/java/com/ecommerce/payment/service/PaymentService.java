package com.ecommerce.payment.service;

import com.ecommerce.payment.dto.PaymentRequest;
import com.ecommerce.payment.dto.PaymentResponse;
import com.ecommerce.payment.entity.Payment;
import com.ecommerce.payment.repository.PaymentRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class PaymentService {

    private final PaymentRepository repository;

    public PaymentService(PaymentRepository repository) {
        this.repository = repository;
    }

    public PaymentResponse createPayment(PaymentRequest request) {
        Payment payment = new Payment();
        payment.setOrderId(request.getOrderId());
        payment.setAmount(request.getAmount());
        payment.setCurrency(request.getCurrency());
        payment.setPaymentMethod(request.getPaymentMethod());
        payment.setTransactionId(request.getTransactionId());
        payment.setStatus("PENDING");
        payment.setCreatedAt(LocalDateTime.now());
        payment.setUpdatedAt(LocalDateTime.now());

        Payment saved = repository.save(payment);
        return mapToResponse(saved);
    }

    public PaymentResponse getPaymentById(Long id) {
        Payment payment = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Payment not found"));
        return mapToResponse(payment);
    }

    public List<PaymentResponse> getPaymentsByOrderId(Long orderId) {
        return repository.findByOrderId(orderId).stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    public PaymentResponse updatePaymentStatus(Long id, String status) {
        Payment payment = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Payment not found"));
        payment.setStatus(status);
        payment.setUpdatedAt(LocalDateTime.now());
        Payment updated = repository.save(payment);
        return mapToResponse(updated);
    }

    private PaymentResponse mapToResponse(Payment payment) {
        PaymentResponse response = new PaymentResponse();
        response.setId(payment.getId());
        response.setOrderId(payment.getOrderId());
        response.setAmount(payment.getAmount());
        response.setCurrency(payment.getCurrency());
        response.setStatus(payment.getStatus());
        response.setPaymentMethod(payment.getPaymentMethod());
        response.setTransactionId(payment.getTransactionId());
        response.setCreatedAt(payment.getCreatedAt());
        response.setUpdatedAt(payment.getUpdatedAt());
        return response;
    }
}
