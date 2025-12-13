import chess
import chess.engine
import chess.pgn
import google.generativeai as genai
import time
import datetime

# --- CONFIGURATION ---
# REPLACE THIS with the path to your downloaded stockfish file
# Windows example: "C:/Users/Jon/Downloads/stockfish/stockfish-windows-x86-64.exe"
# Mac example: "/opt/homebrew/bin/stockfish"
STOCKFISH_PATH = "YOUR_STOCKFISH_PATH_HERE" 

# REPLACE THIS with your Google Gemini API Key
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Setup Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Using Flash for speed

def get_gemini_move(board, retries=3):
    """
    Sends the board state to Gemini and asks for a move.
    Includes a retry loop for illegal moves.
    """
    legal_moves = [move.uci() for move in board.legal_moves]
    
    # We provide the FEN (Board State) and the list of legal moves to help Gemini
    # ground its reasoning and avoid hallucinations.
    prompt = f"""
    You are playing a game of Chess against Stockfish. You are playing Black.
    
    Current Board Position (FEN): {board.fen()}
    
    Here is the list of legally possible moves you can make:
    {', '.join(legal_moves)}
    
    Your goal is to survive and learn. Analyze the board.
    Pick the best move from the legal list above.
    
    IMPORTANT: Reply ONLY with the move in UCI format (e.g., e7e5). Do not write any other text.
    """

    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            move_str = response.text.strip().replace("\n", "").replace(" ", "")
            
            # clean up common formatting issues if Gemini adds markdown
            move_str = move_str.replace("`", "") 

            move = chess.Move.from_uci(move_str)

            if move in board.legal_moves:
                return move
            else:
                print(f" > Gemini tried illegal move: {move_str}. Retrying...")
                # Add feedback to the next prompt (In-Context Learning)
                prompt += f"\n\nERROR: {move_str} is not a legal move. Please choose strictly from the provided list."
        
        except Exception as e:
            print(f" > Error parsing Gemini response: {e}")
            prompt += f"\n\nERROR: Invalid format. Please reply ONLY with the move string (e.g., e7e5)."

    # If Gemini fails 3 times, we make a random move to keep the game going (fallback)
    print(" > Gemini failed to produce a legal move. Making random move.")
    import random
    return random.choice(list(board.legal_moves))

def play_game():
    # Initialize Board and Stockfish
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    
    # Set Stockfish skill level (Lower it initially so Gemini has a chance)
    # Skill level 0 is weak, 20 is Grandmaster. Let's start at 5.
    engine.configure({"Skill Level": 5})

    print("--- CYBERCHESS: Stockfish (White) vs Gemini (Black) ---")
    
    game_moves = []
    
    while not board.is_game_over():
        print(f"\nMove {board.fullmove_number}")
        print(board)
        
        if board.turn == chess.WHITE:
            # --- STOCKFISH TURN ---
            print("Stockfish is thinking...")
            # Limit Stockfish to 0.1 seconds so it plays fast
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)
            print(f"Stockfish played: {result.move.uci()}")
            game_moves.append(result.move)
            
        else:
            # --- GEMINI TURN ---
            print("Gemini is thinking...")
            move = get_gemini_move(board)
            board.push(move)
            print(f"Gemini played: {move.uci()}")
            game_moves.append(move)

    # --- GAME OVER ---
    print("\n--- GAME OVER ---")
    print(f"Result: {board.result()}")
    
    engine.quit()
    return board

def save_game_data(board):
    """
    Saves the game to a PGN file. 
    This is the dataset we will use later to FINE TUNE Gemini.
    """
    pgn_game = chess.pgn.Game.from_board(board)
    pgn_game.headers["Event"] = "Cyberchess Dojo"
    pgn_game.headers["White"] = "Stockfish Level 5"
    pgn_game.headers["Black"] = "Gemini 1.5 Flash"
    pgn_game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")

    with open("training_data.pgn", "a") as f:
        f.write(str(pgn_game) + "\n\n")
    print("Game saved to 'training_data.pgn'")

if __name__ == "__main__":
    # In a real app, you would loop this: while True: play_game()
    finished_board = play_game()
    save_game_data(finished_board)
