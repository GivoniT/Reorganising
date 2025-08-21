"""Data loading helpers."""
from __future__ import annotations
import pandas as pd
from .paths import DATA_DIR


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame]:
    games = pd.read_csv(DATA_DIR / "games.csv")
    playoffs = pd.read_csv(DATA_DIR / "playoffs.csv")
    return games, playoffs

name_map = {
    "Los Angeles Clippers": "LA Clippers",
    "New Jersey Nets": "Brooklyn Nets",
    "New Orleans Hornets": "New Orleans Pelicans",
    "New Orleans Hornet": "New Orleans Pelicans",
    "Charlotte Bobcats": "Charlotte Hornets",
}


def normalise_team_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["TEAM_NAME"] = df["TEAM_NAME"].replace(name_map)
    return df


def ensure_playoff_WL_numeric(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "WL" in df.columns:
        df["WL"] = df["WL"].apply(lambda x: 0 if x == "L" else 1)
    return df
