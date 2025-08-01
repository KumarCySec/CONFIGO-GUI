"""
CONFIGO GUI - Progress Indicator Component
=========================================

Modern progress indicator component with smooth animations and glassmorphism effects.
Provides visual feedback for long-running operations.

Author: CONFIGO Team
"""

from typing import Optional
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtGui import QColor, QFont, QPainter, QLinearGradient


class ProgressIndicator(QWidget):
    """
    Modern progress indicator with animations and glassmorphism effects.
    
    Features:
    - Smooth progress animations
    - Glass-like styling
    - Customizable colors and sizes
    - Text labels and descriptions
    """
    
    def __init__(self, title: str = "", description: str = "", theme=None, parent=None):
        super().__init__(parent)
        
        self.theme = theme
        self.title = title
        self.description = description
        
        # Setup UI
        self.setup_ui()
        self.setup_animations()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the progress indicator UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Title
        if self.title:
            self.title_label = QLabel(self.title)
            if self.theme:
                self.title_label.setFont(self.theme.fonts['heading_small'])
            layout.addWidget(self.title_label)
        
        # Description
        if self.description:
            self.description_label = QLabel(self.description)
            if self.theme:
                self.description_label.setFont(self.theme.fonts['body_medium'])
                self.description_label.setStyleSheet(f"color: {self.theme.colors['text_secondary'].name()};")
            layout.addWidget(self.description_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        if self.theme:
            self.status_label.setFont(self.theme.fonts['body_small'])
        layout.addWidget(self.status_label)
    
    def setup_animations(self):
        """Setup progress animations."""
        self.progress_animation = QPropertyAnimation(self.progress_bar, b"value")
        self.progress_animation.setDuration(500)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def setup_styling(self):
        """Apply modern progress styling."""
        if not self.theme:
            return
        
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: rgba(255, 255, 255, 0.05);
                border: none;
                border-radius: {self.theme.effects['border_radius']}px;
                text-align: center;
                color: {self.theme.colors['text_primary'].name()};
                font: {self.theme.fonts['body_small'].pointSize()}pt "{self.theme.fonts['inter']}";
                font-weight: 500;
                height: 8px;
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {self.theme.colors['primary'].name()}, 
                    stop:1 {self.theme.colors['primary_light'].name()});
                border-radius: {self.theme.effects['border_radius']}px;
            }}
        """)
    
    def set_progress(self, value: int, status: str = None):
        """Set progress value with animation."""
        self.progress_animation.setStartValue(self.progress_bar.value())
        self.progress_animation.setEndValue(value)
        self.progress_animation.start()
        
        if status:
            self.status_label.setText(status)
    
    def set_title(self, title: str):
        """Update the progress title."""
        self.title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)
    
    def set_description(self, description: str):
        """Update the progress description."""
        self.description = description
        if hasattr(self, 'description_label'):
            self.description_label.setText(description)
    
    def set_status(self, status: str):
        """Update the status message."""
        if hasattr(self, 'status_label'):
            self.status_label.setText(status) 