package com.cricmind.backend.security;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Field;

import static org.junit.jupiter.api.Assertions.*;

class JwtServiceTest {

    private JwtService jwtService;

    @BeforeEach
    void setUp() throws Exception {
        jwtService = new JwtService();
        setField("secret", "test-secret-key-min-32-characters-long");
        setField("expirationMs", 60_000L);
    }

    @Test
    void generatesTokenThatContainsUsernameAndIsValid() {
        String token = jwtService.generateToken("alice", "USER");

        assertEquals("alice", jwtService.extractUsername(token));
        assertTrue(jwtService.isValid(token));
    }

    @Test
    void rejectsMalformedToken() {
        assertFalse(jwtService.isValid("not-a-jwt"));
    }

    private void setField(String name, Object value) throws Exception {
        Field field = JwtService.class.getDeclaredField(name);
        field.setAccessible(true);
        field.set(jwtService, value);
    }
}
