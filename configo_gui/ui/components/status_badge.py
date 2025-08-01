"""
CONFIGO GUI - Status Badge Component
===================================

Modern status badge component for displaying status indicators.
Provides different status types with appropriate colors and animations.

Author: CONFIGO Team
"""

from typing import Optional
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PySide6.QtGui import QColor, QFont, QPainter


class StatusBadge(QLabel):
    """
    Modern status badge component with different status types.
    
    Features:
    - Multiple status types (success, error, warning, info, pending)
    - Color-coded status indicators
    - Smooth animations
    - Customizable styling
    """
    
    def __init__(self, text: str = "", status_type: str = "info", theme=None, parent=None):
        super().__init__(text, parent)
        
        self.theme = theme
        self.status_type = status_type
        
        # Setup styling
        self.setup_styling()
        self.setup_animations()
    
    def setup_styling(self):
        """Apply status badge styling."""
        if not self.theme:
            return
        
        # Get colors based on status type
        colors = {
            "success": self.theme.colors['accent'],
            "error": self.theme.colors['error'],
            "warning": self.theme.colors['warning'],
            "info": self.theme.colors['primary'],
            "pending": self.theme.colors['text_secondary']
        }
        
        color = colors.get(self.status_type, self.theme.colors['primary'])
        
        self.setStyleSheet(f"""
            StatusBadge {{
                background-color: rgba({color.red()}, {color.green()}, {color.blue()}, 0.2);
                border: 1px solid rgba({color.red()}, {color.green()}, {color.blue()}, 0.5);
                border-radius: 12px;
                color: {color.name()};
                font: {self.theme.fonts['body_small'].pointSize()}pt "{self.theme.fonts['inter']}";
                font-weight: 500;
                padding: 4px 12px;
                min-height: 20px;
            }}
        """)
        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def setup_animations(self):
        """Setup badge animations."""
        self.pulse_animation = QPropertyAnimation(self, b"geometry")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setLoopCount(-1)
        self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    
    def set_status(self, text: str, status_type: str = None):
        """Update badge status and type."""
        self.setText(text)
        
        if status_type:
            self.status_type = status_type
            self.setup_styling()
    
    def start_pulse(self):
        """Start pulsing animation for pending status."""
        if self.status_type == "pending":
            current_rect = self.geometry()
            pulse_rect = current_rect.adjusted(2, 2, -2, -2)
            
            self.pulse_animation.setStartValue(current_rect)
            self.pulse_animation.setEndValue(pulse_rect)
            self.pulse_animation.start()
    
    def stop_pulse(self):
        """Stop pulsing animation."""
        if self.pulse_animation.isRunning():
            self.pulse_animation.stop() 