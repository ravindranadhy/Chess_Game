import pygame
import chess
from typing import Optional, Tuple

# Colors
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
VALID_MOVE = (100, 200, 100)
CHECK_HIGHLIGHT = (255, 100, 100)
TEXT_COLOR = (0, 0, 0)

# Board dimensions
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8
MARGIN = 40

# Unicode chess pieces
PIECE_SYMBOLS = {
    'P': '♙',
    'N': '♘',
    'B': '♗',
    'R': '♖',
    'Q': '♕',
    'K': '♔',
    'p': '♟',
    'n': '♞',
    'b': '♝',
    'r': '♜',
    'q': '♛',
    'k': '♚'
}

class ChessGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE + 2 * MARGIN, BOARD_SIZE + 2 * MARGIN))
        pygame.display.set_caption("Chess AI")
        self.clock = pygame.time.Clock()
        # Try to use a font that supports Unicode chess symbols
        self.font = pygame.font.SysFont("segoeuisymbol", 64)
        if self.font is None:
            self.font = pygame.font.SysFont("arialunicode", 64)
        if self.font is None:
            self.font = pygame.font.SysFont("dejavusans", 64)
        if self.font is None:
            self.font = pygame.font.SysFont("arial", 64)  # Fallback
            
        self.small_font = pygame.font.SysFont("arial", 36)
        
        self.selected_square = None
        self.valid_moves = []
        self.dragging_piece = None
        self.drag_pos = None
    
    def square_to_pixel(self, square: chess.Square) -> Tuple[int, int]:
        """Convert chess square to pixel coordinates (standard orientation)."""
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        x = MARGIN + file * SQUARE_SIZE
        y = MARGIN + (7 - rank) * SQUARE_SIZE
        return x, y
    
    def pixel_to_square(self, x: int, y: int) -> Optional[chess.Square]:
        """Convert pixel coordinates to chess square (standard orientation)."""
        if x < MARGIN or x > BOARD_SIZE + MARGIN or y < MARGIN or y > BOARD_SIZE + MARGIN:
            return None
        file = (x - MARGIN) // SQUARE_SIZE
        rank = 7 - (y - MARGIN) // SQUARE_SIZE
        return chess.square(file, rank)
    
    def draw_board(self, board: chess.Board):
        """Draw the chess board."""
        self.screen.fill(WHITE)
        
        # Draw squares
        for square in chess.SQUARES:
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            x = MARGIN + file * SQUARE_SIZE
            y = MARGIN + (7 - rank) * SQUARE_SIZE
            
            if (file + rank) % 2 == 0:
                color = LIGHT_SQUARE
            else:
                color = DARK_SQUARE
            
            pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            
            # Highlight selected square
            if square == self.selected_square:
                pygame.draw.rect(self.screen, HIGHLIGHT, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            
            # Highlight valid moves
            if square in self.valid_moves:
                center_x = x + SQUARE_SIZE // 2
                center_y = y + SQUARE_SIZE // 2
                pygame.draw.circle(self.screen, VALID_MOVE, (center_x, center_y), SQUARE_SIZE // 6)
        
        # Highlight king in check
        if board.is_check():
            king_square = board.king(board.turn)
            if king_square is not None:
                x, y = self.square_to_pixel(king_square)
                pygame.draw.rect(self.screen, CHECK_HIGHLIGHT, (x, y, SQUARE_SIZE, SQUARE_SIZE))
    
    def draw_pieces(self, board: chess.Board):
        """Draw chess pieces on the board."""
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
            
            # Skip the piece being dragged
            if self.dragging_piece == square:
                continue
            
            x, y = self.square_to_pixel(square)
            symbol = PIECE_SYMBOLS[piece.symbol()]
            
            # Use text for pieces (simple approach)
            text = self.font.render(symbol, True, WHITE if piece.color == chess.WHITE else BLACK)
            text_rect = text.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
            self.screen.blit(text, text_rect)
    
    def draw_dragging_piece(self):
        """Draw the piece being dragged."""
        if self.dragging_piece is not None and self.drag_pos is not None:
            symbol = '♔'  # Default, will be replaced
            text = self.font.render(symbol, True, BLACK)
            text_rect = text.get_rect(center=self.drag_pos)
            self.screen.blit(text, text_rect)
    
    def draw_info(self, board: chess.Board, ai_thinking: bool = False):
        """Draw game information."""
        # Draw turn indicator
        if board.turn == chess.WHITE:
            turn_text = "White's Turn (You)"
        else:
            turn_text = "Black's Turn (AI)"
        
        if ai_thinking:
            turn_text = "AI is thinking..."
        
        text = self.small_font.render(turn_text, True, TEXT_COLOR)
        self.screen.blit(text, (MARGIN, 10))
        
        # Draw game status
        if board.is_checkmate():
            winner = "Black" if board.turn == chess.WHITE else "White"
            status_text = f"Checkmate! {winner} wins!"
            text = self.small_font.render(status_text, True, CHECK_HIGHLIGHT)
            self.screen.blit(text, (BOARD_SIZE // 2, 10))
        elif board.is_stalemate():
            status_text = "Stalemate! Draw."
            text = self.small_font.render(status_text, True, TEXT_COLOR)
            self.screen.blit(text, (BOARD_SIZE // 2, 10))
        elif board.is_check():
            status_text = "Check!"
            text = self.small_font.render(status_text, True, CHECK_HIGHLIGHT)
            self.screen.blit(text, (BOARD_SIZE // 2, 10))
    
    def get_valid_moves(self, board: chess.Board, square: chess.Square) -> list:
        """Get valid moves for a piece at the given square."""
        if square is None:
            return []
        
        valid_moves = []
        for move in board.legal_moves:
            if move.from_square == square:
                valid_moves.append(move.to_square)
        
        return valid_moves
    
    def handle_click(self, pos: Tuple[int, int], board: chess.Board) -> Optional[chess.Move]:
        """Handle mouse click on the board."""
        square = self.pixel_to_square(pos[0], pos[1])
        
        if square is None:
            self.selected_square = None
            self.valid_moves = []
            return None
        
        # If no piece selected, select this square
        if self.selected_square is None:
            piece = board.piece_at(square)
            if piece is not None and piece.color == board.turn:
                self.selected_square = square
                self.valid_moves = self.get_valid_moves(board, square)
            return None
        
        # If same square clicked, deselect
        if square == self.selected_square:
            self.selected_square = None
            self.valid_moves = []
            return None
        
        # If valid move clicked, make the move
        if square in self.valid_moves:
            move = chess.Move(self.selected_square, square)
            
            # Handle pawn promotion
            piece = board.piece_at(self.selected_square)
            if piece and piece.piece_type == chess.PAWN:
                if chess.square_rank(square) == 7 or chess.square_rank(square) == 0:
                    move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)
            
            self.selected_square = None
            self.valid_moves = []
            return move
        
        # If different piece of same color clicked, select it
        piece = board.piece_at(square)
        if piece is not None and piece.color == board.turn:
            self.selected_square = square
            self.valid_moves = self.get_valid_moves(board, square)
            return None
        
        # Otherwise deselect
        self.selected_square = None
        self.valid_moves = []
        return None
    
    def render(self, board: chess.Board, ai_thinking: bool = False):
        """Render the complete game state."""
        self.draw_board(board)
        self.draw_pieces(board)
        self.draw_info(board, ai_thinking)
        pygame.display.flip()
    
    def quit(self):
        """Clean up pygame."""
        pygame.quit()
