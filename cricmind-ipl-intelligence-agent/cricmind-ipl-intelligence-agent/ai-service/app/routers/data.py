"""Direct data endpoints -- useful for the frontend to hydrate dashboards
without going through the conversational agent for simple lookups."""
from fastapi import APIRouter

from app.tools import cricket_tools as tools

router = APIRouter(prefix="/api/data", tags=["data"])


@router.get("/schedule")
def schedule():
    return tools.get_match_schedule()


@router.get("/standings")
def standings():
    return tools.get_points_table()


@router.get("/players/{player_name}")
def player(player_name: str):
    return tools.get_player_stats(player_name=player_name)


@router.get("/teams/{team_code}")
def team(team_code: str):
    return tools.get_team_stats(team_code=team_code)
