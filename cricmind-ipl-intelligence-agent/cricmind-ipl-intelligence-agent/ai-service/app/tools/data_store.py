"""
In-memory IPL data store.

This stands in for the PostgreSQL-backed queries described in the project
schema (see /database/schema.sql). Swap the functions in this module for
SQLAlchemy queries against `teams`, `players`, `matches`, `player_stats`,
`team_stats`, and `venues` once real historical IPL data has been ingested.
Keeping the interface identical means the tools in cricket_tools.py do not
need to change when you plug in the real database.
"""
from datetime import date, timedelta

TEAMS = {
    "RCB": {"name": "Royal Challengers Bengaluru", "home_venue": "M. Chinnaswamy Stadium", "recent_form": ["W", "W", "L", "W", "L"]},
    "GT":  {"name": "Gujarat Titans", "home_venue": "Narendra Modi Stadium", "recent_form": ["W", "L", "W", "W", "W"]},
    "MI":  {"name": "Mumbai Indians", "home_venue": "Wankhede Stadium", "recent_form": ["L", "W", "W", "L", "W"]},
    "CSK": {"name": "Chennai Super Kings", "home_venue": "M. A. Chidambaram Stadium", "recent_form": ["W", "L", "L", "W", "W"]},
    "KKR": {"name": "Kolkata Knight Riders", "home_venue": "Eden Gardens", "recent_form": ["W", "W", "W", "L", "W"]},
}

PLAYERS = {
    "Virat Kohli": {"team": "RCB", "role": "Batsman", "matches": 240, "runs": 8004, "average": 38.2, "strike_rate": 131.9},
    "Shubman Gill": {"team": "GT", "role": "Batsman", "matches": 100, "runs": 3800, "average": 44.1, "strike_rate": 135.2},
    "Rashid Khan": {"team": "GT", "role": "Bowler", "matches": 130, "wickets": 160, "economy": 6.8},
    "Jasprit Bumrah": {"team": "MI", "role": "Bowler", "matches": 133, "wickets": 176, "economy": 7.3},
    "MS Dhoni": {"team": "CSK", "role": "WK-Batsman", "matches": 264, "runs": 5243, "average": 38.8, "strike_rate": 135.9},
    "Andre Russell": {"team": "KKR", "role": "All-rounder", "matches": 130, "runs": 2500, "wickets": 100},
}

VENUES = {
    "M. Chinnaswamy Stadium": {"avg_first_innings_score": 178, "toss_win_bat_win_pct": 46, "bat_first_win_pct": 44},
    "Narendra Modi Stadium": {"avg_first_innings_score": 168, "toss_win_bat_win_pct": 51, "bat_first_win_pct": 49},
    "Wankhede Stadium": {"avg_first_innings_score": 172, "toss_win_bat_win_pct": 48, "bat_first_win_pct": 47},
}

HEAD_TO_HEAD = {
    frozenset({"RCB", "GT"}): {"matches": 10, "RCB_wins": 4, "GT_wins": 6},
    frozenset({"MI", "CSK"}): {"matches": 36, "MI_wins": 20, "CSK_wins": 16},
    frozenset({"RCB", "KKR"}): {"matches": 32, "RCB_wins": 16, "KKR_wins": 16},
}

POINTS_TABLE = [
    {"team": "GT", "played": 10, "won": 7, "lost": 3, "points": 14, "nrr": 0.712},
    {"team": "RCB", "played": 10, "won": 6, "lost": 4, "points": 12, "nrr": 0.341},
    {"team": "KKR", "played": 10, "won": 6, "lost": 4, "points": 12, "nrr": 0.198},
    {"team": "CSK", "played": 10, "won": 5, "lost": 5, "points": 10, "nrr": -0.102},
    {"team": "MI", "played": 10, "won": 4, "lost": 6, "points": 8, "nrr": -0.410},
]


def upcoming_matches():
    today = date.today()
    return [
        {"id": 501, "date": str(today + timedelta(days=2)), "team1": "RCB", "team2": "GT", "venue": "M. Chinnaswamy Stadium"},
        {"id": 502, "date": str(today + timedelta(days=4)), "team1": "MI", "team2": "CSK", "venue": "Wankhede Stadium"},
    ]
