"""
Chess puzzles and training module for Cyberchess.
Provides tactical puzzles for players to solve.
"""

import sys
import chess
import chess.engine
from typing import List, Dict, Optional
import os

# Configure stdout/stderr to use UTF-8 encoding on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


class ChessPuzzle:
    """Represents a single chess puzzle."""

    def __init__(
        self,
        fen: str,
        solution: List[str],
        theme: str,
        difficulty: str,
        description: str = "",
    ):
        """
        Initialize a chess puzzle.

        Args:
            fen: Starting position in FEN notation
            solution: List of moves (in UCI format) that solve the puzzle
            theme: Tactical theme (e.g., "Fork", "Pin", "Mate in 2")
            difficulty: Difficulty level ("Easy", "Medium", "Hard")
            description: Optional description of the puzzle
        """
        self.fen = fen
        self.solution = solution
        self.theme = theme
        self.difficulty = difficulty
        self.description = description

    def get_board(self) -> chess.Board:
        """Get a board with the puzzle position."""
        return chess.Board(self.fen)


class PuzzleTrainer:
    """Chess puzzle trainer for tactical practice."""

    def __init__(self):
        """Initialize the puzzle trainer with a collection of puzzles."""
        self.puzzles = self._load_puzzles()
        self.current_puzzle = None
        self.current_index = 0

    def _load_puzzles(self) -> List[ChessPuzzle]:
        """Load built-in chess puzzles."""
        return [
            # Easy Puzzles
            ChessPuzzle(
                fen="r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4",
                solution=["h5f7"],  # Qxf7#
                theme="Back Rank Mate",
                difficulty="Easy",
                description="White to move and checkmate in 1",
            ),
            ChessPuzzle(
                fen="rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 4",
                solution=[
                    "c4d5",
                    "f6d5",
                    "d1a4",
                ],  # Take pawn, knight recaptures, check wins piece
                theme="Fork",
                difficulty="Easy",
                description="White to move - win material with a fork",
            ),
            # Medium Puzzles
            ChessPuzzle(
                fen="r1bqk2r/ppp2ppp/2n5/2bpp3/4P3/2P2N2/PP1P1PPP/RNBQKB1R w KQkq - 0 6",
                solution=["f3e5", "c6e5", "d1h5", "e8f8", "h5e5"],  # Nxe5 and win
                theme="Removing the Defender",
                difficulty="Medium",
                description="White to move and win material",
            ),
            ChessPuzzle(
                fen="r2qkb1r/ppp2ppp/2n5/4P3/2Bn4/8/PPP2PPP/RNBQK2R b KQkq - 0 7",
                solution=["d8d4"],  # Queen threatens multiple pieces
                theme="Double Attack",
                difficulty="Medium",
                description="Black to move - create a double attack",
            ),
            # Hard Puzzles
            ChessPuzzle(
                fen="r1b2rk1/ppq2ppp/2p5/4p3/1bP5/1P2BN2/P3QPPP/R4RK1 w - - 0 15",
                solution=["f3g5", "g7g6", "e3h6"],  # Ng5 followed by Bh6 wins
                theme="Attacking the King",
                difficulty="Hard",
                description="White to move - find the winning attack",
            ),
            ChessPuzzle(
                fen="2rq1rk1/pp3pbp/3p1np1/3Pp3/2P1P3/2N3P1/PP1QNPBP/3R1RK1 b - - 0 14",
                solution=["f6e4", "c3e4", "d8h4"],  # Sacrifice knight to open attack
                theme="Sacrifice",
                difficulty="Hard",
                description="Black to move - sacrifice for a winning attack",
            ),
            # Mate in 2
            ChessPuzzle(
                fen="6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1",
                solution=["e1e8", "g8h7", "e8h8"],  # Re8+ Kh7 Rh8#
                theme="Mate in 2",
                difficulty="Medium",
                description="White to move and mate in 2",
            ),
            ChessPuzzle(
                fen="r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
                solution=["f3e5", "c6e5", "d1h5"],  # Nxe5 Nxe5 Qh5+ wins material
                theme="Fork",
                difficulty="Medium",
                description="White to move - find the winning combination",
            ),
        ]

    def get_puzzle(self, index: int = 0) -> Optional[ChessPuzzle]:
        """Get a puzzle by index."""
        if 0 <= index < len(self.puzzles):
            return self.puzzles[index]
        return None

    def get_random_puzzle(
        self, difficulty: Optional[str] = None
    ) -> Optional[ChessPuzzle]:
        """Get a random puzzle, optionally filtered by difficulty."""
        import random

        if difficulty:
            filtered = [p for p in self.puzzles if p.difficulty == difficulty]
            if filtered:
                return random.choice(filtered)

        return random.choice(self.puzzles) if self.puzzles else None

    def solve_puzzle(self, puzzle: ChessPuzzle, stockfish_path: Optional[str] = None):
        """
        Interactive puzzle solving session.

        Args:
            puzzle: The puzzle to solve
            stockfish_path: Optional path to Stockfish for hints
        """
        print("\n" + "=" * 60)
        print(f"🧩 PUZZLE: {puzzle.theme} ({puzzle.difficulty})")
        print("=" * 60)

        if puzzle.description:
            print(f"\n{puzzle.description}")

        board = puzzle.get_board()
        print("\n" + str(board))
        print(f"\n{'White' if board.turn == chess.WHITE else 'Black'} to move")

        move_count = 0
        solution_index = 0

        while solution_index < len(puzzle.solution):
            # Player's turn
            if solution_index % 2 == 0:
                print(f"\nMove {move_count + 1}:")

                while True:
                    user_input = (
                        input("Enter your move (UCI format, or 'hint'/'solution'): ")
                        .strip()
                        .lower()
                    )

                    if user_input == "hint":
                        if stockfish_path and os.path.exists(stockfish_path):
                            self._show_hint(board, stockfish_path)
                        else:
                            print(
                                "💡 Hint: Look for forcing moves (checks, captures, threats)"
                            )
                        continue

                    if user_input == "solution":
                        self._show_solution(board, puzzle.solution[solution_index:])
                        return False

                    try:
                        user_move = chess.Move.from_uci(user_input)

                        if user_move not in board.legal_moves:
                            print("❌ Illegal move! Try again.")
                            continue

                        # Check if move matches solution
                        expected_move = chess.Move.from_uci(
                            puzzle.solution[solution_index]
                        )

                        if user_move == expected_move:
                            san = board.san(user_move)
                            board.push(user_move)
                            print(f"✅ Correct! {san}")
                            solution_index += 1
                            move_count += 1
                            break
                        else:
                            print(f"❌ Not the best move. Try again!")
                            print(f"💡 Hint: Think about the theme - {puzzle.theme}")

                    except Exception as e:
                        print(f"❌ Invalid input: {e}")

            else:
                # Computer's response (part of solution)
                if solution_index < len(puzzle.solution):
                    response_move = chess.Move.from_uci(puzzle.solution[solution_index])
                    san = board.san(response_move)
                    board.push(response_move)
                    print(f"\nOpponent plays: {san}")
                    solution_index += 1
                    move_count += 1

            # Show the position
            print("\n" + str(board))

            # Check if puzzle is solved
            if board.is_checkmate():
                print("\n🎉 CHECKMATE! Puzzle solved!")
                return True
            elif solution_index >= len(puzzle.solution):
                print("\n🎉 Puzzle solved correctly!")
                return True

        return True

    def _show_hint(self, board: chess.Board, stockfish_path: str):
        """Show a hint using Stockfish analysis."""
        try:
            engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            info = engine.analyse(board, chess.engine.Limit(depth=15))
            engine.quit()

            if "pv" in info and info["pv"]:
                best_move = info["pv"][0]
                print(
                    f"💡 Hint: Consider the move {board.san(best_move)} ({best_move.uci()})"
                )
            else:
                print("💡 Hint: Look for forcing moves!")
        except Exception as e:
            print(f"💡 Hint: Look for checks and captures! (Engine error: {e})")

    def _show_solution(self, board: chess.Board, remaining_moves: List[str]):
        """Show the complete solution."""
        print("\n📖 SOLUTION:")
        temp_board = board.copy()

        for i, move_uci in enumerate(remaining_moves):
            move = chess.Move.from_uci(move_uci)
            san = temp_board.san(move)
            temp_board.push(move)

            if i % 2 == 0:
                print(f"  {i//2 + 1}. {san}", end="")
            else:
                print(f" {san}")

        if len(remaining_moves) % 2 == 1:
            print()  # New line if odd number of moves

    def training_session(
        self, num_puzzles: int = 3, stockfish_path: Optional[str] = None
    ):
        """
        Run a training session with multiple puzzles.

        Args:
            num_puzzles: Number of puzzles to solve
            stockfish_path: Optional path to Stockfish for hints
        """
        print("\n" + "♔" * 60)
        print("CHESS PUZZLE TRAINING SESSION")
        print("♔" * 60)

        solved = 0

        for i in range(min(num_puzzles, len(self.puzzles))):
            puzzle = self.puzzles[i]

            if self.solve_puzzle(puzzle, stockfish_path):
                solved += 1

            if i < num_puzzles - 1:
                input("\nPress Enter for next puzzle...")

        print("\n" + "=" * 60)
        print(f"SESSION COMPLETE: {solved}/{num_puzzles} puzzles solved")
        print("=" * 60)


def demo_puzzles():
    """Demonstrate the puzzle trainer."""
    print("=" * 60)
    print("CHESS PUZZLES DEMONSTRATION")
    print("=" * 60)

    trainer = PuzzleTrainer()

    print(f"\n📚 Available puzzles: {len(trainer.puzzles)}")

    # Show puzzle themes
    themes = set(p.theme for p in trainer.puzzles)
    print(f"\n🎯 Puzzle themes: {', '.join(themes)}")

    # Show difficulty levels
    difficulties = set(p.difficulty for p in trainer.puzzles)
    print(f"📊 Difficulty levels: {', '.join(difficulties)}")

    # Show an example puzzle
    puzzle = trainer.get_puzzle(0)
    if puzzle:
        print(f"\n📝 Example Puzzle:")
        print(f"   Theme: {puzzle.theme}")
        print(f"   Difficulty: {puzzle.difficulty}")
        print(f"   Description: {puzzle.description}")

        board = puzzle.get_board()
        print("\n" + str(board))
        print(f"\nSolution: {' '.join(puzzle.solution)}")

    print("\n✅ Puzzle demonstration complete")


if __name__ == "__main__":
    demo_puzzles()
