"""
CONFIGO GUI - Environment Selector View
Modern environment selection with glassmorphism cards
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGraphicsDropShadowEffect,
    QScrollArea, QGridLayout, QLineEdit, QTextEdit
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QColor, QPainter


class EnvironmentSelectorView(QWidget):
    """Environment selection screen with modern design"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.selected_template = None
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Setup the environment selector UI"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Header section
        self.create_header_section(layout)
        
        # Template selection
        self.create_template_section(layout)
        
        # Custom input section
        self.create_custom_section(layout)
        
        # Action buttons
        self.create_action_buttons(layout)
        
        # Apply glassmorphism effect
        self.apply_glassmorphism()
        
    def create_header_section(self, layout):
        """Create the header section"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            #headerFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 30px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 30, 30, 30)
        header_layout.setSpacing(16)
        
        # Title
        title_label = QLabel("Configure Your Environment")
        title_label.setObjectName("envTitle")
        title_label.setStyleSheet("""
            #envTitle {
                color: #ffffff;
                font-size: 28px;
                font-weight: 700;
                text-align: center;
            }
        """)
        
        # Subtitle
        subtitle_label = QLabel("Choose a template or describe your needs")
        subtitle_label.setObjectName("envSubtitle")
        subtitle_label.setStyleSheet("""
            #envSubtitle {
                color: #a1a1aa;
                font-size: 16px;
                font-weight: 400;
                text-align: center;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
        
    def create_template_section(self, layout):
        """Create the template selection section"""
        template_frame = QFrame()
        template_frame.setObjectName("templateFrame")
        template_frame.setStyleSheet("""
            #templateFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 30px;
            }
        """)
        
        template_layout = QVBoxLayout(template_frame)
        template_layout.setContentsMargins(30, 30, 30, 30)
        template_layout.setSpacing(20)
        
        # Section title
        section_title = QLabel("Quick Templates")
        section_title.setObjectName("sectionTitle")
        section_title.setStyleSheet("""
            #sectionTitle {
                color: #ffffff;
                font-size: 20px;
                font-weight: 600;
                text-align: center;
            }
        """)
        template_layout.addWidget(section_title)
        
        # Templates grid
        templates_grid = QGridLayout()
        templates_grid.setSpacing(16)
        
        templates = [
            {
                "id": "web_dev",
                "icon": "🌐",
                "title": "Web Development",
                "description": "React, Node.js, TypeScript, and modern web tools",
                "tools": ["Node.js", "React", "TypeScript", "VS Code"]
            },
            {
                "id": "python_dev",
                "icon": "🐍",
                "title": "Python Development",
                "description": "Python, Django, Flask, and data science tools",
                "tools": ["Python", "Django", "Jupyter", "PyCharm"]
            },
            {
                "id": "ai_ml",
                "icon": "🤖",
                "title": "AI/ML Development",
                "description": "TensorFlow, PyTorch, and machine learning tools",
                "tools": ["Python", "TensorFlow", "Jupyter", "CUDA"]
            },
            {
                "id": "mobile_dev",
                "icon": "📱",
                "title": "Mobile Development",
                "description": "React Native, Flutter, and mobile development tools",
                "tools": ["React Native", "Flutter", "Android Studio", "Xcode"]
            },
            {
                "id": "devops",
                "icon": "🔧",
                "title": "DevOps & Cloud",
                "description": "Docker, Kubernetes, AWS, and infrastructure tools",
                "tools": ["Docker", "Kubernetes", "AWS CLI", "Terraform"]
            },
            {
                "id": "game_dev",
                "icon": "🎮",
                "title": "Game Development",
                "description": "Unity, Unreal Engine, and game development tools",
                "tools": ["Unity", "Unreal", "Blender", "Visual Studio"]
            }
        ]
        
        for i, template in enumerate(templates):
            template_card = self.create_template_card(template)
            row = i // 2
            col = i % 2
            templates_grid.addWidget(template_card, row, col)
            
        template_layout.addLayout(templates_grid)
        layout.addWidget(template_frame)
        
    def create_template_card(self, template):
        """Create a template card"""
        card = QFrame()
        card.setObjectName(f"templateCard_{template['id']}")
        card.setCheckable(True)
        card.setStyleSheet(f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame:hover {{
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.25);
            }}
            QFrame:checked {{
                background: rgba(99, 102, 241, 0.2);
                border: 2px solid rgba(99, 102, 241, 0.6);
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)
        
        # Icon and title row
        header_layout = QHBoxLayout()
        
        # Icon
        icon_label = QLabel(template["icon"])
        icon_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(template["title"])
        title_label.setStyleSheet("""
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)
        
        # Description
        desc_label = QLabel(template["description"])
        desc_label.setStyleSheet("""
            color: #a1a1aa;
            font-size: 13px;
            font-weight: 400;
            line-height: 1.4;
        """)
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        # Tools list
        tools_label = QLabel("Tools: " + ", ".join(template["tools"]))
        tools_label.setStyleSheet("""
            color: #71717a;
            font-size: 11px;
            font-weight: 400;
        """)
        card_layout.addWidget(tools_label)
        
        # Connect click event
        card.mousePressEvent = lambda event, t=template: self.on_template_selected(t)
        
        return card
        
    def create_custom_section(self, layout):
        """Create the custom input section"""
        custom_frame = QFrame()
        custom_frame.setObjectName("customFrame")
        custom_frame.setStyleSheet("""
            #customFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 30px;
            }
        """)
        
        custom_layout = QVBoxLayout(custom_frame)
        custom_layout.setContentsMargins(30, 30, 30, 30)
        custom_layout.setSpacing(16)
        
        # Section title
        custom_title = QLabel("Custom Environment")
        custom_title.setObjectName("customTitle")
        custom_title.setStyleSheet("""
            #customTitle {
                color: #ffffff;
                font-size: 20px;
                font-weight: 600;
                text-align: center;
            }
        """)
        custom_layout.addWidget(custom_title)
        
        # Description
        custom_desc = QLabel("Describe your development environment needs in natural language:")
        custom_desc.setStyleSheet("""
            color: #a1a1aa;
            font-size: 14px;
            font-weight: 400;
            text-align: center;
        """)
        custom_layout.addWidget(custom_desc)
        
        # Text input
        self.custom_input = QTextEdit()
        self.custom_input.setPlaceholderText(
            "e.g., 'I need a Python environment for data science with Jupyter, pandas, and matplotlib'"
        )
        self.custom_input.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 2px solid rgba(99, 102, 241, 0.6);
            }
        """)
        self.custom_input.setMaximumHeight(100)
        custom_layout.addWidget(self.custom_input)
        
        layout.addWidget(custom_frame)
        
    def create_action_buttons(self, layout):
        """Create action buttons"""
        buttons_frame = QFrame()
        buttons_frame.setObjectName("buttonsFrame")
        buttons_frame.setStyleSheet("""
            #buttonsFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 30px;
            }
        """)
        
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(30, 30, 30, 30)
        buttons_layout.setSpacing(16)
        
        # Back button
        back_button = QPushButton("← Back")
        back_button.setObjectName("backButton")
        back_button.setStyleSheet("""
            #backButton {
                background: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: 600;
            }
            #backButton:hover {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        back_button.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_button)
        
        buttons_layout.addStretch()
        
        # Generate Plan button
        generate_button = QPushButton("🚀 Generate Installation Plan")
        generate_button.setObjectName("generateButton")
        generate_button.setStyleSheet("""
            #generateButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6366f1, stop:1 #4f46e5);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: 600;
            }
            #generateButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #818cf8, stop:1 #6366f1);
            }
        """)
        generate_button.clicked.connect(self.on_generate_plan)
        buttons_layout.addWidget(generate_button)
        
        layout.addWidget(buttons_frame)
        
    def apply_glassmorphism(self):
        """Apply glassmorphism effect"""
        # Create drop shadow
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(30)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        shadow_effect.setOffset(0, 10)
        self.setGraphicsEffect(shadow_effect)
        
    def setup_animations(self):
        """Setup animations"""
        self.animations = {}
        
        # Animate cards on load
        QTimer.singleShot(100, self.animate_cards)
        
    def animate_cards(self):
        """Animate template cards"""
        # Find all template cards
        for child in self.findChildren(QFrame):
            if "templateCard_" in child.objectName():
                self.animate_card_in(child)
                
    def animate_card_in(self, card):
        """Animate a card in"""
        # Create opacity animation
        opacity_animation = QPropertyAnimation(card, b"windowOpacity")
        opacity_animation.setDuration(400)
        opacity_animation.setStartValue(0.0)
        opacity_animation.setEndValue(1.0)
        opacity_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Create slide animation
        slide_animation = QPropertyAnimation(card, b"geometry")
        slide_animation.setDuration(400)
        slide_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Get current geometry
        current_geo = card.geometry()
        
        # Start from below
        start_geo = current_geo.translated(0, 50)
        
        slide_animation.setStartValue(start_geo)
        slide_animation.setEndValue(current_geo)
        
        # Start animations
        opacity_animation.start()
        slide_animation.start()
        
    def on_template_selected(self, template):
        """Handle template selection"""
        # Uncheck all cards
        for child in self.findChildren(QFrame):
            if "templateCard_" in child.objectName():
                child.setChecked(False)
                
        # Check the selected card
        selected_card = self.findChild(QFrame, f"templateCard_{template['id']}")
        if selected_card:
            selected_card.setChecked(True)
            
        self.selected_template = template
        
        # Clear custom input
        self.custom_input.clear()
        
        if self.parent:
            self.parent.show_toast(f"Selected {template['title']} template", "info")
            
    def on_back(self):
        """Handle back button click"""
        if self.parent:
            self.parent.navigate_to_view("welcome")
            
    def on_generate_plan(self):
        """Handle generate plan button click"""
        # Get the selected template or custom input
        if self.selected_template:
            description = f"Setup {self.selected_template['title']} environment: {self.selected_template['description']}"
        else:
            description = self.custom_input.toPlainText().strip()
            
        if not description:
            if self.parent:
                self.parent.show_toast("Please select a template or enter a description", "warning")
            return
            
        # Store the description for the install plan view
        if self.parent:
            self.parent.install_description = description
            self.parent.navigate_to_view("install")
            self.parent.show_toast("Generating installation plan...", "info")
            
    def paintEvent(self, event):
        """Custom paint event for glassmorphism effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient background
        gradient = QColor(15, 15, 35, 100)  # Semi-transparent dark background
        painter.fillRect(self.rect(), gradient) 