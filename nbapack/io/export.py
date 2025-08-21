"""Export helpers for saving artifacts."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
from .paths import OUT_DIR
from .. import config


def save_full_ratings(engine_name: str, ratings_full: pd.DataFrame) -> Path:
    path = OUT_DIR / config.OUT_RATINGS_PATTERN.format(engine=engine_name)
    ratings_full.to_csv(path, index=False)
    return path


def save_results_with_predictions(df: pd.DataFrame) -> Path:
    path = OUT_DIR / config.OUT_RESULTS_WITH_PRED
    df.to_csv(path, index=False)
    return path


def save_accuracy_summary(df: pd.DataFrame) -> Path:
    path = OUT_DIR / config.OUT_ACCURACY_SUMMARY
    df.to_csv(path, index=False)
    return path


def save_score_summary(df: pd.DataFrame) -> Path:
    path = OUT_DIR / config.OUT_SCORE_SUMMARY
    df.to_csv(path, index=False)
    return path


def to_full_panel(ratings_df: pd.DataFrame) -> pd.DataFrame:
    all_dates = pd.date_range(start=ratings_df["GAME_DATE"].min(), end=ratings_df["GAME_DATE"].max(), freq="D")
    all_teams = ratings_df["TEAM"].unique()
    full_index = pd.MultiIndex.from_product([all_dates, all_teams], names=["GAME_DATE", "TEAM"])
    full_ratings = ratings_df.set_index(["GAME_DATE", "TEAM"]).reindex(full_index)
    full_ratings = full_ratings.groupby("TEAM").ffill().reset_index()
    return full_ratings
