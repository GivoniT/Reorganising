"""Utilities for combining regular season and playoff data."""
from __future__ import annotations
import pandas as pd


def join_regular_and_playoffs(games: pd.DataFrame, playoffs: pd.DataFrame) -> pd.DataFrame:
    common_cols = sorted(set(games.columns).intersection(playoffs.columns))
    games_sub = games[common_cols].copy()
    playoffs_sub = playoffs[common_cols].copy()
    games_sub["IS_PLAYOFF"] = 0
    playoffs_sub["IS_PLAYOFF"] = 1
    combined = pd.concat([games_sub, playoffs_sub], ignore_index=True)
    combined = combined.drop_duplicates()
    combined = combined.sort_values("IS_PLAYOFF", ascending=False)
    cols_no_flag = [c for c in combined.columns if c != "IS_PLAYOFF"]
    combined = combined.drop_duplicates(subset=cols_no_flag, keep="first")
    return combined


def exceptions_where_gameid_not_paired(df: pd.DataFrame) -> pd.Series:
    counts = df["GAME_ID"].value_counts()
    return counts[counts != 2]
