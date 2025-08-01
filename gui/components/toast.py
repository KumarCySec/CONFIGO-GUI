"""
CONFIGO GUI - Toast Notification Component
Modern toast notifications with smooth animations
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
    QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, Signal
from PySide6.QtGui import QFont, QColor, QPainter


class ToastManager:
    """Manages toast notifications"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.toasts = []
        self.toast_container = None
        
        if parent:
            self.setup_toast_container()
            
    def setup_toast_container(self):
        """Setup the toast container"""
        self.toast_container = QWidget(self.parent)
        self.toast_container.setObjectName("toastContainer")
        self.toast_container.setStyleSheet("""
            #toastContainer {
                background: transparent;
                border: none;
            }
        """)
        
        # Position in top-right corner
        self.toast_container.setFixedSize(400, 0)
        self.toast_container.move(
            self.parent.width() - 420,
            20
        )
        
    def show_toast(self, message: str, toast_type: str = "info", duration: int = 3000):
        """Show a toast notification"""
        if not self.toast_container:
            return
            
        toast = Toast(message, toast_type, self.toast_container)
        self.toasts.append(toast)
        
        # Position the toast
        self.position_toasts()
        
        # Auto-remove after duration
        QTimer.singleShot(duration, lambda: self.remove_toast(toast))
        
    def remove_toast(self, toast):
        """Remove a toast notification"""
        if toast in self.toasts:
            self.toasts.remove(toast)
            toast.animate_out()
            self.position_toasts()
            
    def position_toasts(self):
        """Position all toasts"""
        y_offset = 20
        for toast in self.toasts:
            toast.move(0, y_offset)
            y_offset += toast.height() + 10
            
        # Update container height
        if self.toasts:
            self.toast_container.setFixedHeight(y_offset + 20)


class Toast(QFrame):
    """Individual toast notification"""
    
    def __init__(self, message: str, toast_type: str = "info", parent=None):
        super().__init__(parent)
        self.message = message
        self.toast_type = toast_type
        self.setFixedHeight(60)
        
        self.setup_ui()
        self.setup_animations()
        self.animate_in()
        
    def setup_ui(self):
        """Setup the toast UI"""
        # Set object name for styling
        self.setObjectName(f"toast_{self.toast_type}")
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # Icon
        icon_label = QLabel(self.get_icon())
        icon_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(icon_label)
        
        # Message
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            color: #ffffff;
            font-size: 13px;
            font-weight: 500;
        """)
        layout.addWidget(message_label, 1)
        
        # Close button
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #a1a1aa;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)
        close_button.clicked.connect(self.close_toast)
        layout.addWidget(close_button)
        
        # Apply styles based on type
        self.apply_toast_styles()
        
        # Add glassmorphism effect
        self.apply_glassmorphism()
        
    def get_icon(self) -> str:
        """Get icon for toast type"""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        return icons.get(self.toast_type, "ℹ️")
        
    def apply_toast_styles(self):
        """Apply styles based on toast type"""
        base_styles = """
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 0px;
            }
        """
        
        type_styles = {
            "info": f"""
                QFrame {{
                    background: rgba(59, 130, 246, 0.2);
                    border: 1px solid rgba(59, 130, 246, 0.4);
                }}
            """,
            "success": f"""
                QFrame {{
                    background: rgba(16, 185, 129, 0.2);
                    border: 1px solid rgba(16, 185, 129, 0.4);
                }}
            """,
            "warning": f"""
                QFrame {{
                    background: rgba(245, 158, 11, 0.2);
                    border: 1px solid rgba(245, 158, 11, 0.4);
                }}
            """,
            "error": f"""
                QFrame {{
                    background: rgba(239, 68, 68, 0.2);
                    border: 1px solid rgba(239, 68, 68, 0.4);
                }}
            """
        }
        
        self.setStyleSheet(base_styles + type_styles.get(self.toast_type, type_styles["info"]))
        
    def apply_glassmorphism(self):
        """Apply glassmorphism effect"""
        # Create drop shadow
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        shadow_effect.setOffset(0, 5)
        self.setGraphicsEffect(shadow_effect)
        
    def setup_animations(self):
        """Setup animations"""
        self.animations = {}
        
    def animate_in(self):
        """Animate the toast in"""
        # Start with 0 opacity
        self.setGraphicsEffect(None)  # Temporarily remove shadow for opacity animation
        
        # Create opacity animation
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(300)
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Create slide animation
        self.slide_animation = QPropertyAnimation(self, b"geometry")
        self.slide_animation.setDuration(300)
        self.slide_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Get current geometry
        current_geo = self.geometry()
        
        # Start from off-screen
        start_geo = current_geo.translated(-current_geo.width(), 0)
        
        self.slide_animation.setStartValue(start_geo)
        self.slide_animation.setEndValue(current_geo)
        
        # Start animations
        self.opacity_animation.start()
        self.slide_animation.start()
        
        # Re-apply glassmorphism after animation
        self.opacity_animation.finished.connect(self.apply_glassmorphism)
        
    def animate_out(self):
        """Animate the toast out"""
        # Create opacity animation
        opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        opacity_animation.setDuration(200)
        opacity_animation.setStartValue(1.0)
        opacity_animation.setEndValue(0.0)
        opacity_animation.setEasingCurve(QEasingCurve.InCubic)
        
        # Create slide animation
        slide_animation = QPropertyAnimation(self, b"geometry")
        slide_animation.setDuration(200)
        slide_animation.setEasingCurve(QEasingCurve.InCubic)
        
        # Get current geometry
        current_geo = self.geometry()
        
        # End off-screen
        end_geo = current_geo.translated(-current_geo.width(), 0)
        
        slide_animation.setStartValue(current_geo)
        slide_animation.setEndValue(end_geo)
        
        # Start animations
        opacity_animation.start()
        slide_animation.start()
        
        # Delete widget after animation
        slide_animation.finished.connect(self.deleteLater)
        
    def close_toast(self):
        """Close the toast"""
        self.animate_out()
        
    def paintEvent(self, event):
        """Custom paint event for glassmorphism effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create semi-transparent background
        if self.toast_type == "info":
            bg_color = QColor(59, 130, 246, 40)
        elif self.toast_type == "success":
            bg_color = QColor(16, 185, 129, 40)
        elif self.toast_type == "warning":
            bg_color = QColor(245, 158, 11, 40)
        elif self.toast_type == "error":
            bg_color = QColor(239, 68, 68, 40)
        else:
            bg_color = QColor(59, 130, 246, 40)
            
        painter.fillRect(self.rect(), bg_color) 