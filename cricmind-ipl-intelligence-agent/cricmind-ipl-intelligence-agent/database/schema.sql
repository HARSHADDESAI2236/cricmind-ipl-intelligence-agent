-- CricMind IPL Intelligence Agent — PostgreSQL Schema
-- Enable pgvector for RAG embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- ==========================================================
-- USERS & AUTH
-- ==========================================================
CREATE TABLE users (
    id              BIGSERIAL PRIMARY KEY,
    username        VARCHAR(50) UNIQUE NOT NULL,
    email           VARCHAR(120) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    role            VARCHAR(20) NOT NULL DEFAULT 'USER', -- USER, ADMIN
    created_at      TIMESTAMP NOT NULL DEFAULT now()
);

-- ==========================================================
-- CORE CRICKET ENTITIES
-- ==========================================================
CREATE TABLE teams (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(100) UNIQUE NOT NULL,
    short_code      VARCHAR(10) UNIQUE NOT NULL,
    home_venue      VARCHAR(120),
    founded_year    INT,
    logo_url        VARCHAR(255)
);

CREATE TABLE players (
    id              BIGSERIAL PRIMARY KEY,
    full_name       VARCHAR(120) NOT NULL,
    team_id         BIGINT REFERENCES teams(id),
    role            VARCHAR(30),           -- Batsman, Bowler, All-rounder, WK
    batting_style    VARCHAR(30),
    bowling_style    VARCHAR(30),
    date_of_birth   DATE,
    nationality     VARCHAR(60),
    photo_url       VARCHAR(255)
);

CREATE TABLE venues (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(150) NOT NULL,
    city            VARCHAR(80),
    country         VARCHAR(80),
    avg_first_innings_score NUMERIC(6,2),
    toss_win_bat_win_pct    NUMERIC(5,2)
);

CREATE TABLE matches (
    id              BIGSERIAL PRIMARY KEY,
    season          INT NOT NULL,
    match_date      DATE NOT NULL,
    team1_id        BIGINT REFERENCES teams(id),
    team2_id        BIGINT REFERENCES teams(id),
    venue_id        BIGINT REFERENCES venues(id),
    toss_winner_id  BIGINT REFERENCES teams(id),
    toss_decision   VARCHAR(10),           -- bat / field
    winner_id       BIGINT REFERENCES teams(id),
    result_type     VARCHAR(20),           -- normal, tie, no result, super_over
    win_margin      VARCHAR(30),
    status          VARCHAR(20) DEFAULT 'SCHEDULED' -- SCHEDULED, LIVE, COMPLETED
);

CREATE TABLE innings (
    id              BIGSERIAL PRIMARY KEY,
    match_id        BIGINT REFERENCES matches(id) ON DELETE CASCADE,
    innings_number  INT NOT NULL,
    batting_team_id BIGINT REFERENCES teams(id),
    bowling_team_id BIGINT REFERENCES teams(id),
    total_runs      INT DEFAULT 0,
    total_wickets   INT DEFAULT 0,
    overs_played    NUMERIC(4,1) DEFAULT 0
);

CREATE TABLE deliveries (
    id              BIGSERIAL PRIMARY KEY,
    innings_id      BIGINT REFERENCES innings(id) ON DELETE CASCADE,
    over_number     INT NOT NULL,
    ball_number     INT NOT NULL,
    batsman_id      BIGINT REFERENCES players(id),
    bowler_id       BIGINT REFERENCES players(id),
    runs_batsman    INT DEFAULT 0,
    runs_extras     INT DEFAULT 0,
    extras_type     VARCHAR(20),
    wicket          BOOLEAN DEFAULT FALSE,
    dismissal_type  VARCHAR(30),
    player_dismissed_id BIGINT REFERENCES players(id)
);

-- ==========================================================
-- AGGREGATED STATS (materialized/derived, refreshed by batch jobs)
-- ==========================================================
CREATE TABLE player_stats (
    id              BIGSERIAL PRIMARY KEY,
    player_id       BIGINT REFERENCES players(id),
    season          INT,
    matches         INT DEFAULT 0,
    runs            INT DEFAULT 0,
    balls_faced     INT DEFAULT 0,
    strike_rate     NUMERIC(6,2),
    average         NUMERIC(6,2),
    wickets         INT DEFAULT 0,
    economy         NUMERIC(5,2),
    fifties         INT DEFAULT 0,
    hundreds        INT DEFAULT 0,
    UNIQUE(player_id, season)
);

CREATE TABLE team_stats (
    id              BIGSERIAL PRIMARY KEY,
    team_id         BIGINT REFERENCES teams(id),
    season          INT,
    matches_played  INT DEFAULT 0,
    wins            INT DEFAULT 0,
    losses          INT DEFAULT 0,
    points          INT DEFAULT 0,
    net_run_rate    NUMERIC(5,3),
    UNIQUE(team_id, season)
);

-- ==========================================================
-- ML PREDICTIONS
-- ==========================================================
CREATE TABLE predictions (
    id              BIGSERIAL PRIMARY KEY,
    match_id        BIGINT REFERENCES matches(id),
    model_version   VARCHAR(30),
    predicted_winner_id BIGINT REFERENCES teams(id),
    win_probability NUMERIC(5,2),
    key_factors     JSONB,
    actual_winner_id BIGINT REFERENCES teams(id),
    created_at      TIMESTAMP DEFAULT now()
);

-- ==========================================================
-- RAG / KNOWLEDGE BASE
-- ==========================================================
CREATE TABLE documents (
    id              BIGSERIAL PRIMARY KEY,
    title           VARCHAR(200),
    source          VARCHAR(255),
    doc_type        VARCHAR(50),           -- rules, player_profile, venue_info, terminology
    content         TEXT,
    created_at      TIMESTAMP DEFAULT now()
);

CREATE TABLE document_chunks (
    id              BIGSERIAL PRIMARY KEY,
    document_id     BIGINT REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index     INT,
    chunk_text      TEXT,
    embedding       vector(1536),
    metadata        JSONB
);

CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ==========================================================
-- CHAT / AGENT SESSIONS
-- ==========================================================
CREATE TABLE chat_sessions (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT REFERENCES users(id),
    title           VARCHAR(200),
    created_at      TIMESTAMP DEFAULT now()
);

CREATE TABLE chat_messages (
    id              BIGSERIAL PRIMARY KEY,
    session_id      BIGINT REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role            VARCHAR(20) NOT NULL,  -- user, agent, tool
    content         TEXT NOT NULL,
    tools_used      JSONB,
    sources         JSONB,
    created_at      TIMESTAMP DEFAULT now()
);

-- ==========================================================
-- INDEXES
-- ==========================================================
CREATE INDEX idx_matches_season ON matches(season);
CREATE INDEX idx_deliveries_innings ON deliveries(innings_id);
CREATE INDEX idx_player_stats_player ON player_stats(player_id);
CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);
