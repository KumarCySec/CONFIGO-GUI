"""
CONFIGO GUI - Dark Theme
Modern dark theme with glassmorphism effects
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt


class DarkTheme:
    """Modern dark theme with glassmorphism effects"""
    
    def __init__(self):
        self.colors = {
            # Primary colors
            'primary': '#6366f1',
            'primary_dark': '#4f46e5',
            'primary_light': '#818cf8',
            
            # Background colors
            'bg_primary': '#0f0f23',
            'bg_secondary': '#1a1a2e',
            'bg_tertiary': '#16213e',
            'bg_glass': 'rgba(255, 255, 255, 0.1)',
            
            # Text colors
            'text_primary': '#ffffff',
            'text_secondary': '#a1a1aa',
            'text_muted': '#71717a',
            
            # Accent colors
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'info': '#3b82f6',
            
            # Border colors
            'border_primary': 'rgba(255, 255, 255, 0.2)',
            'border_secondary': 'rgba(255, 255, 255, 0.1)',
            
            # Shadow colors
            'shadow_primary': 'rgba(0, 0, 0, 0.3)',
            'shadow_secondary': 'rgba(0, 0, 0, 0.1)',
        }
        
    def apply(self, app_or_widget):
        """Apply the dark theme to the application or widget"""
        if isinstance(app_or_widget, QApplication):
            self._apply_to_app(app_or_widget)
        else:
            self._apply_to_widget(app_or_widget)
            
    def _apply_to_app(self, app: QApplication):
        """Apply theme to the entire application"""
        # Set application-wide stylesheet
        app.setStyleSheet(self._get_global_stylesheet())
        
        # Set custom palette
        palette = self._create_palette()
        app.setPalette(palette)
        
        # Set custom font
        font = QFont("Inter", 10)
        font.setWeight(QFont.Normal)
        app.setFont(font)
        
    def _apply_to_widget(self, widget):
        """Apply theme to a specific widget"""
        widget.setStyleSheet(self._get_widget_stylesheet())
        
    def _create_palette(self) -> QPalette:
        """Create a custom color palette"""
        palette = QPalette()
        
        # Window colors
        palette.setColor(QPalette.Window, QColor(self.colors['bg_primary']))
        palette.setColor(QPalette.WindowText, QColor(self.colors['text_primary']))
        
        # Base colors
        palette.setColor(QPalette.Base, QColor(self.colors['bg_secondary']))
        palette.setColor(QPalette.AlternateBase, QColor(self.colors['bg_tertiary']))
        
        # Text colors
        palette.setColor(QPalette.Text, QColor(self.colors['text_primary']))
        palette.setColor(QPalette.PlaceholderText, QColor(self.colors['text_muted']))
        
        # Button colors
        palette.setColor(QPalette.Button, QColor(self.colors['primary']))
        palette.setColor(QPalette.ButtonText, QColor(self.colors['text_primary']))
        
        # Link colors
        palette.setColor(QPalette.Link, QColor(self.colors['primary_light']))
        palette.setColor(QPalette.LinkVisited, QColor(self.colors['primary_dark']))
        
        # Highlight colors
        palette.setColor(QPalette.Highlight, QColor(self.colors['primary']))
        palette.setColor(QPalette.HighlightedText, QColor(self.colors['text_primary']))
        
        return palette
        
    def _get_global_stylesheet(self) -> str:
        """Get the global stylesheet for the application"""
        return f"""
        /* Global Styles */
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        /* Main Window */
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.colors['bg_primary']}, 
                stop:1 {self.colors['bg_secondary']});
            color: {self.colors['text_primary']};
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background: {self.colors['bg_secondary']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {self.colors['text_muted']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {self.colors['text_secondary']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* Tooltips */
        QToolTip {{
            background: {self.colors['bg_tertiary']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border_primary']};
            border-radius: 8px;
            padding: 8px;
        }}
        
        /* Menu */
        QMenu {{
            background: {self.colors['bg_secondary']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border_primary']};
            border-radius: 8px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 16px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background: {self.colors['primary']};
        }}
        """
        
    def _get_widget_stylesheet(self) -> str:
        """Get stylesheet for specific widgets"""
        return f"""
        /* Widget-specific styles */
        QWidget {{
            background: transparent;
            color: {self.colors['text_primary']};
        }}
        
        /* Frames */
        QFrame {{
            background: {self.colors['bg_glass']};
            border: 1px solid {self.colors['border_primary']};
            border-radius: 12px;
        }}
        
        /* Buttons */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['primary']}, 
                stop:1 {self.colors['primary_dark']});
            color: {self.colors['text_primary']};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 14px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.colors['primary_light']}, 
                stop:1 {self.colors['primary']});
        }}
        
        QPushButton:pressed {{
            background: {self.colors['primary_dark']};
        }}
        
        QPushButton:disabled {{
            background: {self.colors['bg_tertiary']};
            color: {self.colors['text_muted']};
        }}
        
        /* Labels */
        QLabel {{
            color: {self.colors['text_primary']};
            background: transparent;
        }}
        
        /* Line Edits */
        QLineEdit {{
            background: {self.colors['bg_secondary']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border_secondary']};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
        }}
        
        QLineEdit:focus {{
            border: 2px solid {self.colors['primary']};
        }}
        
        /* Text Edits */
        QTextEdit {{
            background: {self.colors['bg_secondary']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border_secondary']};
            border-radius: 8px;
            padding: 12px;
        }}
        
        /* Combo Boxes */
        QComboBox {{
            background: {self.colors['bg_secondary']};
            color: {self.colors['text_primary']};
            border: 1px solid {self.colors['border_secondary']};
            border-radius: 8px;
            padding: 8px 12px;
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {self.colors['text_secondary']};
        }}
        
        /* Progress Bars */
        QProgressBar {{
            background: {self.colors['bg_secondary']};
            border: 1px solid {self.colors['border_secondary']};
            border-radius: 8px;
            text-align: center;
            color: {self.colors['text_primary']};
        }}
        
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.colors['primary']}, 
                stop:1 {self.colors['primary_light']});
            border-radius: 7px;
        }}
        """
        
    def get_color(self, color_name: str) -> str:
        """Get a color by name"""
        return self.colors.get(color_name, '#ffffff')
        
    def get_gradient(self, start_color: str, end_color: str, direction: str = "vertical") -> str:
        """Get a gradient string"""
        if direction == "vertical":
            return f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {start_color}, stop:1 {end_color})"
        else:
            return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {start_color}, stop:1 {end_color})" 