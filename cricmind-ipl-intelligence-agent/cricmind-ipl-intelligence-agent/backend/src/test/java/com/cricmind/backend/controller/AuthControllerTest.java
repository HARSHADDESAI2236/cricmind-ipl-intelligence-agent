package com.cricmind.backend.controller;

import com.cricmind.backend.dto.AuthDtos.*;
import com.cricmind.backend.model.User;
import com.cricmind.backend.repository.UserRepository;
import com.cricmind.backend.security.JwtService;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

class AuthControllerTest {

    private final UserRepository userRepository = mock(UserRepository.class);
    private final PasswordEncoder passwordEncoder = mock(PasswordEncoder.class);
    private final JwtService jwtService = mock(JwtService.class);
    private final AuthController controller = new AuthController(userRepository, passwordEncoder, jwtService);

    @Test
    void registersNewUserAndReturnsToken() {
        RegisterRequest request = new RegisterRequest("alice", "alice@example.com", "password");
        when(userRepository.existsByUsername("alice")).thenReturn(false);
        when(passwordEncoder.encode("password")).thenReturn("hashed");
        when(jwtService.generateToken("alice", "USER")).thenReturn("token");

        ResponseEntity<?> response = controller.register(request);

        assertEquals(200, response.getStatusCode().value());
        assertEquals("token", ((AuthResponse) response.getBody()).token());
        verify(userRepository).save(argThat(user -> user.getUsername().equals("alice")
                && user.getPasswordHash().equals("hashed")
                && user.getRole().equals("USER")));
    }

    @Test
    void rejectsDuplicateUsername() {
        when(userRepository.existsByUsername("alice")).thenReturn(true);

        ResponseEntity<?> response = controller.register(
                new RegisterRequest("alice", "alice@example.com", "password"));

        assertEquals(400, response.getStatusCode().value());
        assertEquals("Username already taken", response.getBody());
        verify(userRepository, never()).save(any());
    }

    @Test
    void logsInWithValidCredentials() {
        User user = User.builder().username("alice").passwordHash("hashed").role("USER").build();
        when(userRepository.findByUsername("alice")).thenReturn(Optional.of(user));
        when(passwordEncoder.matches("password", "hashed")).thenReturn(true);
        when(jwtService.generateToken("alice", "USER")).thenReturn("token");

        ResponseEntity<?> response = controller.login(new LoginRequest("alice", "password"));

        assertEquals(200, response.getStatusCode().value());
        assertEquals("alice", ((AuthResponse) response.getBody()).username());
    }

    @Test
    void rejectsMissingOrIncorrectCredentials() {
        when(userRepository.findByUsername("alice")).thenReturn(Optional.empty());

        ResponseEntity<?> response = controller.login(new LoginRequest("alice", "password"));

        assertEquals(401, response.getStatusCode().value());
        assertEquals("Invalid credentials", response.getBody());
    }
}
