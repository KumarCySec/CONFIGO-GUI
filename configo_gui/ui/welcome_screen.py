"""
CONFIGO GUI - Welcome Screen
============================

The welcome screen component for CONFIGO GUI application.
Displays the logo, tagline, and start button.

Author: CONFIGO Team
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap, QIcon


class WelcomeScreen(QWidget):
    """
    Welcome screen for CONFIGO GUI application.
    
    Features:
    - Animated logo and title
    - Welcome message and tagline
    - Start button with hover effects
    - Modern dark theme styling
    """
    
    # Signal emitted when start button is clicked
    start_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_animations()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the welcome screen UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Add top spacer
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(top_spacer)
        
        # Logo and title section
        self.setup_logo_section(main_layout)
        
        # Welcome message section
        self.setup_welcome_message(main_layout)
        
        # Start button section
        self.setup_start_button(main_layout)
        
        # Add bottom spacer
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(bottom_spacer)
    
    def setup_logo_section(self, main_layout):
        """Create the logo and title section."""
        # Logo container
        logo_frame = QFrame()
        logo_frame.setObjectName("logo-frame")
        logo_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setAlignment(Qt.AlignCenter)
        
        # Logo icon (placeholder - you can replace with actual logo)
        self.logo_label = QLabel("🤖")
        self.logo_label.setObjectName("logo-icon")
        self.logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.logo_label)
        
        # Title
        self.title_label = QLabel("CONFIGO")
        self.title_label.setObjectName("title-label")
        self.title_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("AI Setup Agent")
        self.subtitle_label.setObjectName("subtitle-label")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.subtitle_label)
        
        main_layout.addWidget(logo_frame)
    
    def setup_welcome_message(self, main_layout):
        """Create the welcome message section."""
        # Welcome message container
        message_frame = QFrame()
        message_frame.setObjectName("message-frame")
        message_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        message_layout = QVBoxLayout(message_frame)
        message_layout.setAlignment(Qt.AlignCenter)
        
        # Welcome message
        self.welcome_label = QLabel(
            "Welcome to CONFIGO, your intelligent development environment setup assistant!"
        )
        self.welcome_label.setObjectName("welcome-label")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setWordWrap(True)
        message_layout.addWidget(self.welcome_label)
        
        # Description
        self.description_label = QLabel(
            "CONFIGO uses AI to intelligently install tools, handle extensions, "
            "perform validation, and automate your development environment setup. "
            "Just tell us what you want to build, and we'll handle the rest!"
        )
        self.description_label.setObjectName("description-label")
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)
        message_layout.addWidget(self.description_label)
        
        main_layout.addWidget(message_frame)
    
    def setup_start_button(self, main_layout):
        """Create the start button section."""
        # Button container
        button_frame = QFrame()
        button_frame.setObjectName("button-frame")
        button_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        button_layout = QHBoxLayout(button_frame)
        button_layout.setAlignment(Qt.AlignCenter)
        
        # Start button
        self.start_button = QPushButton("🚀 Start Setup")
        self.start_button.setObjectName("start-button")
        self.start_button.setMinimumSize(200, 50)
        self.start_button.clicked.connect(self.on_start_clicked)
        button_layout.addWidget(self.start_button)
        
        main_layout.addWidget(button_frame)
    
    def setup_animations(self):
        """Setup animations for the welcome screen."""
        # Fade in animation for logo
        self.logo_animation = QPropertyAnimation(self.logo_label, b"styleSheet")
        self.logo_animation.setDuration(1000)
        self.logo_animation.setStartValue("opacity: 0;")
        self.logo_animation.setEndValue("opacity: 1;")
        self.logo_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Start animation when widget is shown
        self.start_animation()
    
    def setup_styling(self):
        """Apply custom styling to the welcome screen."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            
            #logo-frame {
                background-color: transparent;
            }
            
            #logo-icon {
                font-size: 80px;
                color: #0066cc;
                margin-bottom: 20px;
            }
            
            #title-label {
                font-size: 48px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 10px;
            }
            
            #subtitle-label {
                font-size: 24px;
                color: #cccccc;
                margin-bottom: 40px;
            }
            
            #message-frame {
                background-color: transparent;
                padding: 20px;
            }
            
            #welcome-label {
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 15px;
            }
            
            #description-label {
                font-size: 16px;
                color: #cccccc;
                line-height: 1.5;
                margin-bottom: 30px;
            }
            
            #button-frame {
                background-color: transparent;
            }
            
            #start-button {
                background-color: #0066cc;
                border: none;
                border-radius: 25px;
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 200px;
                min-height: 50px;
            }
            
            #start-button:hover {
                background-color: #0077ee;
                transform: scale(1.05);
            }
            
            #start-button:pressed {
                background-color: #0052a3;
                transform: scale(0.95);
            }
        """)
    
    def start_animation(self):
        """Start the welcome screen animations."""
        self.logo_animation.start()
    
    def on_start_clicked(self):
        """Handle start button click."""
        self.start_clicked.emit()
    
    def showEvent(self, event):
        """Handle show event to start animations."""
        super().showEvent(event)
        self.start_animation() 