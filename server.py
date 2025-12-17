"""
Cyberchess Server
Flask-based server for online multiplayer chess.
Provides REST API and WebSocket support for real-time gameplay.
"""

import json
import os
import secrets
import time
from datetime import datetime
from typing import Dict, Optional

import chess
import chess.pgn
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room

from database import ChessDatabase

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(32))
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize database
db = ChessDatabase()

# Active game sessions (in-memory for real-time state)
active_sessions: Dict[str, Dict] = {}


# ==================== REST API Routes ====================


@app.route("/")
def index():
    """Serve the mobile web interface."""
    return send_from_directory("static", "mobile_gui.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user_id = db.create_user(username, password, email)
    if user_id:
        return jsonify(
            {"success": True, "user_id": user_id, "message": "User created successfully"}
        )
    else:
        return jsonify({"error": "Username or email already exists"}), 409


@app.route("/api/login", methods=["POST"])
def login():
    """Authenticate a user."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = db.authenticate_user(username, password)
    if user:
        # Create a session token
        session_token = secrets.token_urlsafe(32)
        return jsonify(
            {
                "success": True,
                "user_id": user["user_id"],
                "username": user["username"],
                "rating": user["rating"],
                "session_token": session_token,
            }
        )
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get user profile."""
    user = db.get_user_by_id(user_id)
    if user:
        # Don't return password hash
        user.pop("password_hash", None)
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """Get the leaderboard."""
    limit = request.args.get("limit", default=10, type=int)
    leaderboard = db.get_leaderboard(limit)
    return jsonify(leaderboard)


@app.route("/api/user/<int:user_id>/games", methods=["GET"])
def get_user_games(user_id):
    """Get a user's game history."""
    limit = request.args.get("limit", default=10, type=int)
    games = db.get_user_games(user_id, limit)
    return jsonify(games)


@app.route("/api/matchmaking/join", methods=["POST"])
def join_matchmaking():
    """Join the matchmaking queue."""
    data = request.json
    user_id = data.get("user_id")
    time_control = data.get("time_control", "blitz")

    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    user = db.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Add to matchmaking queue
    if db.join_matchmaking_queue(user_id, user["rating"], time_control):
        # Try to find a match
        opponent = db.find_match(user_id)
        if opponent:
            # Create a game session
            session_id = secrets.token_urlsafe(16)
            
            # Randomly assign colors
            import random
            if random.random() < 0.5:
                white_id, black_id = user_id, opponent["user_id"]
            else:
                white_id, black_id = opponent["user_id"], user_id

            # Remove both from queue
            db.leave_matchmaking_queue(user_id)
            db.leave_matchmaking_queue(opponent["user_id"])

            # Create active game
            db.create_active_game(session_id, white_id, black_id, time_control)

            return jsonify(
                {
                    "success": True,
                    "matched": True,
                    "session_id": session_id,
                    "your_color": "white" if user_id == white_id else "black",
                    "opponent_id": opponent["user_id"],
                }
            )
        else:
            return jsonify({"success": True, "matched": False, "message": "Waiting for opponent"})
    else:
        return jsonify({"error": "Already in queue"}), 409


@app.route("/api/matchmaking/leave", methods=["POST"])
def leave_matchmaking():
    """Leave the matchmaking queue."""
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    db.leave_matchmaking_queue(user_id)
    return jsonify({"success": True})


@app.route("/api/game/<session_id>", methods=["GET"])
def get_game_state(session_id):
    """Get current game state."""
    game = db.get_active_game(session_id)
    if game:
        return jsonify(game)
    else:
        return jsonify({"error": "Game not found"}), 404


# ==================== WebSocket Events ====================


@socketio.on("connect")
def handle_connect():
    """Handle client connection."""
    print(f"Client connected: {request.sid}")
    emit("connected", {"message": "Connected to Cyberchess server"})


@socketio.on("disconnect")
def handle_disconnect():
    """Handle client disconnection."""
    print(f"Client disconnected: {request.sid}")


@socketio.on("join_game")
def handle_join_game(data):
    """Handle player joining a game session."""
    session_id = data.get("session_id")
    user_id = data.get("user_id")

    if not session_id or not user_id:
        emit("error", {"message": "Session ID and User ID required"})
        return

    # Join the room for this game
    join_room(session_id)

    # Get game state from database
    game = db.get_active_game(session_id)
    if game:
        # Determine player's color
        if user_id == game["white_player_id"]:
            color = "white"
        elif user_id == game["black_player_id"]:
            color = "black"
        else:
            color = "spectator"

        emit(
            "game_joined",
            {
                "session_id": session_id,
                "color": color,
                "fen": game["current_fen"],
                "move_history": game["move_history"],
                "white_time": game["white_time_remaining"],
                "black_time": game["black_time_remaining"],
            },
        )

        # Notify other players
        emit(
            "player_joined",
            {"user_id": user_id, "color": color},
            room=session_id,
            include_self=False,
        )
    else:
        emit("error", {"message": "Game not found"})


@socketio.on("leave_game")
def handle_leave_game(data):
    """Handle player leaving a game session."""
    session_id = data.get("session_id")
    if session_id:
        leave_room(session_id)
        emit("player_left", {"user_id": data.get("user_id")}, room=session_id)


@socketio.on("make_move")
def handle_make_move(data):
    """Handle a chess move."""
    session_id = data.get("session_id")
    user_id = data.get("user_id")
    move_uci = data.get("move")

    if not session_id or not user_id or not move_uci:
        emit("error", {"message": "Session ID, User ID, and move required"})
        return

    # Get game state
    game = db.get_active_game(session_id)
    if not game:
        emit("error", {"message": "Game not found"})
        return

    # Verify it's the player's turn
    board = chess.Board(game["current_fen"])
    if (board.turn == chess.WHITE and user_id != game["white_player_id"]) or \
       (board.turn == chess.BLACK and user_id != game["black_player_id"]):
        emit("error", {"message": "Not your turn"})
        return

    # Validate and make the move
    try:
        move = chess.Move.from_uci(move_uci)
        if move not in board.legal_moves:
            emit("error", {"message": "Illegal move"})
            return

        # Make the move
        san_move = board.san(move)
        board.push(move)

        # Update move history
        move_history = game["move_history"]
        if move_history:
            move_history += " " + move_uci
        else:
            move_history = move_uci

        # Update database
        db.update_active_game(
            session_id,
            board.fen(),
            move_history,
            game["white_time_remaining"],
            game["black_time_remaining"],
        )

        # Broadcast the move to all players in the room
        emit(
            "move_made",
            {
                "move": move_uci,
                "san": san_move,
                "fen": board.fen(),
                "game_over": board.is_game_over(),
                "result": board.result() if board.is_game_over() else None,
            },
            room=session_id,
        )

        # If game is over, save to database and update ratings
        if board.is_game_over():
            result = board.result()
            
            # Create PGN
            game_pgn = chess.pgn.Game()
            game_pgn.headers["Event"] = "Cyberchess Online Game"
            game_pgn.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
            game_pgn.headers["Result"] = result
            
            # Rebuild game from moves
            node = game_pgn
            temp_board = chess.Board()
            for uci_move in move_history.split():
                move = chess.Move.from_uci(uci_move)
                node = node.add_variation(move)
                temp_board.push(move)
            
            pgn_string = str(game_pgn)

            # Get player ratings
            white_player = db.get_user_by_id(game["white_player_id"])
            black_player = db.get_user_by_id(game["black_player_id"])

            white_rating_before = white_player["rating"]
            black_rating_before = black_player["rating"]

            # Calculate new ratings
            if result == "1-0":
                white_score, black_score = 1.0, 0.0
            elif result == "0-1":
                white_score, black_score = 0.0, 1.0
            else:
                white_score, black_score = 0.5, 0.5

            white_rating_after = db.calculate_elo_rating(
                white_rating_before, black_rating_before, white_score
            )
            black_rating_after = db.calculate_elo_rating(
                black_rating_before, white_rating_before, black_score
            )

            # Update ratings in database
            db.update_user_rating(game["white_player_id"], white_rating_after)
            db.update_user_rating(game["black_player_id"], black_rating_after)

            # Record the game
            db.record_game(
                game["white_player_id"],
                game["black_player_id"],
                result,
                pgn_string,
                white_rating_before,
                black_rating_before,
                white_rating_after,
                black_rating_after,
                game["time_control"],
            )

            # Delete active game
            db.delete_active_game(session_id)

            # Notify players of rating changes
            emit(
                "ratings_updated",
                {
                    "white_rating_change": white_rating_after - white_rating_before,
                    "black_rating_change": black_rating_after - black_rating_before,
                },
                room=session_id,
            )

    except Exception as e:
        emit("error", {"message": str(e)})


@socketio.on("resign")
def handle_resign(data):
    """Handle player resignation."""
    session_id = data.get("session_id")
    user_id = data.get("user_id")

    if not session_id or not user_id:
        emit("error", {"message": "Session ID and User ID required"})
        return

    game = db.get_active_game(session_id)
    if not game:
        emit("error", {"message": "Game not found"})
        return

    # Determine result based on who resigned
    if user_id == game["white_player_id"]:
        result = "0-1"
    else:
        result = "1-0"

    # Broadcast resignation
    emit("player_resigned", {"user_id": user_id, "result": result}, room=session_id)

    # Update ratings and save game (similar to game over)
    # ... (similar logic to game over in make_move)

    db.delete_active_game(session_id)


def main():
    """Run the server."""
    print("=" * 60)
    print("🎮 CYBERCHESS SERVER")
    print("=" * 60)
    print(f"Server starting on http://localhost:5000")
    print(f"Mobile interface: http://localhost:5000")
    print(f"API endpoint: http://localhost:5000/api")
    print("=" * 60)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
