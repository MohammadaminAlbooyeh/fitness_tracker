package com.ecommerce.payment.service;

import com.ecommerce.payment.dto.PaymentRequest;
import com.ecommerce.payment.dto.PaymentResponse;
import com.ecommerce.payment.entity.Payment;
import com.ecommerce.payment.event.PaymentEventPublisher;
import com.ecommerce.payment.repository.PaymentRepository;
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
class PaymentServiceTest {

    @Mock
    private PaymentRepository repository;

    @Mock
    private PaymentEventPublisher eventPublisher;

    @InjectMocks
    private PaymentService service;

    private PaymentRequest request;

    @BeforeEach
    void setUp() {
        request = new PaymentRequest();
        request.setOrderId(1L);
        request.setAmount(new BigDecimal("99.99"));
        request.setCurrency("USD");
        request.setPaymentMethod("credit_card");
        request.setTransactionId("txn_123");
    }

    @Test
    void createPayment_shouldCreatePaymentWithPendingStatus() {
        Payment savedPayment = new Payment();
        savedPayment.setId(1L);
        savedPayment.setOrderId(request.getOrderId());
        savedPayment.setAmount(request.getAmount());
        savedPayment.setCurrency(request.getCurrency());
        savedPayment.setPaymentMethod(request.getPaymentMethod());
        savedPayment.setTransactionId(request.getTransactionId());
        savedPayment.setStatus("PENDING");

        when(repository.save(any(Payment.class))).thenReturn(savedPayment);

        PaymentResponse response = service.createPayment(request);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("PENDING", response.getStatus());
        assertEquals(request.getOrderId(), response.getOrderId());
        verify(repository).save(any(Payment.class));
    }

    @Test
    void getPaymentById_shouldReturnPayment() {
        Payment payment = new Payment();
        payment.setId(1L);
        payment.setOrderId(1L);
        payment.setAmount(new BigDecimal("99.99"));
        payment.setStatus("COMPLETED");

        when(repository.findById(1L)).thenReturn(Optional.of(payment));

        PaymentResponse response = service.getPaymentById(1L);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("COMPLETED", response.getStatus());
    }

    @Test
    void getPaymentById_shouldThrowWhenNotFound() {
        when(repository.findById(999L)).thenReturn(Optional.empty());

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.getPaymentById(999L));
        assertEquals("Payment not found", exception.getMessage());
    }

    @Test
    void getPaymentsByOrderId_shouldReturnList() {
        Payment payment1 = new Payment();
        payment1.setId(1L);
        payment1.setOrderId(1L);
        payment1.setStatus("COMPLETED");

        Payment payment2 = new Payment();
        payment2.setId(2L);
        payment2.setOrderId(1L);
        payment2.setStatus("PENDING");

        when(repository.findByOrderId(1L)).thenReturn(List.of(payment1, payment2));

        List<PaymentResponse> responses = service.getPaymentsByOrderId(1L);

        assertEquals(2, responses.size());
        assertEquals(1L, responses.get(0).getId());
        assertEquals(2L, responses.get(1).getId());
    }

    @Test
    void updatePaymentStatus_shouldUpdateStatus() {
        Payment payment = new Payment();
        payment.setId(1L);
        payment.setOrderId(1L);
        payment.setStatus("PENDING");

        when(repository.findById(1L)).thenReturn(Optional.of(payment));
        when(repository.save(any(Payment.class))).thenReturn(payment);

        PaymentResponse response = service.updatePaymentStatus(1L, "COMPLETED");

        assertNotNull(response);
        assertEquals("COMPLETED", response.getStatus());
        verify(repository).save(payment);
    }

    @Test
    void updatePaymentStatus_shouldThrowWhenNotFound() {
        when(repository.findById(999L)).thenReturn(Optional.empty());

        RuntimeException exception = assertThrows(RuntimeException.class,
                () -> service.updatePaymentStatus(999L, "COMPLETED"));
        assertEquals("Payment not found", exception.getMessage());
    }
}
