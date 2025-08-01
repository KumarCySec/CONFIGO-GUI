#!/usr/bin/env python3
"""
CONFIGO GUI - Test Script
==========================

Simple test script to verify the GUI application can be launched.
This script tests the basic functionality without requiring the full CONFIGO backend.

Author: CONFIGO Team
"""

import sys
import os
from pathlib import Path

# Add the configo_gui directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        # Test PySide6 imports
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        print("✅ PySide6 imports successful")
        
        # Test GUI components
        from ui.main_window import MainWindow
        from ui.welcome_screen import WelcomeScreen
        from ui.environment_setup import EnvironmentSetupScreen
        from ui.plan_renderer import PlanRendererScreen
        from ui.log_console import LogConsoleWidget
        from ui.portal_integration import PortalIntegrationWidget
        from ui.memory_view import MemoryViewWidget
        from ui.error_handler import ErrorHandlerWidget
        print("✅ GUI component imports successful")
        
        # Test backend wrapper
        from configo_core.gui_agent import ConfigoGUIAgent
        print("✅ Backend wrapper import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_gui_creation():
    """Test that the GUI can be created without errors."""
    try:
        from PySide6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
        # Check if QApplication already exists
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create main window
        window = MainWindow()
        
        # Test that window was created successfully
        assert window is not None
        print("✅ GUI creation successful")
        
        # Clean up
        window.deleteLater()
        
        return True
        
    except Exception as e:
        print(f"❌ GUI creation error: {e}")
        return False

def test_backend_wrapper():
    """Test that the backend wrapper can be created."""
    try:
        from configo_core.gui_agent import ConfigoGUIAgent
        
        # Create GUI agent
        agent = ConfigoGUIAgent()
        
        # Test basic functionality
        assert agent is not None
        print("✅ Backend wrapper creation successful")
        
        # Test memory info (should work even without backend)
        memory_info = agent.get_memory_info()
        assert isinstance(memory_info, dict)
        print("✅ Backend wrapper functionality test successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend wrapper error: {e}")
        return False

def test_sample_data():
    """Test that sample data can be loaded."""
    try:
        from ui.memory_view import MemoryViewWidget
        from PySide6.QtWidgets import QApplication
        
        # Check if QApplication already exists
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create memory view widget
        memory_widget = MemoryViewWidget()
        
        # Test that sample data was loaded
        assert memory_widget.history_list.count() > 0
        assert len(memory_widget.user_preferences) > 0
        assert len(memory_widget.tool_statistics) > 0
        print("✅ Sample data loading successful")
        
        # Clean up
        memory_widget.deleteLater()
        
        return True
        
    except Exception as e:
        print(f"❌ Sample data error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 CONFIGO GUI Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Tests", test_imports),
        ("GUI Creation Test", test_gui_creation),
        ("Backend Wrapper Test", test_backend_wrapper),
        ("Sample Data Test", test_sample_data),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The GUI application is ready to run.")
        print("\n🚀 To run the application:")
        print("   python configo_gui/main.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 