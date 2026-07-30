package com.ecommerce.payment.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class PaymentResponse {
    private Long id;
    private Long orderId;
    private BigDecimal amount;
    private String currency;
    private String status;
    private String paymentMethod;
    private String transactionId;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
