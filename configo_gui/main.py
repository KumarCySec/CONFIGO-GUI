#!/usr/bin/env python3
"""
CONFIGO GUI - Modern Desktop Application
========================================

A modern, cross-platform GUI desktop application for CONFIGO,
the Autonomous AI Setup Agent. Built with PySide6 (Qt for Python)
with advanced glassmorphism effects and animations.

Features:
- 🎨 Modern glassmorphism UI with blur effects
- 🧠 AI-powered environment setup
- 📋 Visual plan rendering with animations
- 🖥️ Real-time log console with syntax highlighting
- 🌐 Portal integration with modern styling
- 💾 Memory management with visual timeline
- ⚡ Async backend operations
- 🎭 Smooth animations and transitions
- 🌈 Modern color scheme and typography

Author: CONFIGO Team
"""

import sys
import os
import logging
from pathlib import Path
from typing import Optional

# Add current directory to Python path FIRST
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Add parent directory to Python path
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

print(f"📁 Current directory: {current_dir}")
print(f"🐍 Python path starts with: {sys.path[:3]}")

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# Import modern main window
try:
    from ui.modern_main_window import ModernMainWindow
    print("✅ Successfully imported ModernMainWindow")
except ImportError as e:
    print(f"❌ Failed to import ModernMainWindow: {e}")
    # Fallback to demo if modern main window is not available
    try:
        from demo_modern_gui import ModernDemoWindow as ModernMainWindow
        print("✅ Falling back to ModernDemoWindow")
    except ImportError as e2:
        print(f"❌ Failed to import demo window: {e2}")
        sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('configo_gui.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def setup_application_properties(app: QApplication) -> None:
    """
    Configure application-wide properties and styling.
    
    Args:
        app: The QApplication instance
    """
    # Set application properties
    app.setApplicationName("CONFIGO GUI")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("CONFIGO")
    app.setOrganizationDomain("configo.dev")
    
    # Set application icon (if available)
    icon_path = Path(__file__).parent / "assets" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Enable high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Set application style
    app.setStyle("Fusion")


def main() -> None:
    """
    Main entry point for CONFIGO GUI application.
    """
    try:
        print("🚀 Starting CONFIGO GUI...")
        
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Setup application properties
        setup_application_properties(app)
        
        # Create and show modern main window
        window = ModernMainWindow()
        window.show()
        
        print("✅ CONFIGO GUI window created and shown")
        
        # Start application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Failed to start CONFIGO GUI: {e}")
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 