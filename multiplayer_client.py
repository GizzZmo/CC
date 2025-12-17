"""
Multiplayer client module for Cyberchess.
Handles communication with the server for online play.
"""

import json
from typing import Callable, Optional

import chess
import requests
import socketio


class MultiplayerClient:
    """Client for online multiplayer chess."""

    def __init__(self, server_url: str = "http://localhost:5000"):
        """Initialize the multiplayer client."""
        self.server_url = server_url
        self.api_url = f"{server_url}/api"
        self.sio = socketio.Client()

        self.user_id = None
        self.username = None
        self.session_token = None
        self.game_session_id = None
        self.player_color = None

        # Callbacks
        self.on_move_callback: Optional[Callable] = None
        self.on_game_over_callback: Optional[Callable] = None
        self.on_error_callback: Optional[Callable] = None

        # Setup event handlers
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup WebSocket event handlers."""

        @self.sio.on("connected")
        def on_connected(data):
            print(f"✅ {data['message']}")

        @self.sio.on("game_joined")
        def on_game_joined(data):
            self.game_session_id = data["session_id"]
            self.player_color = data["color"]
            print(f"✅ Joined game as {self.player_color}")

        @self.sio.on("move_made")
        def on_move_made(data):
            if self.on_move_callback:
                self.on_move_callback(data)

        @self.sio.on("player_resigned")
        def on_player_resigned(data):
            print(f"⚠️ Player resigned. Result: {data['result']}")
            if self.on_game_over_callback:
                self.on_game_over_callback(data)

        @self.sio.on("error")
        def on_error(data):
            print(f"❌ Error: {data['message']}")
            if self.on_error_callback:
                self.on_error_callback(data)

    def connect(self) -> bool:
        """Connect to the server."""
        try:
            self.sio.connect(self.server_url)
            return True
        except Exception as e:
            print(f"❌ Failed to connect to server: {e}")
            return False

    def disconnect(self):
        """Disconnect from the server."""
        if self.sio.connected:
            self.sio.disconnect()

    def register(
        self, username: str, password: str, email: Optional[str] = None
    ) -> bool:
        """Register a new user account."""
        try:
            response = requests.post(
                f"{self.api_url}/register",
                json={"username": username, "password": password, "email": email},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Registration successful! User ID: {data['user_id']}")
                return True
            else:
                error = response.json().get("error", "Unknown error")
                print(f"❌ Registration failed: {error}")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False

    def login(self, username: str, password: str) -> bool:
        """Login to the server."""
        try:
            response = requests.post(
                f"{self.api_url}/login",
                json={"username": username, "password": password},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                self.user_id = data["user_id"]
                self.username = data["username"]
                self.session_token = data["session_token"]
                print(
                    f"✅ Login successful! Welcome {self.username} (Rating: {data['rating']})"
                )
                return True
            else:
                error = response.json().get("error", "Unknown error")
                print(f"❌ Login failed: {error}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def get_user_profile(self, user_id: Optional[int] = None) -> Optional[dict]:
        """Get user profile information."""
        if user_id is None:
            user_id = self.user_id

        if user_id is None:
            print("❌ Not logged in")
            return None

        try:
            response = requests.get(f"{self.api_url}/user/{user_id}", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get user profile")
                return None
        except Exception as e:
            print(f"❌ Error getting profile: {e}")
            return None

    def get_leaderboard(self, limit: int = 10) -> list:
        """Get the leaderboard."""
        try:
            response = requests.get(
                f"{self.api_url}/leaderboard?limit={limit}", timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f"❌ Error getting leaderboard: {e}")
            return []

    def get_user_games(self, user_id: Optional[int] = None, limit: int = 10) -> list:
        """Get user's game history."""
        if user_id is None:
            user_id = self.user_id

        if user_id is None:
            print("❌ Not logged in")
            return []

        try:
            response = requests.get(
                f"{self.api_url}/user/{user_id}/games?limit={limit}", timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f"❌ Error getting games: {e}")
            return []

    def join_matchmaking(self, time_control: str = "blitz") -> Optional[dict]:
        """Join matchmaking queue to find an opponent."""
        if not self.user_id:
            print("❌ Not logged in")
            return None

        try:
            response = requests.post(
                f"{self.api_url}/matchmaking/join",
                json={"user_id": self.user_id, "time_control": time_control},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("matched"):
                    print(f"✅ Match found! Session: {data['session_id']}")
                    self.game_session_id = data["session_id"]
                    self.player_color = data["your_color"]
                    return data
                else:
                    print("⏳ Waiting for opponent...")
                    return data
            else:
                error = response.json().get("error", "Unknown error")
                print(f"❌ Matchmaking failed: {error}")
                return None
        except Exception as e:
            print(f"❌ Matchmaking error: {e}")
            return None

    def leave_matchmaking(self) -> bool:
        """Leave matchmaking queue."""
        if not self.user_id:
            return False

        try:
            response = requests.post(
                f"{self.api_url}/matchmaking/leave",
                json={"user_id": self.user_id},
                timeout=10,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error leaving queue: {e}")
            return False

    def join_game(self, session_id: Optional[str] = None):
        """Join a game session."""
        if session_id:
            self.game_session_id = session_id

        if not self.game_session_id or not self.user_id:
            print("❌ No game session or not logged in")
            return

        self.sio.emit(
            "join_game",
            {
                "session_id": self.game_session_id,
                "user_id": self.user_id,
            },
        )

    def leave_game(self):
        """Leave the current game session."""
        if self.game_session_id and self.user_id:
            self.sio.emit(
                "leave_game",
                {
                    "session_id": self.game_session_id,
                    "user_id": self.user_id,
                },
            )
            self.game_session_id = None
            self.player_color = None

    def make_move(self, move_uci: str):
        """Send a move to the server."""
        if not self.game_session_id or not self.user_id:
            print("❌ No active game session")
            return

        self.sio.emit(
            "make_move",
            {
                "session_id": self.game_session_id,
                "user_id": self.user_id,
                "move": move_uci,
            },
        )

    def resign(self):
        """Resign from the current game."""
        if not self.game_session_id or not self.user_id:
            print("❌ No active game session")
            return

        self.sio.emit(
            "resign",
            {
                "session_id": self.game_session_id,
                "user_id": self.user_id,
            },
        )

    def get_game_state(self, session_id: Optional[str] = None) -> Optional[dict]:
        """Get the current state of a game."""
        if session_id is None:
            session_id = self.game_session_id

        if not session_id:
            print("❌ No game session")
            return None

        try:
            response = requests.get(f"{self.api_url}/game/{session_id}", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"❌ Error getting game state: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Create client
    client = MultiplayerClient()

    # Connect to server
    if not client.connect():
        print("Failed to connect to server")
        exit(1)

    # Example: Register or login
    username = input("Username: ")
    password = input("Password: ")

    choice = input("(L)ogin or (R)egister? ").lower()
    if choice == "r":
        client.register(username, password)

    if client.login(username, password):
        # Get profile
        profile = client.get_user_profile()
        if profile:
            print(f"\nProfile: {profile['username']}")
            print(f"Rating: {profile['rating']}")
            print(f"Games Played: {profile['games_played']}")

        # Show leaderboard
        print("\n📊 Leaderboard:")
        for i, player in enumerate(client.get_leaderboard(), 1):
            print(f"{i}. {player['username']}: {player['rating']}")

        # Join matchmaking
        if input("\nJoin matchmaking? (y/n): ").lower() == "y":
            match = client.join_matchmaking("blitz")
            if match and match.get("matched"):
                # Join the game
                client.join_game()
                print(f"Playing as {client.player_color}")

                # Game loop would go here
                input("Press Enter to leave game...")
                client.leave_game()

    client.disconnect()
