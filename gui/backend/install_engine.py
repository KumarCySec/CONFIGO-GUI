"""
CONFIGO GUI - Install Engine
Backend interface to CLI submodule for installation logic
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
import asyncio
import json


class InstallEngine:
    """Backend engine that interfaces with CLI submodule"""
    
    def __init__(self):
        self.cli_path = Path(__file__).parent.parent.parent / "cli_submodule"
        self.memory_path = Path(__file__).parent.parent.parent / ".configo_memory"
        
        # Ensure CLI submodule is available
        if not self.cli_path.exists():
            raise RuntimeError("CLI submodule not found. Please run: git submodule update --init")
            
        # Add CLI to Python path
        sys.path.insert(0, str(self.cli_path))
        
    def get_available_tools(self) -> List[Dict]:
        """Get list of available tools from CLI"""
        try:
            # Import CLI modules
            from core.system import SystemInspector
            from core.detection import ToolDetector
            
            # Get system info
            system = SystemInspector()
            detector = ToolDetector()
            
            # Get available package managers
            package_managers = system.get_package_managers()
            
            # Get detected tools
            detected_tools = detector.detect_installed_tools()
            
            return {
                "package_managers": package_managers,
                "installed_tools": detected_tools
            }
            
        except ImportError as e:
            print(f"Warning: Could not import CLI modules: {e}")
            return {
                "package_managers": ["apt", "snap", "flatpak"],
                "installed_tools": []
            }
            
    def generate_installation_plan(self, description: str) -> Dict:
        """Generate installation plan using CLI logic"""
        try:
            # Import CLI modules
            from core.enhanced_llm_agent import EnhancedLLMAgent
            from core.planner import InstallationPlanner
            
            # Create LLM agent
            agent = EnhancedLLMAgent()
            
            # Generate plan
            plan = agent.generate_installation_plan(description)
            
            return {
                "description": description,
                "tools": plan.get("tools", []),
                "commands": plan.get("commands", []),
                "estimated_time": plan.get("estimated_time", "5-10 minutes")
            }
            
        except Exception as e:
            print(f"Warning: Could not generate plan using CLI: {e}")
            # Fallback to mock plan
            return self._generate_mock_plan(description)
            
    def execute_installation(self, plan: Dict, progress_callback=None) -> Dict:
        """Execute installation using CLI logic"""
        try:
            # Import CLI modules
            from core.shell_executor import ShellExecutor
            from core.validator import InstallationValidator
            
            executor = ShellExecutor()
            validator = InstallationValidator()
            
            results = {
                "success": True,
                "installed_tools": [],
                "failed_tools": [],
                "logs": []
            }
            
            # Execute each command
            for i, command in enumerate(plan.get("commands", [])):
                if progress_callback:
                    progress = int((i / len(plan.get("commands", []))) * 100)
                    progress_callback(progress, f"Executing: {command}")
                    
                try:
                    result = executor.execute_command(command)
                    if result["success"]:
                        results["installed_tools"].append(command)
                    else:
                        results["failed_tools"].append(command)
                        
                    results["logs"].append(f"[{'SUCCESS' if result['success'] else 'ERROR'}] {command}")
                    
                except Exception as e:
                    results["failed_tools"].append(command)
                    results["logs"].append(f"[ERROR] {command}: {str(e)}")
                    
            # Validate installation
            validation_result = validator.validate_installation(results["installed_tools"])
            results["validation"] = validation_result
            
            return results
            
        except Exception as e:
            print(f"Warning: Could not execute installation using CLI: {e}")
            # Fallback to mock installation
            return self._execute_mock_installation(plan, progress_callback)
            
    def get_memory_data(self) -> Dict:
        """Get memory data from CLI"""
        try:
            memory_file = self.memory_path / "memory.json"
            if memory_file.exists():
                with open(memory_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Warning: Could not load memory data: {e}")
            return {}
            
    def save_memory_data(self, data: Dict):
        """Save memory data to CLI"""
        try:
            self.memory_path.mkdir(exist_ok=True)
            memory_file = self.memory_path / "memory.json"
            with open(memory_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save memory data: {e}")
            
    def _generate_mock_plan(self, description: str) -> Dict:
        """Generate a mock installation plan"""
        # Parse description to determine tools
        description_lower = description.lower()
        
        tools = []
        commands = []
        
        if "python" in description_lower or "data science" in description_lower:
            tools.extend(["Python 3.11", "pip", "Jupyter"])
            commands.extend([
                "sudo apt update",
                "sudo apt install python3.11 python3-pip -y",
                "pip3 install jupyter pandas numpy matplotlib"
            ])
            
        if "node" in description_lower or "javascript" in description_lower or "web" in description_lower:
            tools.extend(["Node.js", "npm"])
            commands.extend([
                "curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -",
                "sudo apt-get install -y nodejs"
            ])
            
        if "git" in description_lower:
            tools.append("Git")
            commands.append("sudo apt install git -y")
            
        if "docker" in description_lower:
            tools.append("Docker")
            commands.extend([
                "sudo apt install docker.io -y",
                "sudo systemctl start docker",
                "sudo systemctl enable docker"
            ])
            
        if "postgres" in description_lower or "database" in description_lower:
            tools.append("PostgreSQL")
            commands.append("sudo apt install postgresql postgresql-contrib -y")
            
        return {
            "description": description,
            "tools": tools,
            "commands": commands,
            "estimated_time": "5-10 minutes"
        }
        
    def _execute_mock_installation(self, plan: Dict, progress_callback=None) -> Dict:
        """Execute a mock installation"""
        import time
        
        results = {
            "success": True,
            "installed_tools": [],
            "failed_tools": [],
            "logs": []
        }
        
        commands = plan.get("commands", [])
        
        for i, command in enumerate(commands):
            if progress_callback:
                progress = int((i / len(commands)) * 100)
                progress_callback(progress, f"Executing: {command}")
                
            # Simulate execution time
            time.sleep(1)
            
            # Mock success for most commands
            if "error" not in command.lower():
                results["installed_tools"].append(command)
                results["logs"].append(f"[SUCCESS] {command}")
            else:
                results["failed_tools"].append(command)
                results["logs"].append(f"[ERROR] {command}: Mock error")
                
        results["validation"] = {
            "success": True,
            "message": "Mock validation completed"
        }
        
        return results
        
    def get_system_info(self) -> Dict:
        """Get system information"""
        try:
            import platform
            import subprocess
            
            return {
                "os": platform.system(),
                "os_version": platform.release(),
                "python_version": platform.python_version(),
                "architecture": platform.machine()
            }
        except Exception as e:
            return {
                "os": "Unknown",
                "os_version": "Unknown",
                "python_version": "Unknown",
                "architecture": "Unknown"
            }
            
    def validate_environment(self) -> Dict:
        """Validate the current environment"""
        try:
            system_info = self.get_system_info()
            available_tools = self.get_available_tools()
            
            return {
                "system_info": system_info,
                "available_tools": available_tools,
                "cli_available": True,
                "memory_available": self.memory_path.exists()
            }
        except Exception as e:
            return {
                "system_info": self.get_system_info(),
                "available_tools": {"package_managers": [], "installed_tools": []},
                "cli_available": False,
                "memory_available": False,
                "error": str(e)
            } 