#!/usr/bin/env python3
"""
CONFIGO GUI - Enhanced Features Demo
====================================

Demo script to showcase the enhanced CONFIGO GUI features:
- AI Assistant Panel
- Predictive AI Suggestions
- Enhanced Terminal Console
- Main Window Integration

Author: CONFIGO Team
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont

# Import GUI components
from configo_gui.ui.ai_assistant import AIAssistantPanel
from configo_gui.ui.predictive_suggestions import PredictiveSuggestionsPanel
from configo_gui.ui.enhanced_terminal import EnhancedTerminalConsole
from configo_gui.ui.main_window import MainWindow


class EnhancedGUIDemo(QMainWindow):
    """Demo window to showcase enhanced CONFIGO GUI features."""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_styling()
        
    def setup_ui(self):
        """Setup the demo UI."""
        self.setWindowTitle("CONFIGO GUI - Enhanced Features Demo")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("🚀 CONFIGO GUI - Enhanced Features Demo")
        header.setObjectName("demo-header")
        layout.addWidget(header)
        
        # Description
        desc = QLabel("This demo showcases the enhanced CONFIGO GUI features including AI Assistant, Predictive Suggestions, and Enhanced Terminal.")
        desc.setObjectName("demo-description")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Demo buttons
        self.setup_demo_buttons(layout)
        
        # Status
        self.status_label = QLabel("Ready to demo enhanced features!")
        self.status_label.setObjectName("status-label")
        layout.addWidget(self.status_label)
    
    def setup_demo_buttons(self, layout):
        """Setup demo buttons."""
        buttons_layout = QHBoxLayout()
        
        # AI Assistant Demo
        ai_button = QPushButton("🤖 AI Assistant Demo")
        ai_button.setObjectName("demo-button")
        ai_button.clicked.connect(self.demo_ai_assistant)
        buttons_layout.addWidget(ai_button)
        
        # Predictive Suggestions Demo
        suggestions_button = QPushButton("🧠 AI Suggestions Demo")
        suggestions_button.setObjectName("demo-button")
        suggestions_button.clicked.connect(self.demo_predictive_suggestions)
        buttons_layout.addWidget(suggestions_button)
        
        # Enhanced Terminal Demo
        terminal_button = QPushButton("🖥️ Enhanced Terminal Demo")
        terminal_button.setObjectName("demo-button")
        terminal_button.clicked.connect(self.demo_enhanced_terminal)
        buttons_layout.addWidget(terminal_button)
        
        # Full Application Demo
        full_button = QPushButton("🎯 Full Application Demo")
        full_button.setObjectName("demo-button-primary")
        full_button.clicked.connect(self.demo_full_application)
        buttons_layout.addWidget(full_button)
        
        layout.addLayout(buttons_layout)
    
    def setup_styling(self):
        """Apply styling to the demo window."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            
            #demo-header {
                font-size: 24px;
                font-weight: bold;
                color: #ffffff;
                margin: 20px;
                text-align: center;
            }
            
            #demo-description {
                font-size: 16px;
                color: #cccccc;
                margin: 20px;
                line-height: 1.5;
            }
            
            #demo-button {
                background-color: #2c2c2c;
                border: 2px solid #0066cc;
                border-radius: 10px;
                color: #ffffff;
                padding: 15px 20px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
            }
            
            #demo-button:hover {
                background-color: #0066cc;
                transform: scale(1.05);
            }
            
            #demo-button-primary {
                background-color: #0066cc;
                border: 2px solid #0077ee;
                border-radius: 10px;
                color: #ffffff;
                padding: 15px 20px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
            }
            
            #demo-button-primary:hover {
                background-color: #0077ee;
                transform: scale(1.05);
            }
            
            #status-label {
                font-size: 14px;
                color: #4CAF50;
                margin: 20px;
                text-align: center;
            }
        """)
    
    def demo_ai_assistant(self):
        """Demo the AI Assistant Panel."""
        self.status_label.setText("Opening AI Assistant Panel...")
        
        # Create AI Assistant window
        self.ai_window = QMainWindow()
        self.ai_window.setWindowTitle("🤖 AI Assistant Panel Demo")
        self.ai_window.setMinimumSize(800, 600)
        
        # Add AI Assistant to window
        assistant = AIAssistantPanel()
        self.ai_window.setCentralWidget(assistant)
        
        # Show window
        self.ai_window.show()
        
        # Update status
        QTimer.singleShot(1000, lambda: self.status_label.setText("AI Assistant Panel opened! Try chatting with the AI."))
    
    def demo_predictive_suggestions(self):
        """Demo the Predictive AI Suggestions Panel."""
        self.status_label.setText("Opening Predictive AI Suggestions Panel...")
        
        # Create Predictive Suggestions window
        self.suggestions_window = QMainWindow()
        self.suggestions_window.setWindowTitle("🧠 Predictive AI Suggestions Demo")
        self.suggestions_window.setMinimumSize(1000, 700)
        
        # Add Predictive Suggestions to window
        suggestions = PredictiveSuggestionsPanel()
        self.suggestions_window.setCentralWidget(suggestions)
        
        # Show window
        self.suggestions_window.show()
        
        # Update status
        QTimer.singleShot(1000, lambda: self.status_label.setText("Predictive AI Suggestions Panel opened! Check out the tool recommendations."))
    
    def demo_enhanced_terminal(self):
        """Demo the Enhanced Terminal Console."""
        self.status_label.setText("Opening Enhanced Terminal Console...")
        
        # Create Enhanced Terminal window
        self.terminal_window = QMainWindow()
        self.terminal_window.setWindowTitle("🖥️ Enhanced Terminal Console Demo")
        self.terminal_window.setMinimumSize(1200, 800)
        
        # Add Enhanced Terminal to window
        terminal = EnhancedTerminalConsole()
        self.terminal_window.setCentralWidget(terminal)
        
        # Add some demo content
        terminal.add_terminal_output("Welcome to CONFIGO Enhanced Terminal Console!")
        terminal.add_terminal_output("This is a demo of the enhanced terminal features.")
        terminal.add_terminal_output("✅ Success message example")
        terminal.add_terminal_output("❌ Error message example")
        terminal.add_terminal_output("⚠️ Warning message example")
        terminal.add_terminal_output("ℹ️ Info message example")
        
        # Add a timeline step
        terminal.add_timeline_step({
            "name": "Demo Installation",
            "description": "This is a demo installation step",
            "status": "installing"
        })
        
        # Show window
        self.terminal_window.show()
        
        # Update status
        QTimer.singleShot(1000, lambda: self.status_label.setText("Enhanced Terminal Console opened! Check out the dual-pane layout."))
    
    def demo_full_application(self):
        """Demo the full CONFIGO GUI application."""
        self.status_label.setText("Opening full CONFIGO GUI application...")
        
        # Create full application window
        self.full_app_window = MainWindow()
        self.full_app_window.setWindowTitle("🎯 CONFIGO GUI - Full Application Demo")
        
        # Show window
        self.full_app_window.show()
        
        # Update status
        QTimer.singleShot(1000, lambda: self.status_label.setText("Full CONFIGO GUI application opened! Navigate through all features."))


def main():
    """Run the enhanced GUI demo."""
    app = QApplication(sys.argv)
    
    # Create and show demo window
    demo = EnhancedGUIDemo()
    demo.show()
    
    print("🚀 CONFIGO GUI Enhanced Features Demo")
    print("=" * 50)
    print("This demo showcases the enhanced CONFIGO GUI features:")
    print("• 🤖 AI Assistant Panel - Interactive chatbot")
    print("• 🧠 Predictive AI Suggestions - Smart tool recommendations")
    print("• 🖥️ Enhanced Terminal Console - Dual-pane terminal")
    print("• 🎯 Full Application - Complete CONFIGO GUI")
    print("=" * 50)
    print("Click the demo buttons to explore each feature!")
    
    # Start application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 