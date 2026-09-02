package com.cricmind.backend.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "teams")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class Team {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    @Column(name = "short_code", nullable = false, unique = true)
    private String shortCode;

    @Column(name = "home_venue")
    private String homeVenue;

    @Column(name = "founded_year")
    private Integer foundedYear;

    @Column(name = "logo_url")
    private String logoUrl;
}
