#!/usr/bin/env python3
"""
CONFIGO GUI - Application Launcher
==================================

Launcher script that properly sets up the Python path and runs the modern GUI application.

Author: CONFIGO Team
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Add parent directory to Python path
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

print("🚀 Starting CONFIGO GUI...")
print(f"📁 Working directory: {os.getcwd()}")
print(f"🐍 Python path: {sys.path[:3]}...")

try:
    # Import and run the application
    from main import main
    main()
except Exception as e:
    print(f"❌ Error starting CONFIGO GUI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 