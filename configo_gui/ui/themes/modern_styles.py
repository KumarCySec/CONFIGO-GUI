"""
CONFIGO GUI - Modern Styles
===========================

Comprehensive modern styling system for CONFIGO GUI components.
Provides glassmorphism effects, modern layouts, and responsive design.

Author: CONFIGO Team
"""

from typing import Dict, Any, Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QGraphicsBlurEffect


class ModernStyles:
    """
    Modern styling system for CONFIGO GUI components.
    
    Features:
    - Glassmorphism effects
    - Modern color schemes
    - Responsive layouts
    - Custom component styles
    - Animation-ready styling
    """
    
    def __init__(self, theme):
        self.theme = theme
        self.colors = theme.colors
        self.fonts = theme.fonts
        self.effects = theme.effects
    
    def get_glass_card_style(self, border_radius: int = None, padding: int = 16) -> str:
        """
        Get glassmorphism card styling.
        
        Args:
            border_radius: Custom border radius
            padding: Custom padding
            
        Returns:
            CSS stylesheet string
        """
        if border_radius is None:
            border_radius = self.effects['border_radius']
        
        return f"""
            QFrame {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: {border_radius}px;
                padding: {padding}px;
                margin: 8px;
            }}
            
            QFrame:hover {{
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }}
        """
    
    def get_modern_button_style(self, variant: str = "primary", size: str = "medium") -> str:
        """
        Get modern button styling.
        
        Args:
            variant: Button variant ("primary", "secondary", "outline", "ghost")
            size: Button size ("small", "medium", "large")
            
        Returns:
            CSS stylesheet string
        """
        # Size definitions
        sizes = {
            "small": {"padding": "8px 16px", "font_size": "12px", "min_height": "32px"},
            "medium": {"padding": "12px 24px", "font_size": "14px", "min_height": "44px"},
            "large": {"padding": "16px 32px", "font_size": "16px", "min_height": "56px"}
        }
        
        size_config = sizes.get(size, sizes["medium"])
        
        if variant == "primary":
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.colors['primary'].name()}, 
                        stop:1 {self.colors['primary_dark'].name()});
                    border: none;
                    border-radius: {self.effects['border_radius']}px;
                    color: white;
                    font: {size_config['font_size']}pt "{self.fonts['inter']}";
                    font-weight: 500;
                    padding: {size_config['padding']};
                    min-height: {size_config['min_height']}px;
                }}
                
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.colors['primary_light'].name()}, 
                        stop:1 {self.colors['primary'].name()});
                    transform: scale(1.02);
                }}
                
                QPushButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.colors['primary_dark'].name()}, 
                        stop:1 {self.colors['primary'].name()});
                    transform: scale(0.98);
                }}
                
                QPushButton:disabled {{
                    background: {self.colors['surface_light'].name()};
                    color: {self.colors['text_muted'].name()};
                }}
            """
        
        elif variant == "secondary":
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.colors['secondary'].name()}, 
                        stop:1 {self.colors['secondary_dark'].name()});
                    border: none;
                    border-radius: {self.effects['border_radius']}px;
                    color: white;
                    font: {size_config['font_size']}pt "{self.fonts['inter']}";
                    font-weight: 500;
                    padding: {size_config['padding']};
                    min-height: {size_config['min_height']}px;
                }}
                
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 {self.colors['secondary_light'].name()}, 
                        stop:1 {self.colors['secondary'].name()});
                    transform: scale(1.02);
                }}
            """
        
        elif variant == "outline":
            return f"""
                QPushButton {{
                    background: transparent;
                    border: 2px solid {self.colors['primary'].name()};
                    border-radius: {self.effects['border_radius']}px;
                    color: {self.colors['primary'].name()};
                    font: {size_config['font_size']}pt "{self.fonts['inter']}";
                    font-weight: 500;
                    padding: {size_config['padding']};
                    min-height: {size_config['min_height']}px;
                }}
                
                QPushButton:hover {{
                    background: {self.colors['primary'].name()};
                    color: white;
                    transform: scale(1.02);
                }}
            """
        
        elif variant == "ghost":
            return f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-radius: {self.effects['border_radius']}px;
                    color: {self.colors['text_secondary'].name()};
                    font: {size_config['font_size']}pt "{self.fonts['inter']}";
                    font-weight: 500;
                    padding: {size_config['padding']};
                    min-height: {size_config['min_height']}px;
                }}
                
                QPushButton:hover {{
                    background: rgba(255, 255, 255, 0.1);
                    color: {self.colors['text_primary'].name()};
                }}
            """
        
        return ""
    
    def get_modern_input_style(self, variant: str = "default") -> str:
        """
        Get modern input styling.
        
        Args:
            variant: Input variant ("default", "search", "code")
            
        Returns:
            CSS stylesheet string
        """
        if variant == "default":
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
                
                QLineEdit:disabled, QTextEdit:disabled {{
                    background-color: rgba(255, 255, 255, 0.02);
                    color: {self.colors['text_muted'].name()};
                    border: 1px solid rgba(255, 255, 255, 0.05);
                }}
            """
        
        elif variant == "search":
            return f"""
                QLineEdit {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 24px;
                    color: {self.colors['text_primary'].name()};
                    font: {self.fonts['body_medium'].pointSize()}pt "{self.fonts['inter']}";
                    padding: 12px 20px;
                    min-height: 44px;
                }}
                
                QLineEdit:focus {{
                    border: 2px solid {self.colors['primary'].name()};
                    background-color: rgba(255, 255, 255, 0.08);
                }}
            """
        
        elif variant == "code":
            return f"""
                QTextEdit {{
                    background-color: rgba(0, 0, 0, 0.3);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    color: {self.colors['text_primary'].name()};
                    font: {self.fonts['code'].pointSize()}pt "{self.fonts['code'].family()}";
                    padding: 16px;
                    line-height: 1.5;
                }}
                
                QTextEdit:focus {{
                    border: 1px solid {self.colors['primary'].name()};
                }}
            """
        
        return ""
    
    def get_sidebar_style(self) -> str:
        """
        Get modern sidebar styling.
        
        Returns:
            CSS stylesheet string
        """
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
    
    def get_navigation_style(self) -> str:
        """
        Get modern navigation styling.
        
        Returns:
            CSS stylesheet string
        """
        return f"""
            QFrame {{
                background-color: rgba(255, 255, 255, 0.05);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            QLabel {{
                color: {self.colors['text_primary'].name()};
                font: {self.fonts['heading_small'].pointSize()}pt "{self.fonts['inter']}";
                font-weight: 600;
            }}
            
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 6px;
                color: {self.colors['text_secondary'].name()};
                font: {self.fonts['body_medium'].pointSize()}pt "{self.fonts['inter']}";
                font-weight: 500;
                padding: 8px 12px;
            }}
            
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                color: {self.colors['text_primary'].name()};
            }}
        """
    
    def get_status_bar_style(self) -> str:
        """
        Get modern status bar styling.
        
        Returns:
            CSS stylesheet string
        """
        return f"""
            QStatusBar {{
                background-color: rgba(0, 0, 0, 0.2);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                color: {self.colors['text_secondary'].name()};
                font: {self.fonts['caption'].pointSize()}pt "{self.fonts['inter']}";
                padding: 4px 16px;
            }}
        """
    
    def get_progress_bar_style(self) -> str:
        """
        Get modern progress bar styling.
        
        Returns:
            CSS stylesheet string
        """
        return f"""
            QProgressBar {{
                background-color: rgba(255, 255, 255, 0.05);
                border: none;
                border-radius: {self.effects['border_radius']}px;
                text-align: center;
                color: {self.colors['text_primary'].name()};
                font: {self.fonts['body_small'].pointSize()}pt "{self.fonts['inter']}";
                font-weight: 500;
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {self.colors['primary'].name()}, 
                    stop:1 {self.colors['primary_light'].name()});
                border-radius: {self.effects['border_radius']}px;
            }}
        """
    
    def get_tooltip_style(self) -> str:
        """
        Get modern tooltip styling.
        
        Returns:
            CSS stylesheet string
        """
        return f"""
            QToolTip {{
                background-color: rgba(0, 0, 0, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                color: {self.colors['text_primary'].name()};
                font: {self.fonts['body_small'].pointSize()}pt "{self.fonts['inter']}";
                padding: 8px 12px;
            }}
        """
    
    def get_modal_style(self) -> str:
        """
        Get modern modal styling.
        
        Returns:
            CSS stylesheet string
        """
        return f"""
            QDialog {{
                background-color: rgba(15, 23, 42, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: {self.effects['border_radius']}px;
            }}
            
            QDialog QLabel {{
                color: {self.colors['text_primary'].name()};
                font: {self.fonts['body_medium'].pointSize()}pt "{self.fonts['inter']}";
            }}
            
            QDialog QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 {self.colors['primary'].name()}, 
                    stop:1 {self.colors['primary_dark'].name()});
                border: none;
                border-radius: {self.effects['border_radius']}px;
                color: white;
                font: {self.fonts['button'].pointSize()}pt "{self.fonts['inter']}";
                font-weight: 500;
                padding: 12px 24px;
                min-height: 44px;
            }}
            
            QDialog QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 {self.colors['primary_light'].name()}, 
                    stop:1 {self.colors['primary'].name()});
            }}
        """
    
    def get_scrollbar_style(self) -> str:
        """
        Get modern scrollbar styling.
        
        Returns:
            CSS stylesheet string
        """
        return f"""
            QScrollBar:vertical {{
                background: transparent;
                width: 8px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                min-height: 20px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: rgba(255, 255, 255, 0.5);
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                background: transparent;
                height: 8px;
                margin: 0px;
            }}
            
            QScrollBar::handle:horizontal {{
                background: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                min-width: 20px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background: rgba(255, 255, 255, 0.5);
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """
    
    def apply_glass_effect_to_widget(self, widget: QWidget, blur_radius: int = None) -> None:
        """
        Apply glassmorphism effect to a widget.
        
        Args:
            widget: The widget to apply the effect to
            blur_radius: Custom blur radius (optional)
        """
        if blur_radius is None:
            blur_radius = self.effects['glass_blur']
        
        # Create blur effect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(blur_radius)
        widget.setGraphicsEffect(blur_effect)
        
        # Set widget properties for glass effect
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        widget.setStyleSheet(self.get_glass_card_style())
    
    def apply_shadow_effect(self, widget: QWidget, color: QColor = None, 
                          blur_radius: int = 20, offset: int = 4) -> None:
        """
        Apply shadow effect to a widget.
        
        Args:
            widget: The widget to apply the effect to
            color: Shadow color (optional)
            blur_radius: Blur radius for shadow
            offset: Shadow offset
        """
        if color is None:
            color = QColor(0, 0, 0, 50)
        
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(blur_radius)
        shadow_effect.setColor(color)
        shadow_effect.setOffset(offset, offset)
        widget.setGraphicsEffect(shadow_effect)
    
    def get_complete_stylesheet(self) -> str:
        """
        Get complete application stylesheet.
        
        Returns:
            Complete CSS stylesheet string
        """
        return f"""
            {self.theme.get_modern_stylesheet("main")}
            
            {self.get_sidebar_style()}
            {self.get_navigation_style()}
            {self.get_status_bar_style()}
            {self.get_progress_bar_style()}
            {self.get_tooltip_style()}
            {self.get_modal_style()}
            {self.get_scrollbar_style()}
        """ 