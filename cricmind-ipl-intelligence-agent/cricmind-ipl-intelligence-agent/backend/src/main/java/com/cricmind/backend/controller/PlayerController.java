package com.cricmind.backend.controller;

import com.cricmind.backend.model.Player;
import com.cricmind.backend.repository.PlayerRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/players")
public class PlayerController {

    private final PlayerRepository playerRepository;

    public PlayerController(PlayerRepository playerRepository) {
        this.playerRepository = playerRepository;
    }

    @GetMapping
    public List<Player> getAllPlayers(@RequestParam(required = false) String search) {
        if (search != null && !search.isBlank()) {
            return playerRepository.findByFullNameContainingIgnoreCase(search);
        }
        return playerRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Player> getPlayer(@PathVariable Long id) {
        return playerRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/team/{teamId}")
    public List<Player> getPlayersByTeam(@PathVariable Long teamId) {
        return playerRepository.findByTeamId(teamId);
    }
}
