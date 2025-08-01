#!/usr/bin/env python3
"""
CONFIGO GUI - Desktop Application
=================================

A modern, cross-platform GUI desktop application for CONFIGO,
the Autonomous AI Setup Agent. Built with PySide6 (Qt for Python).

Features:
- 🎨 Modern dark theme UI
- 🧠 AI-powered environment setup
- 📋 Visual plan rendering
- 🖥️ Real-time log console
- 🌐 Portal integration
- 💾 Memory management
- ⚡ Async backend operations

Author: CONFIGO Team
License: MIT
"""

import sys
import os
import logging
from pathlib import Path
from typing import Optional

# Add current directory and parent directory to path for importing modules
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QStackedWidget, QLabel, QPushButton,
    QFrame, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap

# Import GUI components
from ui.main_window import MainWindow
from configo_core.gui_agent import ConfigoGUIAgent

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


def setup_dark_theme(app: QApplication) -> None:
    """
    Apply a modern dark theme to the application.
    
    Args:
        app: The QApplication instance
    """
    # Create dark palette
    palette = QPalette()
    
    # Set dark colors
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    # Set the palette
    app.setPalette(palette)
    
    # Set application style
    app.setStyle("Fusion")


def setup_application_style(app: QApplication) -> None:
    """
    Configure application-wide styling.
    
    Args:
        app: The QApplication instance
    """
    # Set application properties
    app.setApplicationName("CONFIGO GUI")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("CONFIGO")
    app.setOrganizationDomain("configo.dev")
    
    # Set application icon (if available)
    icon_path = Path(__file__).parent / "assets" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))


def main() -> None:
    """
    Main entry point for CONFIGO GUI application.
    """
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Setup theme and styling
        setup_dark_theme(app)
        setup_application_style(app)
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Start application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Failed to start CONFIGO GUI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 