package com.cricmind.backend.dto;

import java.util.List;
import java.util.Map;

public class ChatDtos {

    public record ChatRequest(
            String sessionId,
            String message
    ) {}

    public record ChatResponse(
            String answer,
            List<String> toolsUsed,
            List<Map<String, Object>> sources,
            Double confidence
    ) {}

    public record PredictionRequest(
            Long matchId,
            String team1,
            String team2,
            String venue
    ) {}
}
