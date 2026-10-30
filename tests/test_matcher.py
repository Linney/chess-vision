import chess
from chess_vision.matcher import move_finder
from chess_vision.models import Occupancy, Outcome, Reason, Result

def test_1e4():
    # Test the move finder recognises 1.e4

    board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    e4 = Occupancy(white={'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e4', 'f2', 'g2', 'h2'}, black={'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'})

    result = move_finder(board, e4)

    assert result.outcome == Outcome.MOVE
    assert result.moves == (chess.Move.from_uci("e2e4"),)
    assert result.reason == Reason.NONE

def test_capture():
    # Test the move finder recognises a capture

    board = chess.Board("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    cap = Occupancy(white={'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'd5', 'f2', 'g2', 'h2'}, black={'a7', 'b7', 'c7', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'})

    result = move_finder(board, cap)

    assert result.outcome == Outcome.MOVE
    assert result.moves == (chess.Move.from_uci("e4d5"),)
    assert result.reason == Reason.NONE

def test_en_passant():
    # Test the move finder to recognise en passant

    board = chess.Board("rnbqkbnr/pp2pppp/8/2pP4/8/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 3")
    ep = Occupancy(white={'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'c6', 'd2', 'f2', 'g2', 'h2'}, black={'a7', 'b7', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'})

    result = move_finder(board, ep)

    assert result.outcome == Outcome.MOVE
    assert result.moves == (chess.Move.from_uci("d5c6"),)
    assert result.reason == Reason.NONE

def test_short_castle():
    # Test the move finder to recognise short castling

    board = chess.Board("rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/2N2N2/PPPP1PPP/R1BQK2R b KQkq - 5 4")
    short_castle = Occupancy(white={'a1', 'c1', 'c3', 'd1', 'e1', 'c4', 'f3', 'h1', 'a2', 'b2', 'c2', 'd2', 'e4', 'f2', 'g2', 'h2'}, black={'a7', 'b7', 'c7', 'd7', 'e5',  'f6', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'f8', 'c5', 'g8'})

    result = move_finder(board, short_castle)

    assert result.outcome == Outcome.MOVE
    assert result.moves == (chess.Move.from_uci("e8g8"),)
    assert result.reason == Reason.NONE

def test_long_castle():
    # Test the move finder to recognise long castling

    board = chess.Board("rnbqk2r/ppp1bppp/4pn2/3p4/3P1B2/2N5/PPPQPPPP/R3KBNR w KQkq - 2 5")
    long_castle = Occupancy(white={'d1', 'c3', 'f4', 'd2', 'c1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd4', 'e2', 'f2', 'g2', 'h2'}, black={'a7', 'b7', 'c7', 'd5', 'e6', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'e7', 'f6', 'h8'})

    result = move_finder(board, long_castle)

    assert result.outcome == Outcome.MOVE
    assert result.moves == (chess.Move.from_uci("e1c1"),)
    assert result.reason == Reason.NONE

def test_promotion():
    # Test the move finder to recognise promotion, and flag it as 'Assumed Queen'

    board = chess.Board("8/3k1PK1/8/8/8/8/8/8 w - - 0 1")
    promotion = Occupancy(white={'f8', 'g7'}, black={'d7'})    
    
    result = move_finder(board, promotion)

    assert result.outcome == Outcome.MOVE
    assert result.moves == (chess.Move.from_uci("f7f8q"),)
    assert result.reason == Reason.PROMOTION_ASSUMED_QUEEN


def test_illegal_move_check_ignored():
    # Test the move finder to recognise an illegal move (check being ignored)

    board = chess.Board("rnb1kbnr/pppp1ppp/4p3/8/5P1q/2N5/PPPPP1PP/R1BQKBNR w KQkq - 2 3")
    illegal = Occupancy(white={'a1', 'c3', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e4', 'f4', 'g2', 'h2'}, black={'a7', 'b7', 'c7', 'd7', 'e6', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'h4', 'e8', 'f8', 'g8', 'h8'})

    result = move_finder(board, illegal)

    assert result.outcome == Outcome.NO_MATCH
    assert result.moves == ()  
    assert result.reason == Reason.NO_LEGAL_MATCH
 

def test_illegal_move_invalid_move():
    # Test the move finder to recognise an illegal move (invalid move)

    board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    illegal = Occupancy(white={'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e4', 'f2', 'g2', 'h2'}, black={'a7', 'b7', 'c7', 'd4', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'})

    result = move_finder(board, illegal)

    assert result.outcome == Outcome.NO_MATCH
    assert result.moves == ()    
    assert result.reason == Reason.NO_LEGAL_MATCH

def test_illegal_move_missing_piece_and_move():
    # Test the move finder to recognise a move and a missing piece

    board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    illegal = Occupancy(white={'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e4', 'f2', 'g2', 'h2'}, black={'a7', 'b7', 'c7', 'd5', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'e8', 'f8', 'g8', 'h8'})

    result = move_finder(board, illegal)

    assert result.outcome == Outcome.NO_MATCH
    assert result.moves == ()    
    assert result.reason == Reason.NO_LEGAL_MATCH

def test_illegal_move_missing_piece():
    # Test the move finder to recognise a missing piece

    board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    illegal = Occupancy(white={'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e4', 'f2', 'g2', 'h2'}, black={'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'e8', 'f8', 'g8', 'h8'})

    result = move_finder(board, illegal)

    assert result.outcome == Outcome.NO_MATCH
    assert result.moves == ()    
    assert result.reason == Reason.NO_LEGAL_MATCH

def test_no_move():
    # Test the move finder to recognise when no move has been made

    board = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    no_move = Occupancy(white={'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e4', 'f2', 'g2', 'h2'}, black={'a7', 'b7', 'c7', 'd7', 'e5', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'})

    result = move_finder(board, no_move)

    assert result.outcome == Outcome.WAIT
    assert result.moves == ()    
    assert result.reason == Reason.NO_CHANGE
