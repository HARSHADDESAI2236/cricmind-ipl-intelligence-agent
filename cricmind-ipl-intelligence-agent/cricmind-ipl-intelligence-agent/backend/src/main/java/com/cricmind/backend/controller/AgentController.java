package com.cricmind.backend.controller;

import com.cricmind.backend.dto.ChatDtos.*;
import com.cricmind.backend.service.AiServiceClient;
import org.springframework.web.bind.annotation.*;

// Spring Boot acts as the secure gateway: it authenticates/validates the
// request, then forwards it to the Python AI service (FastAPI + LangGraph
// agent) which owns the tool-calling, RAG and ML logic.
@RestController
@RequestMapping("/api")
public class AgentController {

    private final AiServiceClient aiServiceClient;

    public AgentController(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    @PostMapping("/agent/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        return aiServiceClient.chat(request);
    }

    @PostMapping("/predictions/match")
    public Object predict(@RequestBody PredictionRequest request) {
        return aiServiceClient.predict(request);
    }
}
