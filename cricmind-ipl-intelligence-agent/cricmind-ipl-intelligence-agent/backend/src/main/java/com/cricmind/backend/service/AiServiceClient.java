package com.cricmind.backend.service;

import com.cricmind.backend.dto.ChatDtos.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class AiServiceClient {

    private final WebClient webClient;

    public AiServiceClient(@Value("${ai.service.base-url}") String baseUrl) {
        this.webClient = WebClient.builder().baseUrl(baseUrl).build();
    }

    public ChatResponse chat(ChatRequest request) {
        return webClient.post()
                .uri("/api/agent/chat")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ChatResponse.class)
                .block();
    }

    public Object predict(PredictionRequest request) {
        return webClient.post()
                .uri("/api/predictions/match")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(Object.class)
                .block();
    }
}
