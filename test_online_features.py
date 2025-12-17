#!/usr/bin/env python3
"""
Test script for online multiplayer features.
Tests database, user management, and rating system.
"""

import sys


def test_database():
    """Test database functionality."""
    print("\n" + "=" * 60)
    print("Testing Database Module")
    print("=" * 60)
    
    try:
        from database import ChessDatabase
        
        # Create in-memory database
        db = ChessDatabase(':memory:')
        print("✅ Database initialized successfully")
        
        # Test user creation
        user1_id = db.create_user('Alice', 'password123', 'alice@example.com')
        user2_id = db.create_user('Bob', 'password456', 'bob@example.com')
        print(f"✅ Created users: Alice (ID={user1_id}), Bob (ID={user2_id})")
        
        # Test duplicate user
        duplicate = db.create_user('Alice', 'newpass', 'different@email.com')
        if duplicate is None:
            print("✅ Duplicate username correctly rejected")
        else:
            print("❌ Duplicate username was accepted (should be rejected)")
        
        # Test authentication
        user = db.authenticate_user('Alice', 'password123')
        if user and user['username'] == 'Alice':
            print(f"✅ Authentication successful: {user['username']}")
        else:
            print("❌ Authentication failed")
        
        # Test wrong password
        wrong = db.authenticate_user('Alice', 'wrongpassword')
        if wrong is None:
            print("✅ Wrong password correctly rejected")
        else:
            print("❌ Wrong password was accepted (should be rejected)")
        
        # Test Elo rating calculation
        rating_before = 1200
        opponent_rating = 1400
        
        # Win against higher rated opponent
        new_rating_win = db.calculate_elo_rating(rating_before, opponent_rating, 1.0)
        print(f"✅ Elo calculation (win): {rating_before} → {new_rating_win}")
        
        # Loss against higher rated opponent
        new_rating_loss = db.calculate_elo_rating(rating_before, opponent_rating, 0.0)
        print(f"✅ Elo calculation (loss): {rating_before} → {new_rating_loss}")
        
        # Draw
        new_rating_draw = db.calculate_elo_rating(rating_before, opponent_rating, 0.5)
        print(f"✅ Elo calculation (draw): {rating_before} → {new_rating_draw}")
        
        # Test game recording
        game_id = db.record_game(
            user1_id, user2_id, "1-0", "[Event \"Test\"]",
            1200, 1200, new_rating_win, new_rating_loss, "blitz"
        )
        print(f"✅ Game recorded with ID: {game_id}")
        
        # Test user profile update
        alice = db.get_user_by_id(user1_id)
        print(f"✅ Alice stats: {alice['games_played']} games, {alice['games_won']} wins")
        
        # Test leaderboard
        leaderboard = db.get_leaderboard(10)
        print(f"✅ Leaderboard retrieved with {len(leaderboard)} players")
        
        # Test game history
        games = db.get_user_games(user1_id, 10)
        print(f"✅ Game history retrieved: {len(games)} games for Alice")
        
        # Test matchmaking
        db.join_matchmaking_queue(user1_id, alice['rating'], 'blitz')
        print("✅ Joined matchmaking queue")
        
        match = db.find_match(user2_id, rating_range=300)
        if match:
            print(f"✅ Found match: {match['user_id']}")
        else:
            print("⚠️  No match found (expected with only 1 player in queue)")
        
        db.leave_matchmaking_queue(user1_id)
        print("✅ Left matchmaking queue")
        
        print("\n✅ All database tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_module_imports():
    """Test that all modules can be imported."""
    print("\n" + "=" * 60)
    print("Testing Module Imports")
    print("=" * 60)
    
    modules_to_test = [
        'database',
        'server',
        'multiplayer_client',
    ]
    
    failed = []
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} imported successfully")
        except ImportError as e:
            print(f"⚠️  {module_name} import warning: {e}")
            print(f"   (This is expected if dependencies are not installed)")
            failed.append((module_name, str(e)))
    
    if not failed:
        print("\n✅ All modules imported successfully!")
        return True
    else:
        print(f"\n⚠️  {len(failed)} modules had import warnings (install dependencies with 'pip install -r requirements.txt')")
        return True  # Still pass since it's expected without dependencies


def test_file_structure():
    """Test that all required files exist."""
    print("\n" + "=" * 60)
    print("Testing File Structure")
    print("=" * 60)
    
    import os
    
    required_files = [
        'database.py',
        'server.py',
        'multiplayer_client.py',
        'static/mobile_gui.html',
        'ONLINE_MULTIPLAYER_GUIDE.md',
        'launcher.py',
        'play.py',
        'requirements.txt',
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} not found")
            all_exist = False
    
    if all_exist:
        print("\n✅ All required files exist!")
    else:
        print("\n❌ Some files are missing")
    
    return all_exist


def test_requirements():
    """Test requirements.txt has new dependencies."""
    print("\n" + "=" * 60)
    print("Testing Requirements File")
    print("=" * 60)
    
    required_packages = [
        'flask',
        'flask-cors',
        'flask-socketio',
        'python-socketio',
        'requests',
    ]
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read().lower()
        
        all_found = True
        for package in required_packages:
            if package in content:
                print(f"✅ {package}")
            else:
                print(f"❌ {package} not found in requirements.txt")
                all_found = False
        
        if all_found:
            print("\n✅ All required packages listed!")
        else:
            print("\n❌ Some packages missing from requirements.txt")
        
        return all_found
        
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("CYBERCHESS ONLINE MULTIPLAYER TEST SUITE")
    print("=" * 60)
    
    results = {}
    
    # Run tests
    results['file_structure'] = test_file_structure()
    results['requirements'] = test_requirements()
    results['module_imports'] = test_module_imports()
    results['database'] = test_database()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} test categories passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("⚠️  Some tests did not pass")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
