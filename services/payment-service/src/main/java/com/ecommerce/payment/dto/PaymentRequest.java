package com.ecommerce.payment.dto;

import java.math.BigDecimal;

public class PaymentRequest {
    private Long orderId;
    private BigDecimal amount;
    private String currency;
    private String paymentMethod;
    private String transactionId;
}
