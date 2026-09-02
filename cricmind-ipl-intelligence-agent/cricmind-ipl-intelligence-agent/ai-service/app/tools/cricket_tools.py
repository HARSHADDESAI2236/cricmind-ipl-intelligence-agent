"""
Cricket domain tools exposed to the AI agent.

Each function corresponds to one entry in TOOL_SCHEMAS (schemas.py) and to
one row of the "Core AI Agent Tools" table in the project plan. The agent
(app/agent/graph.py) calls `execute_tool(name, args)` to dispatch to these.
"""
from app.tools import data_store as store
from app.ml.predictor import predict_match_winner


def get_match_schedule(**kwargs):
    return {"upcoming_matches": store.upcoming_matches()}


def get_points_table(**kwargs):
    return {"standings": store.POINTS_TABLE}


def get_player_stats(player_name: str, **kwargs):
    player = store.PLAYERS.get(player_name)
    if not player:
        matches = [p for p in store.PLAYERS if player_name.lower() in p.lower()]
        if matches:
            player_name = matches[0]
            player = store.PLAYERS[player_name]
    if not player:
        return {"error": f"No player found matching '{player_name}'"}
    return {"player": player_name, **player}


def get_team_stats(team_code: str, **kwargs):
    team_code = team_code.upper()
    team = store.TEAMS.get(team_code)
    if not team:
        return {"error": f"Unknown team code '{team_code}'"}
    standing = next((s for s in store.POINTS_TABLE if s["team"] == team_code), None)
    return {"team": team_code, **team, "standing": standing}


def compare_players(player_a: str, player_b: str, **kwargs):
    return {
        "player_a": get_player_stats(player_a),
        "player_b": get_player_stats(player_b),
    }


def get_head_to_head(team_a: str, team_b: str, **kwargs):
    key = frozenset({team_a.upper(), team_b.upper()})
    record = store.HEAD_TO_HEAD.get(key)
    if not record:
        return {"note": f"No stored head-to-head data for {team_a} vs {team_b}"}
    return {"team_a": team_a.upper(), "team_b": team_b.upper(), **record}


def get_venue_stats(venue_name: str, **kwargs):
    matches = [v for v in store.VENUES if venue_name.lower() in v.lower()]
    if not matches:
        return {"error": f"No venue data for '{venue_name}'"}
    venue = matches[0]
    return {"venue": venue, **store.VENUES[venue]}


def get_live_score(**kwargs):
    # Placeholder: in production this calls a licensed live-scores provider.
    return {"note": "No live match currently in progress (demo data only)."}


def predict_match(team1: str, team2: str, venue: str = None, **kwargs):
    result = predict_match_winner(team1.upper(), team2.upper(), venue)
    return result


def analyze_match(team1: str, team2: str, venue: str = None, **kwargs):
    h2h = get_head_to_head(team1, team2)
    v_stats = get_venue_stats(venue) if venue else {}
    prediction = predict_match(team1, team2, venue)
    t1 = get_team_stats(team1)
    t2 = get_team_stats(team2)
    return {
        "team1_form": t1,
        "team2_form": t2,
        "head_to_head": h2h,
        "venue_stats": v_stats,
        "prediction": prediction,
    }


def recommend_playing_xi(team_code: str, criteria: str = "form", **kwargs):
    team_code = team_code.upper()
    squad = [name for name, p in store.PLAYERS.items() if p.get("team") == team_code]
    return {"team": team_code, "criteria": criteria, "recommended_core_players": squad}


def search_knowledge_base(query: str, **kwargs):
    from app.rag.knowledge_base import retrieve
    results = retrieve(query, top_k=3)
    return {"query": query, "results": results}


TOOL_REGISTRY = {
    "get_live_score": get_live_score,
    "get_match_schedule": get_match_schedule,
    "get_points_table": get_points_table,
    "get_player_stats": get_player_stats,
    "get_team_stats": get_team_stats,
    "compare_players": compare_players,
    "get_head_to_head": get_head_to_head,
    "get_venue_stats": get_venue_stats,
    "predict_match": predict_match,
    "analyze_match": analyze_match,
    "recommend_playing_xi": recommend_playing_xi,
    "search_knowledge_base": search_knowledge_base,
}


def execute_tool(name: str, args: dict):
    fn = TOOL_REGISTRY.get(name)
    if not fn:
        return {"error": f"Unknown tool '{name}'"}
    try:
        return fn(**args)
    except TypeError as e:
        return {"error": f"Bad arguments for '{name}': {e}"}
