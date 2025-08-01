"""
CONFIGO GUI - Loading Spinner Component
=======================================

Modern loading spinner component with smooth rotation animations
and customizable styling. Provides visual feedback during operations.

Author: CONFIGO Team
"""

from typing import Optional
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QPainter, QColor, QPen, QFont


class LoadingSpinner(QWidget):
    """
    Modern loading spinner component with smooth animations.
    
    Features:
    - Smooth rotation animation
    - Customizable colors and sizes
    - Multiple spinner styles
    - Loading text support
    - Auto-start/stop functionality
    """
    
    def __init__(self, text: str = "Loading...", size: int = 40, 
                 color: QColor = None, theme=None, parent=None):
        super().__init__(parent)
        
        self.theme = theme
        self.text = text
        self.size = size
        self.color = color or (self.theme.colors['primary'] if self.theme else QColor(99, 102, 241))
        
        # Animation properties
        self.rotation_animation = None
        self.is_animating = False
        
        # Setup UI
        self.setup_ui()
        self.setup_animation()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the spinner UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create spinner widget
        self.spinner_widget = SpinnerWidget(self.size, self.color, self.theme)
        layout.addWidget(self.spinner_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Create text label
        if self.text:
            self.text_label = QLabel(self.text)
            if self.theme:
                self.text_label.setFont(self.theme.fonts['body_medium'])
                self.text_label.setStyleSheet(f"color: {self.theme.colors['text_secondary'].name()};")
            layout.addWidget(self.text_label, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def setup_animation(self):
        """Setup rotation animation."""
        self.rotation_animation = QPropertyAnimation(self.spinner_widget, b"rotation")
        self.rotation_animation.setStartValue(0)
        self.rotation_animation.setEndValue(360)
        self.rotation_animation.setDuration(1000)
        self.rotation_animation.setLoopCount(-1)  # Infinite loop
        self.rotation_animation.setEasingCurve(QEasingCurve.Type.Linear)
    
    def setup_styling(self):
        """Apply modern styling."""
        self.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
    
    def start(self):
        """Start the spinner animation."""
        if not self.is_animating:
            self.is_animating = True
            self.setVisible(True)
            self.rotation_animation.start()
    
    def stop(self):
        """Stop the spinner animation."""
        if self.is_animating:
            self.is_animating = False
            self.rotation_animation.stop()
            self.setVisible(False)
    
    def set_text(self, text: str):
        """Update the loading text."""
        self.text = text
        if hasattr(self, 'text_label'):
            self.text_label.setText(text)
    
    def set_color(self, color: QColor):
        """Update the spinner color."""
        self.color = color
        if hasattr(self, 'spinner_widget'):
            self.spinner_widget.set_color(color)
    
    def set_size(self, size: int):
        """Update the spinner size."""
        self.size = size
        if hasattr(self, 'spinner_widget'):
            self.spinner_widget.set_size(size)


class SpinnerWidget(QWidget):
    """
    Custom spinner widget with rotation animation.
    """
    
    def __init__(self, size: int = 40, color: QColor = None, theme=None, parent=None):
        super().__init__(parent)
        
        self.size = size
        self.color = color or QColor(99, 102, 241)
        self.theme = theme
        self.rotation = 0
        
        # Set widget properties
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def set_rotation(self, angle: float):
        """Set rotation angle for animation."""
        self.rotation = angle
        self.update()
    
    def set_color(self, color: QColor):
        """Update spinner color."""
        self.color = color
        self.update()
    
    def set_size(self, size: int):
        """Update spinner size."""
        self.size = size
        self.setFixedSize(size, size)
        self.update()
    
    def paintEvent(self, event):
        """Custom paint event for spinner drawing."""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate center and radius
        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = min(self.width(), self.height()) / 2 - 4
        
        # Create pen for spinner lines
        pen = QPen(self.color)
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        # Draw spinner lines
        num_lines = 8
        for i in range(num_lines):
            # Calculate line position
            angle = (self.rotation + i * 360 / num_lines) * 3.14159 / 180
            start_x = center_x + (radius - 8) * math.cos(angle)
            start_y = center_y + (radius - 8) * math.sin(angle)
            end_x = center_x + radius * math.cos(angle)
            end_y = center_y + radius * math.sin(angle)
            
            # Set line opacity based on position
            opacity = 0.3 + 0.7 * (i / num_lines)
            painter.setOpacity(opacity)
            
            # Draw line
            painter.drawLine(int(start_x), int(start_y), int(end_x), int(end_y))


# Import math for calculations
import math 