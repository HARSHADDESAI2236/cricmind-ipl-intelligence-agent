package com.cricmind.backend.repository;

import com.cricmind.backend.model.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface PlayerRepository extends JpaRepository<Player, Long> {
    List<Player> findByTeamId(Long teamId);
    List<Player> findByFullNameContainingIgnoreCase(String name);
}
