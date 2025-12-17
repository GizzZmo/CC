# Cyberchess Online Multiplayer Guide

## Overview

Cyberchess now supports online multiplayer chess with the following features:

- **User Accounts**: Register and login to track your progress
- **Rating System**: Elo-based rating system to measure your skill
- **Matchmaking**: Automatic pairing with opponents of similar skill
- **Game History**: Track all your online games
- **Leaderboard**: See how you rank against other players
- **Mobile Support**: Play on any device with a web browser

## Getting Started

### 1. Install Dependencies

First, install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Flask-SocketIO (WebSocket support)
- python-socketio (client library)
- requests (HTTP client)

### 2. Start the Server

You can start the server in three ways:

**Option A: Using the Launcher**
```bash
python launcher.py
# Choose option 3 (ONLINE SERVER) or 4 (MOBILE WEB)
```

**Option B: Direct Server Launch**
```bash
python server.py
```

**Option C: Custom Configuration**
```bash
# Set environment variables (optional)
export SECRET_KEY="your-secret-key-here"

# Run the server
python server.py
```

The server will start on `http://localhost:5000` by default.

### 3. Access the Interfaces

Once the server is running, you can access:

- **Mobile Web Interface**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/health

## Using Online Multiplayer

### CLI Interface

1. Launch the CLI:
   ```bash
   python play.py
   ```

2. Select option 4 (Online Multiplayer)

3. Choose to Login or Register:
   - **Login**: Enter your existing username and password
   - **Register**: Create a new account with username and password

4. Available options:
   - **Find Match**: Join matchmaking queue for a blitz game
   - **View Leaderboard**: See top players and rankings
   - **View Game History**: Review your past games

### Mobile Web Interface

1. Open your browser to http://localhost:5000

2. Click "Login" button:
   - Enter username and password
   - Or click "Register" to create a new account

3. Once logged in:
   - Click "Find Match" to search for an opponent
   - View "Leaderboard" to see rankings
   - Play local games without an account

4. During a game:
   - Tap a piece to select it
   - Tap a destination square to move
   - Use "Resign" button to forfeit the game

### Multiplayer Client (Python API)

You can also use the multiplayer client programmatically:

```python
from multiplayer_client import MultiplayerClient

# Create client
client = MultiplayerClient("http://localhost:5000")

# Connect to server
client.connect()

# Register new user
client.register("username", "password")

# Login
if client.login("username", "password"):
    # Get profile
    profile = client.get_user_profile()
    print(f"Rating: {profile['rating']}")
    
    # View leaderboard
    leaderboard = client.get_leaderboard()
    
    # Find a match
    match = client.join_matchmaking("blitz")
    if match and match.get("matched"):
        # Join the game
        client.join_game()
        
        # Make moves
        client.make_move("e2e4")
        
        # Leave game when done
        client.leave_game()

# Disconnect
client.disconnect()
```

## Rating System

Cyberchess uses the Elo rating system to rank players:

- **Starting Rating**: 1200 (default for new accounts)
- **Rating Range**: Typically 800-2400+ for players
- **K-Factor**: 32 (determines rating change magnitude)

### How Ratings Work

When you complete a game:
1. Your performance is compared to your opponent's rating
2. Winning against higher-rated players gains more points
3. Losing against lower-rated players loses more points
4. Draws result in smaller rating changes

Example:
- You (1200) beat opponent (1400): +28 rating
- You (1200) lose to opponent (1400): -4 rating
- You (1200) draw with opponent (1200): ±0 rating

## Database Structure

The system uses SQLite database (`cyberchess.db`) with the following tables:

### Users Table
- `user_id`: Unique identifier
- `username`: Player username (unique)
- `password_hash`: Hashed password (SHA-256)
- `email`: Optional email address
- `rating`: Current Elo rating
- `games_played`: Total games count
- `games_won`: Wins count
- `games_lost`: Losses count
- `games_drawn`: Draws count
- `created_at`: Account creation timestamp
- `last_login`: Last login timestamp

### Games Table
- `game_id`: Unique game identifier
- `white_player_id`: White player's user ID
- `black_player_id`: Black player's user ID
- `result`: Game result (1-0, 0-1, 1/2-1/2)
- `pgn`: Full game notation
- `white_rating_before/after`: Rating changes
- `black_rating_before/after`: Rating changes
- `time_control`: Time control used
- `played_at`: Game completion timestamp

### Active Games Table
- `session_id`: Unique session identifier
- `white_player_id`: White player
- `black_player_id`: Black player
- `current_fen`: Current board position
- `move_history`: List of moves (UCI format)
- `time_control`: Time control
- `white_time_remaining`: White's time left
- `black_time_remaining`: Black's time left
- `last_move_time`: Last move timestamp

### Matchmaking Queue Table
- `queue_id`: Queue entry ID
- `user_id`: Waiting player
- `rating`: Player's rating
- `time_control`: Preferred time control
- `joined_at`: Queue join timestamp

## API Endpoints

### Authentication

**POST /api/register**
```json
{
  "username": "player1",
  "password": "securepassword",
  "email": "optional@email.com"
}
```

**POST /api/login**
```json
{
  "username": "player1",
  "password": "securepassword"
}
```

### User Profile

**GET /api/user/:user_id**

Returns user profile without password hash.

**GET /api/user/:user_id/games?limit=10**

Returns user's game history.

### Leaderboard

**GET /api/leaderboard?limit=10**

Returns top players by rating.

### Matchmaking

**POST /api/matchmaking/join**
```json
{
  "user_id": 1,
  "time_control": "blitz"
}
```

**POST /api/matchmaking/leave**
```json
{
  "user_id": 1
}
```

### Game State

**GET /api/game/:session_id**

Returns current game state.

## WebSocket Events

### Client → Server

**join_game**
```json
{
  "session_id": "abc123",
  "user_id": 1
}
```

**make_move**
```json
{
  "session_id": "abc123",
  "user_id": 1,
  "move": "e2e4"
}
```

**resign**
```json
{
  "session_id": "abc123",
  "user_id": 1
}
```

### Server → Client

**move_made**
```json
{
  "move": "e2e4",
  "san": "e4",
  "fen": "...",
  "game_over": false,
  "result": null
}
```

**game_joined**
```json
{
  "session_id": "abc123",
  "color": "white",
  "fen": "...",
  "move_history": "e2e4 e7e5",
  "white_time": 300.0,
  "black_time": 300.0
}
```

**error**
```json
{
  "message": "Error description"
}
```

## Security Considerations

1. **Password Hashing**: Passwords are hashed using SHA-256 (consider using bcrypt for production)
2. **Session Tokens**: Generated using `secrets.token_urlsafe()`
3. **SQL Injection**: Protected by parameterized queries
4. **CORS**: Enabled for development (configure for production)

**Important**: This implementation is suitable for development and small-scale deployment. For production use, consider:
- Using bcrypt/argon2 for password hashing
- Implementing HTTPS/TLS encryption
- Adding rate limiting
- Using a production-grade database (PostgreSQL)
- Implementing proper session management
- Adding input validation and sanitization

## Troubleshooting

### Server Won't Start

**Issue**: ImportError or ModuleNotFoundError

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Can't Connect to Server

**Issue**: Connection refused

**Solution**: Make sure server is running on http://localhost:5000

### Matchmaking Not Working

**Issue**: No opponent found

**Solution**: 
- Need at least 2 players in queue
- Try using multiple browser tabs/windows
- Check rating difference (must be within 200 points)

### Database Errors

**Issue**: Database locked or permission errors

**Solution**: 
- Close other connections to database
- Check file permissions on `cyberchess.db`
- Delete database file to reset (will lose all data)

## Advanced Configuration

### Custom Server Port

Edit `server.py`:
```python
socketio.run(app, host="0.0.0.0", port=8080, debug=True)
```

### Custom Database Location

Edit `database.py`:
```python
db = ChessDatabase("path/to/custom/database.db")
```

### Custom Rating K-Factor

Edit `database.py` in `calculate_elo_rating()`:
```python
def calculate_elo_rating(self, player_rating, opponent_rating, score, k_factor=32):
    # Change k_factor default value
```

## Future Enhancements

Potential improvements for the online system:

- [ ] Time controls enforcement
- [ ] Friend system and challenges
- [ ] Tournament support
- [ ] Chat system
- [ ] Game analysis integration
- [ ] Mobile apps (iOS/Android)
- [ ] Password recovery via email
- [ ] Two-factor authentication
- [ ] Anti-cheating measures
- [ ] Replay mode for finished games

## Support

For issues or questions:
- GitHub Issues: https://github.com/GizzZmo/CC/issues
- GitHub Discussions: https://github.com/GizzZmo/CC/discussions

---

**Last Updated**: December 2025
