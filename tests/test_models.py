import pytest
from chess_vision.models import Outcome, Reason, Occupancy, Result

def test_duplicate_square():
    # Same square found in both black and white square lists

    white_squares = {'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e7', 'f2', 'g2', 'h2'}
    black_squares = {'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'}

    with pytest.raises(ValueError):
        Occupancy(white=white_squares, black=black_squares)


def test_invalid_square_name():
    # Invalid square name ('e9') found in white squares

    white_squares = {'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e9', 'f2', 'g2', 'h2'}
    black_squares = {'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'}

    with pytest.raises(ValueError):
        Occupancy(white=white_squares, black=black_squares)

def test_valid_occupancy():
    # Builds a VALID Occupancy

    white_squares = {'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'}
    black_squares = {'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'}

    valid = Occupancy(white=white_squares, black=black_squares)

    # Checks both occupancy components are successfully frozen
    assert isinstance(valid.white, frozenset)
    assert isinstance(valid.black, frozenset)

def test_move_outcome_without_move_rejected():
    # Builds a Result with Outcome 'MOVE' but no move attached

    with pytest.raises(ValueError):
        Result(outcome=Outcome.MOVE, moves=(), reason=Reason.NONE, confidence=1.0)

def test_confidence_out_of_range():
    # Builds a result with a confidence level outside of range (0.0-1.0)

    with pytest.raises(ValueError):
        Result(outcome=Outcome.WAIT, moves=(), reason=Reason.NONE, confidence=2.0)

def test_valid_result():
    # Builds a VALID Result

    Result(outcome=Outcome.WAIT, moves=(), reason=Reason.NONE, confidence=1.0)