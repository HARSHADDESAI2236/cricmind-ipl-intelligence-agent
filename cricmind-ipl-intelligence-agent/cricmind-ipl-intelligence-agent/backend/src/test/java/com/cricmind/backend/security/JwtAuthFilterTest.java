package com.cricmind.backend.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.core.context.SecurityContextHolder;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class JwtAuthFilterTest {

    @AfterEach
    void clearSecurityContext() {
        SecurityContextHolder.clearContext();
    }

    @Test
    void authenticatesRequestWithValidBearerToken() throws Exception {
        JwtService jwtService = mock(JwtService.class);
        when(jwtService.isValid("token")).thenReturn(true);
        when(jwtService.extractUsername("token")).thenReturn("alice");
        JwtAuthFilter filter = new JwtAuthFilter(jwtService);
        HttpServletRequest request = mock(HttpServletRequest.class);
        FilterChain chain = mock(FilterChain.class);
        when(request.getHeader("Authorization")).thenReturn("Bearer token");

        filter.doFilterInternal(request, mock(HttpServletResponse.class), chain);

        assertEquals("alice", SecurityContextHolder.getContext().getAuthentication().getName());
        verify(chain).doFilter(eq(request), any(HttpServletResponse.class));
    }

    @Test
    void continuesWithoutAuthenticationWhenHeaderIsMissingOrInvalid() throws Exception {
        JwtService jwtService = mock(JwtService.class);
        when(jwtService.isValid("bad")).thenReturn(false);
        JwtAuthFilter filter = new JwtAuthFilter(jwtService);
        HttpServletRequest request = mock(HttpServletRequest.class);
        FilterChain chain = mock(FilterChain.class);
        when(request.getHeader("Authorization")).thenReturn("Bearer bad");

        filter.doFilterInternal(request, mock(HttpServletResponse.class), chain);

        assertNull(SecurityContextHolder.getContext().getAuthentication());
        verify(chain).doFilter(eq(request), any(HttpServletResponse.class));
        verify(jwtService, never()).extractUsername(anyString());
    }
}
