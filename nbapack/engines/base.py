"""Base classes and helpers for rating engines."""
from __future__ import annotations
from abc import ABC, abstractmethod
import math
import pandas as pd


class RatingEngine(ABC):
    @abstractmethod
    def record_game(self, winner: str, loser: str, game_date: pd.Timestamp) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_rating(self, team: str) -> float:
        raise NotImplementedError

    def get_uncertainty(self, team: str) -> float | None:
        return None

    def expected_score(self, rating_a: float, rating_b: float, rd_a: float | None = None, rd_b: float | None = None) -> float:
        return 1.0 / (1.0 + 10 ** (-(rating_a - rating_b) / 400.0))

    def win_prob(self, rating_a: float, rating_b: float, rd_a: float | None = None, rd_b: float | None = None) -> float:
        return self.expected_score(rating_a, rating_b, rd_a, rd_b)

    @property
    def history(self) -> list[dict]:
        if not hasattr(self, "_history"):
            self._history = []
        return self._history


def glicko_expected_score(rating_a: float, rating_b: float, rd_b: float) -> float:
    q = math.log(10) / 400.0
    g = 1.0 / math.sqrt(1.0 + 3.0 * (q ** 2) * (rd_b ** 2) / (math.pi ** 2))
    return 1.0 / (1.0 + 10.0 ** (-g * (rating_a - rating_b) / 400.0))
