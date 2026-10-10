import chess
from dataclasses import dataclass, field

@dataclass
class Occupancy:
    white: chess.SquareSet
    black: chess.SquareSet


def move_finder (board, occupancy):
#    for move in board.legal_moves:
#        prediction = before.chess.move
#
#        if prediction = occupancy:
#            moves = moves + move           
#    return moves
    return None