"""Factories for rating engines."""
from __future__ import annotations
from .elo import EloEngine
from .glicko import GlickoEngine
from .trueskill_ import TrueSkillEngine

factories = {
    "elo": lambda: EloEngine(),
    "glicko": lambda: GlickoEngine(),
    "trueskill": lambda: TrueSkillEngine(),
}

__all__ = ["factories", "EloEngine", "GlickoEngine", "TrueSkillEngine"]
