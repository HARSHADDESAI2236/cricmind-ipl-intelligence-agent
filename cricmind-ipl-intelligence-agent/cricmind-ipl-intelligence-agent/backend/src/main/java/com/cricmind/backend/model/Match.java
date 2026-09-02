package com.cricmind.backend.model;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDate;

@Entity
@Table(name = "matches")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class Match {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Integer season;

    @Column(name = "match_date")
    private LocalDate matchDate;

    @ManyToOne @JoinColumn(name = "team1_id")
    private Team team1;

    @ManyToOne @JoinColumn(name = "team2_id")
    private Team team2;

    @ManyToOne @JoinColumn(name = "winner_id")
    private Team winner;

    @Column(name = "result_type")
    private String resultType;

    @Column(name = "win_margin")
    private String winMargin;

    private String status;
}
