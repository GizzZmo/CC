#!/usr/bin/env python3
"""
Cyberpunk GUI for Cyberchess
A futuristic, neon-themed graphical interface for chess.
"""

import datetime
import os
import random
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, simpledialog
from typing import Optional, Tuple

import chess
import chess.engine
import chess.pgn

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


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
        "white_piece": "#ffffff",  # White pieces
        "black_piece": "#000000",  # Black pieces
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

    def __init__(self, master, stockfish_path: Optional[str] = None, gemini_api_key: Optional[str] = None):
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
        self.game_mode = None  # 'pvp', 'pvc', 'cvc', 'gvg', 'svg', None
        self.player_color = chess.WHITE
        self.stockfish_path = stockfish_path
        self.gemini_api_key = gemini_api_key
        self.engine = None
        self.engine2 = None  # For AI vs AI modes
        self.gemini_model = None
        self.computer_thinking = False
        
        # Engine parameters
        self.stockfish_skill_level = 5
        self.stockfish_time_limit = 0.5

        # UI components
        self.square_buttons = {}
        self.info_labels = {}

        self._setup_ui()
        self._update_board()

    def _setup_ui(self):
        """Setup the cyberpunk UI."""
        # Make window resizable
        self.master.resizable(True, True)
        
        # Configure grid weights for responsive layout
        self.master.grid_rowconfigure(0, weight=0)  # Title
        self.master.grid_rowconfigure(1, weight=1)  # Main content
        self.master.grid_columnconfigure(0, weight=1)
        
        # Title with neon glow effect
        title_frame = tk.Frame(self.master, bg=self.COLORS["background"])
        title_frame.grid(row=0, column=0, sticky="ew", pady=10)

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
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Configure main frame grid
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)  # Board
        main_frame.grid_columnconfigure(1, weight=0)  # Right panel

        # Left panel - Board
        board_frame = tk.Frame(main_frame, bg=self.COLORS["background"])
        board_frame.grid(row=0, column=0, sticky="nsew", padx=10)

        self._create_board(board_frame)

        # Right panel - Info and controls
        right_frame = tk.Frame(main_frame, bg=self.COLORS["background"])
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        
        # Configure right frame grid
        right_frame.grid_rowconfigure(0, weight=1)  # Info panel
        right_frame.grid_rowconfigure(1, weight=0)  # Control panel
        right_frame.grid_columnconfigure(0, weight=1)

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
        info_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        
        # Configure grid
        info_frame.grid_rowconfigure(6, weight=1)  # Move history expands
        info_frame.grid_columnconfigure(0, weight=1)

        # Title
        tk.Label(
            info_frame,
            text="[ S Y S T E M   I N F O ]",
            font=("Courier New", 12, "bold"),
            fg=self.COLORS["neon_magenta"],
            bg=self.COLORS["background"],
        ).grid(row=0, column=0, pady=5, sticky="ew")

        # Game mode
        self.info_labels["mode"] = tk.Label(
            info_frame,
            text="MODE: Menu",
            font=("Courier New", 10),
            fg=self.COLORS["text"],
            bg=self.COLORS["background"],
            anchor="w",
        )
        self.info_labels["mode"].grid(row=1, column=0, sticky="ew", padx=10, pady=2)

        # Turn
        self.info_labels["turn"] = tk.Label(
            info_frame,
            text="TURN: White",
            font=("Courier New", 10),
            fg=self.COLORS["text"],
            bg=self.COLORS["background"],
            anchor="w",
        )
        self.info_labels["turn"].grid(row=2, column=0, sticky="ew", padx=10, pady=2)

        # Status
        self.info_labels["status"] = tk.Label(
            info_frame,
            text="STATUS: Ready",
            font=("Courier New", 10),
            fg=self.COLORS["neon_green"],
            bg=self.COLORS["background"],
            anchor="w",
        )
        self.info_labels["status"].grid(row=3, column=0, sticky="ew", padx=10, pady=2)

        # Move counter
        self.info_labels["moves"] = tk.Label(
            info_frame,
            text="MOVES: 0",
            font=("Courier New", 10),
            fg=self.COLORS["text"],
            bg=self.COLORS["background"],
            anchor="w",
        )
        self.info_labels["moves"].grid(row=4, column=0, sticky="ew", padx=10, pady=2)

        # Separator
        sep_frame = tk.Frame(info_frame, bg=self.COLORS["neon_cyan"], height=2)
        sep_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=10)

        # Move history
        tk.Label(
            info_frame,
            text="[ M O V E   L O G ]",
            font=("Courier New", 10, "bold"),
            fg=self.COLORS["neon_cyan"],
            bg=self.COLORS["background"],
        ).grid(row=6, column=0, pady=5, sticky="ew")

        # Scrollable move history
        history_container = tk.Frame(info_frame, bg=self.COLORS["background"])
        history_container.grid(row=7, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Configure grid for history container
        history_container.grid_rowconfigure(0, weight=1)
        history_container.grid_columnconfigure(0, weight=1)

        scrollbar = tk.Scrollbar(history_container)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.move_list = tk.Listbox(
            history_container,
            font=("Courier New", 9),
            bg=self.COLORS["board_dark"],
            fg=self.COLORS["neon_green"],
            selectbackground=self.COLORS["highlight"],
            yscrollcommand=scrollbar.set,
            height=12,
        )
        self.move_list.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.move_list.yview)

    def _create_control_panel(self, parent):
        """Create the control panel with buttons."""
        control_frame = tk.Frame(
            parent,
            bg=self.COLORS["background"],
            highlightbackground=self.COLORS["neon_yellow"],
            highlightthickness=2,
        )
        control_frame.grid(row=1, column=0, sticky="ew", pady=5)

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
            "font": ("Courier New", 9, "bold"),
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
        ).pack(fill=tk.X, padx=10, pady=2)

        # Player vs Computer button
        if self.stockfish_path and os.path.exists(self.stockfish_path):
            tk.Button(
                control_frame,
                text="🤖 VS COMPUTER",
                command=self._new_game_pvc,
                **btn_config,
            ).pack(fill=tk.X, padx=10, pady=2)
            
            # Stockfish vs Stockfish
            tk.Button(
                control_frame,
                text="🤖 STOCKFISH vs STOCKFISH",
                command=self._new_game_stockfish_vs_stockfish,
                **btn_config,
            ).pack(fill=tk.X, padx=10, pady=2)

        # Gemini vs Gemini button
        if GEMINI_AVAILABLE and self.gemini_api_key:
            tk.Button(
                control_frame,
                text="🧠 GEMINI vs GEMINI",
                command=self._new_game_gemini_vs_gemini,
                **btn_config,
            ).pack(fill=tk.X, padx=10, pady=2)

        # Stockfish vs Gemini button
        if self.stockfish_path and os.path.exists(self.stockfish_path) and GEMINI_AVAILABLE and self.gemini_api_key:
            tk.Button(
                control_frame,
                text="⚔️ STOCKFISH vs GEMINI",
                command=self._new_game_stockfish_vs_gemini,
                **btn_config,
            ).pack(fill=tk.X, padx=10, pady=2)

        # Settings button
        tk.Button(
            control_frame, 
            text="⚙️ SETTINGS", 
            command=self._show_settings,
            **btn_config
        ).pack(fill=tk.X, padx=10, pady=2)

        # Reset button
        tk.Button(
            control_frame, text="↻ RESET BOARD", command=self._reset_game, **btn_config
        ).pack(fill=tk.X, padx=10, pady=2)

        # Quit button
        quit_btn_config = btn_config.copy()
        quit_btn_config["fg"] = self.COLORS["neon_red"]
        tk.Button(
            control_frame, text="✕ EXIT", command=self.master.quit, **quit_btn_config
        ).pack(fill=tk.X, padx=10, pady=2)

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
                        self.COLORS["white_piece"]
                        if piece.color == chess.WHITE
                        else self.COLORS["black_piece"]
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

        # In AI vs AI modes, ignore all clicks
        if self.game_mode in ["cvc", "gvg", "svg"]:
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
            self.engine.configure({"Skill Level": self.stockfish_skill_level})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Stockfish: {e}")
            self.game_mode = "pvp"
            return

        self._reset_game()

        # If computer plays white, make first move
        if self.player_color == chess.BLACK:
            self.master.after(500, self._computer_move)
    
    def _new_game_stockfish_vs_stockfish(self):
        """Start a new Stockfish vs Stockfish game."""
        if not self.stockfish_path or not os.path.exists(self.stockfish_path):
            messagebox.showerror("Error", "Stockfish engine not found!")
            return

        self.game_mode = "cvc"
        self.info_labels["mode"].config(text="MODE: Stockfish vs Stockfish")

        # Initialize both engines
        try:
            if self.engine:
                self.engine.quit()
            if self.engine2:
                self.engine2.quit()
            
            self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            self.engine.configure({"Skill Level": self.stockfish_skill_level})
            
            self.engine2 = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            self.engine2.configure({"Skill Level": self.stockfish_skill_level})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Stockfish: {e}")
            self.game_mode = "pvp"
            return

        self._reset_game()
        
        # Start the game
        self.master.after(500, self._ai_vs_ai_move)
    
    def _new_game_gemini_vs_gemini(self):
        """Start a new Gemini vs Gemini game."""
        if not GEMINI_AVAILABLE:
            messagebox.showerror("Error", "Gemini library not available!")
            return
        
        if not self.gemini_api_key or self.gemini_api_key == "YOUR_GEMINI_API_KEY_HERE":
            messagebox.showerror("Error", "Gemini API key not configured! Please set it in Settings.")
            return

        self.game_mode = "gvg"
        self.info_labels["mode"].config(text="MODE: Gemini vs Gemini")

        # Initialize Gemini
        try:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize Gemini: {e}")
            self.game_mode = "pvp"
            return

        self._reset_game()
        
        # Start the game
        self.master.after(500, self._ai_vs_ai_move)
    
    def _new_game_stockfish_vs_gemini(self):
        """Start a new Stockfish vs Gemini game."""
        if not self.stockfish_path or not os.path.exists(self.stockfish_path):
            messagebox.showerror("Error", "Stockfish engine not found!")
            return
        
        if not GEMINI_AVAILABLE:
            messagebox.showerror("Error", "Gemini library not available!")
            return
        
        if not self.gemini_api_key or self.gemini_api_key == "YOUR_GEMINI_API_KEY_HERE":
            messagebox.showerror("Error", "Gemini API key not configured! Please set it in Settings.")
            return

        # Ask which AI plays white
        response = messagebox.askyesno(
            "Choose Colors", "Should Stockfish play White?\n\nYes = Stockfish White\nNo = Gemini White"
        )
        stockfish_color = chess.WHITE if response else chess.BLACK

        self.game_mode = "svg"
        self.player_color = stockfish_color  # Store which color is Stockfish
        
        if stockfish_color == chess.WHITE:
            self.info_labels["mode"].config(text="MODE: Stockfish (White) vs Gemini (Black)")
        else:
            self.info_labels["mode"].config(text="MODE: Gemini (White) vs Stockfish (Black)")

        # Initialize engines
        try:
            if self.engine:
                self.engine.quit()
            
            self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            self.engine.configure({"Skill Level": self.stockfish_skill_level})
            
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize engines: {e}")
            self.game_mode = "pvp"
            return

        self._reset_game()
        
        # Start the game
        self.master.after(500, self._ai_vs_ai_move)

    def _computer_move(self):
        """Make a computer move."""
        if not self.engine or self.board.is_game_over():
            return

        self.computer_thinking = True
        self._update_info()

        try:
            result = self.engine.play(self.board, chess.engine.Limit(time=self.stockfish_time_limit))
            self._make_move(result.move)
        except Exception as e:
            messagebox.showerror("Error", f"Computer move failed: {e}")
        finally:
            self.computer_thinking = False
            self._update_info()
    
    def _ai_vs_ai_move(self):
        """Make an AI vs AI move."""
        if self.board.is_game_over():
            return

        self.computer_thinking = True
        self._update_info()

        try:
            move = None
            
            if self.game_mode == "cvc":
                # Stockfish vs Stockfish
                engine = self.engine if self.board.turn == chess.WHITE else self.engine2
                result = engine.play(self.board, chess.engine.Limit(time=self.stockfish_time_limit))
                move = result.move
                
            elif self.game_mode == "gvg":
                # Gemini vs Gemini
                move = self._get_gemini_move()
                
            elif self.game_mode == "svg":
                # Stockfish vs Gemini
                if self.board.turn == self.player_color:
                    # Stockfish's turn
                    result = self.engine.play(self.board, chess.engine.Limit(time=self.stockfish_time_limit))
                    move = result.move
                else:
                    # Gemini's turn
                    move = self._get_gemini_move()
            
            if move:
                self._make_move(move)
                
                # Continue the game if not over
                if not self.board.is_game_over():
                    self.master.after(500, self._ai_vs_ai_move)
                    
        except Exception as e:
            messagebox.showerror("Error", f"AI move failed: {e}")
        finally:
            self.computer_thinking = False
            self._update_info()
    
    def _get_gemini_move(self, retries: int = 3) -> Optional[chess.Move]:
        """Get a move from Gemini AI."""
        if not self.gemini_model:
            return None
            
        legal_moves = [move.uci() for move in self.board.legal_moves]
        color = "White" if self.board.turn == chess.WHITE else "Black"

        prompt = f"""
        You are playing a game of Chess. You are playing {color}.
        
        Current Board Position (FEN): {self.board.fen()}
        
        Here is the list of legally possible moves you can make:
        {', '.join(legal_moves)}
        
        Your goal is to survive and learn. Analyze the board.
        Pick the best move from the legal list above.
        
        IMPORTANT: Reply ONLY with the move in UCI format (e.g., e7e5). Do not write any other text.
        """

        for attempt in range(retries):
            try:
                response = self.gemini_model.generate_content(prompt)
                move_str = (
                    response.text.strip()
                    .replace("\n", "")
                    .replace(" ", "")
                    .replace("`", "")
                )

                move = chess.Move.from_uci(move_str)

                if move in self.board.legal_moves:
                    return move
                else:
                    print(f"Gemini tried illegal move: {move_str}. Retrying...")
                    prompt += f"\n\nERROR: {move_str} is not a legal move. Please choose strictly from the provided list."

            except Exception as e:
                print(f"Error parsing Gemini response: {e}")
                prompt += f"\n\nERROR: Invalid format. Please reply ONLY with the move string (e.g., e7e5)."

        # Fallback to random move
        print("Gemini failed to produce a legal move. Making random move.")
        return random.choice(list(self.board.legal_moves))
    
    def _show_settings(self):
        """Show settings dialog."""
        settings_window = tk.Toplevel(self.master)
        settings_window.title("⚙️ Settings")
        settings_window.configure(bg=self.COLORS["background"])
        settings_window.geometry("500x400")
        
        # Title
        tk.Label(
            settings_window,
            text="[ S E T T I N G S ]",
            font=("Courier New", 16, "bold"),
            fg=self.COLORS["neon_cyan"],
            bg=self.COLORS["background"],
        ).pack(pady=10)
        
        # Settings frame
        settings_frame = tk.Frame(settings_window, bg=self.COLORS["background"])
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Stockfish Path
        tk.Label(
            settings_frame,
            text="Stockfish Path:",
            font=("Courier New", 10, "bold"),
            fg=self.COLORS["neon_yellow"],
            bg=self.COLORS["background"],
            anchor="w",
        ).pack(fill=tk.X, pady=(5, 2))
        
        stockfish_entry = tk.Entry(
            settings_frame,
            font=("Courier New", 9),
            bg=self.COLORS["board_dark"],
            fg=self.COLORS["text"],
            insertbackground=self.COLORS["neon_cyan"],
        )
        stockfish_entry.insert(0, self.stockfish_path if self.stockfish_path else "")
        stockfish_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Gemini API Key
        tk.Label(
            settings_frame,
            text="Gemini API Key:",
            font=("Courier New", 10, "bold"),
            fg=self.COLORS["neon_yellow"],
            bg=self.COLORS["background"],
            anchor="w",
        ).pack(fill=tk.X, pady=(5, 2))
        
        gemini_entry = tk.Entry(
            settings_frame,
            font=("Courier New", 9),
            bg=self.COLORS["board_dark"],
            fg=self.COLORS["text"],
            insertbackground=self.COLORS["neon_cyan"],
            show="*",
        )
        gemini_entry.insert(0, self.gemini_api_key if self.gemini_api_key else "")
        gemini_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Stockfish Skill Level
        tk.Label(
            settings_frame,
            text="Stockfish Skill Level (0-20):",
            font=("Courier New", 10, "bold"),
            fg=self.COLORS["neon_yellow"],
            bg=self.COLORS["background"],
            anchor="w",
        ).pack(fill=tk.X, pady=(5, 2))
        
        skill_frame = tk.Frame(settings_frame, bg=self.COLORS["background"])
        skill_frame.pack(fill=tk.X, pady=(0, 10))
        
        skill_var = tk.IntVar(value=self.stockfish_skill_level)
        skill_scale = tk.Scale(
            skill_frame,
            from_=0,
            to=20,
            orient=tk.HORIZONTAL,
            variable=skill_var,
            font=("Courier New", 9),
            bg=self.COLORS["board_dark"],
            fg=self.COLORS["text"],
            troughcolor=self.COLORS["board_light"],
            activebackground=self.COLORS["neon_cyan"],
        )
        skill_scale.pack(fill=tk.X)
        
        # Stockfish Time Limit
        tk.Label(
            settings_frame,
            text="Stockfish Time Limit (seconds):",
            font=("Courier New", 10, "bold"),
            fg=self.COLORS["neon_yellow"],
            bg=self.COLORS["background"],
            anchor="w",
        ).pack(fill=tk.X, pady=(5, 2))
        
        time_entry = tk.Entry(
            settings_frame,
            font=("Courier New", 9),
            bg=self.COLORS["board_dark"],
            fg=self.COLORS["text"],
            insertbackground=self.COLORS["neon_cyan"],
        )
        time_entry.insert(0, str(self.stockfish_time_limit))
        time_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Save button
        def save_settings():
            self.stockfish_path = stockfish_entry.get().strip()
            self.gemini_api_key = gemini_entry.get().strip()
            self.stockfish_skill_level = skill_var.get()
            try:
                self.stockfish_time_limit = float(time_entry.get())
            except ValueError:
                self.stockfish_time_limit = 0.5
            
            messagebox.showinfo("Settings", "Settings saved successfully!")
            settings_window.destroy()
            
            # Recreate control panel to show/hide AI buttons
            for widget in self.master.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Frame):
                                    # Find the right panel
                                    pass
            
            # Note: For simplicity, we'll just ask user to restart
            messagebox.showinfo("Settings", "Please restart the application for some changes to take effect.")
        
        save_btn_config = {
            "font": ("Courier New", 10, "bold"),
            "bg": self.COLORS["board_dark"],
            "fg": self.COLORS["neon_green"],
            "activebackground": self.COLORS["neon_green"],
            "activeforeground": self.COLORS["background"],
            "relief": tk.RAISED,
            "borderwidth": 2,
            "cursor": "hand2",
        }
        
        tk.Button(
            settings_window,
            text="💾 SAVE SETTINGS",
            command=save_settings,
            **save_btn_config,
        ).pack(fill=tk.X, padx=20, pady=10)

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
        if self.engine2:
            try:
                self.engine2.quit()
            except:
                pass


def main():
    """Main entry point for the GUI."""
    # Get Stockfish path from environment or config
    stockfish_path = os.environ.get("STOCKFISH_PATH", None)
    
    # Get Gemini API key from environment or config
    gemini_api_key = os.environ.get("GOOGLE_API_KEY", None)

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

    # Make window resizable and set minimum size
    root.minsize(1000, 700)
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set window size to 80% of screen size
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)
    
    # Calculate position to center window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create GUI
    gui = CyberpunkChessGUI(root, stockfish_path, gemini_api_key)

    # Handle window close
    def on_closing():
        gui.cleanup()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start GUI
    root.mainloop()


if __name__ == "__main__":
    main()
