"""
CONFIGO GUI - CLI Submodule Wrapper
====================================

Provides a clean interface to the CONFIGO CLI submodule.
Handles path management, import errors, and provides fallback functionality.

Author: CONFIGO Team
"""

import sys
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class CLISubmoduleManager:
    """
    Manages the CLI submodule integration for the GUI.
    
    Features:
    - Automatic submodule path detection
    - Import error handling with fallbacks
    - Clean interface to CLI functionality
    - Memory and state management
    """
    
    def __init__(self):
        self.cli_path = self._find_cli_submodule()
        self.is_available = self.cli_path is not None
        self._setup_imports()
        
    def _find_cli_submodule(self) -> Optional[Path]:
        """Find the CLI submodule path."""
        possible_paths = [
            Path(__file__).parent.parent.parent / "cli_submodule",
            Path(__file__).parent.parent.parent.parent / "cli_submodule",
            Path.cwd() / "cli_submodule"
        ]
        
        for path in possible_paths:
            if path.exists() and (path / "core").exists():
                logger.info(f"Found CLI submodule at: {path}")
                return path
                
        logger.warning("CLI submodule not found in expected locations")
        return None
    
    def _setup_imports(self):
        """Setup imports from the CLI submodule."""
        if not self.is_available:
            logger.error("CLI submodule not available")
            return
            
        # Add CLI submodule to Python path
        sys.path.insert(0, str(self.cli_path))
        
        # Import core modules
        try:
            from core.ai import suggest_stack, parse_llm_config, LLMClient
            from core.memory import AgentMemory
            from core.planner import PlanGenerator, PlanExecutor, InstallationPlan
            from core.validator import ToolValidator, ValidationReport
            from core.project_scan import scan_project
            from core.chat_agent import ChatAgent
            from core.portal_orchestrator import PortalOrchestrator
            from core.system import get_system_info
            from core.enhanced_llm_agent import EnhancedLLMAgent
            from core.shell_executor import ShellExecutor
            from core.app_name_extractor import AppNameExtractor
            from installers.base import install_tools
            
            # Store imported modules
            self._modules = {
                'suggest_stack': suggest_stack,
                'parse_llm_config': parse_llm_config,
                'LLMClient': LLMClient,
                'AgentMemory': AgentMemory,
                'PlanGenerator': PlanGenerator,
                'PlanExecutor': PlanExecutor,
                'InstallationPlan': InstallationPlan,
                'ToolValidator': ToolValidator,
                'ValidationReport': ValidationReport,
                'scan_project': scan_project,
                'ChatAgent': ChatAgent,
                'PortalOrchestrator': PortalOrchestrator,
                'SystemInspector': get_system_info,  # Use system.get_system_info as SystemInspector
                'EnhancedLLMAgent': EnhancedLLMAgent,
                'ShellExecutor': ShellExecutor,
                'AppNameExtractor': AppNameExtractor,
                'install_tools': install_tools
            }
            
            logger.info("✅ Successfully imported all CLI modules from submodule")
            
        except ImportError as e:
            logger.error(f"Failed to import CLI modules: {e}")
            self._modules = {}
            self._create_fallback_modules()
    
    def _create_fallback_modules(self):
        """Create fallback modules when CLI is not available."""
        logger.warning("Creating fallback modules for testing")
        
        class FallbackAgentMemory:
            def __init__(self):
                self.memory = {}
            
            def get(self, key, default=None):
                return self.memory.get(key, default)
            
            def set(self, key, value):
                self.memory[key] = value
        
        class FallbackPlanGenerator:
            def __init__(self):
                pass
            
            def generate_plan(self, description):
                return {"tools": [], "commands": [], "estimated_time": "5-10 minutes"}
        
        class FallbackSystemInspector:
            def __init__(self):
                pass
            
            def get_system_info(self):
                return {"os": "unknown", "package_managers": []}
        
        self._modules = {
            'AgentMemory': FallbackAgentMemory,
            'PlanGenerator': FallbackPlanGenerator,
            'SystemInspector': FallbackSystemInspector,
            'suggest_stack': lambda *args, **kwargs: ([], []),
            'parse_llm_config': lambda *args, **kwargs: ([], []),
            'scan_project': lambda *args, **kwargs: {},
            'install_tools': lambda *args, **kwargs: True
        }
    
    def get_module(self, name: str):
        """Get a module from the CLI submodule."""
        return self._modules.get(name)
    
    def is_module_available(self, name: str) -> bool:
        """Check if a module is available."""
        return name in self._modules
    
    def get_available_modules(self) -> List[str]:
        """Get list of available modules."""
        return list(self._modules.keys())


# Global CLI manager instance
cli_manager = CLISubmoduleManager()


def get_cli_module(name: str):
    """Get a CLI module by name."""
    return cli_manager.get_module(name)


def is_cli_available() -> bool:
    """Check if CLI submodule is available."""
    return cli_manager.is_available


def get_system_info() -> Dict[str, Any]:
    """Get system information using CLI."""
    SystemInspector = get_cli_module('SystemInspector')
    if SystemInspector:
        inspector = SystemInspector()
        return inspector.get_system_info()
    return {"os": "unknown", "package_managers": []}


def generate_installation_plan(description: str) -> Dict[str, Any]:
    """Generate installation plan using CLI."""
    PlanGenerator = get_cli_module('PlanGenerator')
    if PlanGenerator:
        generator = PlanGenerator()
        return generator.generate_plan(description)
    return {"tools": [], "commands": [], "estimated_time": "5-10 minutes"}


def scan_project_directory(path: str) -> Dict[str, Any]:
    """Scan project directory using CLI."""
    scan_project = get_cli_module('scan_project')
    if scan_project:
        return scan_project(path)
    return {"files": [], "languages": [], "frameworks": []}


def create_memory_instance() -> Any:
    """Create a memory instance using CLI."""
    AgentMemory = get_cli_module('AgentMemory')
    if AgentMemory:
        return AgentMemory()
    return None


def create_llm_agent() -> Any:
    """Create an LLM agent using CLI."""
    EnhancedLLMAgent = get_cli_module('EnhancedLLMAgent')
    if EnhancedLLMAgent:
        return EnhancedLLMAgent()
    return None


def create_chat_agent() -> Any:
    """Create a chat agent using CLI."""
    ChatAgent = get_cli_module('ChatAgent')
    if ChatAgent:
        return ChatAgent()
    return None


def validate_tool(tool_name: str) -> bool:
    """Validate a tool using CLI."""
    ToolValidator = get_cli_module('ToolValidator')
    if ToolValidator:
        validator = ToolValidator()
        return validator.validate_tool(tool_name)
    return False


def install_tools(tools: List[str]) -> bool:
    """Install tools using CLI."""
    install_tools_func = get_cli_module('install_tools')
    if install_tools_func:
        return install_tools_func(tools)
    return False 