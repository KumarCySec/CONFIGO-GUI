"""
CONFIGO GUI - UI Module
========================

UI components for the CONFIGO GUI application.
Contains all the visual components and widgets.

Author: CONFIGO Team
"""

from .main_window import MainWindow
from .welcome_screen import WelcomeScreen
from .environment_setup import EnvironmentSetupScreen
from .plan_renderer import PlanRendererScreen, ToolCard
from .log_console import LogConsoleWidget, LogHighlighter
from .portal_integration import PortalIntegrationWidget, PortalItem
from .memory_view import MemoryViewWidget
from .error_handler import ErrorHandlerWidget, ErrorDialog

# Modern UI components
try:
    from .modern_main_window import ModernMainWindow
    MODERN_UI_AVAILABLE = True
except ImportError:
    MODERN_UI_AVAILABLE = False

__all__ = [
    'MainWindow',
    'WelcomeScreen', 
    'EnvironmentSetupScreen',
    'PlanRendererScreen',
    'ToolCard',
    'LogConsoleWidget',
    'LogHighlighter',
    'PortalIntegrationWidget',
    'PortalItem',
    'MemoryViewWidget',
    'ErrorHandlerWidget',
    'ErrorDialog',
]

# Add modern components if available
if MODERN_UI_AVAILABLE:
    __all__.append('ModernMainWindow') 