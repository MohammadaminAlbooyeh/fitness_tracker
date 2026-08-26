package com.ecommerce.common.security;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.junit.jupiter.api.Test;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class JwtUtilTest {

    private static final String SECRET = "unit-test-common-lib-secret-key-1234567890";
    private final JwtUtil jwtUtil = new JwtUtil(SECRET);

    private String createToken(String subject) {
        SecretKey key = Keys.hmacShaKeyFor(SECRET.getBytes(StandardCharsets.UTF_8));
        return Jwts.builder()
                .subject(subject)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + 60_000))
                .signWith(key)
                .compact();
    }

    @Test
    void isValidToken_shouldAcceptValidToken() {
        assertTrue(jwtUtil.isValidToken(createToken("user@example.com")));
    }

    @Test
    void extractUsername_shouldReturnSubject() {
        assertEquals("user@example.com", jwtUtil.extractUsername(createToken("user@example.com")));
    }

    @Test
    void isValidToken_shouldRejectGarbage() {
        assertFalse(jwtUtil.isValidToken("not-a-valid-token"));
    }

    @Test
    void isValidToken_shouldRejectWrongSecret() {
        String token = Jwts.builder()
                .subject("user@example.com")
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + 60_000))
                .signWith(Keys.hmacShaKeyFor("a-different-secret-that-is-long-enough-123456".getBytes(StandardCharsets.UTF_8)))
                .compact();
        assertFalse(jwtUtil.isValidToken(token));
    }
}