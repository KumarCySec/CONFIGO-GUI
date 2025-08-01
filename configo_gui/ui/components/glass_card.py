"""
CONFIGO GUI - Glass Card Component
==================================

Modern glassmorphism card component with hover effects and animations.
Provides a reusable card widget with glass-like appearance.

Author: CONFIGO Team
"""

from typing import Optional, Any
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtGui import QColor, QFont, QPixmap, QPainter, QLinearGradient


class GlassCard(QFrame):
    """
    Modern glassmorphism card component with hover effects and animations.
    
    Features:
    - Glass-like transparent background with blur effects
    - Smooth hover animations with scaling and glow
    - Customizable content layout
    - Modern typography and spacing
    - Responsive design
    """
    
    def __init__(self, title: str = "", subtitle: str = "", icon_path: str = None,
                 theme=None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.theme = theme
        self.title = title
        self.subtitle = subtitle
        self.icon_path = icon_path
        
        # Animation properties
        self.hover_animation = None
        self.glow_animation = None
        self.is_hovered = False
        
        # Setup UI
        self.setup_ui()
        self.setup_animations()
        self.setup_styling()
        self.setup_events()
    
    def setup_ui(self):
        """Initialize the card UI layout."""
        # Set frame properties
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setLineWidth(0)
        
        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Create header with icon and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Icon (if provided)
        if self.icon_path:
            self.icon_label = QLabel()
            icon_pixmap = QPixmap(self.icon_path)
            if not icon_pixmap.isNull():
                # Scale icon to appropriate size
                icon_pixmap = icon_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, 
                                               Qt.TransformationMode.SmoothTransformation)
                self.icon_label.setPixmap(icon_pixmap)
            header_layout.addWidget(self.icon_label)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        self.title_label = QLabel(self.title)
        if self.theme:
            self.title_label.setFont(self.theme.fonts['heading_small'])
        title_layout.addWidget(self.title_label)
        
        if self.subtitle:
            self.subtitle_label = QLabel(self.subtitle)
            if self.theme:
                self.subtitle_label.setFont(self.theme.fonts['body_medium'])
                self.subtitle_label.setStyleSheet(f"color: {self.theme.colors['text_secondary'].name()};")
            title_layout.addWidget(self.subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Content area (can be populated later)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(8)
        
        layout.addWidget(self.content_widget)
    
    def setup_animations(self):
        """Setup hover animations."""
        if not self.theme:
            return
        
        # Create hover scale animation
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Create glow animation
        if not self.graphicsEffect():
            from PySide6.QtWidgets import QGraphicsDropShadowEffect
            glow_effect = QGraphicsDropShadowEffect()
            glow_effect.setBlurRadius(20)
            glow_effect.setOffset(0, 0)
            glow_effect.setColor(QColor(0, 0, 0, 0))
            self.setGraphicsEffect(glow_effect)
        
        self.glow_animation = QPropertyAnimation(self.graphicsEffect(), b"color")
        self.glow_animation.setDuration(200)
        self.glow_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def setup_styling(self):
        """Apply glassmorphism styling."""
        if not self.theme:
            return
        
        # Apply glass effect
        self.theme.apply_glass_effect_to_widget(self)
        
        # Set card-specific styling
        self.setStyleSheet(f"""
            GlassCard {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: {self.theme.effects['border_radius']}px;
                margin: 8px;
            }}
            
            GlassCard:hover {{
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            
            QLabel {{
                color: {self.theme.colors['text_primary'].name()};
            }}
        """)
    
    def setup_events(self):
        """Setup mouse event handlers for hover effects."""
        self.setMouseTracking(True)
    
    def enterEvent(self, event):
        """Handle mouse enter event for hover animation."""
        super().enterEvent(event)
        self.is_hovered = True
        self.start_hover_animation()
    
    def leaveEvent(self, event):
        """Handle mouse leave event for hover animation."""
        super().leaveEvent(event)
        self.is_hovered = False
        self.start_hover_animation()
    
    def start_hover_animation(self):
        """Start hover animation based on hover state."""
        if not self.hover_animation or not self.theme:
            return
        
        # Calculate target geometry
        current_rect = self.geometry()
        scale_factor = 1.02 if self.is_hovered else 1.0
        
        target_rect = self.calculate_scaled_geometry(current_rect, scale_factor)
        
        # Animate geometry
        self.hover_animation.setStartValue(current_rect)
        self.hover_animation.setEndValue(target_rect)
        self.hover_animation.start()
        
        # Animate glow effect
        if self.glow_animation:
            start_color = QColor(99, 102, 241, 100) if self.is_hovered else QColor(0, 0, 0, 0)
            end_color = QColor(99, 102, 241, 0) if not self.is_hovered else QColor(99, 102, 241, 100)
            
            self.glow_animation.setStartValue(start_color)
            self.glow_animation.setEndValue(end_color)
            self.glow_animation.start()
    
    def calculate_scaled_geometry(self, rect, scale_factor):
        """Calculate scaled geometry for animation."""
        from PySide6.QtCore import QRect
        
        width_diff = rect.width() * (scale_factor - 1)
        height_diff = rect.height() * (scale_factor - 1)
        
        return QRect(
            int(rect.x() - width_diff / 2),
            int(rect.y() - height_diff / 2),
            int(rect.width() * scale_factor),
            int(rect.height() * scale_factor)
        )
    
    def add_widget(self, widget: QWidget):
        """Add a widget to the card content area."""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add a layout to the card content area."""
        self.content_layout.addLayout(layout)
    
    def set_title(self, title: str):
        """Update the card title."""
        self.title = title
        if hasattr(self, 'title_label'):
            self.title_label.setText(title)
    
    def set_subtitle(self, subtitle: str):
        """Update the card subtitle."""
        self.subtitle = subtitle
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(subtitle)
    
    def set_icon(self, icon_path: str):
        """Update the card icon."""
        self.icon_path = icon_path
        if hasattr(self, 'icon_label') and icon_path:
            icon_pixmap = QPixmap(icon_path)
            if not icon_pixmap.isNull():
                icon_pixmap = icon_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, 
                                               Qt.TransformationMode.SmoothTransformation)
                self.icon_label.setPixmap(icon_pixmap)
    
    def clear_content(self):
        """Clear all content from the card."""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def paintEvent(self, event):
        """Custom paint event for enhanced glass effect."""
        super().paintEvent(event)
        
        if not self.theme:
            return
        
        # Create custom painter for additional effects
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Add subtle gradient overlay
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(255, 255, 255, 5))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.fillRect(self.rect(), gradient) 