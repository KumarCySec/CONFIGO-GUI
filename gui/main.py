"""
CONFIGO GUI - Main Application
Modern desktop application for intelligent development environment setup
"""

import sys
import os
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QStackedWidget, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QGraphicsBlurEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QPalette, QColor, QPixmap, QPainter
import qt_material

from .views.welcome import WelcomeView
from .views.env_selector import EnvironmentSelectorView
from .views.install_plan import InstallPlanView
from .components.sidebar import Sidebar
from .components.toast import ToastManager
from .themes.dark_theme import DarkTheme
from .backend.install_engine import InstallEngine


class CONFIGOGUI(QMainWindow):
    """Main CONFIGO GUI Application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CONFIGO - Intelligent Development Environment Setup")
        self.setMinimumSize(1200, 800)
        
        # Initialize components
        self.install_engine = InstallEngine()
        self.toast_manager = ToastManager(self)
        
        # Setup UI
        self.setup_ui()
        self.setup_theme()
        self.setup_animations()
        
        # Center window
        self.center_window()
        
    def setup_ui(self):
        """Setup the main UI components"""
        # Create central widget with glassmorphism effect
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        self.main_layout.addWidget(self.sidebar)
        
        # Create main content area
        self.content_area = QFrame()
        self.content_area.setObjectName("contentArea")
        self.content_area.setStyleSheet("""
            #contentArea {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        
        # Add glassmorphism effect
        self.add_glassmorphism_effect(self.content_area)
        
        # Content layout
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)
        
        # Initialize views
        self.setup_views()
        
        self.main_layout.addWidget(self.content_area, 1)
        
    def setup_views(self):
        """Setup all application views"""
        # Welcome view
        self.welcome_view = WelcomeView(self)
        self.stacked_widget.addWidget(self.welcome_view)
        
        # Environment selector view
        self.env_selector_view = EnvironmentSelectorView(self)
        self.stacked_widget.addWidget(self.env_selector_view)
        
        # Install plan view
        self.install_plan_view = InstallPlanView(self)
        self.stacked_widget.addWidget(self.install_plan_view)
        
        # Connect sidebar navigation
        self.sidebar.navigation_changed.connect(self.navigate_to_view)
        
        # Start with welcome view
        self.show_welcome()
        
    def setup_theme(self):
        """Setup the dark theme with custom styling"""
        # Apply dark theme
        qt_material.apply_stylesheet(self, theme='dark_teal.xml')
        
        # Apply custom dark theme
        self.dark_theme = DarkTheme()
        self.dark_theme.apply(self)
        
    def setup_animations(self):
        """Setup animations and transitions"""
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animations)
        self.animation_timer.start(16)  # 60 FPS
        
    def add_glassmorphism_effect(self, widget: QWidget):
        """Add glassmorphism effect to a widget"""
        # Create blur effect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        widget.setGraphicsEffect(blur_effect)
        
        # Create drop shadow
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        shadow_effect.setOffset(0, 5)
        widget.setGraphicsEffect(shadow_effect)
        
    def center_window(self):
        """Center the window on screen"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def navigate_to_view(self, view_name: str):
        """Navigate to a specific view"""
        view_map = {
            "welcome": 0,
            "environment": 1,
            "install": 2
        }
        
        if view_name in view_map:
            self.stacked_widget.setCurrentIndex(view_map[view_name])
            self.animate_transition()
            
    def show_welcome(self):
        """Show the welcome view with animation"""
        self.stacked_widget.setCurrentIndex(0)
        self.sidebar.set_active_item("welcome")
        
    def animate_transition(self):
        """Animate the transition between views"""
        # Create fade animation
        self.fade_animation = QPropertyAnimation(self.stacked_widget, b"windowOpacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.fade_animation.start()
        
    def update_animations(self):
        """Update ongoing animations"""
        # This will be called at 60 FPS for smooth animations
        pass
        
    def show_toast(self, message: str, toast_type: str = "info"):
        """Show a toast notification"""
        self.toast_manager.show_toast(message, toast_type)
        
    def run(self) -> int:
        """Run the application"""
        self.show()
        return QApplication.instance().exec()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("CONFIGO GUI")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("CONFIGO Team")
    
    # Create and run the main window
    window = CONFIGOGUI()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main()) 