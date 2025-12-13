# Contributing to Cyberchess

Thank you for your interest in contributing to Cyberchess! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## Getting Started

1. **Fork the Repository**
   ```bash
   # Click the "Fork" button on GitHub
   # Then clone your fork
   git clone https://github.com/YOUR_USERNAME/CC.git
   cd CC
   ```

2. **Set Up Development Environment**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # (Optional) Set up Stockfish for testing
   # Download from https://stockfishchess.org/download/
   export STOCKFISH_PATH="/path/to/stockfish"
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager
- (Optional) Stockfish chess engine
- (Optional) Google Gemini API key

### Running in Development Mode

```bash
# Test your changes with the demo
python demo.py

# Test the interactive launcher
python play.py

# Test the legacy mode
python cyberchess.py
```

## Project Structure

```
CC/
├── cyberchess.py         # Legacy AI vs AI implementation
├── game_modes.py         # Core game mode classes
├── play.py               # Interactive game launcher
├── demo.py              # Feature demonstration
├── config_template.py   # Configuration template
├── examples/            # Example games and assets
│   ├── famous_games.pgn
│   └── README.md
├── requirements.txt     # Python dependencies
├── README.md           # Main documentation
├── CHANGELOG.md        # Version history
└── CONTRIBUTING.md     # This file
```

### Key Modules

- **`game_modes.py`**: Contains game mode implementations
  - `ChessGame` - Base class with common functionality
  - `PlayerVsPlayerGame` - Local two-player mode
  - `PlayerVsComputerGame` - Human vs AI mode
  - `AIvsAIGame` - AI vs AI mode

- **`play.py`**: Interactive launcher with menu system

- **`demo.py`**: Demonstrates all implemented features

## Making Changes

### Code Style Guidelines

1. **Python Style**
   - Follow PEP 8 guidelines
   - Use descriptive variable names
   - Add docstrings to functions and classes
   - Keep functions focused and concise

2. **Documentation**
   - Update README.md if adding new features
   - Add docstrings to new functions/classes
   - Update CHANGELOG.md with your changes
   - Include code comments for complex logic

3. **Naming Conventions**
   - Classes: `PascalCase` (e.g., `ChessGame`)
   - Functions/methods: `snake_case` (e.g., `get_player_move`)
   - Constants: `UPPER_CASE` (e.g., `STOCKFISH_PATH`)
   - Private methods: `_leading_underscore` (e.g., `_validate_move`)

### Adding New Features

When adding new features:

1. **Check the Roadmap**: Align with planned features in README.md
2. **Create a Module**: For substantial features, create a new file
3. **Write Tests**: Add validation in demo.py or create test scripts
4. **Update Documentation**: 
   - Add usage examples to README.md
   - Update CHANGELOG.md
   - Add docstrings to new code

### Example: Adding a New Game Mode

```python
# In game_modes.py

class YourNewGameMode(ChessGame):
    """Description of your game mode."""
    
    def __init__(self, param1, param2):
        super().__init__()
        self.param1 = param1
        self.param2 = param2
        
    def play(self):
        """Play a full game in this mode."""
        # Implementation here
        pass
```

Then update `play.py` to include your new mode in the menu.

## Testing

### Manual Testing

```bash
# Run the demo to verify all features work
python demo.py

# Test each game mode
python play.py
# Select each option (1, 2, 3) and verify functionality
```

### Test Checklist

Before submitting changes, verify:

- [ ] Code runs without errors
- [ ] All game modes still work
- [ ] Demo script completes successfully
- [ ] README examples are accurate
- [ ] No breaking changes to existing functionality
- [ ] PGN files are generated correctly
- [ ] Game state detection works (check, checkmate, stalemate)
- [ ] Move history displays correctly

### Future: Automated Testing

Automated tests will be added in Phase 4. For now, manual testing is required.

## Submitting Changes

### Commit Guidelines

1. **Write Clear Commit Messages**
   ```
   Add feature: Brief description
   
   - Detailed point 1
   - Detailed point 2
   - Fixes #issue_number
   ```

2. **Commit Often**: Make small, logical commits

3. **Reference Issues**: Link to related issues in commit messages

### Pull Request Process

1. **Update Your Branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template:
     - Description of changes
     - Related issues
     - Testing performed
     - Screenshots (if UI changes)

4. **Respond to Feedback**
   - Address reviewer comments
   - Make requested changes
   - Push updates to the same branch

### PR Checklist

- [ ] Branch is up to date with main
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] No unnecessary files included (check .gitignore)
- [ ] Commit messages are clear and descriptive

## Areas Needing Contribution

Current priorities (Phase 3 & 4):

1. **Testing**: Create automated test suite
2. **GUI**: Develop graphical interface (web or desktop)
3. **Game Analysis**: Add post-game engine analysis
4. **Training Mode**: Implement chess puzzles
5. **Opening Book**: Integrate opening database
6. **Time Controls**: Add clock functionality
7. **Documentation**: Improve examples and tutorials

## Questions?

- **Issues**: [GitHub Issues](https://github.com/GizzZmo/CC/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GizzZmo/CC/discussions)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Cyberchess! 🎉
