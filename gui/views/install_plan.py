"""
CONFIGO GUI - Install Plan View
Modern installation plan with progress tracking
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGraphicsDropShadowEffect,
    QScrollArea, QProgressBar, QTextEdit
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QColor, QPainter


class InstallPlanView(QWidget):
    """Installation plan view with progress tracking"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.install_thread = None
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Setup the install plan UI"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Header section
        self.create_header_section(layout)
        
        # Plan display section
        self.create_plan_section(layout)
        
        # Progress section
        self.create_progress_section(layout)
        
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
        title_label = QLabel("Installation Plan")
        title_label.setObjectName("planTitle")
        title_label.setStyleSheet("""
            #planTitle {
                color: #ffffff;
                font-size: 28px;
                font-weight: 700;
                text-align: center;
            }
        """)
        
        # Subtitle
        subtitle_label = QLabel("Review and execute your installation plan")
        subtitle_label.setObjectName("planSubtitle")
        subtitle_label.setStyleSheet("""
            #planSubtitle {
                color: #a1a1aa;
                font-size: 16px;
                font-weight: 400;
                text-align: center;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
        
    def create_plan_section(self, layout):
        """Create the plan display section"""
        plan_frame = QFrame()
        plan_frame.setObjectName("planFrame")
        plan_frame.setStyleSheet("""
            #planFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 30px;
            }
        """)
        
        plan_layout = QVBoxLayout(plan_frame)
        plan_layout.setContentsMargins(30, 30, 30, 30)
        plan_layout.setSpacing(20)
        
        # Section title
        plan_title = QLabel("Generated Plan")
        plan_title.setObjectName("planSectionTitle")
        plan_title.setStyleSheet("""
            #planSectionTitle {
                color: #ffffff;
                font-size: 20px;
                font-weight: 600;
                text-align: center;
            }
        """)
        plan_layout.addWidget(plan_title)
        
        # Plan description
        self.plan_description = QLabel("Loading plan...")
        self.plan_description.setObjectName("planDescription")
        self.plan_description.setStyleSheet("""
            #planDescription {
                color: #d1d5db;
                font-size: 14px;
                font-weight: 400;
                text-align: center;
                line-height: 1.6;
            }
        """)
        self.plan_description.setWordWrap(True)
        plan_layout.addWidget(self.plan_description)
        
        # Tools list
        self.tools_list = QLabel("Preparing tools list...")
        self.tools_list.setObjectName("toolsList")
        self.tools_list.setStyleSheet("""
            #toolsList {
                color: #a1a1aa;
                font-size: 13px;
                font-weight: 400;
                text-align: center;
                line-height: 1.5;
            }
        """)
        self.tools_list.setWordWrap(True)
        plan_layout.addWidget(self.tools_list)
        
        layout.addWidget(plan_frame)
        
    def create_progress_section(self, layout):
        """Create the progress tracking section"""
        progress_frame = QFrame()
        progress_frame.setObjectName("progressFrame")
        progress_frame.setStyleSheet("""
            #progressFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 30px;
            }
        """)
        
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setContentsMargins(30, 30, 30, 30)
        progress_layout.setSpacing(20)
        
        # Section title
        progress_title = QLabel("Installation Progress")
        progress_title.setObjectName("progressTitle")
        progress_title.setStyleSheet("""
            #progressTitle {
                color: #ffffff;
                font-size: 20px;
                font-weight: 600;
                text-align: center;
            }
        """)
        progress_layout.addWidget(progress_title)
        
        # Overall progress
        self.overall_progress = QProgressBar()
        self.overall_progress.setObjectName("overallProgress")
        self.overall_progress.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                text-align: center;
                color: #ffffff;
                font-weight: 600;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #818cf8);
                border-radius: 7px;
            }
        """)
        self.overall_progress.setValue(0)
        progress_layout.addWidget(self.overall_progress)
        
        # Current step
        self.current_step = QLabel("Ready to start installation")
        self.current_step.setObjectName("currentStep")
        self.current_step.setStyleSheet("""
            #currentStep {
                color: #a1a1aa;
                font-size: 14px;
                font-weight: 500;
                text-align: center;
            }
        """)
        progress_layout.addWidget(self.current_step)
        
        # Log output
        self.log_output = QTextEdit()
        self.log_output.setObjectName("logOutput")
        self.log_output.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.3);
                color: #d1d5db;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        self.log_output.setMaximumHeight(150)
        self.log_output.setReadOnly(True)
        progress_layout.addWidget(self.log_output)
        
        layout.addWidget(progress_frame)
        
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
        
        # Start Installation button
        self.start_button = QPushButton("🚀 Start Installation")
        self.start_button.setObjectName("startButton")
        self.start_button.setStyleSheet("""
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
            #startButton:disabled {
                background: rgba(255, 255, 255, 0.1);
                color: #71717a;
            }
        """)
        self.start_button.clicked.connect(self.on_start_installation)
        buttons_layout.addWidget(self.start_button)
        
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
        
    def update_plan(self, description: str):
        """Update the plan display"""
        self.plan_description.setText(f"Environment: {description}")
        
        # Generate mock tools list (in real implementation, this would come from the CLI)
        mock_tools = [
            "Python 3.11",
            "Node.js 18",
            "Git",
            "VS Code",
            "Docker",
            "PostgreSQL"
        ]
        
        self.tools_list.setText(f"Tools to install: {', '.join(mock_tools)}")
        
    def on_back(self):
        """Handle back button click"""
        if self.parent:
            self.parent.navigate_to_view("environment")
            
    def on_start_installation(self):
        """Handle start installation button click"""
        if self.parent and hasattr(self.parent, 'install_engine'):
            # Disable start button
            self.start_button.setEnabled(False)
            self.start_button.setText("Installing...")
            
            # Start installation in background thread
            self.start_installation_thread()
            
    def start_installation_thread(self):
        """Start installation in background thread"""
        self.install_thread = InstallThread(self.parent.install_engine)
        self.install_thread.progress_updated.connect(self.update_progress)
        self.install_thread.step_updated.connect(self.update_step)
        self.install_thread.log_updated.connect(self.update_log)
        self.install_thread.finished.connect(self.on_installation_finished)
        self.install_thread.start()
        
    def update_progress(self, value: int):
        """Update progress bar"""
        self.overall_progress.setValue(value)
        
    def update_step(self, step: str):
        """Update current step"""
        self.current_step.setText(step)
        
    def update_log(self, message: str):
        """Update log output"""
        self.log_output.append(message)
        
    def on_installation_finished(self):
        """Handle installation completion"""
        self.start_button.setEnabled(True)
        self.start_button.setText("✅ Installation Complete")
        
        if self.parent:
            self.parent.show_toast("Installation completed successfully!", "success")
            
    def paintEvent(self, event):
        """Custom paint event for glassmorphism effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient background
        gradient = QColor(15, 15, 35, 100)  # Semi-transparent dark background
        painter.fillRect(self.rect(), gradient)


class InstallThread(QThread):
    """Background thread for installation"""
    
    progress_updated = Signal(int)
    step_updated = Signal(str)
    log_updated = Signal(str)
    
    def __init__(self, install_engine):
        super().__init__()
        self.install_engine = install_engine
        
    def run(self):
        """Run the installation process"""
        steps = [
            ("Checking system requirements...", 10),
            ("Installing Python 3.11...", 25),
            ("Installing Node.js 18...", 40),
            ("Installing Git...", 55),
            ("Installing VS Code...", 70),
            ("Installing Docker...", 85),
            ("Installing PostgreSQL...", 95),
            ("Finalizing installation...", 100)
        ]
        
        for step, progress in steps:
            self.step_updated.emit(step)
            self.log_updated.emit(f"[INFO] {step}")
            
            # Simulate work
            self.msleep(1000)
            
            self.progress_updated.emit(progress)
            
        self.log_updated.emit("[SUCCESS] Installation completed successfully!") 