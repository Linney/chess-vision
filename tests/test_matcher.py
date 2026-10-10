import chess
from chess_vision.matcher import Occupancy, move_finder

def test_1e4():
    starting_board = chess.Board()

    white_squares = {
        chess.square_name(square)
        for square in chess.SquareSet(starting_board.occupied_co[chess.WHITE])
    }

    white_squares.remove(chess.square_name(chess.E2))
    white_squares.add(chess.square_name(chess.E4))

    black_squares = {
        chess.square_name(square)
        for square in chess.SquareSet(starting_board.occupied_co[chess.BLACK])
    }
   
    e4 = Occupancy(white= white_squares, black= black_squares)

    assert move_finder(starting_board, e4) == chess.Move.from_uci("e2e4")
