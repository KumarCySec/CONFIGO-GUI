#!/usr/bin/env python3
"""
CONFIGO GUI - Modern Demo Application
=====================================

Demo application showcasing the modern CONFIGO GUI features including:
- Glassmorphism effects and animations
- Modern UI components
- Smooth transitions
- Interactive elements

Author: CONFIGO Team
"""

import sys
import os
from pathlib import Path
from typing import Optional

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QGridLayout,
    QTextEdit, QLineEdit, QProgressBar, QTabWidget
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor, QPainter, QLinearGradient
from PySide6.QtCore import QPoint

# Import modern UI components
from ui.themes.glass_theme import GlassTheme
from ui.themes.animations import AnimationManager
from ui.themes.modern_styles import ModernStyles
from ui.components.glass_card import GlassCard
from ui.components.animated_button import AnimatedButton
from ui.components.loading_spinner import LoadingSpinner


class ModernDemoWindow(QMainWindow):
    """
    Demo window showcasing modern CONFIGO GUI features.
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize theme and styling
        self.theme = GlassTheme()
        self.animation_manager = AnimationManager()
        self.modern_styles = ModernStyles(self.theme)
        
        # Setup UI
        self.setup_ui()
        self.setup_animations()
        self.apply_modern_styling()
        
        # Start demo animations
        self.start_demo_animations()
    
    def setup_ui(self):
        """Initialize the demo UI."""
        # Set window properties
        self.setWindowTitle("CONFIGO GUI - Modern Demo")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Enable transparency for glass effect
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create header
        self.setup_header(main_layout)
        
        # Create content area
        self.setup_content(main_layout)
        
        # Create footer
        self.setup_footer(main_layout)
    
    def setup_header(self, main_layout):
        """Setup demo header with title and navigation."""
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("CONFIGO GUI - Modern Demo")
        title_label.setFont(self.theme.fonts['heading_large'])
        title_label.setStyleSheet(f"color: {self.theme.colors['text_primary'].name()};")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Navigation buttons
        nav_buttons = [
            ("Components", "components"),
            ("Animations", "animations"),
            ("Styling", "styling"),
            ("Effects", "effects")
        ]
        
        for text, section in nav_buttons:
            button = AnimatedButton(text, variant="outline", theme=self.theme)
            button.clicked.connect(lambda checked, s=section: self.show_section(s))
            header_layout.addWidget(button)
        
        main_layout.addLayout(header_layout)
    
    def setup_content(self, main_layout):
        """Setup main content area with demo sections."""
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Add demo sections
        self.setup_components_demo(content_layout)
        self.setup_animations_demo(content_layout)
        self.setup_styling_demo(content_layout)
        self.setup_effects_demo(content_layout)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
    
    def setup_components_demo(self, layout):
        """Setup components demo section."""
        # Section title
        title = QLabel("🎨 Modern Components")
        title.setFont(self.theme.fonts['heading_medium'])
        title.setStyleSheet(f"color: {self.theme.colors['text_primary'].name()}; margin-bottom: 16px;")
        layout.addWidget(title)
        
        # Create grid for components
        grid_layout = QGridLayout()
        grid_layout.setSpacing(16)
        
        # Glass Cards
        cards = [
            ("Glass Card", "Transparent card with blur effects", "💎"),
            ("Animated Button", "Interactive button with hover effects", "🔘"),
            ("Loading Spinner", "Smooth loading animation", "🌀"),
            ("Progress Bar", "Modern progress indicator", "📊")
        ]
        
        for i, (title, subtitle, icon) in enumerate(cards):
            card = GlassCard(title, subtitle, theme=self.theme)
            
            # Add interactive elements to cards
            if "Button" in title:
                button = AnimatedButton("Click Me!", variant="primary", theme=self.theme)
                button.clicked.connect(lambda: self.show_toast("Button clicked!"))
                card.add_widget(button)
            elif "Spinner" in title:
                spinner = LoadingSpinner("Loading...", theme=self.theme)
                card.add_widget(spinner)
                spinner.start()
            elif "Progress" in title:
                progress = QProgressBar()
                progress.setStyleSheet(self.modern_styles.get_progress_bar_style())
                progress.setValue(75)
                card.add_widget(progress)
            
            grid_layout.addWidget(card, i // 2, i % 2)
        
        layout.addLayout(grid_layout)
        layout.addSpacing(20)
    
    def setup_animations_demo(self, layout):
        """Setup animations demo section."""
        # Section title
        title = QLabel("🎭 Animation System")
        title.setFont(self.theme.fonts['heading_medium'])
        title.setStyleSheet(f"color: {self.theme.colors['text_primary'].name()}; margin-bottom: 16px;")
        layout.addWidget(title)
        
        # Animation controls
        controls_layout = QHBoxLayout()
        
        # Fade animation button
        fade_button = AnimatedButton("Fade In/Out", variant="secondary", theme=self.theme)
        fade_button.clicked.connect(self.demo_fade_animation)
        controls_layout.addWidget(fade_button)
        
        # Scale animation button
        scale_button = AnimatedButton("Scale Effect", variant="secondary", theme=self.theme)
        scale_button.clicked.connect(self.demo_scale_animation)
        controls_layout.addWidget(scale_button)
        
        # Slide animation button
        slide_button = AnimatedButton("Slide Effect", variant="secondary", theme=self.theme)
        slide_button.clicked.connect(self.demo_slide_animation)
        controls_layout.addWidget(slide_button)
        
        layout.addLayout(controls_layout)
        
        # Animation target
        self.animation_target = QLabel("Animation Target")
        self.animation_target.setStyleSheet(f"""
            QLabel {{
                background: {self.theme.colors['primary'].name()};
                color: white;
                padding: 20px;
                border-radius: 8px;
                font: {self.theme.fonts['body_medium'].pointSize()}pt "{self.theme.fonts['inter']}";
            }}
        """)
        self.animation_target.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.animation_target)
        
        layout.addSpacing(20)
    
    def setup_styling_demo(self, layout):
        """Setup styling demo section."""
        # Section title
        title = QLabel("🎨 Modern Styling")
        title.setFont(self.theme.fonts['heading_medium'])
        title.setStyleSheet(f"color: {self.theme.colors['text_primary'].name()}; margin-bottom: 16px;")
        layout.addWidget(title)
        
        # Style variants
        variants_layout = QHBoxLayout()
        
        button_variants = [
            ("Primary", "primary"),
            ("Secondary", "secondary"),
            ("Outline", "outline"),
            ("Ghost", "ghost")
        ]
        
        for text, variant in button_variants:
            button = AnimatedButton(text, variant=variant, theme=self.theme)
            variants_layout.addWidget(button)
        
        layout.addLayout(variants_layout)
        
        # Input demo
        input_layout = QHBoxLayout()
        
        # Text input
        text_input = QLineEdit("Modern text input...")
        text_input.setStyleSheet(self.modern_styles.get_modern_input_style())
        input_layout.addWidget(text_input)
        
        # Search input
        search_input = QLineEdit("Search...")
        search_input.setStyleSheet(self.modern_styles.get_modern_input_style("search"))
        input_layout.addWidget(search_input)
        
        layout.addLayout(input_layout)
        
        layout.addSpacing(20)
    
    def setup_effects_demo(self, layout):
        """Setup effects demo section."""
        # Section title
        title = QLabel("✨ Glass Effects")
        title.setFont(self.theme.fonts['heading_medium'])
        title.setStyleSheet(f"color: {self.theme.colors['text_primary'].name()}; margin-bottom: 16px;")
        layout.addWidget(title)
        
        # Effects showcase
        effects_layout = QHBoxLayout()
        
        # Glass panel
        glass_panel = QFrame()
        glass_panel.setStyleSheet(self.modern_styles.get_glass_card_style())
        glass_panel.setMinimumSize(200, 150)
        
        panel_layout = QVBoxLayout(glass_panel)
        panel_layout.addWidget(QLabel("Glass Panel"))
        panel_layout.addWidget(QLabel("With blur effects"))
        
        effects_layout.addWidget(glass_panel)
        
        # Shadow panel
        shadow_panel = QFrame()
        shadow_panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 16px;
            }
        """)
        shadow_panel.setMinimumSize(200, 150)
        
        # Apply shadow effect
        self.modern_styles.apply_shadow_effect(shadow_panel)
        
        shadow_layout = QVBoxLayout(shadow_panel)
        shadow_layout.addWidget(QLabel("Shadow Panel"))
        shadow_layout.addWidget(QLabel("With drop shadow"))
        
        effects_layout.addWidget(shadow_panel)
        
        layout.addLayout(effects_layout)
    
    def setup_footer(self, main_layout):
        """Setup demo footer."""
        footer_layout = QHBoxLayout()
        
        # Status
        status_label = QLabel("Ready")
        status_label.setStyleSheet(f"color: {self.theme.colors['text_secondary'].name()};")
        footer_layout.addWidget(status_label)
        
        footer_layout.addStretch()
        
        # Demo controls
        reset_button = AnimatedButton("Reset Demo", variant="ghost", theme=self.theme)
        reset_button.clicked.connect(self.reset_demo)
        footer_layout.addWidget(reset_button)
        
        main_layout.addLayout(footer_layout)
    
    def setup_animations(self):
        """Setup demo animations."""
        # Window fade-in
        self.fade_in_animation = self.animation_manager.create_fade_animation(
            self, start_opacity=0.0, end_opacity=1.0, duration=800
        )
        self.fade_in_animation.start()
    
    def apply_modern_styling(self):
        """Apply modern styling to the demo window."""
        # Apply theme
        self.theme.apply_theme_to_app(self.app())
        
        # Set complete stylesheet
        self.setStyleSheet(self.modern_styles.get_complete_stylesheet())
    
    def start_demo_animations(self):
        """Start demo animations."""
        # Auto-rotate some elements
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_demo_animations)
        self.animation_timer.start(50)  # 20 FPS
    
    def update_demo_animations(self):
        """Update demo animations."""
        # Add subtle animations here
        pass
    
    def demo_fade_animation(self):
        """Demo fade animation."""
        fade_anim = self.animation_manager.create_fade_animation(
            self.animation_target, start_opacity=0.0, end_opacity=1.0, duration=500
        )
        fade_anim.start()
    
    def demo_scale_animation(self):
        """Demo scale animation."""
        scale_anim = self.animation_manager.create_scale_animation(
            self.animation_target, start_scale=1.0, end_scale=1.2, duration=300
        )
        scale_anim.start()
    
    def demo_slide_animation(self):
        """Demo slide animation."""
        current_pos = self.animation_target.pos()
        slide_anim = self.animation_manager.create_slide_animation(
            self.animation_target,
            current_pos,
            QPoint(current_pos.x() + 50, current_pos.y()),
            duration=300
        )
        slide_anim.start()
    
    def show_section(self, section: str):
        """Show specific demo section."""
        print(f"Showing section: {section}")
        # Implement section navigation
    
    def show_toast(self, message: str):
        """Show toast notification."""
        print(f"Toast: {message}")
        # Implement toast notification
    
    def reset_demo(self):
        """Reset demo to initial state."""
        print("Resetting demo...")
        # Implement demo reset
    
    def paintEvent(self, event):
        """Custom paint event for enhanced glass effect."""
        super().paintEvent(event)
        
        # Create custom painter for background effects
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Add subtle gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(15, 23, 42, 200))  # Slate 900 with alpha
        gradient.setColorAt(1, QColor(30, 41, 59, 200))  # Slate 800 with alpha
        
        painter.fillRect(self.rect(), gradient)


def main():
    """Main entry point for the demo application."""
    app = QApplication(sys.argv)
    
    # Setup application properties
    app.setApplicationName("CONFIGO GUI Demo")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("CONFIGO")
    
    # Enable high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Create and show demo window
    window = ModernDemoWindow()
    window.show()
    
    # Start application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 