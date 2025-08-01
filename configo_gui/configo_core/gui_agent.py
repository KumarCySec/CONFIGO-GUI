"""
CONFIGO GUI - GUI Agent
========================

The GUI agent wrapper that interfaces with the existing CONFIGO backend.
Provides async communication between the GUI and backend components.

Author: CONFIGO Team
"""

import sys
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Add parent directory to path for importing existing CONFIGO modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PySide6.QtCore import QObject, Signal, QThread, QTimer
from PySide6.QtWidgets import QApplication

# Import existing CONFIGO backend modules
try:
    from core.ai import suggest_stack, parse_llm_config
    from core.memory import AgentMemory
    from core.planner import PlanGenerator, PlanExecutor
    from core.validator import ToolValidator
    from core.project_scan import scan_project
    from core.chat_agent import ChatAgent
    from core.portal_orchestrator import PortalOrchestrator
    from core.system_inspector import SystemInspector
    from installers.base import install_tools
except ImportError as e:
    logging.error(f"Failed to import CONFIGO backend modules: {e}")
    # Create dummy functions for testing
    def suggest_stack(*args, **kwargs):
        return [], []
    
    def parse_llm_config(*args, **kwargs):
        return [], []
    
    class AgentMemory:
        def __init__(self):
            pass
    
    class PlanGenerator:
        def __init__(self):
            pass
    
    class PlanExecutor:
        def __init__(self):
            pass
    
    class ToolValidator:
        def __init__(self):
            pass
    
    class ChatAgent:
        def __init__(self):
            pass
    
    class PortalOrchestrator:
        def __init__(self):
            pass
    
    class SystemInspector:
        def __init__(self):
            pass
    
    def install_tools(*args, **kwargs):
        pass


@dataclass
class InstallationStep:
    """Represents a single installation step."""
    name: str
    description: str
    install_command: str
    check_command: str
    dependencies: List[str] = None
    status: str = "pending"  # pending, installing, success, error, skipped


class InstallationWorker(QThread):
    """
    Worker thread for handling installation operations.
    
    Runs installation tasks in the background to avoid blocking the GUI.
    """
    
    # Signals for progress updates
    progress_updated = Signal(int, int, str)  # step, total, message
    step_completed = Signal(str, bool, str)  # step_name, success, message
    installation_finished = Signal(bool, str)  # overall_success, message
    
    def __init__(self, installation_plan: List[InstallationStep]):
        super().__init__()
        self.installation_plan = installation_plan
        self.is_cancelled = False
    
    def run(self):
        """Execute the installation plan."""
        try:
            total_steps = len(self.installation_plan)
            successful_steps = 0
            
            for i, step in enumerate(self.installation_plan):
                if self.is_cancelled:
                    break
                
                # Update progress
                self.progress_updated.emit(i + 1, total_steps, f"Installing {step.name}...")
                
                try:
                    # Execute installation command
                    success = self.execute_installation_step(step)
                    
                    if success:
                        step.status = "success"
                        successful_steps += 1
                        self.step_completed.emit(step.name, True, f"{step.name} installed successfully")
                    else:
                        step.status = "error"
                        self.step_completed.emit(step.name, False, f"Failed to install {step.name}")
                
                except Exception as e:
                    step.status = "error"
                    self.step_completed.emit(step.name, False, f"Error installing {step.name}: {str(e)}")
            
            # Determine overall success
            overall_success = successful_steps == total_steps and not self.is_cancelled
            message = f"Installation completed: {successful_steps}/{total_steps} tools installed successfully"
            
            self.installation_finished.emit(overall_success, message)
            
        except Exception as e:
            self.installation_finished.emit(False, f"Installation failed: {str(e)}")
    
    def execute_installation_step(self, step: InstallationStep) -> bool:
        """Execute a single installation step."""
        try:
            # Import subprocess for command execution
            import subprocess
            import shlex
            
            # Execute the install command
            result = subprocess.run(
                shlex.split(step.install_command),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Check if installation was successful
            if result.returncode == 0:
                # Verify installation
                verify_result = subprocess.run(
                    shlex.split(step.check_command),
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                return verify_result.returncode == 0
            else:
                return False
                
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            logging.error(f"Error executing installation step {step.name}: {e}")
            return False
    
    def cancel(self):
        """Cancel the installation process."""
        self.is_cancelled = True


class ConfigoGUIAgent(QObject):
    """
    GUI agent that interfaces with the CONFIGO backend.
    
    Features:
    - Async communication with backend
    - Installation plan generation
    - Progress tracking
    - Error handling
    - Memory management
    """
    
    # Signals for GUI communication
    plan_generated = Signal(list)  # Emitted when installation plan is generated
    installation_progress = Signal(int, int, str)  # Emitted for progress updates
    installation_finished = Signal(bool, str)  # Emitted when installation completes
    log_message = Signal(str)  # Emitted for log messages
    error_occurred = Signal(str)  # Emitted when an error occurs
    
    def __init__(self):
        super().__init__()
        
        # Initialize backend components
        self.setup_backend_components()
        
        # Installation worker
        self.installation_worker = None
        
        # Current installation plan
        self.current_plan = []
        
        # Setup logging
        self.setup_logging()
    
    def setup_backend_components(self):
        """Initialize backend CONFIGO components."""
        try:
            # Initialize memory
            self.memory = AgentMemory()
            
            # Initialize planners
            self.plan_generator = PlanGenerator()
            self.plan_executor = PlanExecutor()
            
            # Initialize validators
            self.validator = ToolValidator()
            
            # Initialize other components
            self.chat_agent = ChatAgent()
            self.portal_orchestrator = PortalOrchestrator()
            self.system_inspector = SystemInspector()
            
            self.log_message.emit("Backend components initialized successfully")
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to initialize backend components: {str(e)}")
    
    def setup_logging(self):
        """Setup logging for the GUI agent."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_environment(self, environment_description: str):
        """Setup environment based on user description."""
        try:
            self.log_message.emit(f"Generating installation plan for: {environment_description}")
            
            # Generate installation plan using backend
            tools, portals = suggest_stack(environment_description)
            
            # Convert to InstallationStep objects
            installation_steps = []
            for tool in tools:
                step = InstallationStep(
                    name=tool.get('name', 'Unknown Tool'),
                    description=tool.get('description', ''),
                    install_command=tool.get('install_command', ''),
                    check_command=tool.get('check_command', ''),
                    dependencies=tool.get('dependencies', [])
                )
                installation_steps.append(step)
            
            self.current_plan = installation_steps
            
            # Convert to list format for GUI
            plan_list = []
            for step in installation_steps:
                plan_list.append({
                    'name': step.name,
                    'description': step.description,
                    'install_command': step.install_command,
                    'check_command': step.check_command,
                    'dependencies': step.dependencies or [],
                    'status': step.status
                })
            
            self.plan_generated.emit(plan_list)
            self.log_message.emit(f"Generated plan with {len(installation_steps)} tools")
            
        except Exception as e:
            error_msg = f"Failed to generate installation plan: {str(e)}"
            self.error_occurred.emit(error_msg)
            self.log_message.emit(f"ERROR: {error_msg}")
    
    def start_installation(self):
        """Start the installation process."""
        if not self.current_plan:
            self.error_occurred.emit("No installation plan available")
            return
        
        try:
            # Create and start installation worker
            self.installation_worker = InstallationWorker(self.current_plan)
            
            # Connect signals
            self.installation_worker.progress_updated.connect(self.on_progress_updated)
            self.installation_worker.step_completed.connect(self.on_step_completed)
            self.installation_worker.installation_finished.connect(self.on_installation_finished)
            
            # Start worker
            self.installation_worker.start()
            
            self.log_message.emit("Installation started")
            
        except Exception as e:
            error_msg = f"Failed to start installation: {str(e)}"
            self.error_occurred.emit(error_msg)
            self.log_message.emit(f"ERROR: {error_msg}")
    
    def cancel_installation(self):
        """Cancel the current installation."""
        if self.installation_worker and self.installation_worker.isRunning():
            self.installation_worker.cancel()
            self.installation_worker.wait()
            self.log_message.emit("Installation cancelled")
    
    def on_progress_updated(self, step: int, total: int, message: str):
        """Handle progress updates from installation worker."""
        self.installation_progress.emit(step, total, message)
        self.log_message.emit(message)
    
    def on_step_completed(self, step_name: str, success: bool, message: str):
        """Handle step completion from installation worker."""
        self.log_message.emit(message)
        
        # Update step status in current plan
        for step in self.current_plan:
            if step.name == step_name:
                step.status = "success" if success else "error"
                break
    
    def on_installation_finished(self, success: bool, message: str):
        """Handle installation completion."""
        self.installation_finished.emit(success, message)
        self.log_message.emit(message)
        
        # Clean up worker
        if self.installation_worker:
            self.installation_worker.deleteLater()
            self.installation_worker = None
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        try:
            # Use system inspector to get system info
            if hasattr(self, 'system_inspector'):
                return self.system_inspector.get_system_info()
            else:
                # Fallback system info
                import platform
                return {
                    'os': platform.system(),
                    'os_version': platform.release(),
                    'python_version': platform.python_version(),
                    'architecture': platform.machine()
                }
        except Exception as e:
            self.log_message.emit(f"Failed to get system info: {str(e)}")
            return {}
    
    def scan_project(self, project_path: str) -> Dict[str, Any]:
        """Scan a project for technology stack."""
        try:
            if hasattr(self, 'project_scanner'):
                return self.project_scanner.scan_project(project_path)
            else:
                # Fallback project scanning
                return {
                    'languages': [],
                    'frameworks': [],
                    'tools': [],
                    'dependencies': []
                }
        except Exception as e:
            self.log_message.emit(f"Failed to scan project: {str(e)}")
            return {}
    
    def chat_with_agent(self, message: str) -> str:
        """Send a message to the chat agent."""
        try:
            if hasattr(self, 'chat_agent'):
                return self.chat_agent.chat(message)
            else:
                return "Chat agent not available"
        except Exception as e:
            self.log_message.emit(f"Chat error: {str(e)}")
            return f"Error: {str(e)}"
    
    def open_portal(self, portal_name: str) -> bool:
        """Open a development portal."""
        try:
            if hasattr(self, 'portal_orchestrator'):
                return self.portal_orchestrator.open_portal(portal_name)
            else:
                self.log_message.emit(f"Portal orchestrator not available")
                return False
        except Exception as e:
            self.log_message.emit(f"Failed to open portal: {str(e)}")
            return False
    
    def validate_tool(self, tool_name: str) -> bool:
        """Validate if a tool is properly installed."""
        try:
            if hasattr(self, 'validator'):
                return self.validator.validate_tool(tool_name)
            else:
                # Fallback validation
                import subprocess
                result = subprocess.run([tool_name, '--version'], capture_output=True)
                return result.returncode == 0
        except Exception as e:
            self.log_message.emit(f"Validation error: {str(e)}")
            return False
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get memory information."""
        try:
            if hasattr(self, 'memory'):
                return self.memory.get_memory_info()
            else:
                return {
                    'session_history': [],
                    'user_preferences': {},
                    'tool_statistics': {}
                }
        except Exception as e:
            self.log_message.emit(f"Failed to get memory info: {str(e)}")
            return {}
    
    def clear_memory(self):
        """Clear all memory data."""
        try:
            if hasattr(self, 'memory'):
                self.memory.clear_all()
            self.log_message.emit("Memory cleared")
        except Exception as e:
            self.log_message.emit(f"Failed to clear memory: {str(e)}")
    
    def add_tool_to_plan(self, tool_info: Dict[str, Any]):
        """Add a tool to the installation plan."""
        try:
            # Create installation step from tool info
            step = InstallationStep(
                name=tool_info.get("name", "Unknown Tool"),
                description=tool_info.get("description", ""),
                install_command=tool_info.get("install_command", ""),
                check_command=tool_info.get("check_command", ""),
                status="pending"
            )
            
            # Add to plan
            if not hasattr(self, 'installation_plan'):
                self.installation_plan = []
            
            self.installation_plan.append(step)
            self.log_message.emit(f"Added {tool_info['name']} to installation plan")
            
        except Exception as e:
            self.log_message.emit(f"Failed to add tool to plan: {str(e)}")
    
    def update_user_profile(self, profile: Dict[str, Any]):
        """Update user profile information."""
        try:
            if hasattr(self, 'memory'):
                self.memory.update_user_profile(profile)
            
            self.log_message.emit("User profile updated")
            
        except Exception as e:
            self.log_message.emit(f"Failed to update profile: {str(e)}")
    
    def update_step_status(self, step_name: str, success: bool):
        """Update the status of an installation step."""
        try:
            if hasattr(self, 'installation_plan'):
                for step in self.installation_plan:
                    if step.name == step_name:
                        step.status = "completed" if success else "error"
                        break
            
            self.log_message.emit(f"Step '{step_name}' status updated")
            
        except Exception as e:
            self.log_message.emit(f"Failed to update step status: {str(e)}")
    
    def log_command(self, command: str, exit_code: int):
        """Log a command execution."""
        try:
            if hasattr(self, 'memory'):
                self.memory.log_command(command, exit_code)
            
            self.log_message.emit(f"Command logged: {command} (exit code: {exit_code})")
            
        except Exception as e:
            self.log_message.emit(f"Failed to log command: {str(e)}")
    
    def cleanup(self):
        """Cleanup resources when application closes."""
        try:
            # Cancel any running installation
            if self.installation_worker and self.installation_worker.isRunning():
                self.installation_worker.cancel()
                self.installation_worker.wait()
            
            # Save memory
            if hasattr(self, 'memory'):
                self.memory.save()
            
            self.log_message.emit("GUI agent cleanup completed")
            
        except Exception as e:
            self.log_message.emit(f"Cleanup error: {str(e)}") 