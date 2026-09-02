package com.cricmind.backend.exception;

import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class GlobalExceptionHandlerTest {

    @Test
    void returnsInternalErrorPayloadForUnexpectedException() {
        ResponseEntity<Map<String, String>> response =
                new GlobalExceptionHandler().handleGeneric(new IllegalStateException("boom"));

        assertEquals(500, response.getStatusCode().value());
        assertEquals("Internal error", response.getBody().get("error"));
        assertEquals("boom", response.getBody().get("message"));
    }
}
