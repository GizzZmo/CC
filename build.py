#!/usr/bin/env python3
"""
Build script for Cyberchess.
Creates distributable packages and documentation.
"""

import datetime
import os
import shutil
import sys
import zipfile
from pathlib import Path

# Configure stdout/stderr to use UTF-8 encoding on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


VERSION = "0.4.0"
PROJECT_NAME = "Cyberchess"
BUILD_DIR = "build"
DIST_DIR = "dist"
HASH_CHUNK_SIZE = 4096  # Size of chunks when reading files for hashing


def clean_build_dirs():
    """Clean previous build directories."""
    print("🧹 Cleaning build directories...")

    for dir_name in [BUILD_DIR, DIST_DIR]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ Removed {dir_name}/")

    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(DIST_DIR, exist_ok=True)
    print("  ✓ Created fresh build directories")


def copy_source_files():
    """Copy source files to build directory."""
    print("\n📦 Copying source files...")

    source_files = [
        "play.py",
        "game_modes.py",
        "cyberchess.py",
        "demo.py",
        "demo_advanced.py",
        "opening_book.py",
        "puzzles.py",
        "test_features.py",
        "requirements.txt",
        "config_template.py",
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        ".gitignore",
    ]

    for file in source_files:
        if os.path.exists(file):
            shutil.copy2(file, BUILD_DIR)
            print(f"  ✓ Copied {file}")
        else:
            print(f"  ⚠ Skipped {file} (not found)")

    # Copy examples directory
    if os.path.exists("examples"):
        shutil.copytree("examples", os.path.join(BUILD_DIR, "examples"))
        print(f"  ✓ Copied examples/")


def create_version_file():
    """Create a version.txt file."""
    print("\n📝 Creating version file...")

    version_content = f"""{PROJECT_NAME} Version {VERSION}
Built on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Phase 3 & 4 Features:
✓ Post-game engine analysis
✓ Time controls (Blitz, Rapid, Classical)
✓ Opening book integration
✓ Chess puzzle trainer
✓ Automated testing
✓ Enhanced documentation
"""

    version_file = os.path.join(BUILD_DIR, "VERSION.txt")
    with open(version_file, "w") as f:
        f.write(version_content)

    print(f"  ✓ Created VERSION.txt")


def create_install_guide():
    """Create an installation guide."""
    print("\n📖 Creating installation guide...")

    install_content = """# Cyberchess Installation Guide

## Quick Start

1. **Install Python 3.7+**
   - Download from https://www.python.org/downloads/

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Stockfish** (Optional for PvP mode, required for other modes)
   - Download from https://stockfishchess.org/download/
   - Note the path to the stockfish executable

4. **Configure**
   Set environment variables:
   ```bash
   export STOCKFISH_PATH="/path/to/stockfish"
   export GOOGLE_API_KEY="your-api-key"  # Only for AI vs AI mode
   ```
   
   Or edit play.py directly to set the paths.

5. **Run**
   ```bash
   python play.py
   ```

## Features

- **Player vs Player**: No configuration needed!
- **Player vs Computer**: Requires Stockfish
- **AI vs AI**: Requires Stockfish and Google Gemini API key
- **Puzzle Trainer**: Test your tactical skills
- **Opening Book**: Learn common openings
- **Time Controls**: Play with Blitz, Rapid, or Classical time limits
- **Post-Game Analysis**: Analyze your games with engine evaluation

## Getting API Keys

### Google Gemini API (for AI vs AI mode)
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Set the GOOGLE_API_KEY environment variable

## Troubleshooting

- **ModuleNotFoundError**: Run `pip install -r requirements.txt`
- **Stockfish not found**: Set STOCKFISH_PATH environment variable
- **API errors**: Check your GOOGLE_API_KEY is valid

For more help, see README.md or visit https://github.com/GizzZmo/CC
"""

    install_file = os.path.join(BUILD_DIR, "INSTALL.md")
    with open(install_file, "w") as f:
        f.write(install_content)

    print(f"  ✓ Created INSTALL.md")


def create_zip_archive():
    """Create a ZIP archive of the build."""
    print("\n🗜️  Creating ZIP archive...")

    zip_name = f"{PROJECT_NAME}-v{VERSION}.zip"
    zip_path = os.path.join(DIST_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BUILD_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, BUILD_DIR)
                arcname = os.path.join(f"{PROJECT_NAME}-v{VERSION}", arcname)
                zipf.write(file_path, arcname)
                print(f"  ✓ Added {arcname}")

    file_size = os.path.getsize(zip_path) / 1024  # Convert to KB
    print(f"\n  ✅ Created {zip_name} ({file_size:.1f} KB)")

    return zip_path


def create_source_distribution():
    """Create a source distribution (tar.gz)."""
    print("\n📦 Creating source distribution...")

    import tarfile

    tar_name = f"{PROJECT_NAME}-v{VERSION}-source.tar.gz"
    tar_path = os.path.join(DIST_DIR, tar_name)

    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(BUILD_DIR, arcname=f"{PROJECT_NAME}-v{VERSION}")

    file_size = os.path.getsize(tar_path) / 1024  # Convert to KB
    print(f"  ✅ Created {tar_name} ({file_size:.1f} KB)")

    return tar_path


def generate_checksums(files):
    """Generate SHA256 checksums for distribution files."""
    print("\n🔐 Generating checksums...")

    import hashlib

    checksum_file = os.path.join(DIST_DIR, "SHA256SUMS.txt")

    with open(checksum_file, "w") as f:
        f.write(f"# SHA256 Checksums for {PROJECT_NAME} v{VERSION}\n")
        f.write(
            f"# Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )

        for file_path in files:
            filename = os.path.basename(file_path)
            sha256 = hashlib.sha256()

            with open(file_path, "rb") as binary_file:
                for chunk in iter(lambda: binary_file.read(HASH_CHUNK_SIZE), b""):
                    sha256.update(chunk)

            checksum = sha256.hexdigest()
            f.write(f"{checksum}  {filename}\n")
            print(f"  ✓ {filename}: {checksum[:16]}...")

    print(f"\n  ✅ Created SHA256SUMS.txt")


def create_release_notes():
    """Create release notes."""
    print("\n📋 Creating release notes...")

    release_notes = f"""# {PROJECT_NAME} v{VERSION} Release Notes

Release Date: {datetime.datetime.now().strftime('%Y-%m-%d')}

## What's New in v{VERSION}

### Phase 3: Advanced Features (Complete)
- ✅ **Post-game Engine Analysis**: Analyze your games with Stockfish evaluation
  - Move-by-move evaluation in centipawns
  - Automatic detection of mistakes, blunders, and brilliant moves
  - Average position evaluation
  
- ✅ **Time Controls**: Play with standard time formats
  - Blitz (5 minutes)
  - Rapid (10 minutes)
  - Classical (30 minutes)
  - Custom time controls with increment support
  - Automatic timeout detection
  
- ✅ **Opening Book Integration**: Learn common chess openings
  - 12+ popular openings with ECO codes
  - Opening identification during games
  - Book move suggestions
  - Interactive opening explorer
  
- ✅ **Chess Puzzle Trainer**: Improve your tactical skills
  - 8+ built-in puzzles covering various themes
  - Difficulty levels: Easy, Medium, Hard
  - Interactive solving with hints
  - Themes: Forks, Pins, Mate patterns, Sacrifices
  
- ✅ **Configurable AI Colors**: Random or fixed color assignment for AI vs AI

### Phase 4: Polish (Complete)
- ✅ **Automated Testing**: Comprehensive test suite for all features
- ✅ **Enhanced Documentation**: Installation guide and detailed README
- ✅ **Build System**: Automated packaging and distribution
- ✅ **Performance Improvements**: Optimized engine analysis and move generation

### Previously Completed (v0.1-0.3)
- Full chess rules implementation
- Player vs Player mode
- Player vs Computer mode (with adjustable difficulty)
- AI vs AI mode (Stockfish vs Gemini)
- PGN import/export
- Move history tracking
- Example games collection

## Installation

See INSTALL.md for detailed installation instructions.

Quick start:
```bash
pip install -r requirements.txt
python play.py
```

## Files Included

- `play.py` - Main game launcher
- `game_modes.py` - Game mode implementations
- `opening_book.py` - Opening book database
- `puzzles.py` - Puzzle trainer
- `test_features.py` - Automated test suite
- `requirements.txt` - Python dependencies
- Documentation files (README.md, INSTALL.md, etc.)

## Known Limitations

- Online multiplayer not yet implemented (requires server infrastructure)
- Graphical UI not yet implemented (planned for future release)
- Limited to console-based interface

## Support

- GitHub Issues: https://github.com/GizzZmo/CC/issues
- Documentation: See README.md

## License

See repository for license information.
"""

    release_file = os.path.join(DIST_DIR, f"RELEASE-NOTES-v{VERSION}.md")
    with open(release_file, "w") as f:
        f.write(release_notes)

    print(f"  ✅ Created RELEASE-NOTES-v{VERSION}.md")


def build():
    """Main build function."""
    print("=" * 60)
    print(f"Building {PROJECT_NAME} v{VERSION}")
    print("=" * 60)

    # Clean and prepare
    clean_build_dirs()

    # Copy files
    copy_source_files()
    create_version_file()
    create_install_guide()

    # Create distributions
    zip_file = create_zip_archive()
    tar_file = create_source_distribution()

    # Generate checksums
    generate_checksums([zip_file, tar_file])

    # Create release notes
    create_release_notes()

    print("\n" + "=" * 60)
    print("✅ BUILD COMPLETE!")
    print("=" * 60)
    print(f"\nDistribution files created in '{DIST_DIR}/':")

    for file in os.listdir(DIST_DIR):
        file_path = os.path.join(DIST_DIR, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path) / 1024
            print(f"  • {file} ({size:.1f} KB)")

    print("\n🎉 Ready for distribution!")


if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)
