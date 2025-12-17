#!/usr/bin/env python3
"""
Cyberchess Launcher
Choose between CLI and Cyberpunk GUI interfaces.
"""

import os
import sys


def display_launcher_menu():
    """Display the launcher menu."""
    print("\n" + "=" * 60)
    print("⚡" * 30)
    print("=" * 60)
    print(
        """
   ▄████▄ ▓██   ██▓ ▄▄▄▄   ▓█████  ██▀███   ▄████▄   ██░ ██ ▓█████   ██████   ██████ 
  ▒██▀ ▀█  ▒██  ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██    ▒ ▒██    ▒ 
  ▒▓█    ▄  ▒██ ██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒▒▓█    ▄ ▒██▀▀██░▒███   ░ ▓██▄   ░ ▓██▄   
  ▒▓▓▄ ▄██▒ ░ ▐██▓░▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄   ▒   ██▒  ▒   ██▒
  ▒ ▓███▀ ░ ░ ██▒▓░░▓█  ▀█▓░▒████▒░██▓ ▒██▒▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒██████▒▒▒██████▒▒
  ░ ░▒ ▒  ░  ██▒▒▒ ░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░
    ░  ▒   ▓██ ░▒░ ▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░  ░  ▒    ▒ ░▒░ ░ ░ ░  ░░ ░▒  ░ ░░ ░▒  ░ ░
  ░        ▒ ▒ ░░   ░    ░    ░     ░░   ░ ░         ░  ░░ ░   ░   ░  ░  ░  ░  ░  ░  
  ░ ░      ░ ░      ░         ░  ░   ░     ░ ░       ░  ░  ░   ░  ░      ░        ░  
  ░        ░ ░           ░                 ░                                          
    """
    )
    print("=" * 60)
    print("⚡" * 30)
    print("=" * 60)
    print("\n🎮 Choose Your Interface:\n")
    print("  1. 💀 CYBERPUNK GUI - Neon-themed graphical interface")
    print("  2. 🖥️  CLASSIC CLI  - Traditional console interface")
    print("  3. 🌐 ONLINE SERVER - Start multiplayer server")
    print("  4. 📱 MOBILE WEB    - Launch mobile web interface")
    print("  5. ❌ EXIT\n")
    print("=" * 60)


def main():
    """Main launcher function."""
    while True:
        display_launcher_menu()

        choice = input("\n⚡ Enter your choice (1-5): ").strip()

        if choice == "1":
            print("\n🚀 Launching Cyberpunk GUI...")
            print("=" * 60)
            try:
                # Import and run GUI
                from cyberpunk_gui import main as gui_main

                gui_main()
            except ImportError as e:
                print(f"\n❌ Error: Could not load GUI module: {e}")
                print("Make sure tkinter is installed (usually comes with Python)")
            except Exception as e:
                print(f"\n❌ Error launching GUI: {e}")
                import traceback

                traceback.print_exc()

            # Return to menu after GUI closes
            continue

        elif choice == "2":
            print("\n🚀 Launching Classic CLI...")
            print("=" * 60)
            try:
                # Import and run CLI
                from play import main as cli_main

                cli_main()
            except Exception as e:
                print(f"\n❌ Error launching CLI: {e}")
                import traceback

                traceback.print_exc()

            # Return to menu after CLI exits
            continue

        elif choice == "3":
            print("\n🚀 Starting Online Multiplayer Server...")
            print("=" * 60)
            try:
                # Import and run server
                from server import main as server_main

                server_main()
            except ImportError as e:
                print(f"\n❌ Error: Could not load server module: {e}")
                print("Make sure Flask and Flask-SocketIO are installed:")
                print("  pip install flask flask-cors flask-socketio")
            except Exception as e:
                print(f"\n❌ Error launching server: {e}")
                import traceback

                traceback.print_exc()

            # Return to menu after server stops
            continue

        elif choice == "4":
            print("\n🚀 Launching Mobile Web Interface...")
            print("=" * 60)
            print("\n📱 Mobile web interface available at:")
            print("   http://localhost:5000")
            print("\n⚠️  Starting server in 3 seconds...")
            print("   Press Ctrl+C to stop the server and return to menu")
            import time

            time.sleep(3)
            try:
                from server import main as server_main

                server_main()
            except ImportError as e:
                print(f"\n❌ Error: Could not load server module: {e}")
                print("Make sure Flask and Flask-SocketIO are installed:")
                print("  pip install flask flask-cors flask-socketio")
            except Exception as e:
                print(f"\n❌ Error launching server: {e}")
                import traceback

                traceback.print_exc()

            # Return to menu
            continue

        elif choice == "5":
            print("\n👋 Thanks for using Cyberchess! Goodbye!")
            print("=" * 60)
            break

        else:
            print("\n❌ Invalid choice! Please enter 1, 2, 3, 4, or 5.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted. Goodbye!")
        sys.exit(0)
