"""
CONFIGO GUI - Sidebar Component
Modern sidebar with glassmorphism effects and smooth navigation
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor


class Sidebar(QWidget):
    """Modern sidebar with glassmorphism effects"""
    
    navigation_changed = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        self.active_item = "welcome"
        
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Setup the sidebar UI"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Logo section
        self.create_logo_section(layout)
        
        # Navigation items
        self.create_navigation_items(layout)
        
        # Spacer
        layout.addStretch()
        
        # Bottom section
        self.create_bottom_section(layout)
        
        # Apply glassmorphism effect
        self.apply_glassmorphism()
        
    def create_logo_section(self, layout):
        """Create the logo section"""
        logo_frame = QFrame()
        logo_frame.setObjectName("logoFrame")
        logo_frame.setStyleSheet("""
            #logoFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                padding: 20px;
            }
        """)
        
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(16, 16, 16, 16)
        
        # Logo text
        logo_label = QLabel("CONFIGO")
        logo_label.setObjectName("logoLabel")
        logo_label.setStyleSheet("""
            #logoLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: 700;
                text-align: center;
            }
        """)
        
        # Subtitle
        subtitle_label = QLabel("Intelligent Development Environment Setup")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setStyleSheet("""
            #subtitleLabel {
                color: #a1a1aa;
                font-size: 12px;
                font-weight: 400;
                text-align: center;
            }
        """)
        subtitle_label.setWordWrap(True)
        
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(subtitle_label)
        
        layout.addWidget(logo_frame)
        
    def create_navigation_items(self, layout):
        """Create navigation menu items"""
        nav_items = [
            {
                "id": "welcome",
                "title": "Welcome",
                "icon": "🏠",
                "description": "Get started with CONFIGO"
            },
            {
                "id": "environment",
                "title": "Environment",
                "icon": "⚙️",
                "description": "Configure your development environment"
            },
            {
                "id": "install",
                "title": "Install",
                "icon": "📦",
                "description": "Install tools and packages"
            }
        ]
        
        self.nav_buttons = {}
        
        for item in nav_items:
            nav_button = self.create_nav_button(item)
            self.nav_buttons[item["id"]] = nav_button
            layout.addWidget(nav_button)
            
    def create_nav_button(self, item):
        """Create a navigation button"""
        button = QPushButton()
        button.setObjectName(f"navButton_{item['id']}")
        button.setCheckable(True)
        button.setFixedHeight(60)
        
        # Create layout for button content
        button_layout = QHBoxLayout(button)
        button_layout.setContentsMargins(16, 12, 16, 12)
        button_layout.setSpacing(12)
        
        # Icon
        icon_label = QLabel(item["icon"])
        icon_label.setStyleSheet("font-size: 20px;")
        button_layout.addWidget(icon_label)
        
        # Text content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        title_label = QLabel(item["title"])
        title_label.setStyleSheet("""
            color: #ffffff;
            font-size: 14px;
            font-weight: 600;
        """)
        
        desc_label = QLabel(item["description"])
        desc_label.setStyleSheet("""
            color: #a1a1aa;
            font-size: 11px;
            font-weight: 400;
        """)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        button_layout.addLayout(text_layout)
        button_layout.addStretch()
        
        # Connect signal
        button.clicked.connect(lambda checked, item_id=item["id"]: self.on_nav_clicked(item_id))
        
        # Apply styles
        button.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                text-align: left;
                padding: 0px;
            }}
            
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            QPushButton:checked {{
                background: rgba(99, 102, 241, 0.2);
                border: 1px solid rgba(99, 102, 241, 0.4);
            }}
        """)
        
        return button
        
    def create_bottom_section(self, layout):
        """Create the bottom section of the sidebar"""
        bottom_frame = QFrame()
        bottom_frame.setObjectName("bottomFrame")
        bottom_frame.setStyleSheet("""
            #bottomFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 16px;
            }
        """)
        
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(12, 12, 12, 12)
        bottom_layout.setSpacing(8)
        
        # Status indicator
        status_label = QLabel("🟢 Ready")
        status_label.setStyleSheet("""
            color: #10b981;
            font-size: 12px;
            font-weight: 500;
        """)
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("""
            color: #71717a;
            font-size: 11px;
        """)
        
        bottom_layout.addWidget(status_label)
        bottom_layout.addWidget(version_label)
        
        layout.addWidget(bottom_frame)
        
    def apply_glassmorphism(self):
        """Apply glassmorphism effect to the sidebar"""
        # Create blur effect
        from PySide6.QtWidgets import QGraphicsBlurEffect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
        
        # Create drop shadow
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        shadow_effect.setOffset(2, 0)
        self.setGraphicsEffect(shadow_effect)
        
    def setup_animations(self):
        """Setup animations for the sidebar"""
        self.animations = {}
        
    def on_nav_clicked(self, item_id):
        """Handle navigation item clicks"""
        # Update active item
        self.set_active_item(item_id)
        
        # Emit navigation signal
        self.navigation_changed.emit(item_id)
        
        # Animate the transition
        self.animate_nav_transition(item_id)
        
    def set_active_item(self, item_id):
        """Set the active navigation item"""
        # Uncheck all buttons
        for button in self.nav_buttons.values():
            button.setChecked(False)
            
        # Check the active button
        if item_id in self.nav_buttons:
            self.nav_buttons[item_id].setChecked(True)
            self.active_item = item_id
            
    def animate_nav_transition(self, item_id):
        """Animate the navigation transition"""
        if item_id in self.nav_buttons:
            button = self.nav_buttons[item_id]
            
            # Create scale animation
            animation = QPropertyAnimation(button, b"geometry")
            animation.setDuration(200)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # Get current geometry
            current_geo = button.geometry()
            
            # Create slightly larger geometry for animation
            animated_geo = current_geo.adjusted(-2, -2, 2, 2)
            
            animation.setStartValue(current_geo)
            animation.setEndValue(animated_geo)
            
            # Reverse animation
            reverse_animation = QPropertyAnimation(button, b"geometry")
            reverse_animation.setDuration(200)
            reverse_animation.setEasingCurve(QEasingCurve.OutCubic)
            reverse_animation.setStartValue(animated_geo)
            reverse_animation.setEndValue(current_geo)
            
            # Chain animations
            animation.finished.connect(reverse_animation.start)
            animation.start()
            
    def paintEvent(self, event):
        """Custom paint event for glassmorphism effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient background
        gradient = QColor(15, 15, 35, 200)  # Semi-transparent dark background
        painter.fillRect(self.rect(), gradient) 