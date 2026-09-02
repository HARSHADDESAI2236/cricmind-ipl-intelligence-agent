from app.tools.cricket_tools import execute_tool


def test_get_points_table():
    result = execute_tool("get_points_table", {})
    assert "standings" in result
    assert len(result["standings"]) > 0


def test_get_player_stats_known_player():
    result = execute_tool("get_player_stats", {"player_name": "Virat Kohli"})
    assert result["player"] == "Virat Kohli"
    assert result["team"] == "RCB"


def test_get_player_stats_unknown_player():
    result = execute_tool("get_player_stats", {"player_name": "Nobody Real"})
    assert "error" in result


def test_get_head_to_head():
    result = execute_tool("get_head_to_head", {"team_a": "RCB", "team_b": "GT"})
    assert result["matches"] == 10


def test_unknown_tool():
    result = execute_tool("not_a_real_tool", {})
    assert "error" in result
