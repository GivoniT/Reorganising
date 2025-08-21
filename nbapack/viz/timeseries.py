"""Visualization utilities."""
from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd


def save_timeseries_plot(engine_name: str, ratings_full: pd.DataFrame, out_path):
    plt.figure(figsize=(14, 8))
    for team, group in ratings_full.groupby("TEAM"):
        plt.plot(group["GAME_DATE"], group["RATING"], label=team)
    plt.title(f"{engine_name.capitalize()} Ratings Over Time for All Teams")
    plt.xlabel("Date")
    plt.ylabel("Rating")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize="small")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
