#!/usr/bin/env python3
"""
Cyberchess - Main Game Launcher
Provides a menu to select different game modes.
"""

import chess
from game_modes import PlayerVsPlayerGame, PlayerVsComputerGame, AIvsAIGame
import os
import sys


# --- CONFIGURATION ---
# Set these to your actual paths/keys
STOCKFISH_PATH = os.environ.get("STOCKFISH_PATH", "YOUR_STOCKFISH_PATH_HERE")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY_HERE")


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("♔♕♖♗♘♙  CYBERCHESS - MAIN MENU  ♟♞♝♜♛♚")
    print("=" * 50)
    print("\nSelect a game mode:")
    print("1. Player vs Player")
    print("2. Player vs Computer")
    print("3. AI vs AI (Stockfish vs Gemini)")
    print("4. Exit")
    print("=" * 50)


def get_user_choice():
    """Get user's menu choice."""
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")


def check_configuration():
    """Check if required configuration is set."""
    if STOCKFISH_PATH == "YOUR_STOCKFISH_PATH_HERE":
        print("\n⚠️  WARNING: STOCKFISH_PATH not configured!")
        print("Please set the STOCKFISH_PATH environment variable or edit play.py")
        print("Download Stockfish from: https://stockfishchess.org/download/")
        return False
        
    if GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n⚠️  WARNING: GOOGLE_API_KEY not configured!")
        print("This is only required for AI vs AI mode.")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        
    return True


def play_pvp():
    """Start a Player vs Player game."""
    game = PlayerVsPlayerGame()
    game.play()


def play_pvc():
    """Start a Player vs Computer game."""
    if not check_configuration():
        return
        
    print("\n" + "=" * 50)
    print("PLAYER VS COMPUTER SETUP")
    print("=" * 50)
    
    # Choose color
    while True:
        color_choice = input("\nDo you want to play as White or Black? (w/b): ").strip().lower()
        if color_choice in ['w', 'white']:
            player_color = chess.WHITE
            break
        elif color_choice in ['b', 'black']:
            player_color = chess.BLACK
            break
        else:
            print("❌ Invalid choice! Enter 'w' for White or 'b' for Black.")
    
    # Choose difficulty
    while True:
        try:
            skill = input("\nChoose Stockfish skill level (0-20, 0=beginner, 20=grandmaster): ").strip()
            skill_level = int(skill)
            if 0 <= skill_level <= 20:
                break
            else:
                print("❌ Please enter a number between 0 and 20.")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")
    
    game = PlayerVsComputerGame(STOCKFISH_PATH, player_color, skill_level)
    game.play()


def play_ai_vs_ai():
    """Start an AI vs AI game."""
    if not check_configuration():
        return
        
    if GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n❌ ERROR: GOOGLE_API_KEY must be configured for AI vs AI mode.")
        return
        
    print("\n" + "=" * 50)
    print("AI VS AI SETUP")
    print("=" * 50)
    
    # Choose Stockfish difficulty
    while True:
        try:
            skill = input("\nChoose Stockfish skill level (0-20, default=5): ").strip()
            if not skill:
                skill_level = 5
                break
            skill_level = int(skill)
            if 0 <= skill_level <= 20:
                break
            else:
                print("❌ Please enter a number between 0 and 20.")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")
    
    # Choose color assignment
    print("\n🎨 Color Assignment:")
    print("1. Stockfish plays White, Gemini plays Black (classic)")
    print("2. Stockfish plays Black, Gemini plays White")
    print("3. Random color assignment (recommended for diverse training)")
    
    while True:
        color_choice = input("\nChoose option (1-3, default=3): ").strip()
        if not color_choice or color_choice == '3':
            stockfish_color = None  # Random
            print("✨ Colors will be randomly assigned")
            break
        elif color_choice == '1':
            stockfish_color = chess.WHITE
            print("Stockfish will play White")
            break
        elif color_choice == '2':
            stockfish_color = chess.BLACK
            print("Stockfish will play Black")
            break
        else:
            print("❌ Invalid choice! Enter 1, 2, or 3.")
    
    game = AIvsAIGame(STOCKFISH_PATH, GOOGLE_API_KEY, skill_level, stockfish_color)
    game.play()


def main():
    """Main application loop."""
    print("\n" + "♔" * 50)
    print("Welcome to Cyberchess!")
    print("A modern chess platform with multiple game modes")
    print("♔" * 50)
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == '1':
            play_pvp()
        elif choice == '2':
            play_pvc()
        elif choice == '3':
            play_ai_vs_ai()
        elif choice == '4':
            print("\n👋 Thanks for playing Cyberchess! Goodbye!")
            break
            
        input("\nPress Enter to return to main menu...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
        sys.exit(0)
