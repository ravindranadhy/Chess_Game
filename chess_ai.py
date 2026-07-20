import chess
import random
from typing import Optional

# Piece values for evaluation
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Position bonus tables for pawn structure
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

class ChessAI:
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.nodes_searched = 0
    
    def evaluate_board(self, board: chess.Board) -> int:
        """Evaluate the current board position."""
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -100000
            else:
                return 100000
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        score = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
            
            # Get piece value
            piece_value = PIECE_VALUES[piece.piece_type]
            
            # Get position bonus
            position_bonus = 0
            if piece.piece_type == chess.PAWN:
                position_bonus = PAWN_TABLE[square if piece.color == chess.WHITE else 63 - square]
            elif piece.piece_type == chess.KNIGHT:
                position_bonus = KNIGHT_TABLE[square if piece.color == chess.WHITE else 63 - square]
            elif piece.piece_type == chess.BISHOP:
                position_bonus = BISHOP_TABLE[square if piece.color == chess.WHITE else 63 - square]
            elif piece.piece_type == chess.ROOK:
                position_bonus = ROOK_TABLE[square if piece.color == chess.WHITE else 63 - square]
            elif piece.piece_type == chess.QUEEN:
                position_bonus = QUEEN_TABLE[square if piece.color == chess.WHITE else 63 - square]
            elif piece.piece_type == chess.KING:
                position_bonus = KING_TABLE[square if piece.color == chess.WHITE else 63 - square]
            
            if piece.color == chess.WHITE:
                score += piece_value + position_bonus
            else:
                score -= piece_value + position_bonus
        
        return score
    
    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """Minimax algorithm with alpha-beta pruning."""
        self.nodes_searched += 1
        
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)
        
        if maximizing:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Get the best move for the current position."""
        self.nodes_searched = 0
        
        if not board.legal_moves:
            return None
        
        best_move = None
        best_value = float('-inf')
        
        # Order moves for better pruning (captures first)
        legal_moves = list(board.legal_moves)
        legal_moves.sort(key=lambda move: board.is_capture(move), reverse=True)
        
        for move in legal_moves:
            board.push(move)
            value = self.minimax(board, self.depth - 1, float('-inf'), float('inf'), False)
            board.pop()
            
            if value > best_value:
                best_value = value
                best_move = move
        
        print(f"AI searched {self.nodes_searched} positions")
        return best_move
    
    def get_random_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Get a random legal move (for easier difficulty)."""
        legal_moves = list(board.legal_moves)
        if legal_moves:
            return random.choice(legal_moves)
        return None
