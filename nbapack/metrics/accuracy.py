"""Accuracy and score summaries for predictions."""
from __future__ import annotations
import pandas as pd


def accuracy_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for c in [c for c in df.columns if c.startswith("PRED_CORRECT_")]:
        engine = c.replace("PRED_CORRECT_", "")
        correct = int((df[c] == 1).sum())
        total = len(df)
        acc = float(correct) / total if total else 0.0
        rows.append({"engine": engine, "correct": correct, "total": total, "accuracy": acc})
    return pd.DataFrame(rows)


def score_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for c in [c for c in df.columns if c.startswith("PRED_SCORE_")]:
        engine = c.replace("PRED_SCORE_", "")
        score_sum = float(df[c].sum())
        score_mean = float(df[c].mean()) if len(df) else 0.0
        rows.append({"engine": engine, "score_sum": score_sum, "score_mean": score_mean})
    return pd.DataFrame(rows)
