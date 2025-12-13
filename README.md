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
- [License](#license)
- [Support](#support)
- [Acknowledgments](#acknowledgments)

## Overview

CC (Cyberchess) is a modern chess platform designed to provide an advanced chess-playing experience. This project aims to deliver a comprehensive chess solution with features including game play, analysis, and training capabilities.

### Vision

To create an accessible, feature-rich chess platform that serves players of all skill levels while maintaining high standards of code quality and user experience.

## Features

### Planned Features
- **Chess Engine**: Implementation of standard chess rules and move validation
- **Game Modes**: 
  - Player vs Player
  - Player vs Computer
  - Online Multiplayer
- **Game Analysis**: Post-game analysis with move suggestions and evaluations
- **Training Mode**: Chess puzzles and tactical exercises
- **Opening Book**: Database of common chess openings
- **Game History**: Save and replay previous games
- **Multiple Board Themes**: Customizable board and piece designs
- **Time Controls**: Support for various time formats (Blitz, Rapid, Classical)
- **Rating System**: Elo-based player rating system

## Project Structure

```
CC/
├── README.md           # This file - comprehensive project documentation
└── .git/              # Git repository metadata
```

*Note: Project structure will be updated as development progresses.*

## Getting Started

### Prerequisites

Prerequisites will be documented as the project develops. Expected requirements may include:
- A modern web browser (for web-based version)
- Node.js and npm (if using JavaScript/TypeScript)
- Python 3.x (if using Python)
- Or other runtime environments based on final technology stack

### Installation

Installation instructions will be provided once the project has deployable components.

```bash
# Clone the repository
git clone https://github.com/GizzZmo/CC.git
cd CC

# Further installation steps to be documented
```

### Configuration

Configuration guidelines will be added as the project develops configuration requirements.

## Usage

Usage documentation will be provided as features are implemented.

## Development

### Building from Source

Build instructions will be documented once the build system is established.

### Running Tests

Testing procedures will be documented once the test suite is created.

### Code Style

Code style guidelines will be established based on the chosen programming language and framework:
- Follow language-specific best practices
- Maintain consistent formatting
- Write clear, self-documenting code
- Include comprehensive comments for complex logic
- Write unit tests for all new features

## Contributing

Contributions to CC are welcome! Here's how you can help:

1. **Fork the Repository**: Create your own fork of the project
2. **Create a Feature Branch**: `git checkout -b feature/your-feature-name`
3. **Make Your Changes**: Implement your feature or bug fix
4. **Write Tests**: Ensure your changes are covered by tests
5. **Commit Your Changes**: `git commit -m 'Add some feature'`
6. **Push to Branch**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**: Submit your changes for review

### Contribution Guidelines
- Follow the existing code style
- Write clear commit messages
- Update documentation as needed
- Ensure all tests pass before submitting
- Be respectful and constructive in discussions

## Architecture

### Design Principles
- **Modularity**: Components should be loosely coupled and highly cohesive
- **Scalability**: Design for growth in users and features
- **Performance**: Optimize for fast move calculation and responsive UI
- **Testability**: Write code that is easy to test
- **Maintainability**: Keep code clean, documented, and well-structured

### Technology Stack
The technology stack will be determined and documented as development progresses.

## Roadmap

### Phase 1: Foundation (Planned)
- [ ] Choose technology stack
- [ ] Implement basic chess board representation
- [ ] Implement move generation and validation
- [ ] Create basic UI for board display

### Phase 2: Core Features (Planned)
- [ ] Implement full chess rules (castling, en passant, promotion)
- [ ] Add Player vs Player mode
- [ ] Implement game state management (check, checkmate, stalemate)
- [ ] Add move history and notation

### Phase 3: Advanced Features (Planned)
- [ ] Integrate chess engine for AI opponent
- [ ] Add game analysis features
- [ ] Implement online multiplayer
- [ ] Add user accounts and rating system

### Phase 4: Polish (Planned)
- [ ] Multiple themes and customization
- [ ] Performance optimization
- [ ] Mobile responsiveness
- [ ] Comprehensive testing and bug fixes

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

**Status**: 🚧 Project in planning phase

*Last Updated: December 2025*
# CC
Cyberchess


import chess
import chess.engine
import chess.pgn
import google.generativeai as genai
import time
import datetime

# --- CONFIGURATION ---
# REPLACE THIS with the path to your downloaded stockfish file
# Windows example: "C:/Users/Jon/Downloads/stockfish/stockfish-windows-x86-64.exe"
# Mac example: "/opt/homebrew/bin/stockfish"
STOCKFISH_PATH = "YOUR_STOCKFISH_PATH_HERE" 

# REPLACE THIS with your Google Gemini API Key
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Setup Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Using Flash for speed

def get_gemini_move(board, retries=3):
    """
    Sends the board state to Gemini and asks for a move.
    Includes a retry loop for illegal moves.
    """
    legal_moves = [move.uci() for move in board.legal_moves]
    
    # We provide the FEN (Board State) and the list of legal moves to help Gemini
    # ground its reasoning and avoid hallucinations.
    prompt = f"""
    You are playing a game of Chess against Stockfish. You are playing Black.
    
    Current Board Position (FEN): {board.fen()}
    
    Here is the list of legally possible moves you can make:
    {', '.join(legal_moves)}
    
    Your goal is to survive and learn. Analyze the board.
    Pick the best move from the legal list above.
    
    IMPORTANT: Reply ONLY with the move in UCI format (e.g., e7e5). Do not write any other text.
    """

    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            move_str = response.text.strip().replace("\n", "").replace(" ", "")
            
            # clean up common formatting issues if Gemini adds markdown
            move_str = move_str.replace("`", "") 

            move = chess.Move.from_uci(move_str)

            if move in board.legal_moves:
                return move
            else:
                print(f" > Gemini tried illegal move: {move_str}. Retrying...")
                # Add feedback to the next prompt (In-Context Learning)
                prompt += f"\n\nERROR: {move_str} is not a legal move. Please choose strictly from the provided list."
        
        except Exception as e:
            print(f" > Error parsing Gemini response: {e}")
            prompt += f"\n\nERROR: Invalid format. Please reply ONLY with the move string (e.g., e7e5)."

    # If Gemini fails 3 times, we make a random move to keep the game going (fallback)
    print(" > Gemini failed to produce a legal move. Making random move.")
    import random
    return random.choice(list(board.legal_moves))

def play_game():
    # Initialize Board and Stockfish
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    
    # Set Stockfish skill level (Lower it initially so Gemini has a chance)
    # Skill level 0 is weak, 20 is Grandmaster. Let's start at 5.
    engine.configure({"Skill Level": 5})

    print("--- CYBERCHESS: Stockfish (White) vs Gemini (Black) ---")
    
    game_moves = []
    
    while not board.is_game_over():
        print(f"\nMove {board.fullmove_number}")
        print(board)
        
        if board.turn == chess.WHITE:
            # --- STOCKFISH TURN ---
            print("Stockfish is thinking...")
            # Limit Stockfish to 0.1 seconds so it plays fast
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)
            print(f"Stockfish played: {result.move.uci()}")
            game_moves.append(result.move)
            
        else:
            # --- GEMINI TURN ---
            print("Gemini is thinking...")
            move = get_gemini_move(board)
            board.push(move)
            print(f"Gemini played: {move.uci()}")
            game_moves.append(move)

    # --- GAME OVER ---
    print("\n--- GAME OVER ---")
    print(f"Result: {board.result()}")
    
    engine.quit()
    return board

def save_game_data(board):
    """
    Saves the game to a PGN file. 
    This is the dataset we will use later to FINE TUNE Gemini.
    """
    pgn_game = chess.pgn.Game.from_board(board)
    pgn_game.headers["Event"] = "Cyberchess Dojo"
    pgn_game.headers["White"] = "Stockfish Level 5"
    pgn_game.headers["Black"] = "Gemini 1.5 Flash"
    pgn_game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")

    with open("training_data.pgn", "a") as f:
        f.write(str(pgn_game) + "\n\n")
    print("Game saved to 'training_data.pgn'")

if __name__ == "__main__":
    # In a real app, you would loop this: while True: play_game()
    finished_board = play_game()
    save_game_data(finished_board)
