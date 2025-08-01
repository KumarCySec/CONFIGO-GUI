"""
CONFIGO GUI - Welcome View
Beautiful welcome screen with glassmorphism effects
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGraphicsDropShadowEffect,
    QScrollArea, QGridLayout
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont, QColor, QPainter, QPixmap


class WelcomeView(QWidget):
    """Welcome screen with modern design"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Setup the welcome UI"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Header section
        self.create_header_section(layout)
        
        # Features section
        self.create_features_section(layout)
        
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
                padding: 40px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(40, 40, 40, 40)
        header_layout.setSpacing(20)
        
        # Welcome title
        title_label = QLabel("Welcome to CONFIGO")
        title_label.setObjectName("welcomeTitle")
        title_label.setStyleSheet("""
            #welcomeTitle {
                color: #ffffff;
                font-size: 36px;
                font-weight: 700;
                text-align: center;
            }
        """)
        
        # Subtitle
        subtitle_label = QLabel("Intelligent Development Environment Setup")
        subtitle_label.setObjectName("welcomeSubtitle")
        subtitle_label.setStyleSheet("""
            #welcomeSubtitle {
                color: #a1a1aa;
                font-size: 18px;
                font-weight: 400;
                text-align: center;
            }
        """)
        
        # Description
        description_label = QLabel(
            "CONFIGO is your AI-powered assistant for setting up development environments. "
            "Describe your needs in natural language and let CONFIGO handle the rest."
        )
        description_label.setObjectName("welcomeDescription")
        description_label.setStyleSheet("""
            #welcomeDescription {
                color: #d1d5db;
                font-size: 16px;
                font-weight: 400;
                text-align: center;
                line-height: 1.6;
            }
        """)
        description_label.setWordWrap(True)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addWidget(description_label)
        
        layout.addWidget(header_frame)
        
    def create_features_section(self, layout):
        """Create the features section"""
        features_frame = QFrame()
        features_frame.setObjectName("featuresFrame")
        features_frame.setStyleSheet("""
            #featuresFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 30px;
            }
        """)
        
        features_layout = QVBoxLayout(features_frame)
        features_layout.setContentsMargins(30, 30, 30, 30)
        features_layout.setSpacing(24)
        
        # Features title
        features_title = QLabel("Key Features")
        features_title.setObjectName("featuresTitle")
        features_title.setStyleSheet("""
            #featuresTitle {
                color: #ffffff;
                font-size: 24px;
                font-weight: 600;
                text-align: center;
            }
        """)
        features_layout.addWidget(features_title)
        
        # Features grid
        features_grid = QGridLayout()
        features_grid.setSpacing(20)
        
        features = [
            {
                "icon": "🧠",
                "title": "AI-Powered",
                "description": "Intelligent tool recommendations using Google Gemini"
            },
            {
                "icon": "💾",
                "title": "Memory System",
                "description": "Remembers your preferences and installation history"
            },
            {
                "icon": "🔧",
                "title": "Self-Healing",
                "description": "Automatically fixes installation failures"
            },
            {
                "icon": "🎯",
                "title": "Domain Aware",
                "description": "Understands different development domains"
            },
            {
                "icon": "📱",
                "title": "Natural Language",
                "description": "Install apps with simple commands"
            },
            {
                "icon": "🌐",
                "title": "Portal Integration",
                "description": "Automated login portal management"
            }
        ]
        
        for i, feature in enumerate(features):
            feature_card = self.create_feature_card(feature)
            row = i // 2
            col = i % 2
            features_grid.addWidget(feature_card, row, col)
            
        features_layout.addLayout(features_grid)
        layout.addWidget(features_frame)
        
    def create_feature_card(self, feature):
        """Create a feature card"""
        card = QFrame()
        card.setObjectName("featureCard")
        card.setStyleSheet("""
            #featureCard {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 20px;
            }
            #featureCard:hover {
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.25);
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)
        
        # Icon
        icon_label = QLabel(feature["icon"])
        icon_label.setStyleSheet("font-size: 32px; text-align: center;")
        card_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(feature["title"])
        title_label.setStyleSheet("""
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
            text-align: center;
        """)
        card_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(feature["description"])
        desc_label.setStyleSheet("""
            color: #a1a1aa;
            font-size: 13px;
            font-weight: 400;
            text-align: center;
            line-height: 1.4;
        """)
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        return card
        
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
        
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(30, 30, 30, 30)
        buttons_layout.setSpacing(16)
        
        # Buttons title
        buttons_title = QLabel("Get Started")
        buttons_title.setObjectName("buttonsTitle")
        buttons_title.setStyleSheet("""
            #buttonsTitle {
                color: #ffffff;
                font-size: 20px;
                font-weight: 600;
                text-align: center;
            }
        """)
        buttons_layout.addWidget(buttons_title)
        
        # Buttons layout
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(16)
        
        # Start Setup button
        start_button = QPushButton("🚀 Start Environment Setup")
        start_button.setObjectName("startButton")
        start_button.setStyleSheet("""
            #startButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6366f1, stop:1 #4f46e5);
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: 600;
            }
            #startButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #818cf8, stop:1 #6366f1);
            }
        """)
        start_button.clicked.connect(self.on_start_setup)
        buttons_row.addWidget(start_button)
        
        # Quick Install button
        install_button = QPushButton("📦 Quick App Install")
        install_button.setObjectName("installButton")
        install_button.setStyleSheet("""
            #installButton {
                background: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: 600;
            }
            #installButton:hover {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        install_button.clicked.connect(self.on_quick_install)
        buttons_row.addWidget(install_button)
        
        buttons_layout.addLayout(buttons_row)
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
        """Animate feature cards"""
        # Find all feature cards
        for child in self.findChildren(QFrame):
            if child.objectName() == "featureCard":
                self.animate_card_in(child)
                
    def animate_card_in(self, card):
        """Animate a card in"""
        # Create opacity animation
        opacity_animation = QPropertyAnimation(card, b"windowOpacity")
        opacity_animation.setDuration(500)
        opacity_animation.setStartValue(0.0)
        opacity_animation.setEndValue(1.0)
        opacity_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Create scale animation
        scale_animation = QPropertyAnimation(card, b"geometry")
        scale_animation.setDuration(500)
        scale_animation.setEasingCurve(QEasingCurve.OutBack)
        
        # Get current geometry
        current_geo = card.geometry()
        
        # Start with smaller geometry
        start_geo = current_geo.adjusted(
            current_geo.width() // 4,
            current_geo.height() // 4,
            -current_geo.width() // 4,
            -current_geo.height() // 4
        )
        
        scale_animation.setStartValue(start_geo)
        scale_animation.setEndValue(current_geo)
        
        # Start animations
        opacity_animation.start()
        scale_animation.start()
        
    def on_start_setup(self):
        """Handle start setup button click"""
        if self.parent:
            self.parent.navigate_to_view("environment")
            self.parent.show_toast("Starting environment setup...", "info")
            
    def on_quick_install(self):
        """Handle quick install button click"""
        if self.parent:
            self.parent.navigate_to_view("install")
            self.parent.show_toast("Opening app installer...", "info")
            
    def paintEvent(self, event):
        """Custom paint event for glassmorphism effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient background
        gradient = QColor(15, 15, 35, 100)  # Semi-transparent dark background
        painter.fillRect(self.rect(), gradient) 