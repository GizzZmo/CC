# Cyberpunk GUI Guide

## Overview

The Cyberpunk GUI is a futuristic, neon-themed graphical interface for Cyberchess that provides an immersive chess-playing experience.

## Features

- **Neon Aesthetics**: Glowing cyan, magenta, yellow, and green colors on a dark background
- **Animated Background**: Cyberpunk-style scanline effect
- **Click-to-Move**: Intuitive point-and-click interface
- **Real-Time Updates**: Live game status and move history
- **Multiple Game Modes**: Player vs Player and Player vs Computer

## Getting Started

### Quick Start

1. **Launch the GUI**:
   ```bash
   python launcher.py
   # Then select option 1 for Cyberpunk GUI
   ```
   
   Or directly:
   ```bash
   python cyberpunk_gui.py
   ```

2. **Start a Game**:
   - Click "⚡ NEW GAME (PvP)" for Player vs Player
   - Click "🤖 VS COMPUTER" for Player vs Computer (requires Stockfish)

3. **Play Chess**:
   - Click on a piece to select it (legal moves will be highlighted in magenta)
   - Click on a highlighted square to move the piece
   - The selected piece will glow yellow

## Interface Elements

### Board Display
- **Cyan Border**: Glowing neon border around the board
- **Yellow Coordinates**: File (A-H) and rank (1-8) labels
- **Dark Squares**: Deep blue-purple (#1a1f3a)
- **Light Squares**: Lighter blue-purple (#2d3561)
- **White Pieces**: Cyan glowing pieces (♔♕♖♗♘♙)
- **Black Pieces**: Magenta glowing pieces (♚♛♜♝♞♟)

### Color Coding
- **Yellow**: Selected piece or square
- **Magenta**: Legal move destinations
- **Green**: Last move made (from and to squares)
- **Cyan**: General UI elements and text
- **Red**: Game over or error states

### System Info Panel (Magenta Border)
- **MODE**: Current game mode
- **TURN**: Whose turn it is (White/Black)
- **STATUS**: Current game state (Ready, Check, Checkmate, etc.)
- **MOVES**: Number of moves played

### Move Log Panel (Magenta Border)
- Scrollable list of all moves
- Shows standard algebraic notation
- Auto-scrolls to latest move
- Green text on dark background

### Controls Panel (Yellow Border)
- **⚡ NEW GAME (PvP)**: Start a new Player vs Player game
- **🤖 VS COMPUTER**: Play against Stockfish AI (requires configuration)
- **↻ RESET BOARD**: Reset the current game
- **✕ EXIT**: Close the application

## Game Modes

### Player vs Player
- Two human players on the same computer
- Click-based piece movement
- No time limit

### Player vs Computer
- Play against Stockfish chess engine
- Choose your color (White or Black) when starting
- Computer uses Stockfish Skill Level 5 by default
- Computer thinks for 0.5 seconds before each move

## Tips

1. **Pawn Promotion**: When a pawn reaches the opposite end, it automatically promotes to a Queen
2. **Legal Moves**: Only legal moves are shown when you select a piece
3. **Last Move**: The last move made is highlighted in green for reference
4. **Game State**: The STATUS field shows important game states like Check or Checkmate

## Troubleshooting

### GUI doesn't start
- **Issue**: "No module named 'tkinter'"
- **Solution**: Tkinter is usually included with Python. On Linux, install with:
  ```bash
  sudo apt-get install python3-tk  # Ubuntu/Debian
  sudo yum install python3-tkinter  # CentOS/RHEL
  ```

### Computer mode not available
- **Issue**: "Stockfish engine not found"
- **Solution**: 
  1. Download Stockfish from https://stockfishchess.org/download/
  2. Set the STOCKFISH_PATH environment variable:
     ```bash
     export STOCKFISH_PATH="/path/to/stockfish"
     ```
  3. Or edit `cyberpunk_gui.py` and set the path directly

### Board doesn't display correctly
- **Issue**: Pieces not showing or board looks wrong
- **Solution**: Make sure your system supports Unicode characters. Try updating your display settings.

## Technical Details

### Requirements
- Python 3.7+
- tkinter (usually comes with Python)
- python-chess library
- Optional: Stockfish engine (for vs Computer mode)

### Screen Resolution
- Optimized for 1200x800 resolution
- Fixed window size for consistent appearance

### Performance
- Lightweight and responsive
- Uses minimal system resources
- No internet connection required

## Keyboard Shortcuts

Currently, the GUI is mouse-only. Keyboard shortcuts may be added in future versions.

## Future Enhancements

Potential future features:
- Multiple board themes
- Time controls
- Move hints and suggestions
- Game saving and loading
- Undo/Redo functionality
- Sound effects
- Customizable colors

## Support

For issues or questions:
- Check the main README.md
- Visit https://github.com/GizzZmo/CC/issues
- See the launcher menu for returning to CLI mode

---

**Enjoy your cyberpunk chess experience! ⚡**
