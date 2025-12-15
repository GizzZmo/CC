#!/usr/bin/env python3
"""
Advanced features demonstration for Cyberchess Phase 3 & 4.
Showcases new features: time controls, opening book, puzzles, and analysis.
"""

import sys
import chess
from game_modes import ChessGame
from opening_book import OpeningBook
from puzzles import PuzzleTrainer

# Configure stdout/stderr to use UTF-8 encoding on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')


def demo_time_controls():
    """Demonstrate time control features."""
    print("\n" + "=" * 60)
    print("DEMO 1: TIME CONTROLS")
    print("=" * 60)
    
    game = ChessGame()
    
    print("\n🎮 Setting up a Blitz game (5 minutes + 3 seconds increment)...")
    game.enable_time_control(5, 3)
    
    print(f"\nInitial time settings:")
    print(f"  White: {game.format_time(game.white_time)}")
    print(f"  Black: {game.format_time(game.black_time)}")
    
    # Simulate some moves with time usage
    moves = ["e2e4", "e7e5", "g1f3", "b8c6"]
    times = [5.2, 3.8, 4.5, 6.1]  # Simulated thinking time in seconds
    
    print("\n📝 Simulating game with time tracking:")
    for move_uci, think_time in zip(moves, times):
        move = chess.Move.from_uci(move_uci)
        color = game.board.turn
        san = game.make_move(move)
        game.update_time(color, think_time)
        
        color_name = "White" if color == chess.WHITE else "Black"
        print(f"  {color_name} plays {san} (thought for {think_time:.1f}s)")
        print(f"    Remaining: White={game.format_time(game.white_time)}, Black={game.format_time(game.black_time)}")
    
    print("\n✅ Time controls demonstration complete!")


def demo_opening_book():
    """Demonstrate opening book features."""
    print("\n" + "=" * 60)
    print("DEMO 2: OPENING BOOK")
    print("=" * 60)
    
    book = OpeningBook()
    
    print(f"\n📚 Opening book contains {len(book.get_all_openings())} different openings")
    
    # Demonstrate Italian Game
    print("\n🎯 Testing Italian Game recognition:")
    board = chess.Board()
    
    italian_moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"]
    move_display = []
    
    for move_uci in italian_moves:
        move = chess.Move.from_uci(move_uci)
        san = board.san(move)
        board.push(move)
        move_display.append(san)
    
    print(f"  Moves played: {' '.join(move_display)}")
    
    opening = book.identify_opening(board)
    if opening:
        print(f"  ✅ Identified: {opening['name']} ({opening['eco']})")
    
    # Show book suggestion
    suggested = book.suggest_opening_move(board)
    if suggested:
        print(f"  💡 Book suggests: {board.san(suggested)}")
    
    # Test Queen's Gambit
    print("\n🎯 Testing Queen's Gambit recognition:")
    board2 = chess.Board()
    
    qg_moves = ["d2d4", "d7d5", "c2c4"]
    move_display2 = []
    
    for move_uci in qg_moves:
        move = chess.Move.from_uci(move_uci)
        san = board2.san(move)
        board2.push(move)
        move_display2.append(san)
    
    print(f"  Moves played: {' '.join(move_display2)}")
    
    opening2 = book.identify_opening(board2)
    if opening2:
        print(f"  ✅ Identified: {opening2['name']} ({opening2['eco']})")
    
    suggested2 = book.suggest_opening_move(board2)
    if suggested2:
        print(f"  💡 Book suggests: {board2.san(suggested2)}")
    
    print("\n✅ Opening book demonstration complete!")


def demo_puzzle_trainer():
    """Demonstrate chess puzzle features."""
    print("\n" + "=" * 60)
    print("DEMO 3: CHESS PUZZLE TRAINER")
    print("=" * 60)
    
    trainer = PuzzleTrainer()
    
    print(f"\n🧩 Puzzle library contains {len(trainer.puzzles)} puzzles")
    
    # Show puzzle statistics
    themes = {}
    difficulties = {}
    
    for puzzle in trainer.puzzles:
        themes[puzzle.theme] = themes.get(puzzle.theme, 0) + 1
        difficulties[puzzle.difficulty] = difficulties.get(puzzle.difficulty, 0) + 1
    
    print("\n📊 Puzzle Statistics:")
    print(f"  Themes: {', '.join(f'{k} ({v})' for k, v in sorted(themes.items()))}")
    print(f"  Difficulty: {', '.join(f'{k} ({v})' for k, v in sorted(difficulties.items()))}")
    
    # Show an example puzzle
    print("\n📝 Example Puzzle (Easy):")
    puzzle = trainer.get_puzzle(0)  # Back Rank Mate
    
    if puzzle:
        print(f"  Theme: {puzzle.theme}")
        print(f"  Difficulty: {puzzle.difficulty}")
        print(f"  Description: {puzzle.description}")
        
        board = puzzle.get_board()
        print(f"\n{board}")
        print(f"\n  {'White' if board.turn == chess.WHITE else 'Black'} to move")
        print(f"  Solution: {' '.join(puzzle.solution)}")
        
        # Show the solution in SAN
        temp_board = board.copy()
        san_solution = []
        for move_uci in puzzle.solution:
            move = chess.Move.from_uci(move_uci)
            san = temp_board.san(move)
            san_solution.append(san)
            temp_board.push(move)
        
        print(f"  Solution (SAN): {' '.join(san_solution)}")
    
    print("\n✅ Puzzle trainer demonstration complete!")


def demo_game_analysis():
    """Demonstrate post-game analysis features."""
    print("\n" + "=" * 60)
    print("DEMO 4: POST-GAME ANALYSIS")
    print("=" * 60)
    
    print("\n📊 Game analysis can provide:")
    print("  • Move-by-move evaluation in centipawns")
    print("  • Detection of mistakes (>50 cp loss)")
    print("  • Detection of blunders (>100 cp loss)")
    print("  • Detection of brilliant moves (>100 cp gain)")
    print("  • Average position evaluation")
    
    # Create a sample game
    game = ChessGame()
    
    # Scholar's Mate (with a blunder)
    moves = ["e2e4", "e7e5", "f1c4", "b8c6", "d1h5", "g8f6", "h5f7"]
    
    print("\n📝 Sample game (Scholar's Mate):")
    for i, move_uci in enumerate(moves):
        move = chess.Move.from_uci(move_uci)
        san = game.make_move(move)
        move_num = i // 2 + 1
        
        if i % 2 == 0:
            print(f"  {move_num}. {san}", end=" ")
        else:
            print(san)
    
    if len(moves) % 2 == 1:
        print()  # New line if odd number of moves
    
    print(f"\n  Game result: {game.get_result()}")
    print(f"  Total moves: {len(game.move_history)}")
    
    print("\n💡 Note: To run actual analysis, use:")
    print("  analysis = game.analyze_game(stockfish_path, depth=15)")
    print("  game.display_game_analysis(analysis)")
    print("\n  (Requires Stockfish engine)")
    
    print("\n✅ Game analysis demonstration complete!")


def demo_all_features():
    """Run all advanced feature demonstrations."""
    print("\n" + "♔" * 60)
    print("CYBERCHESS PHASE 3 & 4 ADVANCED FEATURES DEMO")
    print("♔" * 60)
    
    print("\nThis demonstration showcases the new features added in Phase 3 & 4:")
    print("  1. Time Controls")
    print("  2. Opening Book")
    print("  3. Chess Puzzle Trainer")
    print("  4. Post-Game Analysis")
    
    demos = [
        demo_time_controls,
        demo_opening_book,
        demo_puzzle_trainer,
        demo_game_analysis,
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ALL DEMONSTRATIONS COMPLETE")
    print("=" * 60)
    
    print("\n🎮 To try these features interactively, run:")
    print("  python play.py")
    
    print("\n📚 For more information, see:")
    print("  • README.md - Complete documentation")
    print("  • CHANGELOG.md - Version history")
    print("  • INSTALL.md - Installation guide")


if __name__ == "__main__":
    try:
        demo_all_features()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
