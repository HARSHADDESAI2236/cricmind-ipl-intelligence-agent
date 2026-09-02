"""
Runtime wrapper around the trained match-outcome model.

Loads the joblib artifact produced by `train.py` and exposes
`predict_match_winner(team1, team2, venue)`, which the `predict_match`
agent tool calls. Falls back to a transparent heuristic if no trained
model file is present yet (e.g. on first boot before `train.py` has run),
so the API never hard-fails.
"""
import os
import joblib
import pandas as pd

from app.tools import data_store as store

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "match_predictor.joblib")

_model_bundle = None


def _load_model():
    global _model_bundle
    if _model_bundle is None and os.path.exists(MODEL_PATH):
        _model_bundle = joblib.load(MODEL_PATH)
    return _model_bundle


def _form_win_pct(team_code: str) -> float:
    team = store.TEAMS.get(team_code, {})
    form = team.get("recent_form", [])
    if not form:
        return 0.5
    return form.count("W") / len(form)


def _h2h_win_pct(team1: str, team2: str) -> float:
    key = frozenset({team1, team2})
    record = store.HEAD_TO_HEAD.get(key)
    if not record:
        return 0.5
    total = record["matches"]
    wins = record.get(f"{team1}_wins", total / 2)
    return wins / total if total else 0.5


def _venue_win_pct(team_code: str, venue: str) -> float:
    # Simplified proxy: teams playing at/near their home venue get a boost.
    team = store.TEAMS.get(team_code, {})
    if venue and team.get("home_venue") == venue:
        return 0.58
    return 0.5


def _build_features(team1: str, team2: str, venue: str | None):
    return {
        "team1_recent_win_pct": _form_win_pct(team1),
        "team2_recent_win_pct": _form_win_pct(team2),
        "team1_h2h_win_pct": _h2h_win_pct(team1, team2),
        "toss_won_by_team1": 1,  # unknown pre-match -> assume neutral/simulated toss win
        "team1_batting_strength": 0.0,
        "team2_bowling_strength": 0.0,
        "team1_venue_win_pct": _venue_win_pct(team1, venue),
    }


def predict_match_winner(team1: str, team2: str, venue: str | None = None) -> dict:
    features = _build_features(team1, team2, venue)
    bundle = _load_model()

    if bundle:
        model = bundle["model"]
        feature_order = bundle["features"]
        X = pd.DataFrame([[features[f] for f in feature_order]], columns=feature_order)
        team1_win_prob = float(model.predict_proba(X)[0][1])
        model_version = bundle.get("model_name", "unknown")
    else:
        # Transparent fallback heuristic (used only if train.py hasn't run yet).
        team1_win_prob = 0.5 + 0.3 * (features["team1_recent_win_pct"] - features["team2_recent_win_pct"])
        team1_win_prob = min(max(team1_win_prob, 0.05), 0.95)
        model_version = "heuristic_fallback_v0"

    winner = team1 if team1_win_prob >= 0.5 else team2
    confidence = max(team1_win_prob, 1 - team1_win_prob)

    key_factors = []
    if features["team1_recent_win_pct"] != features["team2_recent_win_pct"]:
        better = team1 if features["team1_recent_win_pct"] > features["team2_recent_win_pct"] else team2
        key_factors.append(f"{better} has better recent form")
    if features["team1_h2h_win_pct"] != 0.5:
        leader = team1 if features["team1_h2h_win_pct"] > 0.5 else team2
        key_factors.append(f"{leader} leads the head-to-head record")
    if venue and features["team1_venue_win_pct"] > 0.5:
        key_factors.append(f"{team1} has a home-venue advantage at {venue}")

    return {
        "team1": team1,
        "team2": team2,
        "venue": venue,
        "predicted_winner": winner,
        "win_probability": round(confidence * 100, 1),
        "team1_win_probability": round(team1_win_prob * 100, 1),
        "team2_win_probability": round((1 - team1_win_prob) * 100, 1),
        "model_version": model_version,
        "key_factors": key_factors,
        "disclaimer": "This is a statistical estimate, not a guaranteed outcome.",
    }
