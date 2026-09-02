package com.cricmind.backend.controller;

import com.cricmind.backend.model.Match;
import com.cricmind.backend.repository.MatchRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/matches")
public class MatchController {

    private final MatchRepository matchRepository;

    public MatchController(MatchRepository matchRepository) {
        this.matchRepository = matchRepository;
    }

    @GetMapping
    public List<Match> getMatches(@RequestParam(required = false) Integer season) {
        if (season != null) {
            return matchRepository.findBySeason(season);
        }
        return matchRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Match> getMatch(@PathVariable Long id) {
        return matchRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
