# Changelog

All notable changes to the Cyberchess project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-12-15

### Added
- **Cyberpunk GUI** - Graphical user interface with futuristic neon theme
  - Neon color scheme with glowing effects (cyan, magenta, yellow, green)
  - Click-to-move interface for intuitive piece movement
  - Real-time game status and move history display
  - Animated background with cyberpunk aesthetics
  - Support for Player vs Player and Player vs Computer modes
  - Unicode chess piece symbols with color-coded players
  - Legal move highlighting and last move indicators
  - Full implementation in `cyberpunk_gui.py` using tkinter
  
- **Main Launcher** (`launcher.py`)
  - Unified entry point for choosing between GUI and CLI interfaces
  - ASCII art branding for Cyberchess
  - Menu-driven interface for mode selection
  - Graceful error handling for missing dependencies
  
- **Cyberpunk GUI Guide** (`CYBERPUNK_GUI_GUIDE.md`)
  - Comprehensive documentation for the GUI interface
  - Feature descriptions and usage instructions
  - Troubleshooting guide for common issues
  - Technical details and requirements
  
- **GUI Preview** (`gui_preview.html`)
  - HTML demo showcasing the cyberpunk aesthetic
  - Visual preview of the GUI's neon theme
  - Animated background effects

### Changed
- Updated README.md to reflect GUI implementation completion
- Marked "Graphical UI" as completed in Phase 4 roadmap
- Enhanced project structure documentation with GUI files
- Updated usage instructions to include both GUI and CLI options

### Technical Details
- GUI built with Python's tkinter library (cross-platform compatible)
- Integrates with existing chess engine and Stockfish
- Maintains consistent game logic with CLI version
- Supports optional Stockfish engine for computer opponent

## [0.4.1] - 2025-12-14

### Added
- **Board Display Themes**
  - Three display themes for board visualization
  - ASCII theme (letters and dots) - Default, works on all terminals
  - Unicode theme (chess symbols) - Prettier display with Unicode support
  - Borders theme (Unicode with borders and coordinates) - Most detailed view
  - Theme selection integrated into all game modes (PvP, PvC, AI vs AI)
  - `set_theme()` method for dynamic theme switching during games
  - `list_themes()` class method to display available themes
  - Theme configuration added to `config_template.py`
  - Interactive theme selection in `play.py` for all game modes

### Changed
- Updated `ChessGame` base class to accept theme parameter
- Modified `display_board()` method to use selected theme
- Updated `PlayerVsPlayerGame`, `PlayerVsComputerGame`, and `AIvsAIGame` to support theme parameter
- Enhanced configuration template with `DEFAULT_BOARD_THEME` setting
- Updated README.md with board theme documentation and usage examples

## [0.4.0] - 2025-12-13

### Added - Phase 3 & 4 Implementation (Complete)

#### Phase 3: Advanced Features
- **Post-Game Engine Analysis**
  - Move-by-move evaluation in centipawns
  - Automatic detection of mistakes (>50 cp loss), blunders (>100 cp loss), and brilliant moves (>100 cp gain)
  - Average position evaluation calculation
  - Optional analysis prompt after Player vs Computer games
  - Configurable analysis depth (default: 15 ply)
  
- **Time Controls**
  - Blitz mode: 5 minutes per player
  - Rapid mode: 10 minutes per player
  - Classical mode: 30 minutes per player
  - Custom time controls with increment support
  - Real-time clock display during games
  - Automatic timeout detection and handling
  - Time tracking for both Player vs Player and Player vs Computer modes
  
- **Opening Book Integration**
  - Database of 12+ popular chess openings with ECO codes
  - Openings included: Italian Game, Ruy Lopez, Sicilian Defense, French Defense, 
    Caro-Kann, Queen's Gambit, King's Indian, English Opening, Nimzo-Indian, 
    Scandinavian, Pirc Defense, London System
  - Opening identification during gameplay
  - Book move suggestions based on position
  - Interactive opening explorer mode
  - Display opening name and ECO code
  
- **Chess Puzzle Trainer**
  - Collection of 8+ tactical puzzles
  - Difficulty levels: Easy, Medium, Hard
  - Tactical themes: Back Rank Mate, Fork, Removing the Defender, Double Attack, 
    Mate in 2, Sacrifice, Attacking the King
  - Interactive puzzle solving with move validation
  - Hint system using Stockfish analysis
  - Solution display option
  - Training session mode for multiple puzzles
  - Puzzle filtering by difficulty

#### Phase 4: Polish
- **Automated Testing**
  - Comprehensive test suite (`test_features.py`)
  - Tests for time controls, game analysis, board display, move history, game states, and PGN export
  - 6 automated test cases covering all major features
  - Console output validation
  
- **Build System**
  - Automated build script (`build.py`)
  - Creates ZIP and tar.gz distribution packages
  - Generates SHA256 checksums for verification
  - Produces release notes automatically
  - Creates installation guide
  - Version tracking and metadata
  
- **Documentation Improvements**
  - Updated README.md with all new features
  - Created INSTALL.md with detailed setup instructions
  - Enhanced code documentation and docstrings
  - Added release notes template
  - Comprehensive feature descriptions
  
- **Performance Optimizations**
  - Efficient move generation in opening book
  - Optimized engine analysis with configurable depth
  - Improved board display performance
  - Better time tracking accuracy

### Changed
- Enhanced `ChessGame` base class with time control support
- Updated all game mode classes to support optional time controls
- Modified board display to show remaining time when time controls are enabled
- Extended menu in `play.py` to include Puzzle Trainer and Opening Book Explorer
- Improved error handling across all modules
- Better separation of concerns between game logic and UI

### Technical Details
- Added `time` module import for accurate time tracking
- Introduced `OpeningBook` class in new `opening_book.py` module
- Introduced `PuzzleTrainer` and `ChessPuzzle` classes in new `puzzles.py` module
- Added comprehensive type hints using `typing` module
- Extended `game_modes.py` with analysis and time control methods
- Created modular, testable code structure
- Maintained backward compatibility with existing features

### Files Added
- `opening_book.py` - Opening book database and functionality
- `puzzles.py` - Puzzle trainer implementation
- `test_features.py` - Automated test suite
- `build.py` - Build and packaging script

## [0.3.0] - 2025-12-13

### Added - Phase 3 (First Feature)
- **Configurable/Randomized AI Color Assignment**
  - AI vs AI mode now supports choosing which AI plays which color
  - Three options: Classic (Stockfish White), Reversed (Gemini White), or Random (recommended)
  - Random color assignment by default for more diverse training data
  - Updated PGN export to correctly reflect actual player colors
  - Legacy mode (`cyberchess.py`) now randomizes colors by default
  
### Changed
- `AIvsAIGame.__init__()` now accepts optional `stockfish_color` parameter
- `play_ai_vs_ai()` in `play.py` now prompts for color assignment preference
- Updated game display to show which AI is playing which color
- Updated documentation to reflect new capabilities

### Technical Details
- Maintains backward compatibility (color defaults to random if not specified)
- Gemini prompts already supported dynamic color assignment
- PGN headers now correctly show White and Black players based on actual game setup

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
- ✅ **Phase 3**: Advanced Features - Complete (5/7 features, 2 deferred)
- ✅ **Phase 4**: Polish - Complete (5/6 features, 1 deferred)
- 🔮 **Future**: Online features and mobile GUI (requires infrastructure)

## Version History

- **v0.5.0** (Current) - Cyberpunk GUI: Desktop graphical interface with neon theme
- **v0.4.1** - Board Display Themes: Multiple visualization options
- **v0.4.0** - Phase 3 & 4 Complete: All feasible advanced features and polish
- **v0.3.0** - Phase 3 Started: Configurable AI color assignment
- **v0.2.0** - Phase 2 Complete: Multiple game modes, interactive launcher, demo assets
- **v0.1.0** - Phase 1 Complete: Basic AI vs AI implementation

## Deferred Features

The following features have been deferred as they require external infrastructure:
- **Online Multiplayer**: Requires server infrastructure and networking code
- **User Accounts and Rating System**: Requires database and authentication system
- **Mobile Responsiveness**: Requires mobile-specific GUI implementation
