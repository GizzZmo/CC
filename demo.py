#!/usr/bin/env python3
"""
Demo script showing all Cyberchess capabilities.
This demonstrates the features implemented in Phase 2.
"""

import sys

import chess
import chess.pgn

# Configure stdout/stderr to use UTF-8 encoding on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


def demo_basic_features():
    """Demonstrate basic chess features."""
    print("=" * 60)
    print("DEMO 1: Basic Chess Features")
    print("=" * 60)

    board = chess.Board()
    print("\nStarting position:")
    print(board)

    # Make some moves
    print("\n1. Playing e2-e4 (e4)")
    board.push_san("e4")
    print(board)

    print("\n2. Playing e7-e5 (e5)")
    board.push_san("e5")
    print(board)

    print("\n3. Playing Ng1-f3 (Nf3)")
    board.push_san("Nf3")
    print(board)

    print("\nMove history (UCI):", [move.uci() for move in board.move_stack])

    # To get SAN, we need to replay the game from the start
    temp_board = chess.Board()
    san_moves = []
    for move in board.move_stack:
        san_moves.append(temp_board.san(move))
        temp_board.push(move)
    print("Move history (SAN):", san_moves)


def demo_special_moves():
    """Demonstrate special chess moves: castling, en passant, promotion."""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Special Moves (Castling, En Passant, Promotion)")
    print("=" * 60)

    # Castling
    print("\n--- CASTLING ---")
    board = chess.Board()
    # Quick setup for castling
    moves = ["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "O-O"]
    for move in moves:
        board.push_san(move)
    print("After castling kingside (O-O):")
    print(board)

    # En Passant
    print("\n--- EN PASSANT ---")
    board = chess.Board()
    # Setup for en passant
    moves = ["e4", "a6", "e5", "f5"]
    for move in moves:
        board.push_san(move)
    print("Before en passant capture:")
    print(board)

    # En passant is available
    board.push_san("exf6")  # en passant capture
    print("\nAfter en passant (exf6):")
    print(board)

    # Pawn Promotion
    print("\n--- PAWN PROMOTION ---")
    # Create a position where we can promote
    board = chess.Board("8/3P4/8/8/8/8/8/4K2k w - - 0 1")
    print("Before promotion (pawn on d7):")
    print(board)

    board.push_san("d8=Q")  # Promote to queen
    print("\nAfter promotion to Queen (d8=Q):")
    print(board)


def demo_game_states():
    """Demonstrate check, checkmate, and stalemate detection."""
    print("\n\n" + "=" * 60)
    print("DEMO 3: Game States (Check, Checkmate, Stalemate)")
    print("=" * 60)

    # Check
    print("\n--- CHECK ---")
    board = chess.Board()
    moves = ["e4", "e5", "Bc4", "Nc6", "Qh5", "Nf6", "Qxf7+"]
    for move in moves:
        board.push_san(move)
    print(board)
    print(f"Is in check? {board.is_check()}")
    print(f"Checking piece: King is attacked!")

    # Checkmate - Scholar's Mate
    print("\n--- CHECKMATE (Scholar's Mate) ---")
    board = chess.Board()
    moves = ["e4", "e5", "Bc4", "Nc6", "Qh5", "Nf6", "Qxf7#"]
    for move in moves:
        board.push_san(move)
    print(board)
    print(f"Is checkmate? {board.is_checkmate()}")
    print(f"Result: {board.result()}")

    # Stalemate
    print("\n--- STALEMATE ---")
    board = chess.Board("7k/8/6Q1/8/8/8/8/7K b - - 0 1")
    print(board)
    print(f"Is stalemate? {board.is_stalemate()}")
    print(f"Result: {board.result()}")
    print("Black has no legal moves but is not in check = Stalemate!")


def demo_draw_conditions():
    """Demonstrate various draw conditions."""
    print("\n\n" + "=" * 60)
    print("DEMO 4: Draw Conditions")
    print("=" * 60)

    # Insufficient material
    print("\n--- INSUFFICIENT MATERIAL ---")
    board = chess.Board("8/8/8/8/8/3k4/8/3K4 w - - 0 1")
    print(board)
    print(f"Insufficient material? {board.is_insufficient_material()}")
    print("Only kings remaining = Draw")

    # Note: 50-move rule and threefold repetition are harder to demo
    # in a simple script, but they are automatically tracked by python-chess
    print("\n--- OTHER DRAW CONDITIONS ---")
    print("50-move rule: Automatically tracked by board.is_fifty_moves()")
    print("Threefold repetition: Automatically tracked by board.is_repetition()")


def demo_move_generation():
    """Demonstrate move generation and validation."""
    print("\n\n" + "=" * 60)
    print("DEMO 5: Move Generation and Validation")
    print("=" * 60)

    board = chess.Board()
    print("\nStarting position - White to move")
    print(f"Number of legal moves: {board.legal_moves.count()}")
    print(f"Legal moves: {', '.join([move.uci() for move in list(board.legal_moves)])}")

    # After a few moves
    board.push_san("e4")
    board.push_san("e5")
    board.push_san("Nf3")
    print("\nAfter 1.e4 e5 2.Nf3 - Black to move")
    print(board)
    print(f"Number of legal moves: {board.legal_moves.count()}")
    print(
        f"Sample legal moves: {', '.join([move.uci() for move in list(board.legal_moves)[:10]])}..."
    )


def demo_pgn_loading():
    """Demonstrate loading and replaying games from PGN."""
    print("\n\n" + "=" * 60)
    print("DEMO 6: Loading Games from PGN")
    print("=" * 60)

    try:
        with open("examples/famous_games.pgn") as pgn_file:
            # Load first game (The Immortal Game)
            game = chess.pgn.read_game(pgn_file)

            print(f"\nGame: {game.headers['Event']}")
            print(f"White: {game.headers['White']}")
            print(f"Black: {game.headers['Black']}")
            print(f"Date: {game.headers['Date']}")
            print(f"Result: {game.headers['Result']}")

            print("\nReplaying moves...")
            board = game.board()
            move_count = 0
            for move in game.mainline_moves():
                if move_count >= 5:  # Show first 5 moves
                    print("... (game continues)")
                    break
                san = board.san(move)
                board.push(move)
                move_count += 1
                if board.turn == chess.WHITE:  # Just made black's move
                    print(f"{board.fullmove_number - 1}. ... {san}")
                else:  # Just made white's move
                    print(f"{board.fullmove_number}. {san}", end=" ")

    except FileNotFoundError:
        print("\nNote: Famous games PGN file not found.")
        print("Run this from the repository root directory.")


def main():
    """Run all demonstrations."""
    print("\n" + "♔" * 60)
    print("CYBERCHESS - FEATURE DEMONSTRATION")
    print("Showcasing Phase 2 Roadmap Implementation")
    print("♔" * 60)

    demo_basic_features()
    demo_special_moves()
    demo_game_states()
    demo_draw_conditions()
    demo_move_generation()
    demo_pgn_loading()

    print("\n\n" + "=" * 60)
    print("✅ All demonstrations complete!")
    print("=" * 60)
    print("\nThese demos showcase:")
    print("✓ Full chess rules (castling, en passant, promotion)")
    print("✓ Game state management (check, checkmate, stalemate)")
    print("✓ Draw conditions (insufficient material, 50-move, repetition)")
    print("✓ Move history and notation (UCI and SAN)")
    print("✓ Move generation and validation")
    print("✓ PGN import/export")
    print("\n🎮 Try 'python play.py' for interactive game modes!")
    print("=" * 60)


if __name__ == "__main__":
    main()
