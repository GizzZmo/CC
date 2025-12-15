#!/usr/bin/env python3
"""
Cyberpunk GUI for Cyberchess
A futuristic, neon-themed graphical interface for chess.
"""

import datetime
import os
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from typing import Optional, Tuple

import chess
import chess.engine
import chess.pgn


class CyberpunkChessGUI:
    """Cyberpunk-themed chess GUI."""

    # Cyberpunk color scheme
    COLORS = {
        "background": "#0a0e27",  # Dark space blue
        "board_dark": "#1a1f3a",  # Dark square
        "board_light": "#2d3561",  # Light square
        "neon_cyan": "#00fff9",
        "neon_magenta": "#ff00ff",
        "neon_yellow": "#ffff00",
        "neon_green": "#39ff14",
        "neon_red": "#ff073a",
        "neon_blue": "#0ff0fc",
        "text": "#00fff9",
        "highlight": "#ff00ff",
        "selected": "#ffff00",
        "last_move": "#39ff14",
        "grid": "#00fff9",
    }

    # Chess piece Unicode symbols
    PIECES = {
        "P": "♙",
        "N": "♘",
        "B": "♗",
        "R": "♖",
        "Q": "♕",
        "K": "♔",
        "p": "♟",
        "n": "♞",
        "b": "♝",
        "r": "♜",
        "q": "♛",
        "k": "♚",
    }

    def __init__(self, master, stockfish_path: Optional[str] = None):
        self.master = master
        self.master.title("⚡ CYBERCHESS ⚡")
        self.master.configure(bg=self.COLORS["background"])

        # Game state
        self.board = chess.Board()
        self.selected_square = None
        self.legal_moves = []
        self.move_history = []
        self.last_move = None

        # Game mode
        self.game_mode = None  # 'pvp', 'pvc', None
        self.player_color = chess.WHITE
        self.stockfish_path = stockfish_path
        self.engine = None
        self.computer_thinking = False

        # UI components
        self.square_buttons = {}
        self.info_labels = {}

        self._setup_ui()
        self._update_board()

    def _setup_ui(self):
        """Setup the cyberpunk UI."""
        # Title with neon glow effect
        title_frame = tk.Frame(self.master, bg=self.COLORS["background"])
        title_frame.pack(pady=10)

        title = tk.Label(
            title_frame,
            text="⚡ C Y B E R C H E S S ⚡",
            font=("Courier New", 28, "bold"),
            fg=self.COLORS["neon_cyan"],
            bg=self.COLORS["background"],
        )
        title.pack()

        subtitle = tk.Label(
            title_frame,
            text="[ N E O N   C H E S S   I N T E R F A C E ]",
            font=("Courier New", 10),
            fg=self.COLORS["neon_magenta"],
            bg=self.COLORS["background"],
        )
        subtitle.pack()

        # Main container
        main_frame = tk.Frame(self.master, bg=self.COLORS["background"])
        main_frame.pack(padx=20, pady=10)

        # Left panel - Board
        board_frame = tk.Frame(main_frame, bg=self.COLORS["background"])
        board_frame.pack(side=tk.LEFT, padx=10)

        self._create_board(board_frame)

        # Right panel - Info and controls
        right_frame = tk.Frame(main_frame, bg=self.COLORS["background"])
        right_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH)

        self._create_info_panel(right_frame)
        self._create_control_panel(right_frame)

    def _create_board(self, parent):
        """Create the chess board with cyberpunk styling."""
        # Board container with neon border
        board_container = tk.Frame(
            parent,
            bg=self.COLORS["neon_cyan"],
            highlightbackground=self.COLORS["neon_cyan"],
            highlightthickness=3,
        )
        board_container.pack()

        # Coordinates
        coord_frame = tk.Frame(board_container, bg=self.COLORS["background"])
        coord_frame.pack()

        # Top coordinates (a-h)
        top_coord = tk.Frame(coord_frame, bg=self.COLORS["background"])
        top_coord.grid(row=0, column=1)

        for i, letter in enumerate("abcdefgh"):
            tk.Label(
                top_coord,
                text=letter.upper(),
                font=("Courier New", 10, "bold"),
                fg=self.COLORS["neon_yellow"],
                bg=self.COLORS["background"],
                width=6,
            ).grid(row=0, column=i)

        # Board squares
        squares_frame = tk.Frame(coord_frame, bg=self.COLORS["background"])
        squares_frame.grid(row=1, column=1)

        for row in range(8):
            # Left coordinates (8-1)
            tk.Label(
                coord_frame,
                text=str(8 - row),
                font=("Courier New", 10, "bold"),
                fg=self.COLORS["neon_yellow"],
                bg=self.COLORS["background"],
                width=2,
            ).grid(row=row + 1, column=0)

            for col in range(8):
                square = chess.square(col, 7 - row)
                is_light = (row + col) % 2 == 0

                btn = tk.Button(
                    squares_frame,
                    text="",
                    font=("Arial", 32),
                    width=3,
                    height=1,
                    bg=(
                        self.COLORS["board_light"]
                        if is_light
                        else self.COLORS["board_dark"]
                    ),
                    fg=self.COLORS["neon_cyan"],
                    activebackground=self.COLORS["selected"],
                    relief=tk.FLAT,
                    borderwidth=2,
                    command=lambda s=square: self._on_square_click(s),
                )
                btn.grid(row=row, column=col, padx=1, pady=1)
                self.square_buttons[square] = btn

            # Right coordinates (8-1)
            tk.Label(
                coord_frame,
                text=str(8 - row),
                font=("Courier New", 10, "bold"),
                fg=self.COLORS["neon_yellow"],
                bg=self.COLORS["background"],
                width=2,
            ).grid(row=row + 1, column=2)

        # Bottom coordinates (a-h)
        bottom_coord = tk.Frame(coord_frame, bg=self.COLORS["background"])
        bottom_coord.grid(row=9, column=1)

        for i, letter in enumerate("abcdefgh"):
            tk.Label(
                bottom_coord,
                text=letter.upper(),
                font=("Courier New", 10, "bold"),
                fg=self.COLORS["neon_yellow"],
                bg=self.COLORS["background"],
                width=6,
            ).grid(row=0, column=i)

    def _create_info_panel(self, parent):
        """Create the information panel."""
        info_frame = tk.Frame(
            parent,
            bg=self.COLORS["background"],
            highlightbackground=self.COLORS["neon_magenta"],
            highlightthickness=2,
        )
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Title
        tk.Label(
            info_frame,
            text="[ S Y S T E M   I N F O ]",
            font=("Courier New", 12, "bold"),
            fg=self.COLORS["neon_magenta"],
            bg=self.COLORS["background"],
        ).pack(pady=5)

        # Game mode
        self.info_labels["mode"] = tk.Label(
            info_frame,
            text="MODE: Menu",
            font=("Courier New", 10),
            fg=self.COLORS["text"],
            bg=self.COLORS["background"],
            anchor="w",
        )
        self.info_labels["mode"].pack(fill=tk.X, padx=10, pady=2)

        # Turn
        self.info_labels["turn"] = tk.Label(
            info_frame,
            text="TURN: White",
            font=("Courier New", 10),
            fg=self.COLORS["text"],
            bg=self.COLORS["background"],
            anchor="w",
        )
        self.info_labels["turn"].pack(fill=tk.X, padx=10, pady=2)

        # Status
        self.info_labels["status"] = tk.Label(
            info_frame,
            text="STATUS: Ready",
            font=("Courier New", 10),
            fg=self.COLORS["neon_green"],
            bg=self.COLORS["background"],
            anchor="w",
        )
        self.info_labels["status"].pack(fill=tk.X, padx=10, pady=2)

        # Move counter
        self.info_labels["moves"] = tk.Label(
            info_frame,
            text="MOVES: 0",
            font=("Courier New", 10),
            fg=self.COLORS["text"],
            bg=self.COLORS["background"],
            anchor="w",
        )
        self.info_labels["moves"].pack(fill=tk.X, padx=10, pady=2)

        # Separator
        tk.Frame(info_frame, bg=self.COLORS["neon_cyan"], height=2).pack(
            fill=tk.X, padx=10, pady=10
        )

        # Move history
        tk.Label(
            info_frame,
            text="[ M O V E   L O G ]",
            font=("Courier New", 10, "bold"),
            fg=self.COLORS["neon_cyan"],
            bg=self.COLORS["background"],
        ).pack(pady=5)

        # Scrollable move history
        history_container = tk.Frame(info_frame, bg=self.COLORS["background"])
        history_container.pack(fill=tk.BOTH, expand=True, padx=10)

        scrollbar = tk.Scrollbar(history_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.move_list = tk.Listbox(
            history_container,
            font=("Courier New", 9),
            bg=self.COLORS["board_dark"],
            fg=self.COLORS["neon_green"],
            selectbackground=self.COLORS["highlight"],
            yscrollcommand=scrollbar.set,
            height=12,
        )
        self.move_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.move_list.yview)

    def _create_control_panel(self, parent):
        """Create the control panel with buttons."""
        control_frame = tk.Frame(
            parent,
            bg=self.COLORS["background"],
            highlightbackground=self.COLORS["neon_yellow"],
            highlightthickness=2,
        )
        control_frame.pack(fill=tk.X, pady=5)

        # Title
        tk.Label(
            control_frame,
            text="[ C O N T R O L S ]",
            font=("Courier New", 10, "bold"),
            fg=self.COLORS["neon_yellow"],
            bg=self.COLORS["background"],
        ).pack(pady=5)

        # Button style
        btn_config = {
            "font": ("Courier New", 10, "bold"),
            "bg": self.COLORS["board_dark"],
            "fg": self.COLORS["neon_cyan"],
            "activebackground": self.COLORS["neon_cyan"],
            "activeforeground": self.COLORS["background"],
            "relief": tk.RAISED,
            "borderwidth": 2,
            "cursor": "hand2",
        }

        # New Game button
        tk.Button(
            control_frame,
            text="⚡ NEW GAME (PvP)",
            command=self._new_game_pvp,
            **btn_config,
        ).pack(fill=tk.X, padx=10, pady=3)

        # Player vs Computer button
        if self.stockfish_path and os.path.exists(self.stockfish_path):
            tk.Button(
                control_frame,
                text="🤖 VS COMPUTER",
                command=self._new_game_pvc,
                **btn_config,
            ).pack(fill=tk.X, padx=10, pady=3)

        # Reset button
        tk.Button(
            control_frame, text="↻ RESET BOARD", command=self._reset_game, **btn_config
        ).pack(fill=tk.X, padx=10, pady=3)

        # Quit button
        quit_btn_config = btn_config.copy()
        quit_btn_config["fg"] = self.COLORS["neon_red"]
        tk.Button(
            control_frame, text="✕ EXIT", command=self.master.quit, **quit_btn_config
        ).pack(fill=tk.X, padx=10, pady=3)

    def _update_board(self):
        """Update the board display."""
        for square in chess.SQUARES:
            btn = self.square_buttons[square]
            piece = self.board.piece_at(square)

            # Set piece symbol
            if piece:
                symbol = self.PIECES.get(piece.symbol(), piece.symbol())
                btn.config(text=symbol)
                # Color based on piece color
                btn.config(
                    fg=(
                        self.COLORS["neon_cyan"]
                        if piece.color == chess.WHITE
                        else self.COLORS["neon_magenta"]
                    )
                )
            else:
                btn.config(text="")

            # Reset background
            row, col = chess.square_rank(square), chess.square_file(square)
            is_light = (row + col) % 2 == 1
            default_bg = (
                self.COLORS["board_light"] if is_light else self.COLORS["board_dark"]
            )

            # Highlight selected square
            if square == self.selected_square:
                btn.config(
                    bg=self.COLORS["selected"],
                    highlightbackground=self.COLORS["neon_yellow"],
                    highlightthickness=3,
                )
            # Highlight legal move targets
            elif square in [move.to_square for move in self.legal_moves]:
                btn.config(
                    bg=self.COLORS["highlight"],
                    highlightbackground=self.COLORS["neon_magenta"],
                    highlightthickness=2,
                )
            # Highlight last move
            elif self.last_move and square in [
                self.last_move.from_square,
                self.last_move.to_square,
            ]:
                btn.config(
                    bg=self.COLORS["last_move"],
                    highlightbackground=self.COLORS["neon_green"],
                    highlightthickness=2,
                )
            else:
                btn.config(bg=default_bg, highlightthickness=0)

        # Update info panel
        self._update_info()

    def _update_info(self):
        """Update the information panel."""
        # Turn
        turn_text = "White" if self.board.turn == chess.WHITE else "Black"
        self.info_labels["turn"].config(text=f"TURN: {turn_text}")

        # Move counter
        self.info_labels["moves"].config(text=f"MOVES: {len(self.move_history)}")

        # Status
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            self.info_labels["status"].config(
                text=f"STATUS: Checkmate! {winner} wins!", fg=self.COLORS["neon_red"]
            )
        elif self.board.is_stalemate():
            self.info_labels["status"].config(
                text="STATUS: Stalemate - Draw!", fg=self.COLORS["neon_yellow"]
            )
        elif self.board.is_check():
            self.info_labels["status"].config(
                text="STATUS: Check!", fg=self.COLORS["neon_red"]
            )
        elif self.computer_thinking:
            self.info_labels["status"].config(
                text="STATUS: Computer thinking...", fg=self.COLORS["neon_cyan"]
            )
        else:
            self.info_labels["status"].config(
                text="STATUS: Ready", fg=self.COLORS["neon_green"]
            )

    def _on_square_click(self, square):
        """Handle square click."""
        if self.board.is_game_over():
            messagebox.showinfo("Game Over", "Game is over! Start a new game.")
            return

        # If computer is thinking, ignore clicks
        if self.computer_thinking:
            return

        # If playing as computer and it's computer's turn, ignore clicks
        if self.game_mode == "pvc" and self.board.turn != self.player_color:
            return

        # If no square selected, try to select this square
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.legal_moves = [
                    move
                    for move in self.board.legal_moves
                    if move.from_square == square
                ]
                self._update_board()
        else:
            # Try to make a move
            # Find all legal moves to the clicked square
            possible_moves = [m for m in self.legal_moves if m.to_square == square]

            if possible_moves:
                # If there are multiple moves (e.g., different promotions), default to queen
                move = None
                for m in possible_moves:
                    if m.promotion == chess.QUEEN or m.promotion is None:
                        move = m
                        break

                # If no queen promotion found, just take the first move
                if move is None:
                    move = possible_moves[0]

                self._make_move(move)

            # Deselect
            self.selected_square = None
            self.legal_moves = []
            self._update_board()

            # If playing against computer, trigger computer move
            if self.game_mode == "pvc" and not self.board.is_game_over():
                self.master.after(500, self._computer_move)

    def _make_move(self, move):
        """Make a move on the board."""
        san = self.board.san(move)
        self.board.push(move)
        self.move_history.append(san)
        self.last_move = move

        # Add to move list
        move_num = len(self.move_history)
        if move_num % 2 == 1:
            self.move_list.insert(tk.END, f"{(move_num + 1) // 2}. {san}")
        else:
            # Update last line with black's move
            last_idx = self.move_list.size() - 1
            current = self.move_list.get(last_idx)
            self.move_list.delete(last_idx)
            self.move_list.insert(last_idx, f"{current} {san}")

        self.move_list.see(tk.END)
        self._update_board()

    def _new_game_pvp(self):
        """Start a new Player vs Player game."""
        self.game_mode = "pvp"
        self.info_labels["mode"].config(text="MODE: Player vs Player")
        self._reset_game()

    def _new_game_pvc(self):
        """Start a new Player vs Computer game."""
        if not self.stockfish_path or not os.path.exists(self.stockfish_path):
            messagebox.showerror("Error", "Stockfish engine not found!")
            return

        # Ask for color
        response = messagebox.askyesno(
            "Choose Color", "Do you want to play as White?\n\nYes = White\nNo = Black"
        )
        self.player_color = chess.WHITE if response else chess.BLACK

        self.game_mode = "pvc"
        color_text = "White" if self.player_color == chess.WHITE else "Black"
        self.info_labels["mode"].config(text=f"MODE: Player ({color_text}) vs Computer")

        # Initialize engine
        try:
            if self.engine:
                self.engine.quit()
            self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            self.engine.configure({"Skill Level": 5})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Stockfish: {e}")
            self.game_mode = "pvp"
            return

        self._reset_game()

        # If computer plays white, make first move
        if self.player_color == chess.BLACK:
            self.master.after(500, self._computer_move)

    def _computer_move(self):
        """Make a computer move."""
        if not self.engine or self.board.is_game_over():
            return

        self.computer_thinking = True
        self._update_info()

        try:
            result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
            self._make_move(result.move)
        except Exception as e:
            messagebox.showerror("Error", f"Computer move failed: {e}")
        finally:
            self.computer_thinking = False
            self._update_info()

    def _reset_game(self):
        """Reset the game."""
        self.board = chess.Board()
        self.selected_square = None
        self.legal_moves = []
        self.move_history = []
        self.last_move = None
        self.computer_thinking = False
        self.move_list.delete(0, tk.END)
        self._update_board()

    def cleanup(self):
        """Clean up resources."""
        if self.engine:
            try:
                self.engine.quit()
            except:
                pass


def main():
    """Main entry point for the GUI."""
    # Get Stockfish path from environment or config
    stockfish_path = os.environ.get("STOCKFISH_PATH", None)

    # Try to find stockfish in common locations
    if not stockfish_path or stockfish_path == "YOUR_STOCKFISH_PATH_HERE":
        common_paths = [
            "/usr/bin/stockfish",
            "/usr/local/bin/stockfish",
            "/opt/homebrew/bin/stockfish",
            "C:\\Program Files\\Stockfish\\stockfish.exe",
        ]
        for path in common_paths:
            if os.path.exists(path):
                stockfish_path = path
                break

    root = tk.Tk()

    # Set window size
    root.geometry("1200x800")
    root.resizable(False, False)

    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Create GUI
    gui = CyberpunkChessGUI(root, stockfish_path)

    # Handle window close
    def on_closing():
        gui.cleanup()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start GUI
    root.mainloop()


if __name__ == "__main__":
    main()
