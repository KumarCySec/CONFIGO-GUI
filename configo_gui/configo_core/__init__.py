"""
CONFIGO GUI - Core Module
==========================

Core backend integration for the CONFIGO GUI application.
Contains the GUI agent wrapper and backend communication.

Author: CONFIGO Team
"""

from .gui_agent import ConfigoGUIAgent, InstallationStep, InstallationWorker
from .cli_wrapper import (
    CLISubmoduleManager, cli_manager,
    get_cli_module, is_cli_available,
    get_system_info, generate_installation_plan,
    scan_project_directory, create_memory_instance,
    create_llm_agent, create_chat_agent,
    validate_tool, install_tools
)

__all__ = [
    'ConfigoGUIAgent',
    'InstallationStep',
    'InstallationWorker',
    'CLISubmoduleManager',
    'cli_manager',
    'get_cli_module',
    'is_cli_available',
    'get_system_info',
    'generate_installation_plan',
    'scan_project_directory',
    'create_memory_instance',
    'create_llm_agent',
    'create_chat_agent',
    'validate_tool',
    'install_tools',
] 