package com.ecommerce.payment.controller;

import com.ecommerce.payment.dto.PaymentRequest;
import com.ecommerce.payment.dto.PaymentResponse;
import com.ecommerce.payment.service.PaymentService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class PaymentControllerTest {

    @Mock
    private PaymentService service;

    @InjectMocks
    private PaymentController controller;

    @Test
    void getAll_shouldReturnAllPayments() {
        PaymentResponse response = new PaymentResponse();
        response.setId(1L);
        response.setOrderId(1L);
        response.setAmount(new BigDecimal("99.99"));
        response.setStatus("PENDING");
        response.setCurrency("USD");
        response.setPaymentMethod("credit_card");

        when(service.getPaymentsByOrderId(null)).thenReturn(List.of(response));

        List<PaymentResponse> result = controller.getAll();

        assertEquals(1, result.size());
        assertEquals(1L, result.get(0).getId());
    }

    @Test
    void getById_shouldReturnPayment() {
        PaymentResponse response = new PaymentResponse();
        response.setId(1L);
        response.setOrderId(1L);
        response.setAmount(new BigDecimal("99.99"));
        response.setStatus("COMPLETED");

        when(service.getPaymentById(1L)).thenReturn(response);

        PaymentResponse result = controller.getById(1L);

        assertEquals(1L, result.getId());
        assertEquals("COMPLETED", result.getStatus());
    }

    @Test
    void create_shouldReturnCreatedPayment() {
        PaymentRequest request = new PaymentRequest();
        request.setOrderId(1L);
        request.setAmount(new BigDecimal("99.99"));
        request.setCurrency("USD");
        request.setPaymentMethod("credit_card");
        request.setTransactionId("txn_123");

        PaymentResponse response = new PaymentResponse();
        response.setId(1L);
        response.setOrderId(1L);
        response.setAmount(new BigDecimal("99.99"));
        response.setStatus("PENDING");
        response.setCurrency("USD");
        response.setPaymentMethod("credit_card");
        response.setTransactionId("txn_123");

        when(service.createPayment(request)).thenReturn(response);

        PaymentResponse result = controller.create(request);

        assertNotNull(result);
        assertEquals(1L, result.getId());
        assertEquals("PENDING", result.getStatus());
    }

    @Test
    void updateStatus_shouldReturnUpdatedPayment() {
        PaymentResponse response = new PaymentResponse();
        response.setId(1L);
        response.setStatus("COMPLETED");

        when(service.updatePaymentStatus(1L, "COMPLETED")).thenReturn(response);

        PaymentResponse result = controller.updateStatus(1L, "COMPLETED");

        assertEquals("COMPLETED", result.getStatus());
    }
}
