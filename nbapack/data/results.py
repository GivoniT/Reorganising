"""Convert game records to results dataframe."""
from __future__ import annotations
import pandas as pd


def to_results_df(games_all: pd.DataFrame) -> pd.DataFrame:
    results = []
    for game_id, group in games_all.groupby("GAME_ID"):
        if len(group) != 2:
            continue
        row1, row2 = group.iloc[0], group.iloc[1]
        if row1["WL"]:
            win_team = row1["TEAM_NAME"]
            lose_team = row2["TEAM_NAME"]
            points_w = row1["PTS"]
            points_l = row2["PTS"]
        else:
            win_team = row2["TEAM_NAME"]
            lose_team = row1["TEAM_NAME"]
            points_w = row2["PTS"]
            points_l = row1["PTS"]
        results.append({
            "GAME_ID": game_id,
            "GAME_DATE": row1["GAME_DATE"],
            "WIN_TEAM": win_team,
            "LOSE_TEAM": lose_team,
            "POINTS_W": points_w,
            "POINTS_L": points_l,
        })
    df = pd.DataFrame(results)
    df = df.sort_values("GAME_DATE").reset_index(drop=True)
    return df
