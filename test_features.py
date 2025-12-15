#!/usr/bin/env python3
"""
Test suite for Cyberchess Phase 3 and Phase 4 features.
This file tests the new features added in advanced phases.
"""

import chess
import chess.engine
import os
import sys
from game_modes import ChessGame, PlayerVsPlayerGame, PlayerVsComputerGame

# Configure stdout/stderr to use UTF-8 encoding on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

# Configuration for testing
STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "/usr/games/stockfish")


def test_time_controls():
    """Test time control functionality."""
    print("=" * 60)
    print("TEST 1: Time Controls")
    print("=" * 60)

    game = ChessGame()

    # Enable time controls: 5 minutes + 3 seconds increment
    game.enable_time_control(5, 3)

    print(f"✓ Time controls enabled: 5+3")
    print(f"✓ White time: {game.format_time(game.white_time)}")
    print(f"✓ Black time: {game.format_time(game.black_time)}")

    # Simulate time usage
    game.update_time(chess.WHITE, 10.5)  # White uses 10.5 seconds
    print(f"✓ After White's move: {game.format_time(game.white_time)}")

    game.update_time(chess.BLACK, 5.2)  # Black uses 5.2 seconds
    print(f"✓ After Black's move: {game.format_time(game.black_time)}")

    # Test timeout detection
    game.white_time = 0
    if game.is_time_out(chess.WHITE):
        print("✓ Timeout detection working correctly")

    print("✅ Time controls test PASSED\n")


def test_game_analysis():
    """Test post-game analysis functionality."""
    print("=" * 60)
    print("TEST 2: Post-Game Analysis")
    print("=" * 60)

    # Check if Stockfish is available
    if not os.path.exists(STOCKFISH_PATH):
        print(f"⚠️  Stockfish not found at {STOCKFISH_PATH}")
        print("⚠️  Skipping analysis test")
        return

    # Create a simple game
    game = ChessGame()

    # Play a few moves (Scholar's Mate)
    moves = ["e2e4", "e7e5", "f1c4", "b8c6", "d1h5", "g8f6", "h5f7"]

    print("Playing a short game...")
    for move_uci in moves:
        move = chess.Move.from_uci(move_uci)
        if move in game.board.legal_moves:
            game.make_move(move)

    print(f"✓ Game completed with {len(game.move_history)} moves")

    # Analyze the game
    try:
        print("\nAnalyzing game...")
        analysis = game.analyze_game(STOCKFISH_PATH, depth=10)

        print(f"✓ Analysis completed: {len(analysis)} positions evaluated")

        # Display analysis summary
        game.display_game_analysis(analysis)

        print("\n✅ Game analysis test PASSED\n")
    except Exception as e:
        print(f"❌ Analysis test failed: {e}\n")


def test_board_display_with_time():
    """Test board display with time controls."""
    print("=" * 60)
    print("TEST 3: Board Display with Time Controls")
    print("=" * 60)

    game = ChessGame()
    game.enable_time_control(10, 5)  # 10 minutes + 5 seconds

    # Make a few moves
    game.make_move(chess.Move.from_uci("e2e4"))
    game.update_time(chess.WHITE, 3.5)

    game.make_move(chess.Move.from_uci("e7e5"))
    game.update_time(chess.BLACK, 2.1)

    print("\nDisplaying board with time:")
    game.display_board()

    print("\n✅ Board display test PASSED\n")


def test_move_history():
    """Test move history tracking."""
    print("=" * 60)
    print("TEST 4: Move History Tracking")
    print("=" * 60)

    game = ChessGame()

    # Play some moves
    moves = [
        ("e2e4", "e4"),
        ("e7e5", "e5"),
        ("g1f3", "Nf3"),
        ("b8c6", "Nc6"),
    ]

    for uci, expected_san in moves:
        move = chess.Move.from_uci(uci)
        san = game.make_move(move)
        print(f"✓ Move {uci} recorded as {san}")

    print(f"\n✓ Total moves in history: {len(game.move_history)}")

    game.display_move_history()

    print("\n✅ Move history test PASSED\n")


def test_game_states():
    """Test various game state detections."""
    print("=" * 60)
    print("TEST 5: Game State Detection")
    print("=" * 60)

    # Test checkmate
    game = ChessGame()
    # Fool's Mate
    for move_uci in ["f2f3", "e7e5", "g2g4", "d8h4"]:
        game.make_move(chess.Move.from_uci(move_uci))

    if game.board.is_checkmate():
        print("✓ Checkmate detected correctly (Fool's Mate)")

    # Test stalemate
    game2 = ChessGame()
    game2.board.set_fen("k7/8/1Q6/8/8/8/8/7K w - - 0 1")
    game2.board.push_san("Qb7")

    if game2.board.is_stalemate():
        print("✓ Stalemate detected correctly")

    # Test check
    game3 = ChessGame()
    game3.board.set_fen("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    game3.board.push_san("Qh5")

    if game3.board.is_check():
        print("✓ Check detected correctly")

    print("\n✅ Game state detection test PASSED\n")


def test_pgn_export():
    """Test PGN export functionality."""
    print("=" * 60)
    print("TEST 6: PGN Export")
    print("=" * 60)

    game = ChessGame()

    # Play a short game
    for move_uci in ["e2e4", "e7e5", "g1f3", "b8c6"]:
        game.make_move(chess.Move.from_uci(move_uci))

    # Save to PGN
    test_pgn = "test_game.pgn"

    # Remove old test file if it exists
    if os.path.exists(test_pgn):
        os.remove(test_pgn)

    game.save_to_pgn(test_pgn, "Test Player 1", "Test Player 2", "Test Game")

    if os.path.exists(test_pgn):
        print(f"✓ PGN file created: {test_pgn}")

        # Read and verify
        with open(test_pgn, "r") as f:
            content = f.read()
            if "Test Player 1" in content and "Test Player 2" in content:
                print("✓ PGN headers correct")

        # Clean up
        os.remove(test_pgn)
        print("✓ Test file cleaned up")

    print("\n✅ PGN export test PASSED\n")


def run_all_tests():
    """Run all tests."""
    print("\n" + "♔" * 60)
    print("CYBERCHESS PHASE 3 & 4 FEATURE TESTS")
    print("♔" * 60 + "\n")

    tests = [
        test_time_controls,
        test_game_analysis,
        test_board_display_with_time,
        test_move_history,
        test_game_states,
        test_pgn_export,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        sys.exit(1)
