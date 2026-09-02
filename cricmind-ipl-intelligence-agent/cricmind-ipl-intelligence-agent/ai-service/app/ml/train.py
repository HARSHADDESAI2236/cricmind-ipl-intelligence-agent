"""
Trains a baseline match-outcome classifier.

For the real project, replace `generate_synthetic_dataset()` with a loader
that reads engineered features from `matches` / `team_stats` / `player_stats`
(see /database/schema.sql) built from actual historical ball-by-ball IPL
data. The feature set and model interface are kept realistic so the swap is
a drop-in replacement.

Run with:  python -m app.ml.train
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import os

FEATURE_COLUMNS = [
    "team1_recent_win_pct",
    "team2_recent_win_pct",
    "team1_h2h_win_pct",
    "toss_won_by_team1",
    "team1_batting_strength",
    "team2_bowling_strength",
    "team1_venue_win_pct",
]

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "match_predictor.joblib")


def generate_synthetic_dataset(n=4000, seed=42):
    """Synthetic but structurally realistic training data: team1's win
    probability increases with recent form, head-to-head dominance, batting
    strength, and winning the toss -- which is exactly the kind of signal
    real IPL features carry."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "team1_recent_win_pct": rng.uniform(0, 1, n),
        "team2_recent_win_pct": rng.uniform(0, 1, n),
        "team1_h2h_win_pct": rng.uniform(0, 1, n),
        "toss_won_by_team1": rng.integers(0, 2, n),
        "team1_batting_strength": rng.normal(0, 1, n),
        "team2_bowling_strength": rng.normal(0, 1, n),
        "team1_venue_win_pct": rng.uniform(0, 1, n),
    })
    logit = (
        2.2 * (df.team1_recent_win_pct - df.team2_recent_win_pct)
        + 1.4 * (df.team1_h2h_win_pct - 0.5)
        + 0.5 * df.toss_won_by_team1
        + 0.8 * df.team1_batting_strength
        - 0.8 * df.team2_bowling_strength
        + 1.0 * (df.team1_venue_win_pct - 0.5)
        + rng.normal(0, 0.6, n)
    )
    prob = 1 / (1 + np.exp(-logit))
    df["team1_wins"] = (rng.uniform(0, 1, n) < prob).astype(int)
    return df


def train_and_evaluate():
    df = generate_synthetic_dataset()
    X = df[FEATURE_COLUMNS]
    y = df["team1_wins"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    candidates = {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42),
    }

    best_model, best_name, best_auc = None, None, -1
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        proba = model.predict_proba(X_test)[:, 1]
        preds = model.predict(X_test)
        metrics = {
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds),
            "recall": recall_score(y_test, preds),
            "f1": f1_score(y_test, preds),
            "roc_auc": roc_auc_score(y_test, proba),
        }
        print(f"[{name}] " + ", ".join(f"{k}={v:.3f}" for k, v in metrics.items()))
        if metrics["roc_auc"] > best_auc:
            best_model, best_name, best_auc = model, name, metrics["roc_auc"]

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"model": best_model, "features": FEATURE_COLUMNS, "model_name": best_name}, MODEL_PATH)
    print(f"\nSaved best model ({best_name}, ROC-AUC={best_auc:.3f}) to {MODEL_PATH}")


if __name__ == "__main__":
    train_and_evaluate()
