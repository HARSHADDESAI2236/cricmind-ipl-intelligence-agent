# 🏏 CricMind — IPL Intelligence Agent

**An industry-style, full-stack AI cricket analytics platform** combining an agentic tool-calling LLM, retrieval-augmented generation (RAG), and a machine-learning match-prediction pipeline behind a secure REST API and a React dashboard.

CricMind isn't just a chatbot wrapper — it's a multi-service system where a **Spring Boot API gateway** authenticates and routes requests to a **Python/FastAPI AI service**, which runs a **LangGraph agent** capable of choosing between 12 cricket-domain tools (live stats, schedules, standings, head-to-head, venue analytics, playing-XI recommendations, semantic knowledge search) and a trained **scikit-learn win-probability model**.

> Ask it things like: *"Why is RCB likely to win against GT?"* and the agent pulls recent form, head-to-head history, venue stats, and an ML prediction — then explains its reasoning with sources attached.

---

## Architecture

```
┌─────────────┐      REST       ┌──────────────────┐      REST       ┌────────────────────┐
│   React     │ ───────────────▶│   Spring Boot     │ ───────────────▶│  FastAPI AI Service │
│  Frontend   │◀─────────────── │   API Gateway     │◀─────────────── │  (LangGraph Agent)  │
│ (Tailwind)  │   JSON / JWT     │  Auth, CRUD, CORS │   JSON           │  Tools · RAG · ML    │
└─────────────┘                 └─────────┬─────────┘                 └──────────┬──────────┘
                                           │                                      │
                                           ▼                                      ▼
                                   ┌───────────────────────────────────────────────────┐
                                   │            PostgreSQL + pgvector                    │
                                   │  teams · players · matches · deliveries · stats     │
                                   │  documents · document_chunks (RAG embeddings)       │
                                   │  predictions · chat_sessions · chat_messages        │
                                   └───────────────────────────────────────────────────┘
```

**Why two backend services instead of one?** Spring Boot is the secure, typed API gateway (auth, validation, rate limiting, CRUD) that a Java shop would recognize; Python/FastAPI is where the AI/ML ecosystem (LangGraph, scikit-learn, pgvector) actually lives. This mirrors how AI features get bolted onto existing enterprise Java systems in practice.

### Agent flow

```
User question
   → Spring Boot authenticates & forwards to /api/agent/chat
   → LangGraph agent (Claude) decides: answer directly, or call tool(s)?
   → Tool(s) run: get_team_stats, get_head_to_head, get_venue_stats, predict_match, search_knowledge_base, ...
   → Results fed back to the model
   → Model synthesizes a grounded answer with sources + confidence
   → Response streamed back to the React "AI Analyst" chat UI
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, React Router, Tailwind CSS, Axios, Recharts |
| Backend (Gateway) | Java 25, Spring Boot 3, Spring Security (JWT), WebClient |
| AI Service | Python 3.11, FastAPI, LangGraph, Anthropic API (tool use) |
| ML | scikit-learn (Logistic Regression / Random Forest), pandas, joblib |
| RAG | pgvector, TF-IDF fallback retriever (swap-in for production embeddings) |
| Database | PostgreSQL 15+ with the `pgvector` extension |
| DevOps | Docker, Docker Compose, GitHub Actions CI |
| Testing | JUnit 5 + MockMvc (backend), Pytest (AI service) |

---

## Repository Structure

```
cricmind-ipl-intelligence-agent/
├── backend/                # Spring Boot API gateway
│   ├── src/main/java/com/cricmind/backend/
│   │   ├── controller/      # REST endpoints (Auth, Team, Player, Match, Agent)
│   │   ├── model/           # JPA entities
│   │   ├── repository/      # Spring Data repositories
│   │   ├── security/        # JWT filter + service
│   │   ├── service/         # AiServiceClient (WebClient → Python service)
│   │   ├── dto/              # Request/response records
│   │   └── exception/        # Global exception handling
│   └── src/test/            # JUnit + MockMvc tests
├── ai-service/              # Python FastAPI AI microservice
│   ├── app/
│   │   ├── agent/graph.py    # LangGraph agent (tool-calling loop)
│   │   ├── tools/             # 12 cricket tools + JSON schemas + mock data layer
│   │   ├── rag/                # Knowledge base + retrieval
│   │   ├── ml/                  # train.py (model training) + predictor.py (inference)
│   │   └── routers/              # /api/agent/chat, /api/predictions/match, /api/data/*
│   └── tests/                # Pytest suite
├── frontend/                 # React + Tailwind SPA
│   └── src/pages/            # Dashboard, AI Analyst, Teams, Predictions
├── database/schema.sql       # Full PostgreSQL + pgvector schema
├── docker-compose.yml        # One-command local stack
└── .github/workflows/ci.yml  # CI: tests + Docker build checks for all 3 services
```

---

## Features

- 🤖 **Agentic AI Analyst** — LangGraph-orchestrated agent that autonomously selects from 12 cricket tools per question
- 📊 **Live dashboards** — points table, upcoming fixtures, team/player analytics
- 🔮 **ML match predictions** — Logistic Regression / Random Forest trained on engineered match features, with win probability, key factors, and an explicit "not a guarantee" disclaimer
- 📚 **RAG knowledge search** — semantic retrieval over IPL rules/terminology documents with source attribution
- 🔐 **JWT authentication** — Spring Security-backed register/login, stateless sessions
- 🐳 **One-command deployment** — `docker compose up` brings up Postgres, both backends, and the frontend
- ✅ **CI pipeline** — automated backend (JUnit), AI service (Pytest), and frontend build checks on every push

---

## Getting Started

### Option 1 — Docker Compose (recommended)

```bash
git clone https://github.com/<your-username>/cricmind-ipl-intelligence-agent.git
cd cricmind-ipl-intelligence-agent
cp ai-service/.env.example ai-service/.env   # add your ANTHROPIC_API_KEY
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API + Swagger UI: http://localhost:8080/swagger-ui.html
- AI service docs: http://localhost:8000/docs

### Option 2 — Run each service locally

**Database**
```bash
docker run -d --name cricmind-pg -e POSTGRES_DB=cricmind -e POSTGRES_USER=cricmind \
  -e POSTGRES_PASSWORD=cricmind -p 5432:5432 ankane/pgvector
psql postgresql://cricmind:cricmind@localhost:5432/cricmind -f database/schema.sql
```

**AI service**
```bash
cd ai-service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY
python -m app.ml.train        # trains and saves the win-probability model
uvicorn app.main:app --reload --port 8000
```

**Backend**
```bash
cd backend
mvn spring-boot:run
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

---

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` / `/api/auth/login` | JWT auth |
| GET | `/api/teams`, `/api/players`, `/api/matches` | Core CRUD data |
| GET | `/api/standings` | Points table |
| POST | `/api/agent/chat` | Ask the AI analyst anything (forwards to LangGraph agent) |
| POST | `/api/predictions/match` | Run the ML win-probability model directly |

Full interactive docs at `/swagger-ui.html` (backend) and `/docs` (AI service).

---

## Machine Learning

`ai-service/app/ml/train.py` engineers 7 match-context features (recent form differential, head-to-head win %, toss, batting/bowling strength, venue win %), trains and compares Logistic Regression and Random Forest, and reports accuracy, precision, recall, F1, and ROC-AUC before saving the best model. `predictor.py` loads that model at inference time and falls back to a transparent heuristic if no trained artifact exists yet, so the API never hard-fails.

> **Note on data:** this repo ships with a small in-memory mock dataset (`app/tools/data_store.py`) and synthetic training data so the whole system runs end-to-end out of the box. Swap in real historical IPL ball-by-ball data (e.g. from Cricsheet) and the PostgreSQL schema in `database/schema.sql` for production-grade accuracy — the tool and model interfaces are designed so that swap doesn't require touching the agent or API layers.

---

## Testing

```bash
# Backend
cd backend && mvn test

# AI service
cd ai-service && pytest tests/ -v

# Frontend build check
cd frontend && npm run build
```

All three run automatically in CI on every push via `.github/workflows/ci.yml`.

---

## Roadmap / Future Improvements

- [ ] Real historical IPL data ingestion (Cricsheet ball-by-ball → PostgreSQL)
- [ ] Live score integration via a licensed provider + WebSocket push to frontend
- [ ] Production-grade embeddings for RAG (replace TF-IDF fallback) with pgvector similarity search
- [ ] Model monitoring: track `predictions.actual_winner_id` vs predicted to measure real-world accuracy over a season
- [ ] Rate limiting on `/api/agent/chat` and `/api/predictions/match`
- [ ] Streaming responses in the AI Analyst chat UI

## Limitations

This is a portfolio/demo build: the cricket statistics are a small illustrative dataset, not live IPL data, and the ML model is trained on synthetic (not historical) match data. See the Roadmap above for what a production version would add.

---

## Resume Bullet

> **CricMind — IPL Intelligence Agent** · Java, Spring Boot, React, Python, LangGraph, PostgreSQL, scikit-learn
> Built a full-stack AI cricket intelligence platform combining agentic tool-calling, RAG, and ML win-probability prediction behind a secure multi-service architecture (Spring Boot gateway + Python AI microservice), with Dockerized deployment and CI-tested endpoints.

---

## License

MIT — see [LICENSE](./LICENSE).
