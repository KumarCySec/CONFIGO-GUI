"""
CONFIGO GUI - Animated Button Component
======================================

Modern animated button component with hover effects, ripple animations,
and various styling variants. Provides a comprehensive button system.

Author: CONFIGO Team
"""

from typing import Optional, Callable, Any
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint, QRect
from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PySide6.QtGui import QColor, QFont, QPainter, QLinearGradient, QRadialGradient


class AnimatedButton(QPushButton):
    """
    Modern animated button component with advanced effects.
    
    Features:
    - Multiple button variants (primary, secondary, outline, ghost)
    - Hover animations with scaling and glow effects
    - Ripple effect on click
    - Loading state with spinner
    - Customizable sizes and colors
    - Smooth transitions and animations
    """
    
    def __init__(self, text: str = "", variant: str = "primary", size: str = "medium",
                 theme=None, parent=None):
        super().__init__(text, parent)
        
        self.theme = theme
        self.variant = variant
        self.size = size
        self.is_loading = False
        self.ripple_center = QPoint(0, 0)
        
        # Animation properties
        self.hover_animation = None
        self.glow_animation = None
        self.ripple_animation = None
        self.loading_animation = None
        self.is_hovered = False
        
        # Setup button
        self.setup_animations()
        self.setup_styling()
        self.setup_events()
    
    def setup_animations(self):
        """Setup button animations."""
        if not self.theme:
            return
        
        # Hover scale animation
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Glow effect animation
        if not self.graphicsEffect():
            glow_effect = QGraphicsDropShadowEffect()
            glow_effect.setBlurRadius(20)
            glow_effect.setOffset(0, 0)
            glow_effect.setColor(QColor(0, 0, 0, 0))
            self.setGraphicsEffect(glow_effect)
        
        self.glow_animation = QPropertyAnimation(self.graphicsEffect(), b"color")
        self.glow_animation.setDuration(200)
        self.glow_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Ripple animation
        self.ripple_animation = QPropertyAnimation(self, b"geometry")
        self.ripple_animation.setDuration(300)
        self.ripple_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def setup_styling(self):
        """Apply modern button styling."""
        if not self.theme:
            return
        
        # Get size configuration
        sizes = {
            "small": {"padding": "8px 16px", "font_size": "12px", "min_height": "32px"},
            "medium": {"padding": "12px 24px", "font_size": "14px", "min_height": "44px"},
            "large": {"padding": "16px 32px", "font_size": "16px", "min_height": "56px"}
        }
        
        size_config = sizes.get(self.size, sizes["medium"])
        
        # Set button properties
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(self.theme.fonts['button'])
        
        # Apply variant-specific styling
        if self.variant == "primary":
            self.setStyleSheet(f"""
                AnimatedButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.theme.colors['primary'].name()}, 
                        stop:1 {self.theme.colors['primary_dark'].name()});
                    border: none;
                    border-radius: {self.theme.effects['border_radius']}px;
                    color: white;
                    font: {size_config['font_size']}pt "{self.theme.fonts['inter']}";
                    font-weight: 500;
                    padding: {size_config['padding']};
                    min-height: {size_config['min_height']}px;
                }}
                
                AnimatedButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.theme.colors['primary_light'].name()}, 
                        stop:1 {self.theme.colors['primary'].name()});
                }}
                
                AnimatedButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.theme.colors['primary_dark'].name()}, 
                        stop:1 {self.theme.colors['primary'].name()});
                }}
                
                AnimatedButton:disabled {{
                    background: {self.theme.colors['surface_light'].name()};
                    color: {self.theme.colors['text_muted'].name()};
                }}
            """)
        
        elif self.variant == "secondary":
            self.setStyleSheet(f"""
                AnimatedButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.theme.colors['secondary'].name()}, 
                        stop:1 {self.theme.colors['secondary_dark'].name()});
                    border: none;
                    border-radius: {self.theme.effects['border_radius']}px;
                    color: white;
                    font: {size_config['font_size']}pt "{self.theme.fonts['inter']}";
                    font-weight: 500;
                    padding: {size_config['padding']};
                    min-height: {size_config['min_height']}px;
                }}
                
                AnimatedButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.theme.colors['secondary_light'].name()}, 
                        stop:1 {self.theme.colors['secondary'].name()});
                }}
            """)
        
        elif self.variant == "outline":
            self.setStyleSheet(f"""
                AnimatedButton {{
                    background: transparent;
                    border: 2px solid {self.theme.colors['primary'].name()};
                    border-radius: {self.theme.effects['border_radius']}px;
                    color: {self.theme.colors['primary'].name()};
                    font: {size_config['font_size']}pt "{self.theme.fonts['inter']}";
                    font-weight: 500;
                    padding: {size_config['padding']};
                    min-height: {size_config['min_height']}px;
                }}
                
                AnimatedButton:hover {{
                    background: {self.theme.colors['primary'].name()};
                    color: white;
                }}
            """)
        
        elif self.variant == "ghost":
            self.setStyleSheet(f"""
                AnimatedButton {{
                    background: transparent;
                    border: none;
                    border-radius: {self.theme.effects['border_radius']}px;
                    color: {self.theme.colors['text_secondary'].name()};
                    font: {size_config['font_size']}pt "{self.theme.fonts['inter']}";
                    font-weight: 500;
                    padding: {size_config['padding']};
                    min-height: {size_config['min_height']}px;
                }}
                
                AnimatedButton:hover {{
                    background: rgba(255, 255, 255, 0.1);
                    color: {self.theme.colors['text_primary'].name()};
                }}
            """)
    
    def setup_events(self):
        """Setup mouse event handlers."""
        self.setMouseTracking(True)
    
    def enterEvent(self, event):
        """Handle mouse enter event."""
        super().enterEvent(event)
        self.is_hovered = True
        self.start_hover_animation()
    
    def leaveEvent(self, event):
        """Handle mouse leave event."""
        super().leaveEvent(event)
        self.is_hovered = False
        self.start_hover_animation()
    
    def mousePressEvent(self, event):
        """Handle mouse press event for ripple effect."""
        super().mousePressEvent(event)
        self.ripple_center = event.pos()
        self.start_ripple_animation()
    
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
    
    def start_ripple_animation(self):
        """Start ripple effect animation."""
        if not self.ripple_animation or not self.theme:
            return
        
        # Create ripple effect
        current_rect = self.geometry()
        ripple_size = min(current_rect.width(), current_rect.height()) * 0.8
        
        # Calculate ripple geometry
        ripple_rect = QRect(
            int(self.ripple_center.x() - ripple_size / 2),
            int(self.ripple_center.y() - ripple_size / 2),
            int(ripple_size),
            int(ripple_size)
        )
        
        # Animate ripple
        self.ripple_animation.setStartValue(current_rect)
        self.ripple_animation.setEndValue(ripple_rect)
        self.ripple_animation.start()
    
    def calculate_scaled_geometry(self, rect, scale_factor):
        """Calculate scaled geometry for animation."""
        width_diff = rect.width() * (scale_factor - 1)
        height_diff = rect.height() * (scale_factor - 1)
        
        return QRect(
            int(rect.x() - width_diff / 2),
            int(rect.y() - height_diff / 2),
            int(rect.width() * scale_factor),
            int(rect.height() * scale_factor)
        )
    
    def set_loading(self, loading: bool):
        """Set loading state with spinner animation."""
        self.is_loading = loading
        
        if loading:
            self.setEnabled(False)
            self.start_loading_animation()
        else:
            self.setEnabled(True)
            self.stop_loading_animation()
    
    def start_loading_animation(self):
        """Start loading spinner animation."""
        if not self.theme:
            return
        
        # Create loading animation (rotation)
        self.loading_animation = QPropertyAnimation(self, b"rotation")
        self.loading_animation.setStartValue(0)
        self.loading_animation.setEndValue(360)
        self.loading_animation.setDuration(1000)
        self.loading_animation.setLoopCount(-1)  # Infinite loop
        self.loading_animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.loading_animation.start()
    
    def stop_loading_animation(self):
        """Stop loading spinner animation."""
        if self.loading_animation and self.loading_animation.isRunning():
            self.loading_animation.stop()
    
    def set_variant(self, variant: str):
        """Change button variant."""
        self.variant = variant
        self.setup_styling()
    
    def set_size(self, size: str):
        """Change button size."""
        self.size = size
        self.setup_styling()
    
    def paintEvent(self, event):
        """Custom paint event for enhanced effects."""
        super().paintEvent(event)
        
        if not self.theme:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Add subtle gradient overlay
        if self.is_hovered:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(255, 255, 255, 20))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.fillRect(self.rect(), gradient)
        
        # Add ripple effect
        if hasattr(self, 'ripple_center') and self.ripple_center != QPoint(0, 0):
            ripple_gradient = QRadialGradient(self.ripple_center, 20)
            ripple_gradient.setColorAt(0, QColor(255, 255, 255, 50))
            ripple_gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.fillRect(self.rect(), ripple_gradient) 