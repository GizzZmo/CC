# CC - Cyberchess

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
  - [Building from Source](#building-from-source)
  - [Running Tests](#running-tests)
  - [Code Style](#code-style)
- [Contributing](#contributing)
- [Architecture](#architecture)
- [Roadmap](#roadmap)
- [Changelog](#changelog)
- [License](#license)
- [Support](#support)
- [Acknowledgments](#acknowledgments)

## Overview

CC (Cyberchess) is a modern chess platform designed to provide an advanced chess-playing experience. This project aims to deliver a comprehensive chess solution with features including game play, analysis, and training capabilities.

### Vision

To create an accessible, feature-rich chess platform that serves players of all skill levels while maintaining high standards of code quality and user experience.

## Features

### Implemented Features ✅
- **Chess Engine**: Full implementation of chess rules via python-chess library
  - Move generation and validation
  - Special moves: castling, en passant, pawn promotion
  - Check, checkmate, and stalemate detection
  - Draw conditions: 50-move rule, threefold repetition, insufficient material
- **Game Modes**: 
  - ✅ Player vs Player (local)
  - ✅ Player vs Computer (Stockfish)
  - ✅ AI vs AI (Stockfish vs Gemini) with configurable/randomized color assignment
- **Advanced Analysis**: 
  - ✅ Post-game engine analysis with move evaluations
  - ✅ Automatic detection of mistakes, blunders, and brilliant moves
  - ✅ Move-by-move centipawn evaluation
  - ✅ Average position evaluation
- **Time Controls**: 
  - ✅ Blitz mode (5 minutes)
  - ✅ Rapid mode (10 minutes)
  - ✅ Classical mode (30 minutes)
  - ✅ Custom time controls with increment support
  - ✅ Automatic timeout detection
- **Opening Book**: 
  - ✅ 12+ popular chess openings with ECO codes
  - ✅ Opening identification during play
  - ✅ Book move suggestions
  - ✅ Interactive opening explorer
- **Training Mode**: 
  - ✅ Chess puzzles with tactical exercises
  - ✅ 8+ built-in puzzles covering various themes
  - ✅ Difficulty levels: Easy, Medium, Hard
  - ✅ Interactive solving with hints
  - ✅ Puzzle themes: Forks, Pins, Mate patterns, Sacrifices
- **Game Analysis**: 
  - ✅ Move history tracking (UCI and SAN notation)
  - ✅ Game state display
  - ✅ PGN import/export for game storage and replay
- **Board Display Themes**: 
  - ✅ ASCII theme (letters and dots) - Default, works everywhere
  - ✅ Unicode theme (chess symbols) - Prettier, requires Unicode support
  - ✅ Borders theme (Unicode with borders and coordinates) - Most detailed
  - ✅ Theme selection available in all game modes
- **Interactive UI**: Console-based with clear board visualization
- **Example Assets**: Famous chess games collection for learning
- **Testing**: Comprehensive automated test suite
- **Build System**: Automated packaging and distribution

### Planned Features 🔮
- **Online Features**: 
  - Online multiplayer support (requires server infrastructure)
  - User accounts and rating system (requires database)
- **UI Enhancements**:
  - Graphical UI - web or desktop (large scope project)
  - Mobile responsiveness

## Project Structure

```
CC/
├── README.md              # This file - comprehensive project documentation
├── CHANGELOG.md           # Version history and change log
├── CONTRIBUTING.md        # Contribution guidelines
├── cyberchess.py          # Legacy chess game (Stockfish vs Gemini)
├── game_modes.py          # Game mode implementations (PvP, PvC, AI vs AI)
├── play.py                # Main interactive game launcher
├── demo.py                # Feature demonstration script
├── opening_book.py        # Opening book database and explorer
├── puzzles.py             # Chess puzzle trainer
├── test_features.py       # Automated test suite
├── build.py               # Build and packaging script
├── requirements.txt       # Python dependencies
├── config_template.py     # Configuration template
├── .gitignore            # Git ignore rules
├── examples/             # Example games and assets
│   ├── README.md         # Examples documentation
│   └── famous_games.pgn  # Collection of famous chess games
├── build/                # Build artifacts (generated)
├── dist/                 # Distribution packages (generated)
└── .git/                 # Git repository metadata
```

*Updated: December 15, 2025 - Phase 3 & 4 Complete*

## Getting Started

### Quick Start

For the simplest experience without any external dependencies:

```bash
# Install dependencies
pip install -r requirements.txt

# Try Player vs Player mode (no Stockfish needed!)
python play.py
# Select option 1 for Player vs Player
```

For the full experience with AI opponents, continue with Prerequisites below.

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Stockfish chess engine (optional, for Player vs Computer and AI vs AI modes)
  - Download from [stockfishchess.org](https://stockfishchess.org/download/)
- Google Gemini API Key (optional, only for AI vs AI mode)
  - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation

```bash
# Clone the repository
git clone https://github.com/GizzZmo/CC.git
cd CC

# Install Python dependencies
pip install -r requirements.txt

# Download Stockfish chess engine from https://stockfishchess.org/download/
# Note the path to the stockfish executable

# (Optional) Create configuration file from template
cp config_template.py config.py

# Configure the application by setting environment variables OR editing play.py/cyberchess.py:
# - STOCKFISH_PATH: Path to your stockfish executable
# - GOOGLE_API_KEY: Your Google Gemini API key (only for AI vs AI mode)
```

### Configuration

You can configure Cyberchess in multiple ways:

1. **Environment Variables** (Recommended):
   ```bash
   export STOCKFISH_PATH="/path/to/stockfish"
   export GOOGLE_API_KEY="your-gemini-api-key"
   ```

2. **Configuration File**:
   ```bash
   cp config_template.py config.py
   # Edit config.py with your settings
   ```

3. **Direct Script Modification**:
   Edit the configuration constants at the top of `play.py` or `cyberchess.py`

**Note**: Only `STOCKFISH_PATH` is required for Player vs Player and Player vs Computer modes. `GOOGLE_API_KEY` is only needed for AI vs AI mode.

## Usage

### Interactive Game Launcher

Run the main interactive launcher to choose from different game modes:

```bash
python play.py
```

This provides a menu with options:
1. **Player vs Player** - Two humans playing locally
   - Choose board display theme (ASCII, Unicode, or Borders)
   - Optional time controls (Blitz, Rapid, Classical, or Custom)
2. **Player vs Computer** - Play against Stockfish AI
   - Choose board display theme
   - Choose your color and difficulty level (0-20)
   - Optional time controls
   - Post-game analysis with engine evaluation
3. **AI vs AI** - Watch Stockfish play against Gemini AI
   - Choose board display theme
   - Choose color assignment: classic, reversed, or random (recommended for training)
   - Configurable Stockfish skill level
4. **Puzzle Trainer** - Solve tactical chess puzzles
   - Multiple difficulty levels
   - Interactive solving with hints
   - Various tactical themes
5. **Opening Book Explorer** - Learn chess openings
   - View all 12+ openings in database
   - Interactive opening practice
   - Opening identification
6. Exit

### Board Display Themes

Cyberchess supports three board display themes:

- **ASCII** (default): Uses letters and dots, works on all terminals
  ```
  r n b q k b n r
  p p p p p p p p
  . . . . . . . .
  ```

- **Unicode**: Uses chess symbols for a prettier display
  ```
  ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
  ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
  ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
  ```

- **Borders**: Unicode with borders and coordinates for detailed view
  ```
    -----------------
  8 |♖|♘|♗|♕|♔|♗|♘|♖|
    -----------------
  7 |♙|♙|♙|♙|♙|♙|♙|♙|
    -----------------
     a b c d e f g h
  ```

You can select your preferred theme when starting any game mode. The theme can also be configured in `config.py` by setting `DEFAULT_BOARD_THEME`.

### Legacy Mode

To run a single AI vs AI game (legacy mode) with randomized colors:

```bash
python cyberchess.py
```

This runs one game between Stockfish and Gemini AI with randomly assigned colors and saves it to `training_data.pgn`.

### Feature Demonstration

To see all implemented features in action:

```bash
python demo.py
```

This demonstrates:
- Basic chess moves
- Special moves (castling, en passant, promotion)
- Game states (check, checkmate, stalemate)
- Draw conditions
- Move generation and validation
- PGN import/export

### Game Output

Games are automatically saved to PGN files:
- `pvp_games.pgn` - Player vs Player games
- `pvc_games.pgn` - Player vs Computer games
- `ai_vs_ai_games.pgn` - AI vs AI games
- `training_data.pgn` - Legacy mode games

The program displays:
- Current board state after each move
- Move history in algebraic notation
- Game status (check, checkmate, stalemate, draws)
- Final result (1-0, 0-1, or 1/2-1/2)

## Development

### Building from Source

No build process is required for this Python project. Simply install dependencies and run:

```bash
pip install -r requirements.txt
python play.py
```

### Running Tests

```bash
# Run the automated test suite
python test_features.py

# Run the feature demonstration to validate all functionality
python demo.py

# Test the opening book
python opening_book.py

# Test the puzzle trainer
python puzzles.py

# Play test games to verify game modes work correctly
python play.py
```

Automated test suite validates:
- Time control functionality
- Post-game analysis
- Board display with time
- Move history tracking
- Game state detection
- PGN export

### Code Style

This project follows Python best practices:
- **PEP 8**: Python style guide compliance
- **Docstrings**: All functions and classes documented
- **Descriptive Names**: Clear, self-documenting code
- **Modular Design**: Separation of concerns
- **Consistent Formatting**: Uniform code structure

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed style guidelines.

## Contributing

Contributions to CC are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contributing Guide

1. **Fork the Repository**: Create your own fork of the project
2. **Create a Feature Branch**: `git checkout -b feature/your-feature-name`
3. **Make Your Changes**: Implement your feature or bug fix
4. **Write Tests**: Ensure your changes are tested (run `python demo.py`)
5. **Update Documentation**: Keep README.md and CHANGELOG.md current
6. **Commit Your Changes**: `git commit -m 'Add some feature'`
7. **Push to Branch**: `git push origin feature/your-feature-name`
8. **Open a Pull Request**: Submit your changes for review

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Architecture

### Design Principles
- **Modularity**: Components should be loosely coupled and highly cohesive
- **Scalability**: Design for growth in users and features
- **Performance**: Optimize for fast move calculation and responsive UI
- **Testability**: Write code that is easy to test
- **Maintainability**: Keep code clean, documented, and well-structured

### Technology Stack

**Current Stack**:
- **Language**: Python 3.7+
- **Chess Library**: python-chess (board representation, move generation, and validation)
- **AI Integration**: Google Gemini 1.5 Flash (for AI opponent)
- **Chess Engine**: Stockfish (for strong AI play)
- **UI**: Console-based (text output)

## Roadmap

### Phase 1: Foundation ✅ (Completed)
- [x] Choose technology stack
- [x] Implement basic chess board representation
- [x] Implement move generation and validation
- [x] Create basic UI for board display

### Phase 2: Core Features ✅ (Completed)
- [x] Implement full chess rules (castling, en passant, promotion)
- [x] Add Player vs Player mode
- [x] Add Player vs Computer mode
- [x] Implement game state management (check, checkmate, stalemate)
- [x] Add move history and notation (UCI and SAN)
- [x] PGN import/export functionality
- [x] Multiple game modes with menu launcher
- [x] Example games and demo assets

### Phase 3: Advanced Features ✅ (Completed)
- [x] Configurable/randomized AI color assignment in AI vs AI mode
- [x] Post-game engine analysis with evaluations
- [x] Opening book integration (12+ openings with ECO codes)
- [x] Chess puzzles and training mode (8+ puzzles)
- [x] Time controls (Blitz, Rapid, Classical)
- [ ] Online multiplayer support (deferred - requires server infrastructure)
- [ ] User accounts and rating system (deferred - requires database)

### Phase 4: Polish ✅ (Completed)
- [ ] Graphical UI (web or desktop) (deferred - large scope)
- [x] Multiple board display themes
- [x] Performance optimization
- [ ] Mobile responsiveness (deferred - requires GUI)
- [x] Comprehensive automated testing
- [x] Documentation improvements
- [x] Build system and distribution artifacts

## Changelog

For a detailed history of changes, see [CHANGELOG.md](CHANGELOG.md).

### Recent Changes

#### v0.4.1 (2025-12-14)
- ✅ Added board display themes (ASCII, Unicode, Borders)
- ✅ Theme selection integrated into all game modes
- ✅ Dynamic theme switching during games
- ✅ Theme configuration in config template

#### v0.4.0 (2025-12-13) - Phase 3 & 4 Complete
- ✅ Added post-game engine analysis with move evaluations
- ✅ Added time controls (Blitz, Rapid, Classical, Custom)
- ✅ Added opening book with 12+ popular openings
- ✅ Added chess puzzle trainer with 8+ tactical puzzles
- ✅ Added comprehensive automated test suite
- ✅ Added build system for creating distribution packages
- ✅ Enhanced documentation with installation guide
- ✅ Performance optimizations throughout codebase
- ✅ All Phase 3 and Phase 4 feasible features implemented

## License

The license for this project will be specified as development progresses. Please check back later for licensing information.

## Support

For support, questions, or feedback:
- **Issues**: [GitHub Issues](https://github.com/GizzZmo/CC/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GizzZmo/CC/discussions)

## Acknowledgments

- Chess programming community for insights and best practices
- Open source chess engines and libraries for inspiration
- All contributors who help make this project better

---

**Status**: 🎉 Phase 3 & 4 Complete - Advanced Features Implemented!

*Last Updated: December 15, 2025*
