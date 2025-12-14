# Cyberchess Configuration Template
# Copy this file to config.py and update with your settings

# Path to Stockfish executable
# Download from: https://stockfishchess.org/download/
# 
# Examples:
# Windows: "C:/Users/YourName/Downloads/stockfish/stockfish-windows-x86-64.exe"
# Mac (Homebrew): "/opt/homebrew/bin/stockfish"
# Mac (manual): "/usr/local/bin/stockfish"
# Linux: "/usr/games/stockfish" or "/usr/bin/stockfish"
STOCKFISH_PATH = "YOUR_STOCKFISH_PATH_HERE"

# Google Gemini API Key (only needed for AI vs AI mode)
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Default Stockfish skill level (0-20)
# 0 = Beginner, 10 = Intermediate, 20 = Grandmaster
DEFAULT_SKILL_LEVEL = 10

# Board Display Theme
# Options: 'ascii', 'unicode', 'borders'
# - ascii: Letters and dots (default, works everywhere)
# - unicode: Chess symbols (prettier, requires Unicode support)
# - borders: Unicode with borders and coordinates (most detailed)
DEFAULT_BOARD_THEME = "ascii"

# PGN file locations for saving games
PVP_GAMES_FILE = "pvp_games.pgn"
PVC_GAMES_FILE = "pvc_games.pgn"
AI_VS_AI_GAMES_FILE = "ai_vs_ai_games.pgn"
TRAINING_DATA_FILE = "training_data.pgn"
