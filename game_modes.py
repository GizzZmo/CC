"""
Game modes module for Cyberchess.
Provides different ways to play chess (PvP, PvE, AI vs AI).
"""

import sys
import chess
import chess.engine
import chess.pgn
import google.generativeai as genai
import random
import datetime
import time
from typing import Optional, List, Tuple

# Configure stdout/stderr to use UTF-8 encoding on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')


class ChessGame:
    """Base chess game class with common functionality."""
    
    # Available board themes
    THEMES = {
        'ascii': 'ASCII (letters and dots)',
        'unicode': 'Unicode (chess symbols)',
        'borders': 'Unicode with borders and coordinates'
    }
    
    def __init__(self, theme: str = 'ascii'):
        self.board = chess.Board()
        self.move_history = []
        self.time_controls = None  # Optional time control settings
        self.white_time = None
        self.black_time = None
        self.theme = theme if theme in self.THEMES else 'ascii'
        
    def display_board(self):
        """Display the current board state using the selected theme."""
        print("\n" + "=" * 50)
        print(f"Move {self.board.fullmove_number}")
        
        # Display time if time controls are enabled
        if self.time_controls is not None:
            white_time_str = self.format_time(self.white_time)
            black_time_str = self.format_time(self.black_time)
            print(f"⏱️  White: {white_time_str} | Black: {black_time_str}")
        
        # Display board based on theme
        if self.theme == 'unicode':
            print(self.board.unicode())
        elif self.theme == 'borders':
            print(self.board.unicode(borders=True))
        else:  # ascii
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
    
    def set_theme(self, theme: str):
        """Set the board display theme."""
        if theme in self.THEMES:
            self.theme = theme
            print(f"✅ Board theme set to: {self.THEMES[theme]}")
        else:
            print(f"❌ Invalid theme. Available themes: {', '.join(self.THEMES.keys())}")
    
    @classmethod
    def list_themes(cls):
        """List all available board themes."""
        print("\n🎨 Available Board Themes:")
        for key, description in cls.THEMES.items():
            print(f"  {key}: {description}")
        
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
    
    def analyze_game(self, engine_path: str, depth: int = 15) -> List[Tuple[str, int, int]]:
        """
        Analyze the game with an engine and return evaluations for each move.
        Returns list of tuples: (move_san, evaluation_before, evaluation_after)
        Evaluation is in centipawns from White's perspective.
        """
        print("\n" + "=" * 50)
        print("🔍 ANALYZING GAME WITH ENGINE...")
        print("=" * 50)
        
        engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        
        try:
            analysis = []
            temp_board = chess.Board()
            
            for i, move in enumerate(self.board.move_stack):
                # Get evaluation before the move
                info_before = engine.analyse(temp_board, chess.engine.Limit(depth=depth))
                score_before = info_before.get("score")
                
                # Make the move
                san_move = temp_board.san(move)
                temp_board.push(move)
                
                # Get evaluation after the move
                info_after = engine.analyse(temp_board, chess.engine.Limit(depth=depth))
                score_after = info_after.get("score")
                
                # Convert scores to centipawns (from White's perspective)
                eval_before = self._score_to_cp(score_before, temp_board.turn)
                eval_after = self._score_to_cp(score_after, not temp_board.turn)
                
                analysis.append((san_move, eval_before, eval_after))
                
                print(f"Move {i+1}: {san_move:8} | Before: {eval_before:+6} cp | After: {eval_after:+6} cp")
            
            return analysis
            
        finally:
            engine.quit()
    
    def _score_to_cp(self, score, from_perspective: chess.Color) -> int:
        """
        Convert a chess.engine.Score to centipawns.
        Returns the score from White's perspective.
        """
        if score is None:
            return 0
            
        # Get score relative to the side to move
        cp = score.relative.score(mate_score=10000)
        
        if cp is None:
            cp = 0
        
        # If the perspective is Black, negate the score
        if from_perspective == chess.BLACK:
            cp = -cp
            
        return cp
    
    def display_game_analysis(self, analysis: List[Tuple[str, int, int]]):
        """Display analysis results in a human-readable format."""
        print("\n" + "=" * 50)
        print("📊 GAME ANALYSIS SUMMARY")
        print("=" * 50)
        
        mistakes = []
        blunders = []
        brilliant_moves = []
        
        for i, (move, eval_before, eval_after) in enumerate(analysis):
            move_num = i // 2 + 1
            is_white = (i % 2 == 0)
            player = "White" if is_white else "Black"
            
            # Calculate evaluation change (from the player's perspective)
            if is_white:
                eval_change = eval_after - eval_before
            else:
                eval_change = eval_before - eval_after
            
            # Classify the move
            if eval_change < -100:
                blunders.append((move_num, player, move, eval_change))
            elif eval_change < -50:
                mistakes.append((move_num, player, move, eval_change))
            elif eval_change > 100:
                brilliant_moves.append((move_num, player, move, eval_change))
        
        # Display brilliant moves
        if brilliant_moves:
            print("\n⭐ BRILLIANT MOVES:")
            for move_num, player, move, change in brilliant_moves:
                print(f"  Move {move_num} ({player}): {move} (+{change} cp)")
        
        # Display mistakes
        if mistakes:
            print("\n⚠️  MISTAKES:")
            for move_num, player, move, change in mistakes:
                print(f"  Move {move_num} ({player}): {move} ({change} cp)")
        
        # Display blunders
        if blunders:
            print("\n❌ BLUNDERS:")
            for move_num, player, move, change in blunders:
                print(f"  Move {move_num} ({player}): {move} ({change} cp)")
        
        if not mistakes and not blunders and not brilliant_moves:
            print("\n✨ Clean game! No significant mistakes or brilliant moves detected.")
        
        # Calculate average position evaluation
        if analysis:
            avg_eval = sum(eval_after for _, _, eval_after in analysis) / len(analysis)
            print(f"\n📈 Average position evaluation: {avg_eval:+.1f} cp")
    
    def enable_time_control(self, minutes: int, increment_seconds: int = 0):
        """
        Enable time controls for the game.
        
        Args:
            minutes: Starting time in minutes for each player
            increment_seconds: Increment added after each move
        """
        self.time_controls = {
            'base': minutes * 60,  # Convert to seconds
            'increment': increment_seconds
        }
        self.white_time = self.time_controls['base']
        self.black_time = self.time_controls['base']
        
    def update_time(self, color: chess.Color, time_used: float):
        """Update time for a player after a move."""
        if self.time_controls is None:
            return
            
        if color == chess.WHITE:
            self.white_time -= time_used
            self.white_time += self.time_controls['increment']
        else:
            self.black_time -= time_used
            self.black_time += self.time_controls['increment']
    
    def get_remaining_time(self, color: chess.Color) -> Optional[float]:
        """Get remaining time for a player in seconds."""
        if self.time_controls is None:
            return None
        return self.white_time if color == chess.WHITE else self.black_time
    
    def format_time(self, seconds: float) -> str:
        """Format time in MM:SS format."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def is_time_out(self, color: chess.Color) -> bool:
        """Check if a player has run out of time."""
        if self.time_controls is None:
            return False
        time_remaining = self.get_remaining_time(color)
        return time_remaining is not None and time_remaining <= 0


class PlayerVsPlayerGame(ChessGame):
    """Player vs Player chess game."""
    
    def __init__(self, theme: str = 'ascii'):
        super().__init__(theme=theme)
        
    def get_player_move(self, player_name: str) -> chess.Move:
        """Get a move from a human player."""
        start_time = time.time()
        
        while True:
            try:
                print(f"\n{player_name}'s turn ({'White' if self.board.turn == chess.WHITE else 'Black'})")
                
                # Check for time out
                if self.is_time_out(self.board.turn):
                    print(f"⏰ TIME OUT! {player_name} loses on time.")
                    return None
                
                print(f"Legal moves: {', '.join([move.uci() for move in list(self.board.legal_moves)[:10]])}...")
                move_str = input("Enter your move (UCI format, e.g., e2e4): ").strip()
                
                move = chess.Move.from_uci(move_str)
                if move in self.board.legal_moves:
                    # Update time
                    time_used = time.time() - start_time
                    self.update_time(self.board.turn, time_used)
                    return move
                else:
                    print("❌ Illegal move! Try again.")
            except Exception as e:
                print(f"❌ Invalid format! Use UCI notation (e.g., e2e4). Error: {e}")
                
    def play(self):
        """Play a full Player vs Player game."""
        print("=" * 50)
        print("🎮 PLAYER VS PLAYER MODE")
        if self.time_controls is not None:
            base_min = self.time_controls['base'] / 60
            inc = self.time_controls['increment']
            print(f"⏱️  Time Control: {base_min:.0f}+{inc}")
        print("=" * 50)
        
        time_forfeit = False
        
        while not self.is_game_over():
            self.display_board()
            
            player_name = "Player 1" if self.board.turn == chess.WHITE else "Player 2"
            move = self.get_player_move(player_name)
            
            if move is None:  # Time forfeit
                time_forfeit = True
                break
                
            self.make_move(move)
            
        # Game over
        self.display_board()
        self.display_move_history()
        print("\n" + "=" * 50)
        if time_forfeit:
            winner = "Player 2" if self.board.turn == chess.WHITE else "Player 1"
            print(f"🏁 GAME OVER - {winner} wins on time!")
        else:
            print(f"🏁 GAME OVER - Result: {self.get_result()}")
        print("=" * 50)
        
        self.save_to_pgn("pvp_games.pgn", "Player 1", "Player 2")


class PlayerVsComputerGame(ChessGame):
    """Player vs Computer chess game."""
    
    # AI thinking time strategy: use this fraction of remaining time per move
    AI_TIME_FRACTION = 20
    
    def __init__(self, stockfish_path: str, player_color: chess.Color = chess.WHITE, skill_level: int = 10, theme: str = 'ascii'):
        super().__init__(theme=theme)
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
        start_time = time.time()
        
        while True:
            try:
                print(f"\nYour turn ({'White' if self.board.turn == chess.WHITE else 'Black'})")
                
                # Check for time out
                if self.is_time_out(self.board.turn):
                    print("⏰ TIME OUT! You lose on time.")
                    return None
                
                print(f"Legal moves: {', '.join([move.uci() for move in list(self.board.legal_moves)[:10]])}...")
                move_str = input("Enter your move (UCI format, e.g., e2e4): ").strip()
                
                move = chess.Move.from_uci(move_str)
                if move in self.board.legal_moves:
                    # Update time
                    time_used = time.time() - start_time
                    self.update_time(self.board.turn, time_used)
                    return move
                else:
                    print("❌ Illegal move! Try again.")
            except Exception as e:
                print(f"❌ Invalid format! Use UCI notation (e.g., e2e4). Error: {e}")
                
    def get_computer_move(self) -> chess.Move:
        """Get a move from Stockfish."""
        print("\n🤖 Computer is thinking...")
        start_time = time.time()
        
        # Use time limit if time controls are enabled
        if self.time_controls is not None:
            time_limit = min(1.0, self.get_remaining_time(self.board.turn) / self.AI_TIME_FRACTION)
            result = self.engine.play(self.board, chess.engine.Limit(time=time_limit))
        else:
            result = self.engine.play(self.board, chess.engine.Limit(time=1.0))
        
        # Update time
        time_used = time.time() - start_time
        self.update_time(self.board.turn, time_used)
        
        return result.move
        
    def play(self):
        """Play a full Player vs Computer game."""
        print("=" * 50)
        print(f"🎮 PLAYER VS COMPUTER MODE (Skill Level {self.skill_level})")
        print(f"You are playing as {'White' if self.player_color == chess.WHITE else 'Black'}")
        if self.time_controls is not None:
            base_min = self.time_controls['base'] / 60
            inc = self.time_controls['increment']
            print(f"⏱️  Time Control: {base_min:.0f}+{inc}")
        print("=" * 50)
        
        self.start_engine()
        time_forfeit = False
        
        try:
            while not self.is_game_over():
                self.display_board()
                
                if self.board.turn == self.player_color:
                    move = self.get_player_move()
                    if move is None:  # Time forfeit
                        time_forfeit = True
                        break
                else:
                    move = self.get_computer_move()
                    
                san_move = self.make_move(move)
                print(f"Move played: {san_move} ({move.uci()})")
                
            # Game over
            self.display_board()
            self.display_move_history()
            print("\n" + "=" * 50)
            if time_forfeit:
                print(f"🏁 GAME OVER - You lose on time!")
            else:
                print(f"🏁 GAME OVER - Result: {self.get_result()}")
            print("=" * 50)
            
            player_name = "Player (White)" if self.player_color == chess.WHITE else "Player (Black)"
            computer_name = f"Stockfish Level {self.skill_level} (Black)" if self.player_color == chess.WHITE else f"Stockfish Level {self.skill_level} (White)"
            
            if self.player_color == chess.WHITE:
                self.save_to_pgn("pvc_games.pgn", player_name, computer_name)
            else:
                self.save_to_pgn("pvc_games.pgn", computer_name, player_name)
            
            # Offer post-game analysis
            if not time_forfeit:
                analyze = input("\n📊 Would you like to analyze this game? (y/n): ").strip().lower()
                if analyze == 'y':
                    analysis = self.analyze_game(self.stockfish_path, depth=15)
                    self.display_game_analysis(analysis)
                
        finally:
            self.stop_engine()


class AIvsAIGame(ChessGame):
    """
    AI vs AI chess game (Stockfish vs Gemini).
    
    Supports configurable or randomized AI color assignment for diverse training data.
    """
    
    def __init__(self, stockfish_path: str, google_api_key: str, stockfish_skill: int = 5, stockfish_color: Optional[chess.Color] = None, theme: str = 'ascii'):
        super().__init__(theme=theme)
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
