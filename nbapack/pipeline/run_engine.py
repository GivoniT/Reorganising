"""Run a single rating engine over results."""
from __future__ import annotations
from collections import namedtuple
import pandas as pd
from ..metrics import predict, accuracy
from ..io import export, paths
from ..viz import timeseries

RunArtifact = namedtuple("RunArtifact", "engine_name ratings_df results_with_preds acc_df score_df paths")


def run_one(engine_name: str, engine_factory, results_df: pd.DataFrame) -> RunArtifact:
    engine = engine_factory()
    enriched = predict.pregame_predictions(engine, results_df, engine_name)
    ratings_history = pd.DataFrame(engine.history)
    ratings_full = export.to_full_panel(ratings_history)
    ratings_path = export.save_full_ratings(engine_name, ratings_full)
    plot_path = paths.OUT_DIR / f"{engine_name}_ratings_over_time.png"
    timeseries.save_timeseries_plot(engine_name, ratings_full, plot_path)
    acc_df = accuracy.accuracy_table(enriched)
    acc_df = acc_df[acc_df["engine"] == engine_name].reset_index(drop=True)
    score_df = accuracy.score_table(enriched)
    score_df = score_df[score_df["engine"] == engine_name].reset_index(drop=True)
    paths_dict = {"ratings": ratings_path, "plot": plot_path}
    return RunArtifact(engine_name, ratings_full, enriched, acc_df, score_df, paths_dict)
