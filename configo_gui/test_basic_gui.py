#!/usr/bin/env python3
"""
CONFIGO GUI - Basic Test Suite
==============================

Simple test suite to verify basic GUI functionality.
Tests component creation and basic functionality without complex threading.

Author: CONFIGO Team
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer


def test_imports():
    """Test that all components can be imported."""
    print("Testing imports...")
    
    try:
        from configo_gui.ui.ai_assistant import AIAssistantPanel
        print("✅ AI Assistant Panel imported successfully")
    except Exception as e:
        print(f"❌ AI Assistant Panel import failed: {e}")
        return False
    
    try:
        from configo_gui.ui.predictive_suggestions import PredictiveSuggestionsPanel
        print("✅ Predictive Suggestions Panel imported successfully")
    except Exception as e:
        print(f"❌ Predictive Suggestions Panel import failed: {e}")
        return False
    
    try:
        from configo_gui.ui.enhanced_terminal import EnhancedTerminalConsole
        print("✅ Enhanced Terminal Console imported successfully")
    except Exception as e:
        print(f"❌ Enhanced Terminal Console import failed: {e}")
        return False
    
    try:
        from configo_gui.ui.main_window import MainWindow
        print("✅ Main Window imported successfully")
    except Exception as e:
        print(f"❌ Main Window import failed: {e}")
        return False
    
    try:
        from configo_gui.configo_core.gui_agent import ConfigoGUIAgent
        print("✅ GUI Agent imported successfully")
    except Exception as e:
        print(f"❌ GUI Agent import failed: {e}")
        return False
    
    return True


def test_component_creation():
    """Test that components can be created."""
    print("\nTesting component creation...")
    
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    try:
        from configo_gui.ui.ai_assistant import AIAssistantPanel
        assistant = AIAssistantPanel()
        print("✅ AI Assistant Panel created successfully")
    except Exception as e:
        print(f"❌ AI Assistant Panel creation failed: {e}")
        return False
    
    try:
        from configo_gui.ui.predictive_suggestions import PredictiveSuggestionsPanel
        suggestions = PredictiveSuggestionsPanel()
        print("✅ Predictive Suggestions Panel created successfully")
    except Exception as e:
        print(f"❌ Predictive Suggestions Panel creation failed: {e}")
        return False
    
    try:
        from configo_gui.ui.enhanced_terminal import EnhancedTerminalConsole
        terminal = EnhancedTerminalConsole()
        print("✅ Enhanced Terminal Console created successfully")
    except Exception as e:
        print(f"❌ Enhanced Terminal Console creation failed: {e}")
        return False
    
    try:
        from configo_gui.ui.main_window import MainWindow
        window = MainWindow()
        print("✅ Main Window created successfully")
    except Exception as e:
        print(f"❌ Main Window creation failed: {e}")
        return False
    
    try:
        from configo_gui.configo_core.gui_agent import ConfigoGUIAgent
        agent = ConfigoGUIAgent()
        print("✅ GUI Agent created successfully")
    except Exception as e:
        print(f"❌ GUI Agent creation failed: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality of components."""
    print("\nTesting basic functionality...")
    
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    try:
        from configo_gui.ui.ai_assistant import AIAssistantPanel
        assistant = AIAssistantPanel()
        
        # Test adding messages
        assistant.add_user_message("Test message")
        assistant.add_ai_message("Test response")
        
        # Check chat history
        if len(assistant.chat_history) >= 3:  # Welcome message + 2 test messages
            print("✅ AI Assistant basic functionality works")
        else:
            print("❌ AI Assistant basic functionality failed")
            return False
    except Exception as e:
        print(f"❌ AI Assistant functionality test failed: {e}")
        return False
    
    try:
        from configo_gui.ui.predictive_suggestions import PredictiveSuggestionsPanel
        suggestions = PredictiveSuggestionsPanel()
        
        # Test system info
        system_info = suggestions.get_system_info()
        if isinstance(system_info, dict):
            print("✅ Predictive Suggestions basic functionality works")
        else:
            print("❌ Predictive Suggestions basic functionality failed")
            return False
    except Exception as e:
        print(f"❌ Predictive Suggestions functionality test failed: {e}")
        return False
    
    try:
        from configo_gui.ui.enhanced_terminal import EnhancedTerminalConsole
        terminal = EnhancedTerminalConsole()
        
        # Test terminal output
        terminal.add_terminal_output("Test terminal message")
        
        # Check command history
        if isinstance(terminal.command_history, list):
            print("✅ Enhanced Terminal basic functionality works")
        else:
            print("❌ Enhanced Terminal basic functionality failed")
            return False
    except Exception as e:
        print(f"❌ Enhanced Terminal functionality test failed: {e}")
        return False
    
    try:
        from configo_gui.configo_core.gui_agent import ConfigoGUIAgent
        agent = ConfigoGUIAgent()
        
        # Test adding tool to plan
        tool_info = {"name": "Test Tool", "description": "Test Description"}
        agent.add_tool_to_plan(tool_info)
        
        print("✅ GUI Agent basic functionality works")
    except Exception as e:
        print(f"❌ GUI Agent functionality test failed: {e}")
        return False
    
    return True


def test_navigation():
    """Test main window navigation."""
    print("\nTesting navigation...")
    
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    try:
        from configo_gui.ui.main_window import MainWindow
        window = MainWindow()
        
        # Test navigation to different screens
        screens_to_test = ["welcome", "suggestions", "assistant", "console"]
        
        for screen in screens_to_test:
            if screen in window.screens:
                window.navigate_to_screen(screen)
                current_widget = window.stacked_widget.currentWidget()
                if current_widget == window.screens[screen]:
                    print(f"✅ Navigation to {screen} works")
                else:
                    print(f"❌ Navigation to {screen} failed")
                    return False
            else:
                print(f"❌ Screen {screen} not found")
                return False
        
        print("✅ All navigation tests passed")
        return True
    except Exception as e:
        print(f"❌ Navigation test failed: {e}")
        return False


def main():
    """Run all basic tests."""
    print("CONFIGO GUI - Basic Test Suite")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return False
    
    # Test component creation
    if not test_component_creation():
        print("\n❌ Component creation tests failed!")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed!")
        return False
    
    # Test navigation
    if not test_navigation():
        print("\n❌ Navigation tests failed!")
        return False
    
    print("\n" + "=" * 40)
    print("✅ ALL BASIC TESTS PASSED!")
    print("=" * 40)
    
    print("\n🎉 CONFIGO GUI is ready to use!")
    print("\nTo run the application:")
    print("  python configo_gui/main.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 