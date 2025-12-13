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
  - ✅ AI vs AI (Stockfish vs Gemini)
- **Game Analysis**: 
  - ✅ Move history tracking (UCI and SAN notation)
  - ✅ Game state display
  - ✅ PGN import/export for game storage and replay
- **Interactive UI**: Console-based with clear board visualization
- **Example Assets**: Famous chess games collection for learning

### Planned Features 🔮
- **Advanced Analysis**: Post-game engine analysis with move suggestions
- **Training Mode**: Chess puzzles and tactical exercises  
- **Opening Book**: Database of common chess openings

## Project Structure

```
CC/
├── README.md              # This file - comprehensive project documentation
├── cyberchess.py          # Legacy chess game (Stockfish vs Gemini)
├── game_modes.py          # Game mode implementations (PvP, PvC, AI vs AI)
├── play.py                # Main interactive game launcher
├── demo.py                # Feature demonstration script
├── requirements.txt       # Python dependencies
├── config_template.py     # Configuration template
├── .gitignore            # Git ignore rules
├── examples/             # Example games and assets
│   ├── README.md         # Examples documentation
│   └── famous_games.pgn  # Collection of famous chess games
└── .git/                 # Git repository metadata
```

*Updated: December 2025 - Phase 2 Complete*

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
2. **Player vs Computer** - Play against Stockfish AI
3. **AI vs AI** - Watch Stockfish play against Gemini AI
4. Exit

### Legacy Mode

To run a single AI vs AI game (legacy mode):

```bash
python cyberchess.py
```

This runs one game between Stockfish (White) and Gemini AI (Black) and saves it to `training_data.pgn`.

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
# Run the feature demonstration to validate all functionality
python demo.py

# Play test games to verify game modes work correctly
python play.py
```

Automated test suite will be added in future phases.

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

### Phase 3: Advanced Features (Planned)
- [ ] Post-game engine analysis with evaluations
- [ ] Opening book integration
- [ ] Chess puzzles and training mode
- [ ] Time controls (Blitz, Rapid, Classical)
- [ ] Online multiplayer support
- [ ] User accounts and rating system

### Phase 4: Polish (Planned)
- [ ] Graphical UI (web or desktop)
- [ ] Multiple themes and customization
- [ ] Performance optimization
- [ ] Mobile responsiveness
- [ ] Comprehensive automated testing
- [ ] Documentation improvements

## Changelog

For a detailed history of changes, see [CHANGELOG.md](CHANGELOG.md).

### Recent Changes (v0.2.0 - Phase 2 Complete)
- ✅ Added Player vs Player game mode
- ✅ Added Player vs Computer game mode
- ✅ Added interactive game launcher with menu
- ✅ Implemented full chess rules (castling, en passant, promotion)
- ✅ Enhanced game state management (check, checkmate, stalemate, draws)
- ✅ Added move history tracking (UCI and SAN notation)
- ✅ Created demo script showcasing all features
- ✅ Added famous games collection as example assets
- ✅ Created comprehensive documentation

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

**Status**: 🎉 Phase 2 Complete - Core Features Implemented

*Last Updated: December 2025*
