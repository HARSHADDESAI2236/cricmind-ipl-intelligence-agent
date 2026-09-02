from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import chat, predictions, data

app = FastAPI(
    title=settings.app_name,
    description="CricMind IPL Intelligence Agent -- Python AI service (LangGraph agent, RAG, ML predictions).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(predictions.router)
app.include_router(data.router)


@app.get("/")
def root():
    return {"service": settings.app_name, "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}
