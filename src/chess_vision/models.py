"""Data shapes shared between the vision, matching and output modules."""

from dataclasses import dataclass
from enum import Enum

import chess


class Outcome(Enum):
    """What the matcher concluded from a before/after pair."""
    MOVE = 1
    NO_MATCH = 2
    WAIT = 3
    AMBIGUOUS = 4


class Reason(Enum):
    """Why the matcher reached its outcome, as a fixed code."""
    NONE = 1
    PROMOTION_ASSUMED_QUEEN = 2
    NO_LEGAL_MATCH = 3
    NO_CHANGE = 4
    MULTIPLE_MATCHES = 5


@dataclass(frozen=True)
class Occupancy:
    """Which squares hold a white piece and which hold a black piece."""
    white: frozenset[str]
    black: frozenset[str]

    def __post_init__(self):
        # Frozen dataclasses block normal assignment, so object.__setattr__ is
        # the standard way to normalise a field during creation.
        object.__setattr__(self, "white", frozenset(self.white))
        object.__setattr__(self, "black", frozenset(self.black))

        for name in self.white | self.black:
            if name not in chess.SQUARE_NAMES:
                raise ValueError(f"not a square name: {name!r}")

        overlap = self.white & self.black
        if overlap:
            raise ValueError(f"squares in both colours: {sorted(overlap)}")


@dataclass(frozen=True)
class Result:
    """What the matcher returns for one before/after pair."""
    outcome: Outcome
    moves: tuple[chess.Move, ...]
    reason: Reason
    confidence: float

    def __post_init__(self):
        if self.outcome == Outcome.MOVE and len(self.moves) != 1:
            raise ValueError("MOVE needs exactly one move")

        if self.outcome == Outcome.AMBIGUOUS and len(self.moves) < 2:
            raise ValueError("AMBIGUOUS needs two or more moves")

        if self.outcome in (Outcome.NO_MATCH, Outcome.WAIT) and self.moves:
            raise ValueError(f"{self.outcome.name} must have no moves")

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence out of range: {self.confidence}")