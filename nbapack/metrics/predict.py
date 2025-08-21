"""Prediction utilities for rating engines."""
from __future__ import annotations
import pandas as pd
from ..engines.base import RatingEngine


def pregame_predictions(engine: RatingEngine, results_df: pd.DataFrame, engine_name: str) -> pd.DataFrame:
    df = results_df.copy()
    pred_sign = []
    pred_conf = []
    pred_correct = []
    for _, row in df.iterrows():
        win = row["WIN_TEAM"]
        lose = row["LOSE_TEAM"]
        gdate = row["GAME_DATE"]
        r_win = float(engine.get_rating(win))
        r_lose = float(engine.get_rating(lose))
        rd_win = None
        rd_lose = None
        try:
            rd_win = engine.get_uncertainty(win)
        except Exception:
            pass
        try:
            rd_lose = engine.get_uncertainty(lose)
        except Exception:
            pass
        p_win = float(engine.win_prob(r_win, r_lose, rd_win, rd_lose))
        if p_win >= 0.5:
            pred_sign.append(1)
            pred_conf.append(p_win)
            pred_correct.append(1)
        else:
            pred_sign.append(-1)
            pred_conf.append(1.0 - p_win)
            pred_correct.append(-1)
        engine.record_game(win, lose, gdate)
    df[f"PRED_{engine_name}"] = pred_sign
    df[f"PRED_CONF_{engine_name}"] = pred_conf
    df[f"PRED_CORRECT_{engine_name}"] = pred_correct
    df[f"PRED_SCORE_{engine_name}"] = [s * c for s, c in zip(pred_sign, pred_conf)]
    return df


def compute_win_probability(ratings_full: pd.DataFrame, team_A_name: str, date_A, team_B_name: str, date_B, engine: RatingEngine) -> float | None:
    date_A = pd.to_datetime(date_A)
    date_B = pd.to_datetime(date_B)
    row_A = ratings_full[(ratings_full["TEAM"] == team_A_name) & (ratings_full["GAME_DATE"] == date_A)]
    row_B = ratings_full[(ratings_full["TEAM"] == team_B_name) & (ratings_full["GAME_DATE"] == date_B)]
    if row_A.empty or row_B.empty:
        return None
    rating_A = float(row_A["RATING"].values[0])
    rating_B = float(row_B["RATING"].values[0])
    rd_A = None
    rd_B = None
    try:
        rd_A = engine.get_uncertainty(team_A_name)
    except Exception:
        pass
    try:
        rd_B = engine.get_uncertainty(team_B_name)
    except Exception:
        pass
    return float(engine.win_prob(rating_A, rating_B, rd_A, rd_B))
