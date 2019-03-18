import chess

def get_board(state):
    board = chess.Board()
    board.set_fen(state)
    return board

def get_two_bishops_start():
    board = chess.Board()
    board.clear()
    board.set_piece_at(0, chess.Piece(chess.BISHOP, True))
    board.set_piece_at(1, chess.Piece(chess.BISHOP, True))
    board.set_piece_at(2, chess.Piece(chess.KING, True))
    board.set_piece_at(56, chess.Piece(chess.KING, False))
    board.turn = True
    return board

def get_rook_start():
    board = chess.Board()
    board.clear()
    board.set_piece_at(1, chess.Piece(chess.ROOK, True))
    board.set_piece_at(2, chess.Piece(chess.KING, True))
    board.set_piece_at(60, chess.Piece(chess.KING, False))
    board.turn = True
    return board

def get_pawn_start():
    board = chess.Board()
    board.clear()
    board.set_piece_at(12, chess.Piece(chess.PAWN, True))
    board.set_piece_at(4, chess.Piece(chess.KING, True))
    board.set_piece_at(60, chess.Piece(chess.KING, False))
    board.turn = True
    return board