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

__version__ = "1.0.0"
__author__ = "CONFIGO Team"
__email__ = "team@configo.dev"
__url__ = "https://github.com/configo/configo-gui"

from .ui import (
    MainWindow,
    WelcomeScreen,
    EnvironmentSetupScreen,
    PlanRendererScreen,
    LogConsoleWidget,
    PortalIntegrationWidget,
    MemoryViewWidget,
    ErrorHandlerWidget,
)

from .configo_core import ConfigoGUIAgent

__all__ = [
    'MainWindow',
    'WelcomeScreen',
    'EnvironmentSetupScreen', 
    'PlanRendererScreen',
    'LogConsoleWidget',
    'PortalIntegrationWidget',
    'MemoryViewWidget',
    'ErrorHandlerWidget',
    'ConfigoGUIAgent',
] 