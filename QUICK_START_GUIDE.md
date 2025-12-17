# Quick Start Guide - Cyberpunk Chess UI

## Overview
The enhanced Cyberpunk Chess UI now features a fully visible, auto-resizing board with improved piece contrast and comprehensive AI battle modes.

## What's New

### 🎨 Visual Improvements
- **Resizable Window**: Window now auto-sizes to 80% of your screen
- **Full Board Visibility**: No more cut-off edges - the entire board is always visible
- **Better Piece Contrast**: White pieces are now pure white, black pieces are pure black
- **Responsive Layout**: All UI elements resize smoothly with the window

### ⚙️ Settings UI
Access via the "⚙️ SETTINGS" button to configure:
- Stockfish executable path
- Gemini API key (shown as asterisks for security)
- Stockfish skill level (0-20 slider)
- Stockfish thinking time (in seconds)

### 🤖 New Game Modes

#### 1. Player vs Player (PvP)
- Click "⚡ NEW GAME (PvP)"
- Two humans play locally
- Click piece, then destination

#### 2. Player vs Computer (PvC)
- Click "🤖 VS COMPUTER"
- Choose your color
- Play against Stockfish engine
- Requires Stockfish installation

#### 3. Stockfish vs Stockfish (CvC)
- Click "🤖 STOCKFISH vs STOCKFISH"
- Watch two engines battle
- Fully automated
- Requires Stockfish installation

#### 4. Gemini vs Gemini (GvG)
- Click "🧠 GEMINI vs GEMINI"
- Watch two AI instances play
- Demonstrates LLM chess
- Requires Gemini API key

#### 5. Stockfish vs Gemini (SvG)
- Click "⚔️ STOCKFISH vs GEMINI"
- Choose which AI plays white
- Engine vs Language Model
- Requires both Stockfish and Gemini

## Installation

### 1. Install Python Dependencies
```bash
pip install chess google-generativeai
```

### 2. Get Stockfish (Optional, for computer modes)
Download from: https://stockfishchess.org/download/
Note the installation path.

### 3. Get Gemini API Key (Optional, for Gemini modes)
Get free key from: https://makersuite.google.com/app/apikey

### 4. Configure via Settings UI
Run the application:
```bash
python cyberpunk_gui.py
```

Click "⚙️ SETTINGS" and enter:
- Stockfish path (e.g., `/usr/bin/stockfish`)
- Gemini API key
- Adjust skill level and time limit as desired
- Click "💾 SAVE SETTINGS"

Alternatively, set environment variables:
```bash
export STOCKFISH_PATH="/path/to/stockfish"
export GOOGLE_API_KEY="your-api-key"
python cyberpunk_gui.py
```

## Usage

### Starting a Game
1. Launch the GUI: `python cyberpunk_gui.py`
2. Click desired game mode button
3. Follow any prompts (color selection, etc.)
4. Game starts automatically

### Playing (PvP/PvC modes)
1. Click a piece to select it
2. Legal moves highlight in magenta
3. Click destination square
4. Piece moves automatically

### Watching AI vs AI
- Games play automatically
- Move log updates in real-time
- Status shows which AI is thinking
- Game continues until completion

### Resizing
- Drag window edges to resize
- All UI elements adjust automatically
- Board remains fully visible
- Minimum size: 1000x700

### Changing Settings
1. Click "⚙️ SETTINGS"
2. Modify desired values
3. Click "💾 SAVE SETTINGS"
4. Changes apply immediately

## Keyboard Shortcuts
- Window resize: Drag edges
- Close: Click "✕ EXIT" or window close button

## Troubleshooting

### "Stockfish engine not found"
- Install Stockfish from https://stockfishchess.org/download/
- Configure path in Settings
- Common paths:
  - Linux: `/usr/bin/stockfish`
  - Mac: `/opt/homebrew/bin/stockfish`
  - Windows: `C:\Program Files\Stockfish\stockfish.exe`

### "Gemini API key not configured"
- Get API key from https://makersuite.google.com/app/apikey
- Enter in Settings dialog
- Click Save

### "Gemini library not available"
- Install: `pip install google-generativeai`
- Restart application

### Board cut off / too small
- Resize window by dragging edges
- Window should auto-size to 80% of screen on startup
- Minimum size is 1000x700

### Pieces hard to see
- White pieces now display as pure white (#ffffff)
- Black pieces now display as pure black (#000000)
- If still hard to see, check display settings

## Tips

### For Best Experience:
1. Use at least 1000x700 resolution
2. Configure both Stockfish and Gemini for all modes
3. Adjust skill level based on your preference:
   - 0-5: Beginner
   - 6-15: Intermediate
   - 16-20: Advanced
4. Increase time limit for stronger play

### For AI vs AI Games:
- Lower skill levels make games faster
- Higher skill levels make more interesting games
- Gemini may make unusual moves (it's learning!)
- Games auto-save to move log

### For Settings:
- Changes apply immediately to active engines
- Restart game for new skill level to take full effect
- Time limit affects thinking time per move
- API key stored in memory only (enter each session)

## Features Summary

✅ **Fully visible board** - no cut-off edges
✅ **Auto-resizing** - adapts to screen size
✅ **Pure white/black pieces** - maximum contrast
✅ **Settings dialog** - easy configuration
✅ **5 game modes** - PvP, PvC, CvC, GvG, SvG
✅ **Real-time updates** - move log and status
✅ **Professional UI** - cyberpunk themed
✅ **Secure input** - API key shown as asterisks

## Support

For issues or questions:
- Check this guide first
- Review CYBERPUNK_UI_IMPROVEMENTS.md for details
- See FINAL_IMPLEMENTATION_SUMMARY.md for technical info

## License

Same as main project (CC - Cyberchess)

---

**Enjoy the enhanced Cyberpunk Chess experience! ⚡**
