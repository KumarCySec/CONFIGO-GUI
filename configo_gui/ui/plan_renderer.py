"""
CONFIGO GUI - Plan Renderer Screen
==================================

The plan renderer screen component for CONFIGO GUI application.
Displays the installation plan with tool cards, progress bars, and controls.

Author: CONFIGO Team
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QProgressBar, QGroupBox,
    QScrollArea, QGridLayout, QSizePolicy, QSpacerItem,
    QListWidget, QListWidgetItem, QTextEdit, QSplitter,
    QMessageBox, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor


class ToolCard(QFrame):
    """
    Individual tool card component for displaying tool information.
    
    Features:
    - Tool name and description
    - Installation status
    - Progress bar
    - Status indicators
    """
    
    def __init__(self, tool_info: dict):
        super().__init__()
        self.tool_info = tool_info
        self.setup_ui()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the tool card UI components."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header with name and status
        header_layout = QHBoxLayout()
        
        # Tool name
        self.name_label = QLabel(self.tool_info.get('name', 'Unknown Tool'))
        self.name_label.setObjectName("tool-name")
        header_layout.addWidget(self.name_label)
        
        # Status indicator
        self.status_label = QLabel("⏳ Pending")
        self.status_label.setObjectName("tool-status")
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)
        
        # Description
        self.desc_label = QLabel(self.tool_info.get('description', 'No description available'))
        self.desc_label.setObjectName("tool-description")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        # Dependencies
        dependencies = self.tool_info.get('dependencies', [])
        if dependencies:
            deps_label = QLabel(f"Dependencies: {', '.join(dependencies)}")
            deps_label.setObjectName("tool-dependencies")
            layout.addWidget(deps_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("tool-progress")
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Install command (collapsible)
        install_cmd = self.tool_info.get('install_command', '')
        if install_cmd:
            self.cmd_label = QLabel(f"Command: {install_cmd}")
            self.cmd_label.setObjectName("tool-command")
            self.cmd_label.setWordWrap(True)
            layout.addWidget(self.cmd_label)
    
    def setup_styling(self):
        """Apply custom styling to the tool card."""
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 8px;
                margin: 5px;
            }
            
            QFrame:hover {
                border-color: #0066cc;
            }
            
            #tool-name {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #tool-status {
                font-size: 12px;
                color: #ffaa00;
            }
            
            #tool-description {
                font-size: 14px;
                color: #cccccc;
                line-height: 1.4;
            }
            
            #tool-dependencies {
                font-size: 12px;
                color: #888888;
                font-style: italic;
            }
            
            #tool-command {
                font-size: 12px;
                color: #00cc00;
                font-family: monospace;
                background-color: #0a0a0a;
                padding: 5px;
                border-radius: 4px;
            }
            
            #tool-progress {
                background-color: #404040;
                border: none;
                border-radius: 4px;
                text-align: center;
                color: #ffffff;
            }
            
            #tool-progress::chunk {
                background-color: #0066cc;
                border-radius: 4px;
            }
        """)
    
    def update_status(self, status: str, progress: int = 0):
        """Update the tool status and progress."""
        status_colors = {
            'pending': ('⏳ Pending', '#ffaa00'),
            'installing': ('🔧 Installing', '#0066cc'),
            'success': ('✅ Installed', '#00cc00'),
            'error': ('❌ Failed', '#ff4444'),
            'skipped': ('⏭️ Skipped', '#888888')
        }
        
        if status in status_colors:
            text, color = status_colors[status]
            self.status_label.setText(text)
            self.status_label.setStyleSheet(f"color: {color};")
        
        if progress > 0:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(progress)
        else:
            self.progress_bar.setVisible(False)


class PlanRendererScreen(QWidget):
    """
    Plan renderer screen for CONFIGO GUI application.
    
    Features:
    - Visual tool cards with status
    - Progress tracking for each tool
    - Installation controls
    - Plan overview
    - Real-time updates
    """
    
    # Signals
    install_requested = Signal()  # Emitted when user requests installation
    plan_updated = Signal(list)  # Emitted when plan is updated
    
    def __init__(self):
        super().__init__()
        self.plan = []
        self.tool_cards = {}
        self.setup_ui()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the plan renderer screen UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header section
        self.setup_header_section(main_layout)
        
        # Plan overview section
        self.setup_overview_section(main_layout)
        
        # Tools section
        self.setup_tools_section(main_layout)
        
        # Controls section
        self.setup_controls_section(main_layout)
    
    def setup_header_section(self, main_layout):
        """Create the header section."""
        # Header container
        header_frame = QFrame()
        header_frame.setObjectName("header-frame")
        header_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel("Installation Plan")
        title_label.setObjectName("title-label")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Review and execute the installation plan")
        subtitle_label.setObjectName("subtitle-label")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_frame)
    
    def setup_overview_section(self, main_layout):
        """Create the plan overview section."""
        # Overview container
        overview_group = QGroupBox("Plan Overview")
        overview_group.setObjectName("overview-group")
        overview_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        overview_layout = QVBoxLayout(overview_group)
        
        # Overview info
        self.overview_label = QLabel("No plan generated yet")
        self.overview_label.setObjectName("overview-label")
        self.overview_label.setWordWrap(True)
        overview_layout.addWidget(self.overview_label)
        
        # Progress summary
        self.progress_summary = QLabel("")
        self.progress_summary.setObjectName("progress-summary")
        overview_layout.addWidget(self.progress_summary)
        
        main_layout.addWidget(overview_group)
    
    def setup_tools_section(self, main_layout):
        """Create the tools section."""
        # Tools container
        tools_group = QGroupBox("Tools to Install")
        tools_group.setObjectName("tools-group")
        tools_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        tools_layout = QVBoxLayout(tools_group)
        
        # Scroll area for tool cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("tools-scroll")
        
        # Container widget for tool cards
        self.tools_container = QWidget()
        self.tools_layout = QVBoxLayout(self.tools_container)
        self.tools_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.tools_container)
        tools_layout.addWidget(scroll_area)
        
        main_layout.addWidget(tools_group)
    
    def setup_controls_section(self, main_layout):
        """Create the controls section."""
        # Controls container
        controls_frame = QFrame()
        controls_frame.setObjectName("controls-frame")
        controls_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setAlignment(Qt.AlignCenter)
        
        # Install button
        self.install_button = QPushButton("🚀 Start Installation")
        self.install_button.setObjectName("install-button")
        self.install_button.setMinimumSize(200, 50)
        self.install_button.clicked.connect(self.on_install_clicked)
        controls_layout.addWidget(self.install_button)
        
        # Cancel button
        self.cancel_button = QPushButton("❌ Cancel")
        self.cancel_button.setObjectName("cancel-button")
        self.cancel_button.setMinimumSize(120, 50)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        controls_layout.addWidget(self.cancel_button)
        
        main_layout.addWidget(controls_frame)
    
    def setup_styling(self):
        """Apply custom styling to the plan renderer screen."""
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
            
            #overview-label {
                font-size: 14px;
                color: #cccccc;
                line-height: 1.5;
            }
            
            #progress-summary {
                font-size: 12px;
                color: #888888;
                margin-top: 10px;
            }
            
            #tools-scroll {
                background-color: transparent;
                border: none;
            }
            
            #tools-scroll QWidget {
                background-color: transparent;
            }
            
            #install-button {
                background-color: #0066cc;
                border: none;
                border-radius: 25px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 200px;
                min-height: 50px;
            }
            
            #install-button:hover {
                background-color: #0077ee;
            }
            
            #install-button:pressed {
                background-color: #0052a3;
            }
            
            #install-button:disabled {
                background-color: #404040;
                color: #888888;
            }
            
            #cancel-button {
                background-color: #ff4444;
                border: none;
                border-radius: 25px;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 120px;
                min-height: 50px;
            }
            
            #cancel-button:hover {
                background-color: #ff6666;
            }
            
            #cancel-button:pressed {
                background-color: #cc3333;
            }
        """)
    
    def update_plan(self, plan: list):
        """Update the installation plan."""
        self.plan = plan
        self.clear_tools()
        self.create_tool_cards()
        self.update_overview()
    
    def clear_tools(self):
        """Clear all tool cards."""
        for card in self.tool_cards.values():
            self.tools_layout.removeWidget(card)
            card.deleteLater()
        self.tool_cards.clear()
    
    def create_tool_cards(self):
        """Create tool cards for each item in the plan."""
        for i, tool_info in enumerate(self.plan):
            card = ToolCard(tool_info)
            self.tool_cards[tool_info.get('name', f'tool_{i}')] = card
            self.tools_layout.addWidget(card)
    
    def update_overview(self):
        """Update the plan overview."""
        if not self.plan:
            self.overview_label.setText("No plan generated yet")
            self.progress_summary.setText("")
            return
        
        total_tools = len(self.plan)
        self.overview_label.setText(
            f"Plan includes {total_tools} tools to install:\n"
            f"• {' • '.join([tool.get('name', 'Unknown') for tool in self.plan])}"
        )
        
        self.progress_summary.setText(f"Total tools: {total_tools}")
    
    def update_progress(self, step: int, total: int, message: str):
        """Update installation progress."""
        if step <= 0 or total <= 0:
            return
        
        # Update overall progress
        progress_percent = int((step / total) * 100)
        self.progress_summary.setText(
            f"Progress: {step}/{total} ({progress_percent}%) - {message}"
        )
        
        # Update individual tool cards
        if step <= len(self.plan):
            current_tool = self.plan[step - 1]
            tool_name = current_tool.get('name', f'tool_{step}')
            
            if tool_name in self.tool_cards:
                card = self.tool_cards[tool_name]
                card.update_status('installing', progress_percent)
    
    def on_install_clicked(self):
        """Handle install button click."""
        if not self.plan:
            QMessageBox.warning(self, "No Plan", "No installation plan available.")
            return
        
        # Confirm installation
        reply = QMessageBox.question(
            self, 
            "Confirm Installation", 
            f"Are you sure you want to install {len(self.plan)} tools?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.install_button.setEnabled(False)
            self.install_button.setText("🔧 Installing...")
            self.install_requested.emit()
    
    def on_cancel_clicked(self):
        """Handle cancel button click."""
        # Reset UI state
        self.install_button.setEnabled(True)
        self.install_button.setText("🚀 Start Installation")
        
        # Reset all tool cards to pending
        for card in self.tool_cards.values():
            card.update_status('pending')
        
        self.progress_summary.setText("Installation cancelled")
    
    def on_installation_complete(self, success: bool, message: str):
        """Handle installation completion."""
        self.install_button.setEnabled(True)
        self.install_button.setText("🚀 Start Installation")
        
        if success:
            # Update all cards to success
            for card in self.tool_cards.values():
                card.update_status('success')
            self.progress_summary.setText("Installation completed successfully!")
        else:
            # Update failed cards
            self.progress_summary.setText(f"Installation failed: {message}")
    
    def on_tool_installed(self, tool_name: str, success: bool):
        """Handle individual tool installation completion."""
        if tool_name in self.tool_cards:
            card = self.tool_cards[tool_name]
            if success:
                card.update_status('success')
            else:
                card.update_status('error') 