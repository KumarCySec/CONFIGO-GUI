#!/usr/bin/env python3
"""
Test CLI Submodule Integration
==============================

Comprehensive test to verify that the CLI submodule is properly integrated
and all imports are working correctly.

Author: CONFIGO Team
"""

import sys
import os
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_submodule_presence():
    """Test that the CLI submodule is present and properly configured."""
    print("🔍 Testing CLI Submodule Presence...")
    
    # Check if submodule directory exists
    cli_submodule_path = Path(__file__).parent / "cli_submodule"
    if not cli_submodule_path.exists():
        print("❌ CLI submodule directory not found")
        return False
    
    print(f"✅ CLI submodule found at: {cli_submodule_path}")
    
    # Check if core directory exists in submodule
    core_path = cli_submodule_path / "core"
    if not core_path.exists():
        print("❌ Core directory not found in submodule")
        return False
    
    print(f"✅ Core directory found in submodule: {core_path}")
    
    # Check if key files exist
    key_files = ["ai.py", "memory.py", "planner.py", "validator.py"]
    for file in key_files:
        file_path = core_path / file
        if not file_path.exists():
            print(f"❌ Key file not found: {file}")
            return False
        print(f"✅ Key file found: {file}")
    
    return True

def test_git_submodule_config():
    """Test that git submodule is properly configured."""
    print("\n🔍 Testing Git Submodule Configuration...")
    
    # Check .gitmodules file
    gitmodules_path = Path(__file__).parent / ".gitmodules"
    if not gitmodules_path.exists():
        print("❌ .gitmodules file not found")
        return False
    
    print("✅ .gitmodules file found")
    
    # Read and check .gitmodules content
    try:
        with open(gitmodules_path, 'r') as f:
            content = f.read()
            if "cli_submodule" in content and "Configo.git" in content:
                print("✅ .gitmodules contains correct submodule configuration")
            else:
                print("❌ .gitmodules configuration appears incorrect")
                return False
    except Exception as e:
        print(f"❌ Error reading .gitmodules: {e}")
        return False
    
    return True

def test_imports_from_submodule():
    """Test that imports from the CLI submodule work correctly."""
    print("\n🔍 Testing Imports from CLI Submodule...")
    
    # Add submodule to path
    cli_submodule_path = Path(__file__).parent / "cli_submodule"
    if cli_submodule_path.exists():
        sys.path.insert(0, str(cli_submodule_path))
    
    # Test imports
    try:
        from core.memory import AgentMemory
        print("✅ Successfully imported AgentMemory from submodule")
    except ImportError as e:
        print(f"❌ Failed to import AgentMemory: {e}")
        return False
    
    try:
        from core.ai import LLMClient
        print("✅ Successfully imported LLMClient from submodule")
    except ImportError as e:
        print(f"❌ Failed to import LLMClient: {e}")
        return False
    
    try:
        from core.planner import PlanGenerator
        print("✅ Successfully imported PlanGenerator from submodule")
    except ImportError as e:
        print(f"❌ Failed to import PlanGenerator: {e}")
        return False
    
    try:
        from core.validator import ToolValidator
        print("✅ Successfully imported ToolValidator from submodule")
    except ImportError as e:
        print(f"❌ Failed to import ToolValidator: {e}")
        return False
    
    try:
        from core.enhanced_llm_agent import EnhancedLLMAgent
        print("✅ Successfully imported EnhancedLLMAgent from submodule")
    except ImportError as e:
        print(f"❌ Failed to import EnhancedLLMAgent: {e}")
        return False
    
    return True

def test_gui_wrapper():
    """Test that the GUI wrapper can access CLI modules."""
    print("\n🔍 Testing GUI Wrapper...")
    
    try:
        # Test CLI wrapper functionality directly
        cli_submodule_path = Path(__file__).parent / "cli_submodule"
        if cli_submodule_path.exists():
            sys.path.insert(0, str(cli_submodule_path))
        
        # Test that we can import from the CLI submodule
        from core.memory import AgentMemory
        from core.ai import LLMClient
        from core.planner import PlanGenerator
        
        print("✅ Successfully imported core modules from submodule")
        
        # Test that we can create instances
        memory = AgentMemory()
        print("✅ Successfully created AgentMemory instance")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import GUI wrapper: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing GUI wrapper: {e}")
        return False

def test_no_duplicate_files():
    """Test that there are no duplicate core directories."""
    print("\n🔍 Testing for Duplicate Files...")
    
    # Check for duplicate core directories (exclude numpy and other external packages)
    core_dirs = []
    for core_dir in Path(__file__).parent.rglob("core"):
        # Skip numpy and other external package core directories
        if "site-packages" in str(core_dir) or "numpy" in str(core_dir):
            continue
        core_dirs.append(core_dir)
    
    if len(core_dirs) == 1:
        print(f"✅ Only one project core directory found: {core_dirs[0]}")
    else:
        print(f"❌ Multiple project core directories found: {core_dirs}")
        return False
    
    # Check that the remaining core directory is in the submodule
    remaining_core = core_dirs[0]
    if "cli_submodule" in str(remaining_core):
        print("✅ Remaining core directory is in CLI submodule")
    else:
        print("❌ Remaining core directory is not in CLI submodule")
        return False
    
    return True

def test_main_entry_point():
    """Test that the main entry point can import from submodule."""
    print("\n🔍 Testing Main Entry Point...")
    
    try:
        # Test that main.py can import from submodule
        main_path = Path(__file__).parent / "main.py"
        if main_path.exists():
            print("✅ main.py file exists")
            
            # Read main.py to check imports
            with open(main_path, 'r') as f:
                content = f.read()
                if "cli_submodule" in content:
                    print("✅ main.py contains submodule path setup")
                else:
                    print("❌ main.py does not contain submodule path setup")
                    return False
        else:
            print("❌ main.py file not found")
            return False
    except Exception as e:
        print(f"❌ Error testing main entry point: {e}")
        return False
    
    return True

def main():
    """Run all submodule integration tests."""
    print("🚀 Starting CLI Submodule Integration Tests\n")
    
    tests = [
        ("Submodule Presence", test_submodule_presence),
        ("Git Submodule Config", test_git_submodule_config),
        ("Imports from Submodule", test_imports_from_submodule),
        ("GUI Wrapper", test_gui_wrapper),
        ("No Duplicate Files", test_no_duplicate_files),
        ("Main Entry Point", test_main_entry_point),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED\n")
            else:
                print(f"❌ {test_name}: FAILED\n")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! CLI submodule integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 