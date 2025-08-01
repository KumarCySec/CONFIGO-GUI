#!/usr/bin/env python3
"""
CONFIGO GUI - Enhanced Components Test Suite
============================================

Test suite for the enhanced CONFIGO GUI components:
- AI Assistant Panel
- Predictive AI Suggestions
- Enhanced Terminal Console
- Main Window Integration

Author: CONFIGO Team
"""

import sys
import os
import unittest
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Import GUI components
from configo_gui.ui.ai_assistant import AIAssistantPanel, ChatMessage
from configo_gui.ui.predictive_suggestions import PredictiveSuggestionsPanel, ToolCard
from configo_gui.ui.enhanced_terminal import EnhancedTerminalConsole, TimelineStep
from configo_gui.ui.main_window import MainWindow


class TestAIAssistant(unittest.TestCase):
    """Test AI Assistant Panel functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        self.assistant = AIAssistantPanel()
    
    def test_assistant_creation(self):
        """Test that AI Assistant Panel can be created."""
        self.assertIsNotNone(self.assistant)
        self.assertEqual(self.assistant.chat_history[0]["role"], "assistant")
    
    def test_message_sending(self):
        """Test sending messages to the assistant."""
        initial_count = len(self.assistant.chat_history)
        
        # Simulate sending a message
        self.assistant.add_user_message("Hello, can you help me setup Python?")
        
        self.assertEqual(len(self.assistant.chat_history), initial_count + 1)
        self.assertEqual(self.assistant.chat_history[-1]["role"], "user")
    
    def test_ai_response(self):
        """Test receiving AI responses."""
        initial_count = len(self.assistant.chat_history)
        
        # Simulate AI response
        self.assistant.add_ai_message("I'd be happy to help you setup Python!")
        
        self.assertEqual(len(self.assistant.chat_history), initial_count + 1)
        self.assertEqual(self.assistant.chat_history[-1]["role"], "assistant")
    
    def test_suggestions(self):
        """Test quick suggestion buttons."""
        initial_count = len(self.assistant.chat_history)
        
        # Simulate clicking a suggestion
        self.assistant.send_suggestion("Setup Python environment")
        
        self.assertEqual(len(self.assistant.chat_history), initial_count + 1)
        self.assertEqual(self.assistant.chat_history[-1]["content"], "Setup Python environment")


class TestPredictiveSuggestions(unittest.TestCase):
    """Test Predictive AI Suggestions functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        self.suggestions = PredictiveSuggestionsPanel()
    
    def test_suggestions_creation(self):
        """Test that Predictive Suggestions Panel can be created."""
        self.assertIsNotNone(self.suggestions)
        self.assertIsInstance(self.suggestions.system_info, dict)
    
    def test_system_info_loading(self):
        """Test system information loading."""
        system_info = self.suggestions.get_system_info()
        self.assertIsInstance(system_info, dict)
        self.assertIn("os", system_info)
    
    def test_profile_updates(self):
        """Test user profile updates."""
        # Simulate profile update
        test_profile = {
            "What type of developer are you?": "Python Developer",
            "What programming languages do you use?": "Python, JavaScript"
        }
        
        self.suggestions.user_profile = test_profile
        self.suggestions.update_profile()
        
        self.assertEqual(self.suggestions.get_user_profile(), test_profile)
    
    def test_recommendations_generation(self):
        """Test tool recommendations generation."""
        # Set up a test profile
        self.suggestions.user_profile = {
            "What programming languages do you use?": "Python"
        }
        
        # Generate recommendations
        recommendations = self.suggestions.analyze_and_recommend()
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Check that recommendations have required fields
        for rec in recommendations:
            self.assertIn("name", rec)
            self.assertIn("description", rec)
            self.assertIn("confidence", rec)


class TestEnhancedTerminal(unittest.TestCase):
    """Test Enhanced Terminal Console functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        self.terminal = EnhancedTerminalConsole()
    
    def test_terminal_creation(self):
        """Test that Enhanced Terminal Console can be created."""
        self.assertIsNotNone(self.terminal)
        self.assertIsInstance(self.terminal.timeline_steps, list)
        self.assertIsInstance(self.terminal.command_history, list)
    
    def test_timeline_step_creation(self):
        """Test timeline step creation."""
        step_info = {
            "name": "Install Python",
            "description": "Installing Python 3.9",
            "status": "pending"
        }
        
        step = TimelineStep(step_info)
        self.assertIsNotNone(step)
        self.assertEqual(step.step_info["name"], "Install Python")
    
    def test_terminal_output(self):
        """Test adding output to terminal."""
        initial_text = self.terminal.terminal_output.toPlainText()
        
        # Add some output
        self.terminal.add_terminal_output("Test message")
        
        new_text = self.terminal.terminal_output.toPlainText()
        self.assertIn("Test message", new_text)
    
    def test_command_history(self):
        """Test command history tracking."""
        initial_count = len(self.terminal.command_history)
        
        # Simulate command execution
        self.terminal.command_input.setText("ls -la")
        self.terminal.execute_command()
        
        self.assertEqual(len(self.terminal.command_history), initial_count + 1)
        self.assertIn("ls -la", self.terminal.command_history)


class TestMainWindowIntegration(unittest.TestCase):
    """Test Main Window integration with new components."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        self.window = MainWindow()
    
    def test_window_creation(self):
        """Test that Main Window can be created with new components."""
        self.assertIsNotNone(self.window)
        self.assertIn("suggestions", self.window.screens)
        self.assertIn("assistant", self.window.screens)
        self.assertIn("console", self.window.screens)
    
    def test_navigation(self):
        """Test navigation to new screens."""
        # Test navigation to AI Suggestions
        self.window.navigate_to_screen("suggestions")
        current_widget = self.window.stacked_widget.currentWidget()
        self.assertEqual(current_widget, self.window.screens["suggestions"])
        
        # Test navigation to AI Assistant
        self.window.navigate_to_screen("assistant")
        current_widget = self.window.stacked_widget.currentWidget()
        self.assertEqual(current_widget, self.window.screens["assistant"])
        
        # Test navigation to Enhanced Console
        self.window.navigate_to_screen("console")
        current_widget = self.window.stacked_widget.currentWidget()
        self.assertEqual(current_widget, self.window.screens["console"])
    
    def test_signal_connections(self):
        """Test that signal connections are properly set up."""
        # Test tool selection signal
        tool_info = {"name": "Docker", "description": "Container platform"}
        self.window.on_tool_selected(tool_info)
        
        # Test profile update signal
        profile = {"developer_type": "Python Developer"}
        self.window.on_profile_updated(profile)
        
        # Test AI message signal
        self.window.on_ai_message_sent("Help me setup Python")
        
        # Test step completion signal
        self.window.on_step_completed("Install Python", True)
        
        # Test command execution signal
        self.window.on_command_executed("python --version", 0)


class TestGUIAgent(unittest.TestCase):
    """Test GUI Agent with new methods."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        from configo_gui.configo_core.gui_agent import ConfigoGUIAgent
        self.agent = ConfigoGUIAgent()
    
    def test_agent_creation(self):
        """Test that GUI Agent can be created."""
        self.assertIsNotNone(self.agent)
    
    def test_add_tool_to_plan(self):
        """Test adding tools to installation plan."""
        tool_info = {
            "name": "Docker",
            "description": "Container platform",
            "install_command": "sudo apt install docker.io",
            "check_command": "docker --version"
        }
        
        self.agent.add_tool_to_plan(tool_info)
        
        # Check that plan was created
        self.assertTrue(hasattr(self.agent, 'installation_plan'))
        self.assertGreater(len(self.agent.installation_plan), 0)
    
    def test_update_user_profile(self):
        """Test updating user profile."""
        profile = {
            "developer_type": "Python Developer",
            "languages": "Python, JavaScript"
        }
        
        self.agent.update_user_profile(profile)
    
    def test_update_step_status(self):
        """Test updating step status."""
        # First add a step
        tool_info = {"name": "Python", "description": "Python interpreter"}
        self.agent.add_tool_to_plan(tool_info)
        
        # Then update its status
        self.agent.update_step_status("Python", True)
    
    def test_log_command(self):
        """Test logging commands."""
        self.agent.log_command("python --version", 0)
        self.agent.log_command("invalid_command", 1)


def run_tests():
    """Run all tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestAIAssistant))
    test_suite.addTest(unittest.makeSuite(TestPredictiveSuggestions))
    test_suite.addTest(unittest.makeSuite(TestEnhancedTerminal))
    test_suite.addTest(unittest.makeSuite(TestMainWindowIntegration))
    test_suite.addTest(unittest.makeSuite(TestGUIAgent))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print("ENHANCED GUI TEST RESULTS")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 