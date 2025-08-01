"""
CONFIGO GUI - Glassmorphism Theme
=================================

Modern glassmorphism theme with blur effects, gradients, and glass-like UI elements.
Inspired by modern design systems like Linear, Raycast, and Notion.

Author: CONFIGO Team
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QPalette, QColor, QFont, QFontDatabase, QPixmap, QPainter
from PySide6.QtWidgets import QApplication, QWidget, QGraphicsBlurEffect


class GlassTheme:
    """
    Modern glassmorphism theme with advanced styling and effects.
    
    Features:
    - Glass-like transparent panels with blur effects
    - Modern color palette with gradients
    - Smooth animations and transitions
    - Responsive design elements
    - Custom fonts and typography
    """
    
    def __init__(self):
        self.colors = self._define_colors()
        self.fonts = self._define_fonts()
        self.effects = self._define_effects()
        self.animations = self._define_animations()
        
    def _define_colors(self) -> Dict[str, QColor]:
        """Define the modern color palette."""
        return {
            # Primary colors
            'primary': QColor(99, 102, 241),      # Indigo
            'primary_light': QColor(139, 142, 255),
            'primary_dark': QColor(79, 82, 221),
            
            # Secondary colors
            'secondary': QColor(168, 85, 247),    # Purple
            'secondary_light': QColor(196, 181, 253),
            'secondary_dark': QColor(147, 51, 234),
            
            # Accent colors
            'accent': QColor(34, 197, 94),        # Green
            'accent_light': QColor(74, 222, 128),
            'accent_dark': QColor(22, 163, 74),
            
            # Warning colors
            'warning': QColor(251, 146, 60),      # Orange
            'warning_light': QColor(251, 191, 36),
            'warning_dark': QColor(245, 101, 101),
            
            # Error colors
            'error': QColor(239, 68, 68),         # Red
            'error_light': QColor(248, 113, 113),
            'error_dark': QColor(220, 38, 38),
            
            # Neutral colors
            'background': QColor(15, 23, 42),     # Slate 900
            'surface': QColor(30, 41, 59),        # Slate 800
            'surface_light': QColor(51, 65, 85),  # Slate 700
            'surface_dark': QColor(15, 23, 42),   # Slate 900
            
            # Text colors
            'text_primary': QColor(248, 250, 252), # Slate 50
            'text_secondary': QColor(203, 213, 225), # Slate 300
            'text_muted': QColor(148, 163, 184),   # Slate 400
            
            # Border colors
            'border': QColor(51, 65, 85, 100),    # Slate 700 with alpha
            'border_light': QColor(71, 85, 105, 80), # Slate 600 with alpha
            'border_dark': QColor(30, 41, 59, 120), # Slate 800 with alpha
            
            # Glass colors
            'glass_primary': QColor(255, 255, 255, 10),   # White with low alpha
            'glass_secondary': QColor(255, 255, 255, 5),  # White with very low alpha
            'glass_border': QColor(255, 255, 255, 20),    # White border with alpha
        }
    
    def _define_fonts(self) -> Dict[str, QFont]:
        """Define modern typography system."""
        fonts = {}
        
        # Load custom fonts if available
        font_path = Path(__file__).parent.parent.parent / "assets" / "fonts"
        if font_path.exists():
            # Load Inter font family
            inter_fonts = [
                "Inter-Regular.ttf",
                "Inter-Medium.ttf", 
                "Inter-SemiBold.ttf",
                "Inter-Bold.ttf"
            ]
            
            for font_file in inter_fonts:
                font_path_file = font_path / font_file
                if font_path_file.exists():
                    font_id = QFontDatabase.addApplicationFont(str(font_path_file))
                    if font_id != -1:
                        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                        fonts['inter'] = font_family
        
        # Fallback to system fonts
        if 'inter' not in fonts:
            fonts['inter'] = "Segoe UI" if os.name == 'nt' else "SF Pro Display" if os.uname().sysname == "Darwin" else "Ubuntu"
        
        # Define font styles
        fonts.update({
            'heading_large': QFont(fonts['inter'], 32, QFont.Weight.Bold),
            'heading_medium': QFont(fonts['inter'], 24, QFont.Weight.SemiBold),
            'heading_small': QFont(fonts['inter'], 20, QFont.Weight.SemiBold),
            'body_large': QFont(fonts['inter'], 16, QFont.Weight.Normal),
            'body_medium': QFont(fonts['inter'], 14, QFont.Weight.Normal),
            'body_small': QFont(fonts['inter'], 12, QFont.Weight.Normal),
            'caption': QFont(fonts['inter'], 11, QFont.Weight.Normal),
            'button': QFont(fonts['inter'], 14, QFont.Weight.Medium),
            'code': QFont("JetBrains Mono" if os.name == 'nt' else "Fira Code", 13, QFont.Weight.Normal),
        })
        
        return fonts
    
    def _define_effects(self) -> Dict[str, Any]:
        """Define glassmorphism and modern effects."""
        return {
            'glass_blur': 15,           # Blur radius for glass effect
            'glass_alpha': 0.1,         # Glass transparency
            'border_radius': 12,        # Default border radius
            'shadow_offset': 4,         # Shadow offset
            'shadow_blur': 20,          # Shadow blur radius
            'animation_duration': 300,  # Default animation duration (ms)
            'hover_scale': 1.02,        # Hover scale factor
        }
    
    def _define_animations(self) -> Dict[str, Any]:
        """Define animation presets."""
        return {
            'easing_standard': QEasingCurve.Type.OutCubic,
            'easing_bounce': QEasingCurve.Type.OutBounce,
            'easing_elastic': QEasingCurve.Type.OutElastic,
            'duration_fast': 150,
            'duration_standard': 300,
            'duration_slow': 500,
        }
    
    def apply_glass_effect(self, widget: QWidget, blur_radius: int = None, alpha: float = None) -> None:
        """
        Apply glassmorphism effect to a widget.
        
        Args:
            widget: The widget to apply the effect to
            blur_radius: Custom blur radius (optional)
            alpha: Custom alpha value (optional)
        """
        if blur_radius is None:
            blur_radius = self.effects['glass_blur']
        if alpha is None:
            alpha = self.effects['glass_alpha']
        
        # Create blur effect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(blur_radius)
        widget.setGraphicsEffect(blur_effect)
        
        # Set widget properties for glass effect
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, {alpha});
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: {self.effects['border_radius']}px;
            }}
        """)
    
    def create_gradient_background(self, start_color: QColor, end_color: QColor, 
                                 direction: str = "vertical") -> str:
        """
        Create CSS gradient background.
        
        Args:
            start_color: Starting color of gradient
            end_color: Ending color of gradient
            direction: Gradient direction ("vertical", "horizontal", "diagonal")
            
        Returns:
            CSS gradient string
        """
        if direction == "vertical":
            return f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {start_color.name()}, stop:1 {end_color.name()})"
        elif direction == "horizontal":
            return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {start_color.name()}, stop:1 {end_color.name()})"
        else:  # diagonal
            return f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {start_color.name()}, stop:1 {end_color.name()})"
    
    def get_modern_stylesheet(self, component: str = "main") -> str:
        """
        Get modern stylesheet for different components.
        
        Args:
            component: Component type ("main", "button", "input", "card", etc.)
            
        Returns:
            CSS stylesheet string
        """
        if component == "main":
            return f"""
                QMainWindow {{
                    background: {self.create_gradient_background(self.colors['background'], self.colors['surface'])};
                    color: {self.colors['text_primary'].name()};
                    font-family: "{self.fonts['inter']}";
                }}
                
                QWidget {{
                    background: transparent;
                    color: {self.colors['text_primary'].name()};
                }}
            """
        
        elif component == "glass_card":
            return f"""
                QFrame {{
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: {self.effects['border_radius']}px;
                    padding: 16px;
                }}
                
                QFrame:hover {{
                    background-color: rgba(255, 255, 255, 0.15);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }}
            """
        
        elif component == "modern_button":
            return f"""
                QPushButton {{
                    background: {self.create_gradient_background(self.colors['primary'], self.colors['primary_dark'])};
                    border: none;
                    border-radius: {self.effects['border_radius']}px;
                    color: white;
                    font: {self.fonts['button'].pointSize()}pt "{self.fonts['inter']}";
                    font-weight: 500;
                    padding: 12px 24px;
                    min-height: 44px;
                }}
                
                QPushButton:hover {{
                    background: {self.create_gradient_background(self.colors['primary_light'], self.colors['primary'])};
                    transform: scale(1.02);
                }}
                
                QPushButton:pressed {{
                    background: {self.create_gradient_background(self.colors['primary_dark'], self.colors['primary'])};
                    transform: scale(0.98);
                }}
                
                QPushButton:disabled {{
                    background: {self.colors['surface_light'].name()};
                    color: {self.colors['text_muted'].name()};
                }}
            """
        
        elif component == "modern_input":
            return f"""
                QLineEdit, QTextEdit {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: {self.effects['border_radius']}px;
                    color: {self.colors['text_primary'].name()};
                    font: {self.fonts['body_medium'].pointSize()}pt "{self.fonts['inter']}";
                    padding: 12px 16px;
                    min-height: 44px;
                }}
                
                QLineEdit:focus, QTextEdit:focus {{
                    border: 2px solid {self.colors['primary'].name()};
                    background-color: rgba(255, 255, 255, 0.08);
                }}
                
                QLineEdit:hover, QTextEdit:hover {{
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    background-color: rgba(255, 255, 255, 0.07);
                }}
            """
        
        elif component == "sidebar":
            return f"""
                QFrame {{
                    background-color: rgba(0, 0, 0, 0.3);
                    border-right: 1px solid rgba(255, 255, 255, 0.1);
                }}
                
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-radius: 8px;
                    color: {self.colors['text_secondary'].name()};
                    font: {self.fonts['body_medium'].pointSize()}pt "{self.fonts['inter']}";
                    font-weight: 500;
                    padding: 12px 16px;
                    text-align: left;
                    margin: 4px 8px;
                }}
                
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                    color: {self.colors['text_primary'].name()};
                }}
                
                QPushButton:checked {{
                    background-color: {self.colors['primary'].name()};
                    color: white;
                }}
            """
        
        return ""
    
    def apply_theme_to_app(self, app: QApplication) -> None:
        """
        Apply the complete glassmorphism theme to the application.
        
        Args:
            app: The QApplication instance
        """
        # Set application-wide stylesheet
        app.setStyleSheet(self.get_modern_stylesheet("main"))
        
        # Set application properties
        app.setApplicationName("CONFIGO GUI")
        app.setApplicationVersion("2.0.0")
        app.setOrganizationName("CONFIGO")
        app.setOrganizationDomain("configo.dev")
        
        # Set default font
        app.setFont(self.fonts['body_medium']) 