# Changelog

All notable changes to the Cyberchess project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-13

### Added - Phase 2 Implementation
- **Game Modes Module** (`game_modes.py`)
  - `ChessGame` base class with common functionality
  - `PlayerVsPlayerGame` for local two-player games
  - `PlayerVsComputerGame` for human vs Stockfish
  - `AIvsAIGame` for Stockfish vs Gemini matches
  
- **Interactive Game Launcher** (`play.py`)
  - Menu-driven interface for selecting game modes
  - Configuration via environment variables
  - Support for Player vs Player (no external dependencies)
  - Support for Player vs Computer with configurable difficulty
  - Support for AI vs AI mode
  
- **Feature Demonstration** (`demo.py`)
  - Demonstrates all chess rules (castling, en passant, promotion)
  - Shows game state detection (check, checkmate, stalemate)
  - Illustrates draw conditions
  - Demonstrates move generation and validation
  - Shows PGN import/export functionality
  
- **Example Assets**
  - `examples/famous_games.pgn` - Collection of three famous games:
    - The Immortal Game (1851)
    - The Evergreen Game (1852)
    - The Opera Game (1858)
  - `examples/README.md` - Documentation for example games
  
- **Configuration**
  - `config_template.py` - Template for user configuration
  - Environment variable support for STOCKFISH_PATH and GOOGLE_API_KEY
  - Multiple configuration methods (env vars, config file, direct edit)

- **Game Features**
  - Full chess rules implementation via python-chess library
  - Move history tracking in both UCI and SAN notation
  - Game state display with emoji indicators
  - Check, checkmate, and stalemate detection
  - Draw condition detection (50-move rule, threefold repetition, insufficient material)
  - PGN export for all game modes
  - Separate PGN files for different game types

### Changed
- Updated `.gitignore` to exclude all generated PGN files
- Completely rewrote README.md with:
  - Updated project structure
  - Completed features section
  - Quick start guide
  - Multiple configuration methods
  - Comprehensive usage instructions
  - Updated roadmap with Phase 2 marked complete
  - Testing procedures
  
### Technical Details
- All special chess moves (castling, en passant, promotion) supported
- Comprehensive game state management
- Clean separation of concerns with modular game modes
- Consistent error handling and user feedback
- Support for running without Stockfish (Player vs Player mode)

## [0.1.0] - 2025-12-13

### Added - Phase 1 Foundation
- Initial project structure
- `cyberchess.py` - AI vs AI chess game (Stockfish vs Gemini)
- `requirements.txt` - Python dependencies (chess, google-generativeai)
- Basic chess board representation via python-chess
- Move generation and validation
- Console-based board display
- PGN export functionality for training data
- Gemini AI integration with retry logic
- Stockfish integration with configurable skill levels

### Infrastructure
- Git repository initialization
- Basic `.gitignore` for Python projects
- Comprehensive README.md with roadmap
- MIT-style project documentation

---

## Roadmap Status

- ✅ **Phase 1**: Foundation - Complete
- ✅ **Phase 2**: Core Features - Complete
- 🔮 **Phase 3**: Advanced Features - Planned
- 🔮 **Phase 4**: Polish - Planned

## Version History

- **v0.2.0** (Current) - Phase 2 Complete: Multiple game modes, interactive launcher, demo assets
- **v0.1.0** - Phase 1 Complete: Basic AI vs AI implementation
