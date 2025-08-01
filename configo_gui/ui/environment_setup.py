"""
CONFIGO GUI - Environment Setup Screen
======================================

The environment setup screen component for CONFIGO GUI application.
Allows users to input their environment requirements and get AI-powered suggestions.

Author: CONFIGO Team
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QLineEdit, QTextEdit,
    QComboBox, QListWidget, QListWidgetItem,
    QGroupBox, QGridLayout, QSizePolicy, QSpacerItem,
    QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon, QPixmap


class EnvironmentSetupScreen(QWidget):
    """
    Environment setup screen for CONFIGO GUI application.
    
    Features:
    - Text input for environment description
    - Quick environment templates
    - AI-powered suggestions
    - Submit button with validation
    - Modern dark theme styling
    """
    
    # Signal emitted when environment setup is requested
    environment_requested = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_connections()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the environment setup screen UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Header section
        self.setup_header_section(main_layout)
        
        # Input section
        self.setup_input_section(main_layout)
        
        # Quick templates section
        self.setup_templates_section(main_layout)
        
        # Suggestions section
        self.setup_suggestions_section(main_layout)
        
        # Submit section
        self.setup_submit_section(main_layout)
    
    def setup_header_section(self, main_layout):
        """Create the header section."""
        # Header container
        header_frame = QFrame()
        header_frame.setObjectName("header-frame")
        header_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel("Environment Setup")
        title_label.setObjectName("title-label")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel(
            "Tell us what kind of development environment you want to set up"
        )
        subtitle_label.setObjectName("subtitle-label")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_frame)
    
    def setup_input_section(self, main_layout):
        """Create the input section."""
        # Input container
        input_group = QGroupBox("Environment Description")
        input_group.setObjectName("input-group")
        input_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        input_layout = QVBoxLayout(input_group)
        
        # Description label
        desc_label = QLabel(
            "Describe what you want to build or the tools you need:"
        )
        desc_label.setObjectName("desc-label")
        input_layout.addWidget(desc_label)
        
        # Text input
        self.environment_input = QTextEdit()
        self.environment_input.setObjectName("environment-input")
        self.environment_input.setPlaceholderText(
            "e.g., 'I want to set up a Python web development environment with Django and PostgreSQL'"
        )
        self.environment_input.setMaximumHeight(120)
        input_layout.addWidget(self.environment_input)
        
        # Character count
        self.char_count_label = QLabel("0 characters")
        self.char_count_label.setObjectName("char-count-label")
        self.char_count_label.setAlignment(Qt.AlignRight)
        input_layout.addWidget(self.char_count_label)
        
        main_layout.addWidget(input_group)
    
    def setup_templates_section(self, main_layout):
        """Create the quick templates section."""
        # Templates container
        templates_group = QGroupBox("Quick Templates")
        templates_group.setObjectName("templates-group")
        templates_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        templates_layout = QVBoxLayout(templates_group)
        
        # Templates description
        templates_desc = QLabel("Choose from common development environments:")
        templates_desc.setObjectName("templates-desc-label")
        templates_layout.addWidget(templates_desc)
        
        # Templates grid
        templates_grid = QGridLayout()
        templates_grid.setSpacing(10)
        
        # Define templates
        templates = [
            ("🐍 Python Web Dev", "Python web development with Django/Flask"),
            ("⚛️ React Development", "React frontend development environment"),
            ("🐘 PHP Development", "PHP web development with Laravel"),
            ("☕ Java Development", "Java development with Spring Boot"),
            ("🔧 DevOps Tools", "DevOps and CI/CD tools setup"),
            ("🤖 AI/ML Environment", "Python AI/ML development with TensorFlow/PyTorch"),
            ("📱 Mobile Development", "React Native or Flutter mobile development"),
            ("🎮 Game Development", "Unity or Unreal Engine game development"),
        ]
        
        # Create template buttons
        self.template_buttons = {}
        for i, (name, desc) in enumerate(templates):
            btn = QPushButton(name)
            btn.setObjectName("template-button")
            btn.setToolTip(desc)
            btn.clicked.connect(lambda checked, d=desc: self.on_template_selected(d))
            self.template_buttons[name] = btn
            
            row = i // 2
            col = i % 2
            templates_grid.addWidget(btn, row, col)
        
        templates_layout.addLayout(templates_grid)
        main_layout.addWidget(templates_group)
    
    def setup_suggestions_section(self, main_layout):
        """Create the AI suggestions section."""
        # Suggestions container
        suggestions_group = QGroupBox("AI Suggestions")
        suggestions_group.setObjectName("suggestions-group")
        suggestions_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        suggestions_layout = QVBoxLayout(suggestions_group)
        
        # Suggestions description
        suggestions_desc = QLabel("AI-powered suggestions based on your input:")
        suggestions_desc.setObjectName("suggestions-desc-label")
        suggestions_layout.addWidget(suggestions_desc)
        
        # Suggestions list
        self.suggestions_list = QListWidget()
        self.suggestions_list.setObjectName("suggestions-list")
        self.suggestions_list.setMaximumHeight(150)
        suggestions_layout.addWidget(self.suggestions_list)
        
        main_layout.addWidget(suggestions_group)
    
    def setup_submit_section(self, main_layout):
        """Create the submit section."""
        # Submit container
        submit_frame = QFrame()
        submit_frame.setObjectName("submit-frame")
        submit_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        submit_layout = QHBoxLayout(submit_frame)
        submit_layout.setAlignment(Qt.AlignCenter)
        
        # Submit button
        self.submit_button = QPushButton("🚀 Generate Setup Plan")
        self.submit_button.setObjectName("submit-button")
        self.submit_button.setMinimumSize(250, 50)
        self.submit_button.clicked.connect(self.on_submit_clicked)
        submit_layout.addWidget(self.submit_button)
        
        main_layout.addWidget(submit_frame)
    
    def setup_connections(self):
        """Setup signal connections."""
        # Connect text input to character count
        self.environment_input.textChanged.connect(self.on_text_changed)
        
        # Connect submit button
        self.submit_button.clicked.connect(self.on_submit_clicked)
    
    def setup_styling(self):
        """Apply custom styling to the environment setup screen."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            #title-label {
                font-size: 32px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 10px;
            }
            
            #subtitle-label {
                font-size: 18px;
                color: #cccccc;
                margin-bottom: 20px;
            }
            
            #desc-label {
                font-size: 14px;
                color: #cccccc;
                margin-bottom: 10px;
            }
            
            #environment-input {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                padding: 10px;
            }
            
            #environment-input:focus {
                border-color: #0066cc;
            }
            
            #char-count-label {
                font-size: 12px;
                color: #888888;
            }
            
            #templates-desc-label, #suggestions-desc-label {
                font-size: 14px;
                color: #cccccc;
                margin-bottom: 10px;
            }
            
            #template-button {
                background-color: #404040;
                border: none;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 12px 16px;
                text-align: left;
            }
            
            #template-button:hover {
                background-color: #505050;
            }
            
            #template-button:pressed {
                background-color: #0066cc;
            }
            
            #suggestions-list {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            
            #suggestions-list::item {
                padding: 8px;
                border-bottom: 1px solid #404040;
            }
            
            #suggestions-list::item:hover {
                background-color: #404040;
            }
            
            #submit-frame {
                background-color: transparent;
            }
            
            #submit-button {
                background-color: #0066cc;
                border: none;
                border-radius: 25px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 250px;
                min-height: 50px;
            }
            
            #submit-button:hover {
                background-color: #0077ee;
            }
            
            #submit-button:pressed {
                background-color: #0052a3;
            }
            
            #submit-button:disabled {
                background-color: #404040;
                color: #888888;
            }
        """)
    
    def on_text_changed(self):
        """Handle text input changes."""
        text = self.environment_input.toPlainText()
        char_count = len(text)
        self.char_count_label.setText(f"{char_count} characters")
        
        # Update submit button state
        self.submit_button.setEnabled(char_count > 0)
        
        # Generate suggestions based on input
        self.generate_suggestions(text)
    
    def on_template_selected(self, template_desc: str):
        """Handle template selection."""
        self.environment_input.setPlainText(template_desc)
    
    def generate_suggestions(self, text: str):
        """Generate AI suggestions based on input text."""
        # Clear existing suggestions
        self.suggestions_list.clear()
        
        if not text.strip():
            return
        
        # Simple keyword-based suggestions (in a real app, this would use AI)
        suggestions = []
        
        text_lower = text.lower()
        
        if "python" in text_lower or "django" in text_lower or "flask" in text_lower:
            suggestions.extend([
                "Python 3.11+",
                "pip and virtualenv",
                "Django or Flask framework",
                "PostgreSQL or SQLite database"
            ])
        
        if "react" in text_lower or "javascript" in text_lower or "node" in text_lower:
            suggestions.extend([
                "Node.js and npm",
                "React development tools",
                "ESLint and Prettier",
                "Webpack or Vite"
            ])
        
        if "ai" in text_lower or "ml" in text_lower or "tensorflow" in text_lower:
            suggestions.extend([
                "Python 3.11+",
                "TensorFlow or PyTorch",
                "Jupyter Notebook",
                "CUDA for GPU support"
            ])
        
        if "devops" in text_lower or "docker" in text_lower:
            suggestions.extend([
                "Docker and Docker Compose",
                "Git and GitHub CLI",
                "CI/CD tools (GitHub Actions)",
                "Kubernetes (optional)"
            ])
        
        # Add suggestions to list
        for suggestion in suggestions:
            item = QListWidgetItem(f"💡 {suggestion}")
            self.suggestions_list.addItem(item)
    
    def on_submit_clicked(self):
        """Handle submit button click."""
        environment_desc = self.environment_input.toPlainText().strip()
        
        if not environment_desc:
            QMessageBox.warning(self, "Input Required", "Please describe the environment you want to set up.")
            return
        
        # Emit signal with environment description
        self.environment_requested.emit(environment_desc) 