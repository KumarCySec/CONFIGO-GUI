"""
CONFIGO GUI - Modern Modal Component
===================================

Modern modal dialog component with glassmorphism effects and animations.
Provides a premium modal experience for confirmations and forms.

Author: CONFIGO Team
"""

from typing import Optional, Callable
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtGui import QColor, QFont, QPainter, QLinearGradient


class ModernModal(QDialog):
    """
    Modern modal dialog with glassmorphism effects.
    
    Features:
    - Glass-like transparent background
    - Smooth fade-in/out animations
    - Customizable content
    - Modern styling and typography
    """
    
    def __init__(self, title: str = "", content: str = "", theme=None, parent=None):
        super().__init__(parent)
        
        self.theme = theme
        self.title = title
        self.content = content
        
        # Setup UI
        self.setup_ui()
        self.setup_animations()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the modal UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Title
        if self.title:
            title_label = QLabel(self.title)
            if self.theme:
                title_label.setFont(self.theme.fonts['heading_small'])
            layout.addWidget(title_label)
        
        # Content
        if self.content:
            content_label = QLabel(self.content)
            content_label.setWordWrap(True)
            if self.theme:
                content_label.setFont(self.theme.fonts['body_medium'])
            layout.addWidget(content_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def setup_animations(self):
        """Setup modal animations."""
        # Fade-in animation
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def setup_styling(self):
        """Apply modern modal styling."""
        if not self.theme:
            return
        
        self.setStyleSheet(f"""
            ModernModal {{
                background-color: rgba(15, 23, 42, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: {self.theme.effects['border_radius']}px;
                color: {self.theme.colors['text_primary'].name()};
            }}
            
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 {self.theme.colors['primary'].name()}, 
                    stop:1 {self.theme.colors['primary_dark'].name()});
                border: none;
                border-radius: {self.theme.effects['border_radius']}px;
                color: white;
                font: {self.theme.fonts['button'].pointSize()}pt "{self.theme.fonts['inter']}";
                font-weight: 500;
                padding: 12px 24px;
                min-height: 44px;
            }}
            
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 {self.theme.colors['primary_light'].name()}, 
                    stop:1 {self.theme.colors['primary'].name()});
            }}
        """)
    
    def showEvent(self, event):
        """Handle show event to start fade-in animation."""
        super().showEvent(event)
        self.fade_in_animation.start()
    
    def paintEvent(self, event):
        """Custom paint event for enhanced glass effect."""
        super().paintEvent(event)
        
        if not self.theme:
            return
        
        # Create custom painter for background effects
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Add subtle gradient overlay
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 255, 255, 5))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.fillRect(self.rect(), gradient) 