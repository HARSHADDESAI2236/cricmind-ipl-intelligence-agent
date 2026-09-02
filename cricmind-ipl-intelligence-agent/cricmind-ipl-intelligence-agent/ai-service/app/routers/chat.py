from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.agent.graph import run_agent

router = APIRouter(prefix="/api/agent", tags=["agent"])


class ChatRequest(BaseModel):
    sessionId: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    answer: str
    toolsUsed: List[str]
    sources: List[Dict[str, Any]]
    confidence: float


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = run_agent(request.message)
    return ChatResponse(
        answer=result["answer"],
        toolsUsed=result["tools_used"],
        sources=result["sources"],
        confidence=result["confidence"],
    )
