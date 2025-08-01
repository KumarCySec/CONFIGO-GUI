"""
CONFIGO GUI - Tool Card Component
=================================

Modern tool card component for displaying tool information and status.
Provides interactive cards for tools with installation status and actions.

Author: CONFIGO Team
"""

from typing import Optional, Dict, Any
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QColor, QFont, QPixmap, QPainter


class ToolCard(QFrame):
    """
    Modern tool card component for displaying tool information.
    
    Features:
    - Tool information display (name, version, description)
    - Installation status indicators
    - Action buttons (install, uninstall, update)
    - Hover effects and animations
    """
    
    # Signals
    install_clicked = Signal(str)  # Emitted with tool name
    uninstall_clicked = Signal(str)
    update_clicked = Signal(str)
    
    def __init__(self, tool_info: Dict[str, Any], theme=None, parent=None):
        super().__init__(parent)
        
        self.theme = theme
        self.tool_info = tool_info
        self.tool_name = tool_info.get('name', 'Unknown Tool')
        
        # Setup UI
        self.setup_ui()
        self.setup_animations()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the tool card UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Header with icon and name
        header_layout = QHBoxLayout()
        
        # Tool icon (placeholder)
        icon_label = QLabel("🔧")
        icon_label.setFont(QFont("Arial", 24))
        header_layout.addWidget(icon_label)
        
        # Tool name and version
        name_layout = QVBoxLayout()
        name_label = QLabel(self.tool_name)
        if self.theme:
            name_label.setFont(self.theme.fonts['heading_small'])
        name_layout.addWidget(name_label)
        
        version = self.tool_info.get('version', 'Unknown')
        version_label = QLabel(f"v{version}")
        if self.theme:
            version_label.setFont(self.theme.fonts['body_small'])
            version_label.setStyleSheet(f"color: {self.theme.colors['text_secondary'].name()};")
        name_layout.addWidget(version_label)
        
        header_layout.addLayout(name_layout)
        header_layout.addStretch()
        
        # Status badge
        status = self.tool_info.get('status', 'unknown')
        self.status_badge = QLabel(status.upper())
        self.status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.status_badge)
        
        layout.addLayout(header_layout)
        
        # Description
        description = self.tool_info.get('description', 'No description available.')
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        if self.theme:
            desc_label.setFont(self.theme.fonts['body_medium'])
        layout.addWidget(desc_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        # Install button
        self.install_button = QPushButton("Install")
        self.install_button.clicked.connect(lambda: self.install_clicked.emit(self.tool_name))
        button_layout.addWidget(self.install_button)
        
        # Uninstall button
        self.uninstall_button = QPushButton("Uninstall")
        self.uninstall_button.clicked.connect(lambda: self.uninstall_clicked.emit(self.tool_name))
        button_layout.addWidget(self.uninstall_button)
        
        # Update button
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(lambda: self.update_clicked.emit(self.tool_name))
        button_layout.addWidget(self.update_button)
        
        layout.addLayout(button_layout)
    
    def setup_animations(self):
        """Setup card animations."""
        # Hover animation
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def setup_styling(self):
        """Apply tool card styling."""
        if not self.theme:
            return
        
        # Get status color
        status = self.tool_info.get('status', 'unknown')
        status_colors = {
            'installed': self.theme.colors['accent'],
            'not_installed': self.theme.colors['text_secondary'],
            'updating': self.theme.colors['warning'],
            'error': self.theme.colors['error'],
            'unknown': self.theme.colors['text_muted']
        }
        
        status_color = status_colors.get(status, self.theme.colors['text_muted'])
        
        self.setStyleSheet(f"""
            ToolCard {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: {self.theme.effects['border_radius']}px;
                padding: 16px;
            }}
            
            ToolCard:hover {{
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 {self.theme.colors['primary'].name()}, 
                    stop:1 {self.theme.colors['primary_dark'].name()});
                border: none;
                border-radius: 6px;
                color: white;
                font: {self.theme.fonts['body_small'].pointSize()}pt "{self.theme.fonts['inter']}";
                font-weight: 500;
                padding: 8px 16px;
                min-height: 32px;
            }}
            
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 {self.theme.colors['primary_light'].name()}, 
                    stop:1 {self.theme.colors['primary'].name()});
            }}
        """)
        
        # Style status badge
        self.status_badge.setStyleSheet(f"""
            QLabel {{
                background-color: rgba({status_color.red()}, {status_color.green()}, {status_color.blue()}, 0.2);
                border: 1px solid rgba({status_color.red()}, {status_color.green()}, {status_color.blue()}, 0.5);
                border-radius: 8px;
                color: {status_color.name()};
                font: {self.theme.fonts['caption'].pointSize()}pt "{self.theme.fonts['inter']}";
                font-weight: 500;
                padding: 4px 8px;
            }}
        """)
    
    def update_status(self, status: str):
        """Update tool status."""
        self.tool_info['status'] = status
        self.setup_styling()
    
    def set_buttons_enabled(self, install: bool = True, uninstall: bool = True, update: bool = True):
        """Enable/disable action buttons."""
        self.install_button.setEnabled(install)
        self.uninstall_button.setEnabled(uninstall)
        self.update_button.setEnabled(update) 