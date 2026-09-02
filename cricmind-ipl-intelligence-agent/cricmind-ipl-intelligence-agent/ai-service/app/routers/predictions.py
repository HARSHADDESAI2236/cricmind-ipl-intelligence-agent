from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.ml.predictor import predict_match_winner

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


class PredictionRequest(BaseModel):
    matchId: Optional[int] = None
    team1: str
    team2: str
    venue: Optional[str] = None


@router.post("/match")
def predict_match(request: PredictionRequest):
    return predict_match_winner(request.team1.upper(), request.team2.upper(), request.venue)
