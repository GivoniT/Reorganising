"""Classic Elo rating engine."""
from __future__ import annotations
from .base import RatingEngine
from .. import config


class EloEngine(RatingEngine):
    def __init__(self, k_factor: float = config.K_FACTOR, init_rating: float = config.INIT_RATING):
        self.k = k_factor
        self.init = init_rating
        self.ratings: dict[str, float] = {}
        self._history: list[dict] = []

    def _get_rating(self, name: str) -> float:
        return self.ratings.get(name, self.init)

    def get_rating(self, team: str) -> float:
        return self._get_rating(team)

    def record_game(self, winner: str, loser: str, game_date):
        Ra = self._get_rating(winner)
        Rb = self._get_rating(loser)
        Ea = 1.0 / (1.0 + 10 ** ((Rb - Ra) / 400.0))
        Eb = 1.0 / (1.0 + 10 ** ((Ra - Rb) / 400.0))
        Ra_new = Ra + self.k * (1 - Ea)
        Rb_new = Rb + self.k * (0 - Eb)
        self.ratings[winner] = Ra_new
        self.ratings[loser] = Rb_new
        self._history.append({"GAME_DATE": game_date, "TEAM": winner, "RATING": Ra_new})
        self._history.append({"GAME_DATE": game_date, "TEAM": loser, "RATING": Rb_new})
