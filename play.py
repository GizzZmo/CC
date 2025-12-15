#!/usr/bin/env python3
"""
Cyberchess - Main Game Launcher
Provides a menu to select different game modes.
"""

import os
import sys

import chess

from game_modes import AIvsAIGame, PlayerVsComputerGame, PlayerVsPlayerGame
from opening_book import OpeningBook
from puzzles import PuzzleTrainer

# Configure stdout/stderr to use UTF-8 encoding on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


# --- CONFIGURATION ---
# Set these to your actual paths/keys
STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "YOUR_STOCKFISH_PATH_HERE")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY_HERE")


def get_board_theme():
    """Get user's preferred board theme."""
    print("\n🎨 Board Display Theme:")
    print("1. ASCII (letters and dots) - Default, works everywhere")
    print("2. Unicode (chess symbols) - Prettier, requires Unicode support")
    print("3. Borders (Unicode with borders and coordinates) - Most detailed")

    while True:
        choice = input("\nEnter your choice (1-3, default=1): ").strip()
        if choice == "" or choice == "1":
            return "ascii"
        elif choice == "2":
            return "unicode"
        elif choice == "3":
            return "borders"
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("♔♕♖♗♘♙  CYBERCHESS - MAIN MENU  ♟♞♝♜♛♚")
    print("=" * 50)
    print("\nSelect a game mode:")
    print("1. Player vs Player")
    print("2. Player vs Computer")
    print("3. AI vs AI (Stockfish vs Gemini)")
    print("4. Puzzle Trainer")
    print("5. Opening Book Explorer")
    print("6. About")
    print("7. Exit")
    print("=" * 50)


def get_user_choice():
    """Get user's menu choice."""
    while True:
        choice = input("\nEnter your choice (1-7): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            return choice
        print("❌ Invalid choice! Please enter 1, 2, 3, 4, 5, 6, or 7.")


def check_configuration():
    """Check if required configuration is set."""
    if STOCKFISH_PATH == "YOUR_STOCKFISH_PATH_HERE":
        print("\n⚠️  WARNING: STOCKFISH_PATH not configured!")
        print("Please set the STOCKFISH_PATH environment variable or edit play.py")
        print("Download Stockfish from: https://stockfishchess.org/download/")
        return False

    if GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n⚠️  WARNING: GOOGLE_API_KEY not configured!")
        print("This is only required for AI vs AI mode.")
        print("Get your API key from: https://makersuite.google.com/app/apikey")

    return True


def play_pvp():
    """Start a Player vs Player game."""
    print("\n" + "=" * 50)
    print("PLAYER VS PLAYER SETUP")
    print("=" * 50)

    # Get board theme preference
    theme = get_board_theme()

    # Ask about time controls
    time_control = (
        input("\nDo you want to use time controls? (y/n, default=n): ").strip().lower()
    )

    game = PlayerVsPlayerGame(theme=theme)

    if time_control == "y":
        print("\n⏱️  Time Control Options:")
        print("1. Blitz (5 minutes)")
        print("2. Rapid (10 minutes)")
        print("3. Classical (30 minutes)")
        print("4. Custom")

        while True:
            choice = input("\nChoose option (1-4): ").strip()
            if choice == "1":
                game.enable_time_control(5, 0)
                break
            elif choice == "2":
                game.enable_time_control(10, 0)
                break
            elif choice == "3":
                game.enable_time_control(30, 0)
                break
            elif choice == "4":
                while True:
                    try:
                        minutes = int(input("Enter minutes per player: ").strip())
                        increment = int(
                            input("Enter increment in seconds (0 for none): ").strip()
                        )
                        game.enable_time_control(minutes, increment)
                        break
                    except ValueError:
                        print("❌ Please enter valid numbers.")
                break
            else:
                print("❌ Invalid choice!")

    game.play()


def play_pvc():
    """Start a Player vs Computer game."""
    if not check_configuration():
        return

    print("\n" + "=" * 50)
    print("PLAYER VS COMPUTER SETUP")
    print("=" * 50)

    # Get board theme preference
    theme = get_board_theme()

    # Choose color
    while True:
        color_choice = (
            input("\nDo you want to play as White or Black? (w/b): ").strip().lower()
        )
        if color_choice in ["w", "white"]:
            player_color = chess.WHITE
            break
        elif color_choice in ["b", "black"]:
            player_color = chess.BLACK
            break
        else:
            print("❌ Invalid choice! Enter 'w' for White or 'b' for Black.")

    # Choose difficulty
    while True:
        try:
            skill = input(
                "\nChoose Stockfish skill level (0-20, 0=beginner, 20=grandmaster): "
            ).strip()
            skill_level = int(skill)
            if 0 <= skill_level <= 20:
                break
            else:
                print("❌ Please enter a number between 0 and 20.")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")

    game = PlayerVsComputerGame(STOCKFISH_PATH, player_color, skill_level, theme=theme)

    # Ask about time controls
    time_control = (
        input("\nDo you want to use time controls? (y/n, default=n): ").strip().lower()
    )

    if time_control == "y":
        print("\n⏱️  Time Control Options:")
        print("1. Blitz (5 minutes)")
        print("2. Rapid (10 minutes)")
        print("3. Classical (30 minutes)")
        print("4. Custom")

        while True:
            choice = input("\nChoose option (1-4): ").strip()
            if choice == "1":
                game.enable_time_control(5, 0)
                break
            elif choice == "2":
                game.enable_time_control(10, 0)
                break
            elif choice == "3":
                game.enable_time_control(30, 0)
                break
            elif choice == "4":
                while True:
                    try:
                        minutes = int(input("Enter minutes per player: ").strip())
                        increment = int(
                            input("Enter increment in seconds (0 for none): ").strip()
                        )
                        game.enable_time_control(minutes, increment)
                        break
                    except ValueError:
                        print("❌ Please enter valid numbers.")
                break
            else:
                print("❌ Invalid choice!")

    game.play()


def play_ai_vs_ai():
    """Start an AI vs AI game."""
    if not check_configuration():
        return

    if GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n❌ ERROR: GOOGLE_API_KEY must be configured for AI vs AI mode.")
        return

    print("\n" + "=" * 50)
    print("AI VS AI SETUP")
    print("=" * 50)

    # Get board theme preference
    theme = get_board_theme()

    # Choose Stockfish difficulty
    while True:
        try:
            skill = input("\nChoose Stockfish skill level (0-20, default=5): ").strip()
            if not skill:
                skill_level = 5
                break
            skill_level = int(skill)
            if 0 <= skill_level <= 20:
                break
            else:
                print("❌ Please enter a number between 0 and 20.")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")

    # Choose color assignment
    print("\n🎨 Color Assignment:")
    print("1. Stockfish plays White, Gemini plays Black (classic)")
    print("2. Stockfish plays Black, Gemini plays White")
    print("3. Random color assignment (recommended for diverse training)")

    while True:
        color_choice = input("\nChoose option (1-3, default=3): ").strip()
        if not color_choice or color_choice == "3":
            stockfish_color = None  # Random
            print("✨ Colors will be randomly assigned")
            break
        elif color_choice == "1":
            stockfish_color = chess.WHITE
            print("Stockfish will play White")
            break
        elif color_choice == "2":
            stockfish_color = chess.BLACK
            print("Stockfish will play Black")
            break
        else:
            print("❌ Invalid choice! Enter 1, 2, or 3.")

    game = AIvsAIGame(
        STOCKFISH_PATH, GOOGLE_API_KEY, skill_level, stockfish_color, theme=theme
    )
    game.play()


def play_puzzles():
    """Start puzzle training mode."""
    print("\n" + "=" * 50)
    print("🧩 PUZZLE TRAINER")
    print("=" * 50)

    trainer = PuzzleTrainer()

    print(f"\nAvailable puzzles: {len(trainer.puzzles)}")
    print("\nOptions:")
    print("1. Solve puzzles in order")
    print("2. Random puzzle")
    print("3. Filter by difficulty")

    while True:
        choice = input("\nChoose option (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            break
        print("❌ Invalid choice!")

    if choice == "1":
        num = input("\nHow many puzzles do you want to solve? (default=3): ").strip()
        num_puzzles = int(num) if num.isdigit() else 3
        trainer.training_session(num_puzzles, STOCKFISH_PATH)

    elif choice == "2":
        puzzle = trainer.get_random_puzzle()
        if puzzle:
            trainer.solve_puzzle(puzzle, STOCKFISH_PATH)

    elif choice == "3":
        print("\nDifficulty levels:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        diff_choice = input("\nChoose difficulty (1-3): ").strip()
        difficulty_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
        difficulty = difficulty_map.get(diff_choice, "Easy")

        puzzle = trainer.get_random_puzzle(difficulty)
        if puzzle:
            trainer.solve_puzzle(puzzle, STOCKFISH_PATH)
        else:
            print(f"\n❌ No puzzles found for difficulty: {difficulty}")


def explore_openings():
    """Explore the opening book."""
    print("\n" + "=" * 50)
    print("📚 OPENING BOOK EXPLORER")
    print("=" * 50)

    book = OpeningBook()

    print("\nOptions:")
    print("1. View all openings")
    print("2. Explore opening interactively")
    print("3. Test opening identification")

    while True:
        choice = input("\nChoose option (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            break
        print("❌ Invalid choice!")

    if choice == "1":
        print("\n📖 All Openings in Database:")
        for name, eco in book.get_all_openings():
            print(f"  • {name} ({eco})")

    elif choice == "2":
        print("\n🎮 Interactive Opening Explorer")
        print("Play moves to see if they match known openings")
        print("Enter 'quit' to exit\n")

        board = chess.Board()
        print(board)

        while not board.is_game_over():
            book.display_opening_info(board)

            suggested = book.suggest_opening_move(board)
            if suggested:
                print(f"💡 Book suggestion: {board.san(suggested)} ({suggested.uci()})")

            move_input = (
                input(
                    f"\n{'White' if board.turn == chess.WHITE else 'Black'} to move (UCI format or 'quit'): "
                )
                .strip()
                .lower()
            )

            if move_input == "quit":
                break

            try:
                move = chess.Move.from_uci(move_input)
                if move in board.legal_moves:
                    san = board.san(move)
                    board.push(move)
                    print(f"\nPlayed: {san}")
                    print(board)
                else:
                    print("❌ Illegal move!")
            except Exception as e:
                print(f"❌ Invalid input: {e}")

    elif choice == "3":
        print("\n🧪 Testing Opening Identification")
        print("\nTesting Italian Game...")

        board = chess.Board()
        for move_uci in ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"]:
            move = chess.Move.from_uci(move_uci)
            san = board.san(move)
            board.push(move)
            print(f"  {san}", end=" ")

        print("\n")
        book.display_opening_info(board)

        suggested = book.suggest_opening_move(board)
        if suggested:
            print(f"💡 Suggested continuation: {board.san(suggested)}")


def show_about():
    """Display information about the application."""
    print("\n" + "=" * 60)
    print("♔♕♖♗♘♙  ABOUT CYBERCHESS  ♟♞♝♜♛♚")
    print("=" * 60)

    print("\n📋 APPLICATION INFO")
    print("  Name:        Cyberchess (CC)")
    print("  Version:     0.4.0")
    print("  Description: A modern chess platform with multiple game modes")

    print("\n✨ FEATURES")
    print("  • Full chess rules implementation")
    print("  • Player vs Player mode")
    print("  • Player vs Computer (Stockfish AI)")
    print("  • AI vs AI (Stockfish vs Gemini)")
    print("  • Chess puzzle trainer with 8+ tactical puzzles")
    print("  • Opening book with 12+ popular openings")
    print("  • Time controls (Blitz, Rapid, Classical, Custom)")
    print("  • Post-game engine analysis")
    print("  • PGN import/export")

    print("\n🔧 TECHNOLOGY STACK")
    print("  • Language: Python 3.7+")
    print("  • Chess Library: python-chess")
    print("  • AI Engine: Stockfish")
    print("  • AI Integration: Google Gemini 1.5 Flash")

    print("\n👥 PROJECT")
    print("  • Repository: https://github.com/GizzZmo/CC")
    print("  • Issues: https://github.com/GizzZmo/CC/issues")
    print("  • Discussions: https://github.com/GizzZmo/CC/discussions")

    print("\n📄 LICENSE")
    print("  • License information will be specified as development progresses")

    print("\n💡 ACKNOWLEDGMENTS")
    print("  • Chess programming community for insights and best practices")
    print("  • Open source chess engines and libraries for inspiration")
    print("  • All contributors who help make this project better")

    print("\n" + "=" * 60)
    print("Status: 🎉 Phase 3 & 4 Complete - Advanced Features Implemented!")
    print("Last Updated: December 2025")
    print("=" * 60)


def main():
    """Main application loop."""
    print("\n" + "♔" * 50)
    print("Welcome to Cyberchess!")
    print("A modern chess platform with multiple game modes")
    print("♔" * 50)

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            play_pvp()
        elif choice == "2":
            play_pvc()
        elif choice == "3":
            play_ai_vs_ai()
        elif choice == "4":
            play_puzzles()
        elif choice == "5":
            explore_openings()
        elif choice == "6":
            show_about()
        elif choice == "7":
            print("\n👋 Thanks for playing Cyberchess! Goodbye!")
            break

        input("\nPress Enter to return to main menu...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
        sys.exit(0)
