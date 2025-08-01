"""
CONFIGO GUI - Main Window
=========================

The main window component for CONFIGO GUI application.
Contains the primary UI layout with navigation and different screens.

Author: CONFIGO Team
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QLabel, QPushButton, QFrame,
    QSizePolicy, QSpacerItem, QScrollArea, QTextEdit,
    QLineEdit, QProgressBar, QGroupBox, QGridLayout,
    QListWidget, QListWidgetItem, QTabWidget, QSplitter,
    QMessageBox, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QThread
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor

# Import GUI components
from .welcome_screen import WelcomeScreen
from .environment_setup import EnvironmentSetupScreen
from .plan_renderer import PlanRendererScreen
from .log_console import LogConsoleWidget
from .portal_integration import PortalIntegrationWidget
from .memory_view import MemoryViewWidget
from .error_handler import ErrorHandlerWidget
from .ai_assistant import AIAssistantPanel
from .predictive_suggestions import PredictiveSuggestionsPanel
from .enhanced_terminal import EnhancedTerminalConsole

# Import backend wrapper
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from configo_gui.configo_core.gui_agent import ConfigoGUIAgent


class MainWindow(QMainWindow):
    """
    Main window for CONFIGO GUI application.
    
    Features:
    - Welcome screen with start button
    - Environment setup prompt
    - Visual plan renderer
    - Real-time log console
    - Portal integration
    - Memory management
    - Error handling with modals
    """
    
    # Signals for communication with backend
    environment_requested = Signal(str)  # Emitted when user requests environment setup
    plan_generated = Signal(list)  # Emitted when plan is generated
    installation_started = Signal()  # Emitted when installation begins
    installation_finished = Signal(bool, str)  # Emitted when installation completes (success, message)
    log_updated = Signal(str)  # Emitted when new log message is available
    error_occurred = Signal(str)  # Emitted when an error occurs
    
    def __init__(self):
        super().__init__()
        
        # Initialize backend agent
        self.gui_agent = ConfigoGUIAgent()
        
        # Setup UI
        self.setup_ui()
        self.setup_connections()
        self.setup_styling()
        
        # Show welcome screen
        self.show_welcome_screen()
    
    def setup_ui(self):
        """Initialize the main window UI components."""
        # Set window properties
        self.setWindowTitle("CONFIGO - AI Setup Agent")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar navigation
        self.setup_sidebar(main_layout)
        
        # Create main content area
        self.setup_main_content(main_layout)
        
        # Create stacked widget for different screens
        self.setup_stacked_widget()
    
    def setup_sidebar(self, main_layout):
        """Create the sidebar navigation."""
        # Sidebar container
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setMaximumWidth(250)
        sidebar.setMinimumWidth(200)
        sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        # Sidebar layout
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)
        
        # Logo and title
        logo_label = QLabel("CONFIGO")
        logo_label.setObjectName("logo-label")
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("🏠", "Welcome", "welcome"),
            ("🧠", "AI Suggestions", "suggestions"),
            ("🤖", "AI Assistant", "assistant"),
            ("⚙️", "Environment Setup", "setup"),
            ("📋", "Plan", "plan"),
            ("🖥️", "Enhanced Console", "console"),
            ("🌐", "Portals", "portals"),
            ("💾", "Memory", "memory"),
        ]
        
        for icon, text, screen_id in nav_items:
            btn = QPushButton(f"{icon} {text}")
            btn.setObjectName(f"nav-{screen_id}")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, sid=screen_id: self.navigate_to_screen(sid))
            self.nav_buttons[screen_id] = btn
            sidebar_layout.addWidget(btn)
        
        # Add spacer at bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        sidebar_layout.addItem(spacer)
        
        # Add sidebar to main layout
        main_layout.addWidget(sidebar)
    
    def setup_main_content(self, main_layout):
        """Create the main content area."""
        # Main content container
        self.content_frame = QFrame()
        self.content_frame.setObjectName("content-frame")
        self.content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Content layout
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)
        
        # Add content frame to main layout
        main_layout.addWidget(self.content_frame)
    
    def setup_stacked_widget(self):
        """Create the stacked widget for different screens."""
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # Create different screens
        self.screens = {}
        
        # Welcome screen
        self.screens["welcome"] = WelcomeScreen()
        self.screens["welcome"].start_clicked.connect(self.on_start_clicked)
        self.stacked_widget.addWidget(self.screens["welcome"])
        
        # Environment setup screen
        self.screens["setup"] = EnvironmentSetupScreen()
        self.screens["setup"].environment_requested.connect(self.on_environment_requested)
        self.stacked_widget.addWidget(self.screens["setup"])
        
        # Plan renderer screen
        self.screens["plan"] = PlanRendererScreen()
        self.stacked_widget.addWidget(self.screens["plan"])
        
        # AI Suggestions screen
        self.screens["suggestions"] = PredictiveSuggestionsPanel()
        self.screens["suggestions"].tool_selected.connect(self.on_tool_selected)
        self.screens["suggestions"].profile_updated.connect(self.on_profile_updated)
        self.stacked_widget.addWidget(self.screens["suggestions"])
        
        # AI Assistant screen
        self.screens["assistant"] = AIAssistantPanel()
        self.screens["assistant"].message_sent.connect(self.on_ai_message_sent)
        self.stacked_widget.addWidget(self.screens["assistant"])
        
        # Enhanced console screen
        self.screens["console"] = EnhancedTerminalConsole()
        self.screens["console"].step_completed.connect(self.on_step_completed)
        self.screens["console"].command_executed.connect(self.on_command_executed)
        self.stacked_widget.addWidget(self.screens["console"])
        
        # Portal integration screen
        self.screens["portals"] = PortalIntegrationWidget()
        self.stacked_widget.addWidget(self.screens["portals"])
        
        # Memory view screen
        self.screens["memory"] = MemoryViewWidget()
        self.stacked_widget.addWidget(self.screens["memory"])
    
    def setup_connections(self):
        """Setup signal connections between components."""
        # Connect backend signals to UI updates
        self.gui_agent.plan_generated.connect(self.on_plan_generated)
        self.gui_agent.installation_progress.connect(self.on_installation_progress)
        self.gui_agent.installation_finished.connect(self.on_installation_finished)
        self.gui_agent.log_message.connect(self.on_log_message)
        self.gui_agent.error_occurred.connect(self.on_error_occurred)
        
        # Connect UI signals to backend
        self.environment_requested.connect(self.gui_agent.setup_environment)
        self.installation_started.connect(self.gui_agent.start_installation)
    
    def setup_styling(self):
        """Apply custom styling to the main window."""
        # Set stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            
            #sidebar {
                background-color: #1e1e1e;
                border-right: 1px solid #404040;
            }
            
            #content-frame {
                background-color: #2b2b2b;
            }
            
            #logo-label {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
            }
            
            QPushButton {
                background-color: #404040;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                color: #ffffff;
                font-size: 14px;
                text-align: left;
            }
            
            QPushButton:hover {
                background-color: #505050;
            }
            
            QPushButton:checked {
                background-color: #0066cc;
            }
            
            QPushButton:pressed {
                background-color: #0052a3;
            }
        """)
    
    def navigate_to_screen(self, screen_id: str):
        """Navigate to a specific screen."""
        if screen_id in self.screens:
            # Update navigation buttons
            for btn_id, btn in self.nav_buttons.items():
                btn.setChecked(btn_id == screen_id)
            
            # Switch to screen
            self.stacked_widget.setCurrentWidget(self.screens[screen_id])
    
    def show_welcome_screen(self):
        """Show the welcome screen."""
        self.navigate_to_screen("welcome")
    
    def on_start_clicked(self):
        """Handle start button click from welcome screen."""
        self.navigate_to_screen("setup")
    
    def on_environment_requested(self, environment: str):
        """Handle environment setup request."""
        # Switch to plan screen
        self.navigate_to_screen("plan")
        
        # Request plan from backend
        self.environment_requested.emit(environment)
    
    def on_plan_generated(self, plan: list):
        """Handle plan generation from backend."""
        # Update plan renderer
        self.screens["plan"].update_plan(plan)
        
        # Switch to plan screen
        self.navigate_to_screen("plan")
    
    def on_installation_progress(self, step: int, total: int, message: str):
        """Handle installation progress updates."""
        # Update plan renderer progress
        self.screens["plan"].update_progress(step, total, message)
        
        # Add log message
        self.screens["console"].add_log_message(message)
    
    def on_installation_finished(self, success: bool, message: str):
        """Handle installation completion."""
        if success:
            # Show success message
            QMessageBox.information(self, "Installation Complete", message)
        else:
            # Show error message
            QMessageBox.critical(self, "Installation Failed", message)
    
    def on_log_message(self, message: str):
        """Handle log message from backend."""
        self.screens["console"].add_log_message(message)
    
    def on_error_occurred(self, error_message: str):
        """Handle error from backend."""
        # Show error modal
        QMessageBox.critical(self, "Error", error_message)
        
        # Add to enhanced console
        if "console" in self.screens:
            self.screens["console"].add_terminal_output(f"ERROR: {error_message}")
    
    def on_tool_selected(self, tool_info: dict):
        """Handle tool selection from AI suggestions."""
        # Add to installation plan
        self.gui_agent.add_tool_to_plan(tool_info)
        
        # Show in console
        if "console" in self.screens:
            self.screens["console"].add_terminal_output(f"Selected tool: {tool_info['name']}")
    
    def on_profile_updated(self, profile: dict):
        """Handle user profile updates."""
        # Update backend with new profile
        self.gui_agent.update_user_profile(profile)
        
        # Show in console
        if "console" in self.screens:
            self.screens["console"].add_terminal_output("User profile updated")
    
    def on_ai_message_sent(self, message: str):
        """Handle AI assistant messages."""
        # Process message with backend
        response = self.gui_agent.chat_with_agent(message)
        
        # Send response back to assistant
        if "assistant" in self.screens:
            self.screens["assistant"].receive_ai_response(response)
    
    def on_step_completed(self, step_name: str, success: bool):
        """Handle step completion."""
        # Update backend
        self.gui_agent.update_step_status(step_name, success)
        
        # Show in console
        if "console" in self.screens:
            status = "completed" if success else "failed"
            self.screens["console"].add_terminal_output(f"Step '{step_name}' {status}")
    
    def on_command_executed(self, command: str, exit_code: int):
        """Handle command execution."""
        # Update backend
        self.gui_agent.log_command(command, exit_code)
        
        # Show in console
        if "console" in self.screens:
            status = "succeeded" if exit_code == 0 else "failed"
            self.screens["console"].add_terminal_output(f"Command {status} (exit code: {exit_code})")
    
    def closeEvent(self, event):
        """Handle application close event."""
        # Cleanup backend agent
        if hasattr(self, 'gui_agent'):
            self.gui_agent.cleanup()
        
        event.accept() 