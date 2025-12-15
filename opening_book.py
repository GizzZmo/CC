"""
Opening book module for Cyberchess.
Provides common chess openings and their variations.
"""

import sys
import chess
import random
from typing import Optional, List, Dict, Tuple

# Configure stdout/stderr to use UTF-8 encoding on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


class OpeningBook:
    """
    Chess opening book with common openings and their main variations.
    """

    def __init__(self):
        """Initialize the opening book with common openings."""
        self.openings = {
            # Italian Game
            "e2e4 e7e5 g1f3 b8c6 f1c4": {
                "name": "Italian Game",
                "eco": "C50",
                "responses": ["g8f6", "f8c5", "d7d6"],
            },
            # Ruy Lopez
            "e2e4 e7e5 g1f3 b8c6 f1b5": {
                "name": "Ruy Lopez (Spanish Opening)",
                "eco": "C60",
                "responses": ["a7a6", "g8f6", "f8c5"],
            },
            # Sicilian Defense
            "e2e4 c7c5": {
                "name": "Sicilian Defense",
                "eco": "B20",
                "responses": ["g1f3", "b1c3", "d2d4"],
            },
            # French Defense
            "e2e4 e7e6": {
                "name": "French Defense",
                "eco": "C00",
                "responses": ["d2d4", "d2d3", "g1f3"],
            },
            # Caro-Kann Defense
            "e2e4 c7c6": {
                "name": "Caro-Kann Defense",
                "eco": "B10",
                "responses": ["d2d4", "b1c3", "g1f3"],
            },
            # Queen's Gambit
            "d2d4 d7d5 c2c4": {
                "name": "Queen's Gambit",
                "eco": "D06",
                "responses": ["e7e6", "c7c6", "d5c4"],
            },
            # King's Indian Defense
            "d2d4 g8f6 c2c4 g7g6": {
                "name": "King's Indian Defense",
                "eco": "E60",
                "responses": ["b1c3", "g1f3", "g2g3"],
            },
            # English Opening
            "c2c4": {
                "name": "English Opening",
                "eco": "A10",
                "responses": ["e7e5", "g8f6", "c7c5"],
            },
            # Nimzo-Indian Defense
            "d2d4 g8f6 c2c4 e7e6 b1c3 f8b4": {
                "name": "Nimzo-Indian Defense",
                "eco": "E20",
                "responses": ["d1c2", "e2e3", "g1f3"],
            },
            # Scandinavian Defense
            "e2e4 d7d5": {
                "name": "Scandinavian Defense",
                "eco": "B01",
                "responses": ["e4d5", "b1c3", "e4e5"],
            },
            # Pirc Defense
            "e2e4 d7d6 d2d4 g8f6 b1c3 g7g6": {
                "name": "Pirc Defense",
                "eco": "B07",
                "responses": ["f1e2", "g1f3", "f2f4"],
            },
            # London System
            "d2d4 d7d5 g1f3 g8f6 c1f4": {
                "name": "London System",
                "eco": "D02",
                "responses": ["c7c5", "e7e6", "c7c6"],
            },
        }

    def get_opening_moves(self, board: chess.Board) -> List[str]:
        """
        Get the move sequence (in UCI) that led to the current position.
        """
        return [move.uci() for move in board.move_stack]

    def identify_opening(self, board: chess.Board) -> Optional[Dict[str, str]]:
        """
        Identify the opening based on the current board position.
        Returns dict with 'name' and 'eco' code if found, None otherwise.
        """
        move_sequence = " ".join(self.get_opening_moves(board))

        # Check for exact matches or prefixes
        for opening_moves, opening_info in self.openings.items():
            if move_sequence == opening_moves or move_sequence.startswith(
                opening_moves + " "
            ):
                return {"name": opening_info["name"], "eco": opening_info["eco"]}

        return None

    def suggest_opening_move(self, board: chess.Board) -> Optional[chess.Move]:
        """
        Suggest a book move based on the current position.
        Returns a Move object if a book move is found, None otherwise.
        """
        move_sequence = " ".join(self.get_opening_moves(board))

        # Check if current position matches an opening
        for opening_moves, opening_info in self.openings.items():
            if move_sequence == opening_moves:
                # We're at a known position, suggest one of the responses
                responses = opening_info["responses"]
                move_uci = random.choice(responses)
                try:
                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        return move
                except:
                    pass

        return None

    def get_all_openings(self) -> List[Tuple[str, str]]:
        """
        Get a list of all openings in the book.
        Returns list of tuples: (name, eco_code)
        """
        openings_list = []
        seen = set()

        for opening_info in self.openings.values():
            key = (opening_info["name"], opening_info["eco"])
            if key not in seen:
                openings_list.append(key)
                seen.add(key)

        return sorted(openings_list)

    def display_opening_info(self, board: chess.Board):
        """
        Display information about the current opening if recognized.
        """
        opening = self.identify_opening(board)

        if opening:
            print(f"\n📚 Opening: {opening['name']} ({opening['eco']})")
        else:
            print("\n📚 Position not in opening book")


def demo_opening_book():
    """Demonstrate the opening book functionality."""
    print("=" * 60)
    print("OPENING BOOK DEMONSTRATION")
    print("=" * 60)

    book = OpeningBook()

    # Display all openings
    print("\n📚 Available Openings:")
    for name, eco in book.get_all_openings():
        print(f"  • {name} ({eco})")

    # Test Italian Game
    print("\n\nTesting Italian Game:")
    board = chess.Board()

    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"]
    for move_uci in moves:
        move = chess.Move.from_uci(move_uci)
        san = board.san(move)
        board.push(move)
        print(f"  {san}", end=" ")

    print("\n")
    book.display_opening_info(board)

    suggested = book.suggest_opening_move(board)
    if suggested:
        print(f"💡 Suggested book move: {board.san(suggested)} ({suggested.uci()})")

    # Test Sicilian Defense
    print("\n\nTesting Sicilian Defense:")
    board2 = chess.Board()

    moves2 = ["e2e4", "c7c5"]
    for move_uci in moves2:
        move = chess.Move.from_uci(move_uci)
        san = board2.san(move)
        board2.push(move)
        print(f"  {san}", end=" ")

    print("\n")
    book.display_opening_info(board2)

    suggested2 = book.suggest_opening_move(board2)
    if suggested2:
        print(f"💡 Suggested book move: {board2.san(suggested2)} ({suggested2.uci()})")

    print("\n✅ Opening book demonstration complete")


if __name__ == "__main__":
    demo_opening_book()
