"""Find the single legal move that explains a change in board occupancy."""

import chess

from chess_vision.models import Occupancy, Outcome, Reason, Result


def move_finder(board: chess.Board, occupancy: Occupancy) -> Result:
    """Match an observed after-occupancy to a legal move from board."""
    move_check = board_to_occupancy(board)

    if move_check == occupancy:
        return Result(
            outcome=Outcome.WAIT,
            moves=(),
            reason=Reason.NO_CHANGE,
            confidence=1.0,
        )

    moves = []

    for move in board.legal_moves:
        if move.promotion is not None and move.promotion != chess.QUEEN:
            continue

        test_board = board.copy()
        test_board.push(move)

        new_occupancy = board_to_occupancy(test_board)

        if new_occupancy == occupancy:
            moves.append(move)

    if len(moves) == 1:
        if moves[0].promotion == chess.QUEEN:
            outcome = Outcome.MOVE
            reason = Reason.PROMOTION_ASSUMED_QUEEN
        else:
            outcome = Outcome.MOVE
            reason = Reason.NONE
    elif len(moves) > 1:
        outcome = Outcome.AMBIGUOUS
        reason = Reason.MULTIPLE_MATCHES
    else:
        outcome = Outcome.NO_MATCH
        reason = Reason.NO_LEGAL_MATCH

    return Result(
        outcome=outcome,
        moves=tuple(moves),
        reason=reason,
        confidence=1.0,
    )


def board_to_occupancy(board: chess.Board) -> Occupancy:
    """Turn a board into an Occupancy of square names."""
    white_squares = set()
    for square in chess.SquareSet(board.occupied_co[chess.WHITE]):
        white_squares.add(chess.square_name(square))

    black_squares = set()
    for square in chess.SquareSet(board.occupied_co[chess.BLACK]):
        black_squares.add(chess.square_name(square))

    return Occupancy(white=white_squares, black=black_squares)