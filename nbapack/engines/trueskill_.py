"""TrueSkill rating engine."""
from __future__ import annotations
import math
import trueskill as ts
from .base import RatingEngine
from .. import config


class TrueSkillEngine(RatingEngine):
    def __init__(self, mu: float = config.TRUESKILL_MU, sigma: float = config.TRUESKILL_SIGMA,
                 beta: float = config.TRUESKILL_BETA, tau: float = config.TRUESKILL_TAU,
                 draw_probability: float = config.TRUESKILL_DRAW_PROB):
        self.env = ts.TrueSkill(mu=mu, sigma=sigma, beta=beta, tau=tau, draw_probability=draw_probability)
        self.players: dict[str, ts.Rating] = {}
        self._history: list[dict] = []

    def _get_player(self, name: str) -> ts.Rating:
        if name not in self.players:
            self.players[name] = self.env.create_rating()
        return self.players[name]

    def record_game(self, winner: str, loser: str, game_date):
        w = self._get_player(winner)
        l = self._get_player(loser)
        w_new, l_new = self.env.rate_1vs1(w, l)
        self.players[winner] = w_new
        self.players[loser] = l_new
        self._history.append({"GAME_DATE": game_date, "TEAM": winner, "RATING": w_new.mu})
        self._history.append({"GAME_DATE": game_date, "TEAM": loser, "RATING": l_new.mu})

    def get_rating(self, team: str) -> float:
        return float(self._get_player(team).mu)

    def get_uncertainty(self, team: str) -> float:
        return float(self._get_player(team).sigma)

    def expected_score(self, rating_a: float, rating_b: float, rd_a: float | None = None, rd_b: float | None = None) -> float:
        sigma_a = rd_a if rd_a is not None else self.env.sigma
        sigma_b = rd_b if rd_b is not None else self.env.sigma
        denom = math.sqrt(2 * (self.env.beta ** 2) + sigma_a ** 2 + sigma_b ** 2)
        z = (rating_a - rating_b) / denom
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
