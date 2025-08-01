"""
CONFIGO GUI - Predictive AI Suggestions
=======================================

The predictive AI suggestions component for CONFIGO GUI application.
Recommends tools based on user's development profile and system information.

Features:
- AI-powered tool recommendations
- Context-aware suggestions
- System information analysis
- Development profile detection
- Smart categorization

Author: CONFIGO Team
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QSizePolicy,
    QSpacerItem, QGroupBox, QGridLayout, QProgressBar,
    QListWidget, QListWidgetItem, QTextEdit, QSplitter
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QThread
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor


class ToolCard(QWidget):
    """Individual tool recommendation card."""
    
    def __init__(self, tool_info: Dict[str, Any]):
        super().__init__()
        self.tool_info = tool_info
        self.setup_ui()
        self.setup_styling()
    
    def setup_ui(self):
        """Setup the tool card UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Tool header
        header_layout = QHBoxLayout()
        
        # Tool icon
        icon_label = QLabel(self.tool_info.get("icon", "🔧"))
        icon_label.setObjectName("tool-icon")
        header_layout.addWidget(icon_label)
        
        # Tool name
        name_label = QLabel(self.tool_info["name"])
        name_label.setObjectName("tool-name")
        header_layout.addWidget(name_label)
        
        header_layout.addStretch()
        
        # Confidence score
        confidence = self.tool_info.get("confidence", 0)
        confidence_label = QLabel(f"{confidence}%")
        confidence_label.setObjectName("confidence-score")
        header_layout.addWidget(confidence_label)
        
        layout.addLayout(header_layout)
        
        # Tool description
        desc_label = QLabel(self.tool_info.get("description", ""))
        desc_label.setObjectName("tool-description")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Tool category
        category_label = QLabel(f"Category: {self.tool_info.get('category', 'General')}")
        category_label.setObjectName("tool-category")
        layout.addWidget(category_label)
        
        # Install button
        self.install_button = QPushButton("Install")
        self.install_button.setObjectName("install-button")
        self.install_button.clicked.connect(self.on_install_clicked)
        layout.addWidget(self.install_button)
    
    def setup_styling(self):
        """Apply styling to the tool card."""
        confidence = self.tool_info.get("confidence", 0)
        
        if confidence >= 80:
            border_color = "#4CAF50"  # Green for high confidence
        elif confidence >= 60:
            border_color = "#FF9800"  # Orange for medium confidence
        else:
            border_color = "#F44336"  # Red for low confidence
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #2c2c2c;
                border: 2px solid {border_color};
                border-radius: 10px;
                color: #ffffff;
            }}
            
            #tool-icon {{
                font-size: 24px;
                margin-right: 10px;
            }}
            
            #tool-name {{
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
            }}
            
            #confidence-score {{
                font-size: 12px;
                color: {border_color};
                font-weight: bold;
            }}
            
            #tool-description {{
                font-size: 14px;
                color: #cccccc;
                line-height: 1.4;
            }}
            
            #tool-category {{
                font-size: 12px;
                color: #888888;
                font-style: italic;
            }}
            
            #install-button {{
                background-color: {border_color};
                border: none;
                border-radius: 5px;
                color: #ffffff;
                padding: 8px 16px;
                font-weight: bold;
                margin-top: 10px;
            }}
            
            #install-button:hover {{
                background-color: {border_color}dd;
            }}
        """)
    
    def on_install_clicked(self):
        """Handle install button click."""
        # This will be connected by parent widget
        pass


class PredictiveSuggestionsPanel(QWidget):
    """
    Predictive AI Suggestions Panel for CONFIGO GUI application.
    
    Features:
    - AI-powered tool recommendations
    - Context-aware suggestions
    - System information analysis
    - Development profile detection
    - Smart categorization
    """
    
    # Signals
    tool_selected = Signal(dict)  # Emitted when a tool is selected for installation
    profile_updated = Signal(dict)  # Emitted when user profile is updated
    
    def __init__(self):
        super().__init__()
        self.system_info = {}
        self.user_profile = {}
        self.tool_recommendations = []
        self.setup_ui()
        self.setup_connections()
        self.setup_styling()
        
        # Load initial data
        self.load_system_info()
        self.generate_recommendations()
    
    def setup_ui(self):
        """Initialize the predictive suggestions panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self.setup_header(layout)
        
        # Main content area
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - System info and profile
        self.setup_left_panel(content_splitter)
        
        # Right panel - Tool recommendations
        self.setup_right_panel(content_splitter)
        
        content_splitter.setSizes([400, 600])
        layout.addWidget(content_splitter)
    
    def setup_header(self, layout):
        """Setup the header section."""
        header = QFrame()
        header.setObjectName("suggestions-header")
        header.setMaximumHeight(60)
        
        header_layout = QHBoxLayout(header)
        
        # Icon and title
        icon_label = QLabel("🧠")
        icon_label.setObjectName("suggestions-icon")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel("AI-Powered Suggestions")
        title_label.setObjectName("suggestions-title")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Refresh button
        refresh_button = QPushButton("🔄 Refresh")
        refresh_button.setObjectName("refresh-button")
        refresh_button.clicked.connect(self.refresh_suggestions)
        header_layout.addWidget(refresh_button)
        
        layout.addWidget(header)
    
    def setup_left_panel(self, splitter):
        """Setup the left panel with system info and profile."""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # System Information
        self.setup_system_info_section(left_layout)
        
        # User Profile
        self.setup_user_profile_section(left_layout)
        
        splitter.addWidget(left_widget)
    
    def setup_system_info_section(self, layout):
        """Setup the system information section."""
        group_box = QGroupBox("System Information")
        group_box.setObjectName("info-group")
        
        group_layout = QVBoxLayout(group_box)
        
        # System info display
        self.system_info_text = QTextEdit()
        self.system_info_text.setObjectName("system-info-text")
        self.system_info_text.setReadOnly(True)
        self.system_info_text.setMaximumHeight(150)
        group_layout.addWidget(self.system_info_text)
        
        layout.addWidget(group_box)
    
    def setup_user_profile_section(self, layout):
        """Setup the user profile section."""
        group_box = QGroupBox("Development Profile")
        group_box.setObjectName("profile-group")
        
        group_layout = QVBoxLayout(group_box)
        
        # Profile questions
        self.setup_profile_questions(group_layout)
        
        layout.addWidget(group_box)
    
    def setup_profile_questions(self, layout):
        """Setup profile questions for user input."""
        questions = [
            "What type of developer are you?",
            "What programming languages do you use?",
            "What frameworks do you work with?",
            "What's your primary development focus?"
        ]
        
        self.profile_answers = {}
        
        for question in questions:
            question_label = QLabel(question)
            question_label.setObjectName("profile-question")
            layout.addWidget(question_label)
            
            answer_input = QTextEdit()
            answer_input.setObjectName("profile-answer")
            answer_input.setMaximumHeight(60)
            answer_input.setPlaceholderText("Enter your answer...")
            answer_input.textChanged.connect(lambda: self.update_profile())
            layout.addWidget(answer_input)
            
            self.profile_answers[question] = answer_input
    
    def setup_right_panel(self, splitter):
        """Setup the right panel with tool recommendations."""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Recommendations header
        header_label = QLabel("Recommended Tools")
        header_label.setObjectName("recommendations-header")
        right_layout.addWidget(header_label)
        
        # Tool recommendations scroll area
        self.setup_recommendations_area(right_layout)
        
        splitter.addWidget(right_widget)
    
    def setup_recommendations_area(self, layout):
        """Setup the tool recommendations scroll area."""
        # Scroll area for recommendations
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Recommendations widget
        self.recommendations_widget = QWidget()
        self.recommendations_layout = QGridLayout(self.recommendations_widget)
        self.recommendations_layout.setAlignment(Qt.AlignTop)
        self.recommendations_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.recommendations_widget)
        layout.addWidget(self.scroll_area)
    
    def setup_connections(self):
        """Setup signal connections."""
        pass  # Will be connected by parent widget
    
    def setup_styling(self):
        """Apply styling to the predictive suggestions panel."""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            
            #suggestions-header {
                background-color: #2c2c2c;
                border-bottom: 1px solid #3c3c3c;
                padding: 10px;
            }
            
            #suggestions-icon {
                font-size: 24px;
                margin-right: 10px;
            }
            
            #suggestions-title {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #refresh-button {
                background-color: #0066cc;
                border: none;
                border-radius: 15px;
                color: #ffffff;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            #refresh-button:hover {
                background-color: #0077ee;
            }
            
            #info-group, #profile-group {
                background-color: #2c2c2c;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                margin: 5px;
                padding: 10px;
            }
            
            #info-group::title, #profile-group::title {
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            
            #system-info-text {
                background-color: #3c3c3c;
                border: 1px solid #4c4c4c;
                border-radius: 5px;
                color: #ffffff;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
            
            #profile-question {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                margin-top: 10px;
            }
            
            #profile-answer {
                background-color: #3c3c3c;
                border: 1px solid #4c4c4c;
                border-radius: 5px;
                color: #ffffff;
                font-size: 12px;
            }
            
            #profile-answer:focus {
                border-color: #0066cc;
            }
            
            #recommendations-header {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                margin: 10px;
            }
            
            QScrollBar:vertical {
                background-color: #2c2c2c;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #4c4c4c;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #5c5c5c;
            }
        """)
    
    def load_system_info(self):
        """Load system information."""
        try:
            import platform
            import psutil
            
            self.system_info = {
                "os": platform.system(),
                "os_version": platform.release(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "memory": f"{psutil.virtual_memory().total // (1024**3)} GB",
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count()
            }
            
            # Update display
            info_text = ""
            for key, value in self.system_info.items():
                info_text += f"{key.replace('_', ' ').title()}: {value}\n"
            
            self.system_info_text.setPlainText(info_text)
            
        except ImportError:
            self.system_info_text.setPlainText("System information unavailable")
    
    def update_profile(self):
        """Update user profile based on answers."""
        self.user_profile = {}
        
        for question, answer_widget in self.profile_answers.items():
            answer = answer_widget.toPlainText().strip()
            if answer:
                self.user_profile[question] = answer
        
        # Emit profile update signal
        if self.user_profile:
            self.profile_updated.emit(self.user_profile)
    
    def generate_recommendations(self):
        """Generate tool recommendations based on system info and profile."""
        # Clear existing recommendations
        for i in reversed(range(self.recommendations_layout.count())):
            widget = self.recommendations_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Generate recommendations based on system info and profile
        recommendations = self.analyze_and_recommend()
        
        # Add recommendation cards
        row = 0
        col = 0
        max_cols = 2
        
        for tool_info in recommendations:
            card = ToolCard(tool_info)
            card.install_button.clicked.connect(lambda checked, info=tool_info: self.on_tool_selected(info))
            
            self.recommendations_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def analyze_and_recommend(self) -> List[Dict[str, Any]]:
        """Analyze system info and profile to generate recommendations."""
        recommendations = []
        
        # Base recommendations based on OS
        os_type = self.system_info.get("os", "").lower()
        
        if "linux" in os_type:
            recommendations.extend([
                {
                    "name": "Docker",
                    "description": "Container platform for development and deployment",
                    "category": "DevOps",
                    "confidence": 85,
                    "icon": "🐳"
                },
                {
                    "name": "Git",
                    "description": "Version control system",
                    "category": "Development",
                    "confidence": 95,
                    "icon": "📝"
                },
                {
                    "name": "VS Code",
                    "description": "Lightweight code editor with extensions",
                    "category": "IDE",
                    "confidence": 90,
                    "icon": "💻"
                }
            ])
        
        # Profile-based recommendations
        profile_text = " ".join(self.user_profile.values()).lower()
        
        if "python" in profile_text:
            recommendations.extend([
                {
                    "name": "PyCharm",
                    "description": "Python IDE with advanced features",
                    "category": "IDE",
                    "confidence": 80,
                    "icon": "🐍"
                },
                {
                    "name": "pip",
                    "description": "Python package installer",
                    "category": "Package Manager",
                    "confidence": 95,
                    "icon": "📦"
                }
            ])
        
        if "javascript" in profile_text or "node" in profile_text:
            recommendations.extend([
                {
                    "name": "Node.js",
                    "description": "JavaScript runtime environment",
                    "category": "Runtime",
                    "confidence": 90,
                    "icon": "🟢"
                },
                {
                    "name": "npm",
                    "description": "Node.js package manager",
                    "category": "Package Manager",
                    "confidence": 95,
                    "icon": "📦"
                }
            ])
        
        if "web" in profile_text or "frontend" in profile_text:
            recommendations.extend([
                {
                    "name": "Chrome DevTools",
                    "description": "Web development tools",
                    "category": "Development Tools",
                    "confidence": 85,
                    "icon": "🌐"
                },
                {
                    "name": "Postman",
                    "description": "API development and testing",
                    "category": "API Tools",
                    "confidence": 75,
                    "icon": "📮"
                }
            ])
        
        # Sort by confidence
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def on_tool_selected(self, tool_info: Dict[str, Any]):
        """Handle tool selection."""
        self.tool_selected.emit(tool_info)
    
    def refresh_suggestions(self):
        """Refresh tool recommendations."""
        self.load_system_info()
        self.update_profile()
        self.generate_recommendations()
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get current system information."""
        return self.system_info.copy()
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Get current user profile."""
        return self.user_profile.copy() 