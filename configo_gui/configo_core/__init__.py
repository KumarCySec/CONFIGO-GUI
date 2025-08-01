"""
CONFIGO GUI - Core Module
==========================

Core backend integration for the CONFIGO GUI application.
Contains the GUI agent wrapper and backend communication.

Author: CONFIGO Team
"""

from .gui_agent import ConfigoGUIAgent, InstallationStep, InstallationWorker

__all__ = [
    'ConfigoGUIAgent',
    'InstallationStep',
    'InstallationWorker',
] 