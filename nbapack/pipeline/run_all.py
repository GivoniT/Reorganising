"""Run multiple rating engines and aggregate results."""
from __future__ import annotations
import pandas as pd
from .run_engine import run_one
from ..io import export


def run_all(results_df: pd.DataFrame, engine_factories: dict[str, callable]):
    merged = results_df.copy()
    acc_frames = []
    score_frames = []
    artifacts = {}
    for name, factory in engine_factories.items():
        art = run_one(name, factory, merged)
        merged = art.results_with_preds
        acc_frames.append(art.acc_df)
        score_frames.append(art.score_df)
        artifacts[name] = art
    acc_summary = pd.concat(acc_frames, ignore_index=True) if acc_frames else pd.DataFrame()
    score_summary = pd.concat(score_frames, ignore_index=True) if score_frames else pd.DataFrame()
    export.save_results_with_predictions(merged)
    export.save_accuracy_summary(acc_summary)
    export.save_score_summary(score_summary)
    return {
        "artifacts": artifacts,
        "results": merged,
        "accuracy": acc_summary,
        "scores": score_summary,
    }
