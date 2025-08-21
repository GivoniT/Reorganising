"""Path utilities for locating data and output directories."""
from __future__ import annotations
from pathlib import Path


def _find_root(start: Path, marker: str = "Datasets_Analysis", max_up: int = 5) -> Path:
    p = start
    for _ in range(max_up):
        if (p / marker).exists():
            return p
        p = p.parent
    return start

ROOT = _find_root(Path(__file__).resolve().parent)
DATA_DIR = ROOT / "Datasets_Analysis" / "Datasets"
OUT_DIR = ROOT / "artifacts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

__all__ = ["ROOT", "DATA_DIR", "OUT_DIR"]
