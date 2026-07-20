# Chess AI Project

An AI-powered chess game using Python with `python-chess` for game logic and `Pygame` for the GUI.

## Setup Instructions

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `chess_ai.py` - Main AI engine with Minimax algorithm
- `chess_gui.py` - Pygame-based graphical interface
- `main.py` - Game loop and integration

## How to Run

```bash
python main.py
```

## Features

- Complete chess rules implementation (castling, en passant, pawn promotion)
- AI using Minimax with Alpha-Beta pruning
- Interactive GUI with drag-and-drop piece movement
- Move validation and game state detection (check, checkmate, stalemate)
