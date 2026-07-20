import chess
import pygame
import sys
from chess_ai import ChessAI
from chess_gui import ChessGUI

def main():
    # Initialize chess board
    board = chess.Board()
    
    # Initialize AI (depth 3 for good performance)
    ai = ChessAI(depth=3)
    
    # Initialize GUI
    gui = ChessGUI()
    
    # Game settings
    play_as_white = True  # Human plays as white
    ai_enabled = True      # AI opponent enabled
    
    print("Chess AI Game")
    print("-------------")
    print("You are playing as WHITE")
    print("AI plays as BLACK")
    print("Click on pieces to select them")
    print("Click on valid moves (green dots) to move")
    print("Press 'R' to restart the game")
    print("Press 'Q' to quit")
    
    running = True
    ai_turn = False  # Human moves first (white)
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    # Restart game
                    board = chess.Board()
                    ai_turn = False  # Human moves first after restart
                    gui.selected_square = None
                    gui.valid_moves = []
                    print("Game restarted!")
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not ai_turn:
                if event.button == 1:  # Left click
                    move = gui.handle_click(event.pos, board)
                    if move:
                        # Make the move
                        board.push(move)
                        print(f"Human move: {move}")
                        
                        # Check for game over
                        if board.is_game_over():
                            if board.is_checkmate():
                                winner = "Black" if board.turn == chess.WHITE else "White"
                                print(f"Checkmate! {winner} wins!")
                            elif board.is_stalemate():
                                print("Stalemate! Draw.")
                            else:
                                print("Game over!")
                        else:
                            # AI's turn
                            if ai_enabled:
                                ai_turn = True
        
        # AI's turn
        if ai_turn and ai_enabled and not board.is_game_over():
            gui.render(board, ai_thinking=True)
            pygame.display.flip()
            
            # Get AI move
            ai_move = ai.get_best_move(board)
            
            if ai_move:
                board.push(ai_move)
                print(f"AI move: {ai_move}")
                
                # Check for game over
                if board.is_game_over():
                    if board.is_checkmate():
                        winner = "Black" if board.turn == chess.WHITE else "White"
                        print(f"Checkmate! {winner} wins!")
                    elif board.is_stalemate():
                        print("Stalemate! Draw.")
                    else:
                        print("Game over!")
            
            ai_turn = False
        
        # Render the game
        gui.render(board)
        gui.clock.tick(60)
    
    # Clean up
    gui.quit()
    sys.exit()

if __name__ == "__main__":
    main()
