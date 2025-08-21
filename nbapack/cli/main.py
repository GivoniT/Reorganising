"""Command-line interface for nbapack."""
from __future__ import annotations
import argparse
import pandas as pd
from ..io import load
from ..data import combine, results
from ..engines import factories
from ..pipeline import run_all


def run_all_cmd():
    games, playoffs = load.load_raw()
    games = load.normalise_team_names(games)
    playoffs = load.normalise_team_names(playoffs)
    playoffs = load.ensure_playoff_WL_numeric(playoffs)
    games_all = combine.join_regular_and_playoffs(games, playoffs)
    res_df = results.to_results_df(games_all)
    res_df["GAME_DATE"] = pd.to_datetime(res_df["GAME_DATE"])
    res_df = res_df.sort_values("GAME_DATE").reset_index(drop=True)
    artifacts = run_all.run_all(res_df, factories)
    acc = artifacts["accuracy"]
    scores = artifacts["scores"]
    for _, row in acc.iterrows():
        print(f"{row['engine']}: accuracy {row['accuracy']:.2%} ({row['correct']}/{row['total']})")
    for _, row in scores.iterrows():
        print(f"{row['engine']}: score sum {row['score_sum']:.3f} mean {row['score_mean']:.5f}")
    return artifacts


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(prog="nbapack")
    sub = parser.add_subparsers(dest="cmd")
    run_all_parser = sub.add_parser("run-all")
    run_all_parser.set_defaults(func=lambda args: run_all_cmd())
    parser.set_defaults(func=lambda args: run_all_cmd())
    args = parser.parse_args(argv)
    return args.func(args)
