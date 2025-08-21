"""Glicko-2 rating engine."""
from __future__ import annotations
from glicko2 import Player
from .base import RatingEngine, glicko_expected_score


class GlickoEngine(RatingEngine):
    def __init__(self):
        self.players: dict[str, Player] = {}
        self._history: list[dict] = []

    def _get_player(self, name: str) -> Player:
        if name not in self.players:
            self.players[name] = Player()
        return self.players[name]

    def record_game(self, winner: str, loser: str, game_date):
        w = self._get_player(winner)
        l = self._get_player(loser)
        w.update_player([l.getRating()], [l.getRd()], [1])
        l.update_player([w.getRating()], [w.getRd()], [0])
        self._history.append({"GAME_DATE": game_date, "TEAM": winner, "RATING": w.getRating()})
        self._history.append({"GAME_DATE": game_date, "TEAM": loser, "RATING": l.getRating()})

    def get_rating(self, team: str) -> float:
        return self._get_player(team).getRating()

    def get_uncertainty(self, team: str) -> float:
        return self._get_player(team).getRd()

    def win_prob(self, rating_a: float, rating_b: float, rd_a: float | None = None, rd_b: float | None = None) -> float:
        if rd_b is None:
            rd_b = 50.0
        return glicko_expected_score(rating_a, rating_b, rd_b)
