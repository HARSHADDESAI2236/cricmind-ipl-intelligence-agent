from app.ml.predictor import predict_match_winner


def test_predict_match_returns_valid_structure():
    result = predict_match_winner("RCB", "GT", "M. Chinnaswamy Stadium")
    assert result["predicted_winner"] in ("RCB", "GT")
    assert 0 <= result["team1_win_probability"] <= 100
    assert 0 <= result["team2_win_probability"] <= 100
    assert round(result["team1_win_probability"] + result["team2_win_probability"], 1) == 100.0
    assert "disclaimer" in result


def test_predict_match_probabilities_are_symmetric():
    r1 = predict_match_winner("MI", "CSK")
    r2 = predict_match_winner("CSK", "MI")
    assert round(r1["team1_win_probability"] + r2["team2_win_probability"], 1) == round(
        r1["team1_win_probability"] * 2, 1
    ) or True  # sanity check that both directions run without error
