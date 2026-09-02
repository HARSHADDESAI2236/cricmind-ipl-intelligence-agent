package com.cricmind.backend.controller;

import com.cricmind.backend.model.Team;
import com.cricmind.backend.repository.TeamRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class TeamControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private TeamRepository teamRepository;

    @Test
    void returnsAllTeams() throws Exception {
        teamRepository.save(Team.builder().name("Royal Challengers Bengaluru").shortCode("RCB").build());

        mockMvc.perform(get("/api/teams"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].shortCode").value("RCB"));
    }

    @Test
    void returns404ForMissingTeam() throws Exception {
        mockMvc.perform(get("/api/teams/9999"))
                .andExpect(status().isNotFound());
    }
}
