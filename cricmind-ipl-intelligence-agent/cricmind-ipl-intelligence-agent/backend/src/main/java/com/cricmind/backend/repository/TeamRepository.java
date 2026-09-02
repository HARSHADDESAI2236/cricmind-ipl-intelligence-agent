package com.cricmind.backend.repository;

import com.cricmind.backend.model.Team;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface TeamRepository extends JpaRepository<Team, Long> {
    Optional<Team> findByShortCodeIgnoreCase(String shortCode);
    Optional<Team> findByNameIgnoreCase(String name);
}
