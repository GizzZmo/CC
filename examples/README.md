# Cyberchess Examples

This directory contains example games, demonstrations, and sample assets for Cyberchess.

## Contents

### Famous Games Collection (`famous_games.pgn`)

A collection of three legendary chess games:

1. **The Immortal Game** (1851) - Anderssen vs Kieseritzky
   - Famous for its spectacular sacrifices
   - White sacrifices both rooks and a bishop to achieve checkmate
   
2. **The Evergreen Game** (1852) - Anderssen vs Dufresne
   - Brilliant combination play
   - Features a stunning queen sacrifice
   
3. **The Opera Game** (1858) - Paul Morphy vs Duke of Brunswick and Count Isouard
   - Played during an opera performance in Paris
   - Demonstration of rapid development and tactical brilliance

## Using the Examples

### Replaying Famous Games

You can load and replay these games using Python:

```python
import chess.pgn

with open("examples/famous_games.pgn") as pgn_file:
    game = chess.pgn.read_game(pgn_file)
    
    print(f"White: {game.headers['White']}")
    print(f"Black: {game.headers['Black']}")
    
    board = game.board()
    for move in game.mainline_moves():
        san = board.san(move)
        board.push(move)
        print(f"{san}", end=" ")
```

### Learning from Examples

These games demonstrate:
- Tactical combinations
- Piece sacrifice for positional advantage
- Checkmate patterns
- Classical opening principles
- Attacking play

## Adding Your Own Games

You can add your own PGN games to this directory. The standard PGN format is:

```
[Event "My Tournament"]
[Site "My City"]
[Date "2025.12.13"]
[Round "1"]
[White "Player 1"]
[Black "Player 2"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 ... 1-0
```

## Resources

- [PGN Format Specification](https://www.chessclub.com/help/PGN-spec)
- [Famous Chess Games Database](https://www.chessgames.com)
- [Chess Opening Theory](https://www.chess.com/openings)
