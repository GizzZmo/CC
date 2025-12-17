"""
Database module for Cyberchess.
Manages user accounts, ratings, and game history using SQLite.
"""

import datetime
import hashlib
import sqlite3
from typing import Dict, List, Optional, Tuple


class ChessDatabase:
    """Database manager for Cyberchess."""

    def __init__(self, db_path: str = "cyberchess.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self.initialize_database()

    def connect(self):
        """
        Connect to the database.

        Note: check_same_thread=False is used for Flask compatibility.
        For production, consider using connection pooling or ensuring
        proper synchronization with locks when sharing connections.
        """
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_database(self):
        """Create database tables if they don't exist."""
        conn = self.connect()
        cursor = conn.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE,
                rating INTEGER DEFAULT 1200,
                games_played INTEGER DEFAULT 0,
                games_won INTEGER DEFAULT 0,
                games_lost INTEGER DEFAULT 0,
                games_drawn INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """
        )

        # Games table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                white_player_id INTEGER,
                black_player_id INTEGER,
                result TEXT,
                pgn TEXT,
                white_rating_before INTEGER,
                black_rating_before INTEGER,
                white_rating_after INTEGER,
                black_rating_after INTEGER,
                time_control TEXT,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (white_player_id) REFERENCES users(user_id),
                FOREIGN KEY (black_player_id) REFERENCES users(user_id)
            )
        """
        )

        # Active games table (for online multiplayer)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS active_games (
                session_id TEXT PRIMARY KEY,
                white_player_id INTEGER,
                black_player_id INTEGER,
                current_fen TEXT,
                move_history TEXT,
                time_control TEXT,
                white_time_remaining REAL,
                black_time_remaining REAL,
                last_move_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (white_player_id) REFERENCES users(user_id),
                FOREIGN KEY (black_player_id) REFERENCES users(user_id)
            )
        """
        )

        # Matchmaking queue table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS matchmaking_queue (
                queue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                rating INTEGER,
                time_control TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )

        conn.commit()

    def hash_password(self, password: str) -> str:
        """
        Hash a password using SHA-256.

        NOTE: For production use, consider upgrading to bcrypt, scrypt, or argon2
        for better security against rainbow table attacks:

        Example with bcrypt:
            import bcrypt
            return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        Current implementation uses SHA-256 for simplicity in development.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(
        self, username: str, password: str, email: Optional[str] = None
    ) -> Optional[int]:
        """Create a new user account. Returns user_id if successful."""
        conn = self.connect()
        cursor = conn.cursor()

        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email),
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Username or email already exists

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate a user. Returns user data if successful."""
        conn = self.connect()
        cursor = conn.cursor()

        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash),
        )

        row = cursor.fetchone()
        if row:
            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?",
                (row["user_id"],),
            )
            conn.commit()
            return dict(row)
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user data by ID."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user data by username."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_user_rating(self, user_id: int, new_rating: int):
        """Update a user's rating."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET rating = ? WHERE user_id = ?", (new_rating, user_id)
        )
        conn.commit()

    def record_game(
        self,
        white_player_id: int,
        black_player_id: int,
        result: str,
        pgn: str,
        white_rating_before: int,
        black_rating_before: int,
        white_rating_after: int,
        black_rating_after: int,
        time_control: Optional[str] = None,
    ) -> int:
        """Record a completed game. Returns game_id."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO games (
                white_player_id, black_player_id, result, pgn,
                white_rating_before, black_rating_before,
                white_rating_after, black_rating_after, time_control
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                white_player_id,
                black_player_id,
                result,
                pgn,
                white_rating_before,
                black_rating_before,
                white_rating_after,
                black_rating_after,
                time_control,
            ),
        )

        game_id = cursor.lastrowid

        # Update user statistics
        cursor.execute(
            "UPDATE users SET games_played = games_played + 1 WHERE user_id IN (?, ?)",
            (white_player_id, black_player_id),
        )

        if result == "1-0":
            cursor.execute(
                "UPDATE users SET games_won = games_won + 1 WHERE user_id = ?",
                (white_player_id,),
            )
            cursor.execute(
                "UPDATE users SET games_lost = games_lost + 1 WHERE user_id = ?",
                (black_player_id,),
            )
        elif result == "0-1":
            cursor.execute(
                "UPDATE users SET games_won = games_won + 1 WHERE user_id = ?",
                (black_player_id,),
            )
            cursor.execute(
                "UPDATE users SET games_lost = games_lost + 1 WHERE user_id = ?",
                (white_player_id,),
            )
        elif result == "1/2-1/2":
            cursor.execute(
                "UPDATE users SET games_drawn = games_drawn + 1 WHERE user_id IN (?, ?)",
                (white_player_id, black_player_id),
            )

        conn.commit()
        return game_id

    def get_user_games(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get recent games for a user."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT g.*, 
                   w.username as white_username,
                   b.username as black_username
            FROM games g
            JOIN users w ON g.white_player_id = w.user_id
            JOIN users b ON g.black_player_id = b.user_id
            WHERE g.white_player_id = ? OR g.black_player_id = ?
            ORDER BY g.played_at DESC
            LIMIT ?
        """,
            (user_id, user_id, limit),
        )

        return [dict(row) for row in cursor.fetchall()]

    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top players by rating."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT user_id, username, rating, games_played, games_won, games_lost, games_drawn
            FROM users
            WHERE games_played > 0
            ORDER BY rating DESC
            LIMIT ?
        """,
            (limit,),
        )

        return [dict(row) for row in cursor.fetchall()]

    def calculate_elo_rating(
        self, player_rating: int, opponent_rating: int, score: float, k_factor: int = 32
    ) -> int:
        """
        Calculate new Elo rating after a game.

        Args:
            player_rating: Current rating of the player
            opponent_rating: Current rating of the opponent
            score: 1.0 for win, 0.5 for draw, 0.0 for loss
            k_factor: K-factor for Elo calculation (default 32)

        Returns:
            New rating for the player
        """
        expected_score = 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))
        new_rating = player_rating + k_factor * (score - expected_score)
        return int(round(new_rating))

    def join_matchmaking_queue(
        self, user_id: int, rating: int, time_control: str = "blitz"
    ) -> bool:
        """Add a user to the matchmaking queue."""
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO matchmaking_queue (user_id, rating, time_control) VALUES (?, ?, ?)",
                (user_id, rating, time_control),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # User already in queue

    def leave_matchmaking_queue(self, user_id: int):
        """Remove a user from the matchmaking queue."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM matchmaking_queue WHERE user_id = ?", (user_id,))
        conn.commit()

    def find_match(self, user_id: int, rating_range: int = 200) -> Optional[Dict]:
        """Find a match for a user from the queue."""
        conn = self.connect()
        cursor = conn.cursor()

        # Get the user's queue entry
        cursor.execute("SELECT * FROM matchmaking_queue WHERE user_id = ?", (user_id,))
        user_entry = cursor.fetchone()

        if not user_entry:
            return None

        user_rating = user_entry["rating"]
        time_control = user_entry["time_control"]

        # Find a suitable opponent
        cursor.execute(
            """
            SELECT * FROM matchmaking_queue 
            WHERE user_id != ? 
            AND time_control = ?
            AND ABS(rating - ?) <= ?
            ORDER BY joined_at ASC
            LIMIT 1
        """,
            (user_id, time_control, user_rating, rating_range),
        )

        opponent = cursor.fetchone()
        if opponent:
            return dict(opponent)
        return None

    def create_active_game(
        self, session_id: str, white_id: int, black_id: int, time_control: str
    ):
        """Create an active game session."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO active_games (
                session_id, white_player_id, black_player_id,
                current_fen, move_history, time_control,
                white_time_remaining, black_time_remaining, last_move_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
            (
                session_id,
                white_id,
                black_id,
                "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "",
                time_control,
                300.0,  # 5 minutes default
                300.0,
            ),
        )
        conn.commit()

    def get_active_game(self, session_id: str) -> Optional[Dict]:
        """Get an active game by session ID."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM active_games WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_active_game(
        self,
        session_id: str,
        fen: str,
        move_history: str,
        white_time: float,
        black_time: float,
    ):
        """Update an active game's state."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE active_games 
            SET current_fen = ?, move_history = ?, 
                white_time_remaining = ?, black_time_remaining = ?,
                last_move_time = CURRENT_TIMESTAMP
            WHERE session_id = ?
        """,
            (fen, move_history, white_time, black_time, session_id),
        )
        conn.commit()

    def delete_active_game(self, session_id: str):
        """Delete an active game session."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM active_games WHERE session_id = ?", (session_id,))
        conn.commit()
