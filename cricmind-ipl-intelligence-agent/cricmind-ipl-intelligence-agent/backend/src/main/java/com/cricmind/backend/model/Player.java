package com.cricmind.backend.model;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDate;

@Entity
@Table(name = "players")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class Player {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "full_name", nullable = false)
    private String fullName;

    @ManyToOne
    @JoinColumn(name = "team_id")
    private Team team;

    private String role;

    @Column(name = "batting_style")
    private String battingStyle;

    @Column(name = "bowling_style")
    private String bowlingStyle;

    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;

    private String nationality;

    @Column(name = "photo_url")
    private String photoUrl;
}
