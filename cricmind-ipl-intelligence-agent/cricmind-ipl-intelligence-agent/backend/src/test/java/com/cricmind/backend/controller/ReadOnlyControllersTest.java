package com.cricmind.backend.controller;

import com.cricmind.backend.dto.ChatDtos.*;
import com.cricmind.backend.model.Match;
import com.cricmind.backend.model.Player;
import com.cricmind.backend.model.Team;
import com.cricmind.backend.repository.MatchRepository;
import com.cricmind.backend.repository.PlayerRepository;
import com.cricmind.backend.service.AiServiceClient;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class ReadOnlyControllersTest {

    @Test
    void matchControllerUsesSeasonFilterWhenProvided() {
        MatchRepository repository = mock(MatchRepository.class);
        Match match = Match.builder().season(2024).build();
        when(repository.findBySeason(2024)).thenReturn(List.of(match));

        assertEquals(List.of(match), new MatchController(repository).getMatches(2024));
        verify(repository).findBySeason(2024);
        verify(repository, never()).findAll();
    }

    @Test
    void matchControllerReturnsAllMatchesWithoutSeason() {
        MatchRepository repository = mock(MatchRepository.class);
        when(repository.findAll()).thenReturn(List.of());

        assertTrue(new MatchController(repository).getMatches(null).isEmpty());
        verify(repository).findAll();
    }

    @Test
    void playerControllerSearchesOnlyForNonBlankSearch() {
        PlayerRepository repository = mock(PlayerRepository.class);
        Player player = Player.builder().fullName("Virat Kohli").build();
        when(repository.findByFullNameContainingIgnoreCase("virat")).thenReturn(List.of(player));

        assertEquals(List.of(player), new PlayerController(repository).getAllPlayers("virat"));
        verify(repository).findByFullNameContainingIgnoreCase("virat");
    }

    @Test
    void playerControllerUsesAllPlayersForBlankSearchAndSupportsTeamLookup() {
        PlayerRepository repository = mock(PlayerRepository.class);
        when(repository.findAll()).thenReturn(List.of());
        when(repository.findByTeamId(7L)).thenReturn(List.of());
        PlayerController controller = new PlayerController(repository);

        assertTrue(controller.getAllPlayers("  ").isEmpty());
        assertTrue(controller.getPlayersByTeam(7L).isEmpty());
        verify(repository).findAll();
        verify(repository).findByTeamId(7L);
    }

    @Test
    void returnsFoundAndMissingEntities() {
        MatchRepository matchRepository = mock(MatchRepository.class);
        PlayerRepository playerRepository = mock(PlayerRepository.class);
        Match match = Match.builder().id(1L).build();
        Player player = Player.builder().id(2L).fullName("Player").build();
        when(matchRepository.findById(1L)).thenReturn(Optional.of(match));
        when(playerRepository.findById(2L)).thenReturn(Optional.of(player));

        ResponseEntity<Match> matchResponse = new MatchController(matchRepository).getMatch(1L);
        ResponseEntity<Player> playerResponse = new PlayerController(playerRepository).getPlayer(2L);

        assertEquals(200, matchResponse.getStatusCode().value());
        assertEquals(200, playerResponse.getStatusCode().value());
    }

    @Test
    void delegatesAgentAndPredictionRequests() {
        AiServiceClient client = mock(AiServiceClient.class);
        AgentController controller = new AgentController(client);
        ChatRequest chat = new ChatRequest("session", "hello");
        ChatResponse chatResponse = new ChatResponse("answer", List.of(), List.of(), 0.9);
        PredictionRequest prediction = new PredictionRequest(1L, "A", "B", "Venue");
        Object predictionResponse = List.of("A");
        when(client.chat(chat)).thenReturn(chatResponse);
        when(client.predict(prediction)).thenReturn(predictionResponse);

        assertSame(chatResponse, controller.chat(chat));
        assertSame(predictionResponse, controller.predict(prediction));
    }
}
