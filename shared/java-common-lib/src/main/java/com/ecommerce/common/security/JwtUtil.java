package com.ecommerce.common.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.JwtParser;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;

/**
 * Utility for validating JWT bearer tokens issued by the platform.
 *
 * <p>Tokens are HS256-signed with a shared secret so they are interoperable with
 * the Python services (which mint the tokens at login). Configure the signing
 * secret via the {@code jwt.secret} property (or {@code JWT_SECRET} env var).
 */
public class JwtUtil {

    private final SecretKey key;
    private final JwtParser parser;

    public JwtUtil(String secret) {
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.parser = Jwts.parser().verifyWith(this.key).build();
    }

    /** Returns the JWT subject (typically the user email) carried by the token. */
    public String extractUsername(String token) {
        return parseClaims(token).getSubject();
    }

    /** Parses and validates the signature/expiry of a token. Throws on invalid tokens. */
    public Claims parseClaims(String token) {
        return parser.parseSignedClaims(token).getPayload();
    }

    /** Returns true when the token has a valid signature and has not expired. */
    public boolean isValidToken(String token) {
        try {
            parseClaims(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
}