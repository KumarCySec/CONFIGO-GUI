"""
CONFIGO GUI - Toast Notification Component
=========================================

Modern toast notification component for displaying temporary messages.
Provides animated notifications with different types (success, error, warning, info).

Author: CONFIGO Team
"""

from typing import Optional
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QColor, QFont, QPainter, QLinearGradient


class ToastNotification(QWidget):
    """
    Modern toast notification component with animations.
    
    Features:
    - Multiple notification types (success, error, warning, info)
    - Smooth slide-in/out animations
    - Auto-dismiss functionality
    - Customizable styling and duration
    """
    
    def __init__(self, message: str = "", notification_type: str = "info", 
                 duration: int = 3000, theme=None, parent=None):
        super().__init__(parent)
        
        self.theme = theme
        self.message = message
        self.notification_type = notification_type
        self.duration = duration
        
        # Setup UI
        self.setup_ui()
        self.setup_animations()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the toast UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # Message label
        self.message_label = QLabel(self.message)
        if self.theme:
            self.message_label.setFont(self.theme.fonts['body_medium'])
        layout.addWidget(self.message_label)
        
        # Close button
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(20, 20)
        self.close_button.clicked.connect(self.dismiss)
        layout.addWidget(self.close_button)
    
    def setup_animations(self):
        """Setup toast animations."""
        # Slide-in animation
        self.slide_in_animation = QPropertyAnimation(self, b"pos")
        self.slide_in_animation.setDuration(300)
        self.slide_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Slide-out animation
        self.slide_out_animation = QPropertyAnimation(self, b"pos")
        self.slide_out_animation.setDuration(300)
        self.slide_out_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.slide_out_animation.finished.connect(self.deleteLater)
    
    def setup_styling(self):
        """Apply notification styling based on type."""
        if not self.theme:
            return
        
        # Get colors based on notification type
        colors = {
            "success": self.theme.colors['accent'],
            "error": self.theme.colors['error'],
            "warning": self.theme.colors['warning'],
            "info": self.theme.colors['primary']
        }
        
        color = colors.get(self.notification_type, self.theme.colors['primary'])
        
        self.setStyleSheet(f"""
            ToastNotification {{
                background-color: rgba({color.red()}, {color.green()}, {color.blue()}, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font: {self.theme.fonts['body_medium'].pointSize()}pt "{self.theme.fonts['inter']}";
            }}
            
            QPushButton {{
                background: transparent;
                border: none;
                color: white;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }}
        """)
    
    def show_notification(self, message: str = None, notification_type: str = None):
        """Show the toast notification with animation."""
        if message:
            self.message = message
            self.message_label.setText(message)
        
        if notification_type:
            self.notification_type = notification_type
            self.setup_styling()
        
        # Position the toast
        self.setFixedSize(300, 60)
        
        # Start slide-in animation
        start_pos = QPoint(self.parent().width(), 20)
        end_pos = QPoint(self.parent().width() - 320, 20)
        
        self.slide_in_animation.setStartValue(start_pos)
        self.slide_in_animation.setEndValue(end_pos)
        self.slide_in_animation.start()
        
        # Auto-dismiss after duration
        QTimer.singleShot(self.duration, self.dismiss)
    
    def dismiss(self):
        """Dismiss the toast notification with animation."""
        current_pos = self.pos()
        end_pos = QPoint(self.parent().width(), current_pos.y())
        
        self.slide_out_animation.setStartValue(current_pos)
        self.slide_out_animation.setEndValue(end_pos)
        self.slide_out_animation.start() 