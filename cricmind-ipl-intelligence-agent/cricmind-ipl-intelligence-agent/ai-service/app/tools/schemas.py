"""Tool schemas passed to the Anthropic API's tool-use ("function calling")
parameter so Claude can decide which cricket tool(s) to call for a given
question. Keep each description tight and unambiguous -- that is what the
model uses to route intent to the correct tool."""

TOOL_SCHEMAS = [
    {
        "name": "get_match_schedule",
        "description": "Get upcoming and recently completed IPL matches.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_points_table",
        "description": "Get the current IPL points table / standings.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_player_stats",
        "description": "Get batting/bowling statistics for a named player.",
        "input_schema": {
            "type": "object",
            "properties": {"player_name": {"type": "string", "description": "Full or partial player name"}},
            "required": ["player_name"],
        },
    },
    {
        "name": "get_team_stats",
        "description": "Get a team's recent form and current standing using its short code (e.g. RCB, GT, MI, CSK, KKR).",
        "input_schema": {
            "type": "object",
            "properties": {"team_code": {"type": "string"}},
            "required": ["team_code"],
        },
    },
    {
        "name": "compare_players",
        "description": "Compare statistics between two players.",
        "input_schema": {
            "type": "object",
            "properties": {
                "player_a": {"type": "string"},
                "player_b": {"type": "string"},
            },
            "required": ["player_a", "player_b"],
        },
    },
    {
        "name": "get_head_to_head",
        "description": "Get historical head-to-head match record between two teams (use short codes).",
        "input_schema": {
            "type": "object",
            "properties": {
                "team_a": {"type": "string"},
                "team_b": {"type": "string"},
            },
            "required": ["team_a", "team_b"],
        },
    },
    {
        "name": "get_venue_stats",
        "description": "Get venue-specific statistics such as average first-innings score and toss impact.",
        "input_schema": {
            "type": "object",
            "properties": {"venue_name": {"type": "string"}},
            "required": ["venue_name"],
        },
    },
    {
        "name": "get_live_score",
        "description": "Get the current state of a live match, if one is in progress.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "predict_match",
        "description": "Run the ML prediction pipeline to estimate win probability for a match between two teams.",
        "input_schema": {
            "type": "object",
            "properties": {
                "team1": {"type": "string"},
                "team2": {"type": "string"},
                "venue": {"type": "string"},
            },
            "required": ["team1", "team2"],
        },
    },
    {
        "name": "analyze_match",
        "description": "Produce a full situation-aware analysis of an upcoming or hypothetical match: form, head-to-head, venue, and ML prediction combined. Use this for 'why will X win' style questions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "team1": {"type": "string"},
                "team2": {"type": "string"},
                "venue": {"type": "string"},
            },
            "required": ["team1", "team2"],
        },
    },
    {
        "name": "recommend_playing_xi",
        "description": "Recommend a core group of players for a team's playing XI based on a given criteria.",
        "input_schema": {
            "type": "object",
            "properties": {
                "team_code": {"type": "string"},
                "criteria": {"type": "string", "description": "e.g. 'form', 'venue-suited', 'balanced'"},
            },
            "required": ["team_code"],
        },
    },
    {
        "name": "search_knowledge_base",
        "description": "Semantic search over IPL knowledge documents (rules, history, terminology, venue guides) for general knowledge questions that are not simple stat lookups.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
]
