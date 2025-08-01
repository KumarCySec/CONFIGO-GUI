#!/usr/bin/env python3
"""
CONFIGO GUI Launcher
Modern desktop application for intelligent development environment setup
"""

import sys
import os
from pathlib import Path

# Add the gui directory to Python path
gui_path = Path(__file__).parent / "gui"
sys.path.insert(0, str(gui_path))

def main():
    """Launch the CONFIGO GUI application"""
    try:
        from gui.main import CONFIGOGUI
        app = CONFIGOGUI()
        sys.exit(app.run())
    except ImportError as e:
        print(f"Error importing GUI components: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r gui/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to launch CONFIGO GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 