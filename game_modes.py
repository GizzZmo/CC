"""
Game modes module for Cyberchess.
Provides different ways to play chess (PvP, PvE, AI vs AI).
"""

import chess
import chess.engine
import chess.pgn
import google.generativeai as genai
import random
import datetime
from typing import Optional


class ChessGame:
    """Base chess game class with common functionality."""
    
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []
        
    def display_board(self):
        """Display the current board state."""
        print("\n" + "=" * 50)
        print(f"Move {self.board.fullmove_number}")
        print(self.board)
        
        # Display game state
        if self.board.is_check():
            print("⚠️  CHECK!")
        if self.board.is_checkmate():
            print("♔ CHECKMATE!")
        if self.board.is_stalemate():
            print("🤝 STALEMATE!")
        if self.board.is_insufficient_material():
            print("🤝 DRAW - Insufficient Material")
        if self.board.is_fifty_moves():
            print("🤝 DRAW - 50 Move Rule")
        if self.board.is_repetition():
            print("🤝 DRAW - Threefold Repetition")
            
    def display_move_history(self):
        """Display the game's move history in algebraic notation."""
        if not self.move_history:
            print("\nNo moves yet.")
            return
            
        print("\nMove History:")
        print("-" * 50)
        for i in range(0, len(self.move_history), 2):
            move_num = i // 2 + 1
            white_move = self.move_history[i]
            black_move = self.move_history[i + 1] if i + 1 < len(self.move_history) else ""
            print(f"{move_num}. {white_move:8} {black_move}")
            
    def make_move(self, move: chess.Move) -> str:
        """Make a move and record it in history. Returns the SAN notation."""
        # Convert to SAN (Standard Algebraic Notation) before making the move
        san_move = self.board.san(move)
        self.board.push(move)
        self.move_history.append(san_move)
        return san_move
        
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.board.is_game_over()
        
    def get_result(self) -> str:
        """Get the game result."""
        return self.board.result()
        
    def save_to_pgn(self, filename: str, white_player: str, black_player: str, event: str = "Cyberchess Game"):
        """Save the game to a PGN file."""
        pgn_game = chess.pgn.Game.from_board(self.board)
        pgn_game.headers["Event"] = event
        pgn_game.headers["White"] = white_player
        pgn_game.headers["Black"] = black_player
        pgn_game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")
        pgn_game.headers["Result"] = self.get_result()
        
        with open(filename, "a") as f:
            f.write(str(pgn_game) + "\n\n")
        print(f"\n✅ Game saved to '{filename}'")


class PlayerVsPlayerGame(ChessGame):
    """Player vs Player chess game."""
    
    def __init__(self):
        super().__init__()
        
    def get_player_move(self, player_name: str) -> chess.Move:
        """Get a move from a human player."""
        while True:
            try:
                print(f"\n{player_name}'s turn ({'White' if self.board.turn == chess.WHITE else 'Black'})")
                print(f"Legal moves: {', '.join([move.uci() for move in list(self.board.legal_moves)[:10]])}...")
                move_str = input("Enter your move (UCI format, e.g., e2e4): ").strip()
                
                move = chess.Move.from_uci(move_str)
                if move in self.board.legal_moves:
                    return move
                else:
                    print("❌ Illegal move! Try again.")
            except Exception as e:
                print(f"❌ Invalid format! Use UCI notation (e.g., e2e4). Error: {e}")
                
    def play(self):
        """Play a full Player vs Player game."""
        print("=" * 50)
        print("🎮 PLAYER VS PLAYER MODE")
        print("=" * 50)
        
        while not self.is_game_over():
            self.display_board()
            
            player_name = "Player 1" if self.board.turn == chess.WHITE else "Player 2"
            move = self.get_player_move(player_name)
            self.make_move(move)
            
        # Game over
        self.display_board()
        self.display_move_history()
        print("\n" + "=" * 50)
        print(f"🏁 GAME OVER - Result: {self.get_result()}")
        print("=" * 50)
        
        self.save_to_pgn("pvp_games.pgn", "Player 1", "Player 2")


class PlayerVsComputerGame(ChessGame):
    """Player vs Computer chess game."""
    
    def __init__(self, stockfish_path: str, player_color: chess.Color = chess.WHITE, skill_level: int = 10):
        super().__init__()
        self.stockfish_path = stockfish_path
        self.player_color = player_color
        self.skill_level = skill_level
        self.engine = None
        
    def start_engine(self):
        """Start the Stockfish engine."""
        self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
        self.engine.configure({"Skill Level": self.skill_level})
        
    def stop_engine(self):
        """Stop the Stockfish engine."""
        if self.engine:
            self.engine.quit()
            
    def get_player_move(self) -> chess.Move:
        """Get a move from the human player."""
        while True:
            try:
                print(f"\nYour turn ({'White' if self.board.turn == chess.WHITE else 'Black'})")
                print(f"Legal moves: {', '.join([move.uci() for move in list(self.board.legal_moves)[:10]])}...")
                move_str = input("Enter your move (UCI format, e.g., e2e4): ").strip()
                
                move = chess.Move.from_uci(move_str)
                if move in self.board.legal_moves:
                    return move
                else:
                    print("❌ Illegal move! Try again.")
            except Exception as e:
                print(f"❌ Invalid format! Use UCI notation (e.g., e2e4). Error: {e}")
                
    def get_computer_move(self) -> chess.Move:
        """Get a move from Stockfish."""
        print("\n🤖 Computer is thinking...")
        result = self.engine.play(self.board, chess.engine.Limit(time=1.0))
        return result.move
        
    def play(self):
        """Play a full Player vs Computer game."""
        print("=" * 50)
        print(f"🎮 PLAYER VS COMPUTER MODE (Skill Level {self.skill_level})")
        print(f"You are playing as {'White' if self.player_color == chess.WHITE else 'Black'}")
        print("=" * 50)
        
        self.start_engine()
        
        try:
            while not self.is_game_over():
                self.display_board()
                
                if self.board.turn == self.player_color:
                    move = self.get_player_move()
                else:
                    move = self.get_computer_move()
                    
                san_move = self.make_move(move)
                print(f"Move played: {san_move} ({move.uci()})")
                
            # Game over
            self.display_board()
            self.display_move_history()
            print("\n" + "=" * 50)
            print(f"🏁 GAME OVER - Result: {self.get_result()}")
            print("=" * 50)
            
            player_name = "Player (White)" if self.player_color == chess.WHITE else "Player (Black)"
            computer_name = f"Stockfish Level {self.skill_level} (Black)" if self.player_color == chess.WHITE else f"Stockfish Level {self.skill_level} (White)"
            
            if self.player_color == chess.WHITE:
                self.save_to_pgn("pvc_games.pgn", player_name, computer_name)
            else:
                self.save_to_pgn("pvc_games.pgn", computer_name, player_name)
                
        finally:
            self.stop_engine()


class AIvsAIGame(ChessGame):
    """
    AI vs AI chess game (Stockfish vs Gemini).
    
    Supports configurable or randomized AI color assignment for diverse training data.
    """
    
    def __init__(self, stockfish_path: str, google_api_key: str, stockfish_skill: int = 5, stockfish_color: Optional[chess.Color] = None):
        super().__init__()
        self.stockfish_path = stockfish_path
        self.stockfish_skill = stockfish_skill
        self.engine = None
        
        # AI color assignment: randomize if not specified
        if stockfish_color is None:
            self.stockfish_color = random.choice([chess.WHITE, chess.BLACK])
        else:
            self.stockfish_color = stockfish_color
        
        self.gemini_color = not self.stockfish_color
        
        # Setup Gemini
        genai.configure(api_key=google_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
    def start_engine(self):
        """Start the Stockfish engine."""
        self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
        self.engine.configure({"Skill Level": self.stockfish_skill})
        
    def stop_engine(self):
        """Stop the Stockfish engine."""
        if self.engine:
            self.engine.quit()
            
    def get_stockfish_move(self) -> chess.Move:
        """Get a move from Stockfish."""
        result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
        return result.move
        
    def get_gemini_move(self, retries: int = 3) -> chess.Move:
        """Get a move from Gemini AI."""
        legal_moves = [move.uci() for move in self.board.legal_moves]
        
        # Use Gemini's assigned color
        color = "White" if self.gemini_color == chess.WHITE else "Black"
        
        prompt = f"""
        You are playing a game of Chess against Stockfish. You are playing {color}.
        
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
                move_str = response.text.strip().replace("\n", "").replace(" ", "").replace("`", "")
                
                move = chess.Move.from_uci(move_str)
                
                if move in self.board.legal_moves:
                    return move
                else:
                    print(f" > Gemini tried illegal move: {move_str}. Retrying...")
                    prompt += f"\n\nERROR: {move_str} is not a legal move. Please choose strictly from the provided list."
            
            except Exception as e:
                print(f" > Error parsing Gemini response: {e}")
                prompt += f"\n\nERROR: Invalid format. Please reply ONLY with the move string (e.g., e7e5)."
        
        # Fallback to random move
        print(" > Gemini failed to produce a legal move. Making random move.")
        return random.choice(list(self.board.legal_moves))
        
    def play(self):
        """Play a full AI vs AI game."""
        print("=" * 50)
        print(f"🤖 AI VS AI MODE: Stockfish (Level {self.stockfish_skill}) vs Gemini")
        stockfish_color_name = "White" if self.stockfish_color == chess.WHITE else "Black"
        gemini_color_name = "White" if self.gemini_color == chess.WHITE else "Black"
        print(f"Stockfish plays {stockfish_color_name}, Gemini plays {gemini_color_name}")
        print("=" * 50)
        
        self.start_engine()
        
        try:
            while not self.is_game_over():
                self.display_board()
                
                if self.board.turn == self.stockfish_color:
                    print("Stockfish is thinking...")
                    move = self.get_stockfish_move()
                    player = "Stockfish"
                else:
                    print("Gemini is thinking...")
                    move = self.get_gemini_move()
                    player = "Gemini"
                    
                san_move = self.make_move(move)
                print(f"{player} played: {san_move} ({move.uci()})")
                
            # Game over
            self.display_board()
            self.display_move_history()
            print("\n" + "=" * 50)
            print(f"🏁 GAME OVER - Result: {self.get_result()}")
            print("=" * 50)
            
            # Set player names based on actual colors
            stockfish_name = f"Stockfish Level {self.stockfish_skill}"
            gemini_name = "Gemini 1.5 Flash"
            
            if self.stockfish_color == chess.WHITE:
                white_player = stockfish_name
                black_player = gemini_name
            else:
                white_player = gemini_name
                black_player = stockfish_name
            
            self.save_to_pgn("ai_vs_ai_games.pgn", 
                           white_player,
                           black_player,
                           "Cyberchess AI Training")
                
        finally:
            self.stop_engine()
