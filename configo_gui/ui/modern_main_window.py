"""
CONFIGO GUI - Modern Main Window
================================

Enhanced main window with modern glassmorphism design, smooth animations,
and advanced UI components. Provides a premium desktop application experience.

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
    QMessageBox, QDialog, QDialogButtonBox, QStatusBar,
    QGraphicsDropShadowEffect, QGraphicsBlurEffect
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QThread, QPoint
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QPainter, QLinearGradient

# Import modern UI components
from .themes.glass_theme import GlassTheme
from .themes.animations import AnimationManager
from .themes.modern_styles import ModernStyles
from .components.glass_card import GlassCard
from .components.animated_button import AnimatedButton

# Import existing GUI components
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
try:
    from configo_gui.configo_core.gui_agent import ConfigoGUIAgent
except ImportError:
    # Create a mock agent for demo purposes
    class ConfigoGUIAgent:
        def __init__(self):
            self.environment_requested = Signal(str)
            self.plan_generated = Signal(list)
            self.installation_started = Signal()
            self.installation_finished = Signal(bool, str)
            self.log_updated = Signal(str)
            self.error_occurred = Signal(str)
        
        def setup_environment(self, environment):
            pass
        
        def cleanup(self):
            pass


class ModernMainWindow(QMainWindow):
    """
    Modern main window for CONFIGO GUI application with glassmorphism design.
    
    Features:
    - Glass-like transparent panels with blur effects
    - Smooth animations and transitions
    - Modern color scheme and typography
    - Responsive layout with sidebar navigation
    - Enhanced user experience with hover effects
    - Real-time status updates and notifications
    """
    
    # Signals for communication with backend
    environment_requested = Signal(str)
    plan_generated = Signal(list)
    installation_started = Signal()
    installation_finished = Signal(bool, str)
    log_updated = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        # Initialize theme and styling
        self.theme = GlassTheme()
        self.animation_manager = AnimationManager()
        self.modern_styles = ModernStyles(self.theme)
        
        # Initialize backend agent
        self.gui_agent = ConfigoGUIAgent()
        
        # Setup UI
        self.setup_ui()
        self.setup_connections()
        self.setup_animations()
        self.apply_modern_styling()
        
        # Show welcome screen with animation
        self.show_welcome_screen()
    
    def setup_ui(self):
        """Initialize the modern main window UI components."""
        # Set window properties
        self.setWindowTitle("CONFIGO - AI Setup Agent")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Enable window transparency for glass effect
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
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
        
        # Create status bar
        self.setup_status_bar()
    
    def setup_sidebar(self, main_layout):
        """Setup modern sidebar navigation."""
        # Create sidebar container
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(280)
        self.sidebar.setStyleSheet(self.modern_styles.get_sidebar_style())
        
        # Apply glass effect to sidebar
        self.theme.apply_glass_effect_to_widget(self.sidebar)
        
        # Create sidebar layout
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(8)
        
        # Logo and title
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(12)
        
        # Logo icon (placeholder)
        logo_label = QLabel("🧠")
        logo_label.setFont(QFont("Arial", 24))
        logo_layout.addWidget(logo_label)
        
        title_label = QLabel("CONFIGO")
        title_label.setFont(self.theme.fonts['heading_small'])
        title_label.setStyleSheet(f"color: {self.theme.colors['text_primary'].name()};")
        logo_layout.addWidget(title_label)
        
        sidebar_layout.addLayout(logo_layout)
        sidebar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠", "Welcome", "welcome"),
            ("⚙️", "Environment", "environment"),
            ("📋", "Plan", "plan"),
            ("🖥️", "Console", "console"),
            ("🌐", "Portals", "portals"),
            ("💾", "Memory", "memory"),
            ("🤖", "AI Assistant", "ai_assistant"),
            ("🔮", "Predictions", "predictions"),
            ("⚡", "Terminal", "terminal")
        ]
        
        for icon, text, screen_id in nav_items:
            button = AnimatedButton(f"{icon} {text}", variant="ghost", theme=self.theme)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, sid=screen_id: self.navigate_to_screen(sid))
            self.nav_buttons[screen_id] = button
            sidebar_layout.addWidget(button)
        
        # Set welcome as active
        self.nav_buttons["welcome"].setChecked(True)
        
        sidebar_layout.addStretch()
        
        # Add sidebar to main layout
        main_layout.addWidget(self.sidebar)
    
    def setup_main_content(self, main_layout):
        """Setup main content area with glass effect."""
        # Create main content container
        self.content_container = QFrame()
        self.content_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                margin: 16px;
            }
        """)
        
        # Apply glass effect
        self.theme.apply_glass_effect_to_widget(self.content_container)
        
        # Create content layout
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(0)
        
        # Create stacked widget for screens
        self.setup_stacked_widget(content_layout)
        
        # Add content container to main layout
        main_layout.addWidget(self.content_container)
    
    def setup_stacked_widget(self, content_layout):
        """Setup stacked widget for different screens."""
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background: transparent;
            }
        """)
        
        # Create screens
        self.screens = {}
        
        # Welcome screen
        self.screens["welcome"] = WelcomeScreen()
        self.stacked_widget.addWidget(self.screens["welcome"])
        
        # Environment setup screen
        self.screens["environment"] = EnvironmentSetupScreen()
        self.stacked_widget.addWidget(self.screens["environment"])
        
        # Plan renderer screen
        self.screens["plan"] = PlanRendererScreen()
        self.stacked_widget.addWidget(self.screens["plan"])
        
        # Log console screen
        self.screens["console"] = LogConsoleWidget()
        self.stacked_widget.addWidget(self.screens["console"])
        
        # Portal integration screen
        self.screens["portals"] = PortalIntegrationWidget()
        self.stacked_widget.addWidget(self.screens["portals"])
        
        # Memory view screen
        self.screens["memory"] = MemoryViewWidget()
        self.stacked_widget.addWidget(self.screens["memory"])
        
        # AI Assistant screen
        self.screens["ai_assistant"] = AIAssistantPanel()
        self.stacked_widget.addWidget(self.screens["ai_assistant"])
        
        # Predictive suggestions screen
        self.screens["predictions"] = PredictiveSuggestionsPanel()
        self.stacked_widget.addWidget(self.screens["predictions"])
        
        # Enhanced terminal screen
        self.screens["terminal"] = EnhancedTerminalConsole()
        self.stacked_widget.addWidget(self.screens["terminal"])
        
        content_layout.addWidget(self.stacked_widget)
    
    def setup_status_bar(self):
        """Setup modern status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(self.modern_styles.get_status_bar_style())
        
        # Status indicators
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(self.modern_styles.get_progress_bar_style())
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def setup_connections(self):
        """Setup signal connections."""
        # Connect backend signals
        self.gui_agent.environment_requested.connect(self.on_environment_requested)
        self.gui_agent.plan_generated.connect(self.on_plan_generated)
        self.gui_agent.installation_started.connect(self.on_installation_started)
        self.gui_agent.installation_finished.connect(self.on_installation_finished)
        self.gui_agent.log_updated.connect(self.on_log_message)
        self.gui_agent.error_occurred.connect(self.on_error_occurred)
        
        # Connect screen signals
        for screen_id, screen in self.screens.items():
            if hasattr(screen, 'environment_requested'):
                screen.environment_requested.connect(self.on_environment_requested)
            if hasattr(screen, 'plan_generated'):
                screen.plan_generated.connect(self.on_plan_generated)
    
    def setup_animations(self):
        """Setup window animations."""
        # Window fade-in animation
        self.fade_in_animation = self.animation_manager.create_fade_animation(
            self, start_opacity=0.0, end_opacity=1.0, duration=500
        )
        self.fade_in_animation.start()
    
    def apply_modern_styling(self):
        """Apply complete modern styling to the window."""
        # Apply theme to application
        self.theme.apply_theme_to_app(self.app())
        
        # Set complete stylesheet
        self.setStyleSheet(self.modern_styles.get_complete_stylesheet())
        
        # Apply shadow effects
        self.modern_styles.apply_shadow_effect(self.content_container)
    
    def navigate_to_screen(self, screen_id: str):
        """Navigate to a specific screen with animation."""
        if screen_id not in self.screens:
            return
        
        # Update navigation buttons
        for button_id, button in self.nav_buttons.items():
            button.setChecked(button_id == screen_id)
        
        # Get current and target screens
        current_screen = self.stacked_widget.currentWidget()
        target_screen = self.screens[screen_id]
        
        # Create transition animation
        transition = self.animation_manager.create_screen_transition(
            current_screen, target_screen, direction="slide_right"
        )
        
        # Switch screens
        self.stacked_widget.setCurrentWidget(target_screen)
        
        # Start transition animation
        transition.start()
        
        # Update status
        self.status_label.setText(f"Viewing {screen_id.replace('_', ' ').title()}")
    
    def show_welcome_screen(self):
        """Show welcome screen with animation."""
        self.navigate_to_screen("welcome")
    
    def on_environment_requested(self, environment: str):
        """Handle environment setup request."""
        self.status_label.setText(f"Setting up {environment} environment...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Navigate to environment screen
        self.navigate_to_screen("environment")
        
        # Start backend process
        self.gui_agent.setup_environment(environment)
    
    def on_plan_generated(self, plan: list):
        """Handle plan generation."""
        self.status_label.setText("Plan generated successfully")
        self.progress_bar.setVisible(False)
        
        # Navigate to plan screen
        self.navigate_to_screen("plan")
        
        # Update plan screen
        if "plan" in self.screens:
            self.screens["plan"].update_plan(plan)
    
    def on_installation_started(self):
        """Handle installation start."""
        self.status_label.setText("Installation in progress...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
    
    def on_installation_finished(self, success: bool, message: str):
        """Handle installation completion."""
        if success:
            self.status_label.setText("Installation completed successfully")
            self.progress_bar.setValue(100)
        else:
            self.status_label.setText(f"Installation failed: {message}")
        
        # Hide progress bar after delay
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))
    
    def on_log_message(self, message: str):
        """Handle log message updates."""
        # Update console screen
        if "console" in self.screens:
            self.screens["console"].append_log(message)
    
    def on_error_occurred(self, error_message: str):
        """Handle error occurrences."""
        self.status_label.setText(f"Error: {error_message}")
        
        # Show error modal
        self.show_error_modal(error_message)
    
    def show_error_modal(self, error_message: str):
        """Show modern error modal."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
        
        modal = QDialog(self)
        modal.setWindowTitle("Error")
        modal.setModal(True)
        modal.setStyleSheet(self.modern_styles.get_modal_style())
        
        layout = QVBoxLayout(modal)
        
        # Error icon and message
        error_label = QLabel("❌ Error")
        error_label.setFont(self.theme.fonts['heading_small'])
        layout.addWidget(error_label)
        
        message_label = QLabel(error_message)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(modal.accept)
        layout.addWidget(button_box)
        
        modal.exec()
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop all animations
        self.animation_manager.stop_all_animations()
        
        # Cleanup backend
        if hasattr(self, 'gui_agent'):
            self.gui_agent.cleanup()
        
        event.accept()
    
    def paintEvent(self, event):
        """Custom paint event for enhanced glass effect."""
        super().paintEvent(event)
        
        # Create custom painter for background effects
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Add subtle gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(15, 23, 42, 200))  # Slate 900 with alpha
        gradient.setColorAt(1, QColor(30, 41, 59, 200))  # Slate 800 with alpha
        
        painter.fillRect(self.rect(), gradient) 