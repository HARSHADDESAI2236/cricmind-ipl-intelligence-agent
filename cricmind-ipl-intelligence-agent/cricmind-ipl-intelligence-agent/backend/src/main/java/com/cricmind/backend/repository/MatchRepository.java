package com.cricmind.backend.repository;

import com.cricmind.backend.model.Match;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface MatchRepository extends JpaRepository<Match, Long> {
    List<Match> findBySeason(Integer season);
    List<Match> findByStatus(String status);
}
