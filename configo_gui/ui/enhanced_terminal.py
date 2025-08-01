"""
CONFIGO GUI - Enhanced Terminal Console
=======================================

The enhanced terminal console component for CONFIGO GUI application.
Features a dual-pane layout with install timeline and real-time styled terminal.

Features:
- Dual-pane layout (timeline + terminal)
- Real-time log streaming
- Syntax highlighting
- Progress tracking
- Command execution
- Error highlighting

Author: CONFIGO Team
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import subprocess
import threading
import queue

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QScrollArea, QSizePolicy,
    QSpacerItem, QGroupBox, QGridLayout, QProgressBar,
    QListWidget, QListWidgetItem, QTextEdit, QSplitter,
    QLineEdit, QComboBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QThread
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QTextCursor, QSyntaxHighlighter, QTextCharFormat


class TerminalHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for terminal output."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_formats()
    
    def setup_formats(self):
        """Setup text formats for syntax highlighting."""
        # Success messages (green)
        self.success_format = QTextCharFormat()
        self.success_format.setForeground(QColor("#4CAF50"))
        self.success_format.setFontWeight(QFont.Bold)
        
        # Error messages (red)
        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor("#F44336"))
        self.error_format.setFontWeight(QFont.Bold)
        
        # Warning messages (yellow)
        self.warning_format = QTextCharFormat()
        self.warning_format.setForeground(QColor("#FF9800"))
        self.warning_format.setFontWeight(QFont.Bold)
        
        # Info messages (blue)
        self.info_format = QTextCharFormat()
        self.info_format.setForeground(QColor("#2196F3"))
        
        # Command prompts (cyan)
        self.command_format = QTextCharFormat()
        self.command_format.setForeground(QColor("#00BCD4"))
        self.command_format.setFontWeight(QFont.Bold)
        
        # Timestamps (gray)
        self.timestamp_format = QTextCharFormat()
        self.timestamp_format.setForeground(QColor("#9E9E9E"))
        self.timestamp_format.setFontItalic(True)
    
    def highlightBlock(self, text):
        """Highlight terminal output syntax."""
        import re
        
        # Highlight timestamps
        timestamp_pattern = r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'
        for match in re.finditer(timestamp_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.timestamp_format)
        
        # Highlight success messages
        success_patterns = [
            r'SUCCESS|✓|successfully|installed|completed',
            r'\[OK\]|\[SUCCESS\]'
        ]
        for pattern in success_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                self.setFormat(match.start(), match.end() - match.start(), self.success_format)
        
        # Highlight error messages
        error_patterns = [
            r'ERROR|✗|failed|error|exception',
            r'\[ERROR\]|\[FAILED\]'
        ]
        for pattern in error_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                self.setFormat(match.start(), match.end() - match.start(), self.error_format)
        
        # Highlight warning messages
        warning_patterns = [
            r'WARNING|⚠|warning|deprecated',
            r'\[WARNING\]'
        ]
        for pattern in warning_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                self.setFormat(match.start(), match.end() - match.start(), self.warning_format)
        
        # Highlight info messages
        info_patterns = [
            r'INFO|ℹ|information|note',
            r'\[INFO\]'
        ]
        for pattern in info_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                self.setFormat(match.start(), match.end() - match.start(), self.info_format)
        
        # Highlight command prompts
        command_patterns = [
            r'\$ .*',  # Unix command prompt
            r'> .*',   # Windows command prompt
            r'# .*'    # Root command prompt
        ]
        for pattern in command_patterns:
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), self.command_format)


class TimelineStep(QWidget):
    """Individual timeline step widget."""
    
    def __init__(self, step_info: Dict[str, Any]):
        super().__init__()
        self.step_info = step_info
        self.setup_ui()
        self.setup_styling()
    
    def setup_ui(self):
        """Setup the timeline step UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Status indicator
        self.status_label = QLabel(self.get_status_icon())
        self.status_label.setObjectName("status-icon")
        layout.addWidget(self.status_label)
        
        # Step info
        info_layout = QVBoxLayout()
        
        # Step name
        name_label = QLabel(self.step_info.get("name", "Unknown Step"))
        name_label.setObjectName("step-name")
        info_layout.addWidget(name_label)
        
        # Step description
        desc_label = QLabel(self.step_info.get("description", ""))
        desc_label.setObjectName("step-description")
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Progress indicator
        if self.step_info.get("status") == "installing":
            self.progress_bar = QProgressBar()
            self.progress_bar.setObjectName("step-progress")
            self.progress_bar.setMaximumWidth(100)
            self.progress_bar.setValue(self.step_info.get("progress", 0))
            layout.addWidget(self.progress_bar)
    
    def setup_styling(self):
        """Apply styling to the timeline step."""
        status = self.step_info.get("status", "pending")
        
        if status == "completed":
            border_color = "#4CAF50"
            bg_color = "#2d4a2d"
        elif status == "error":
            border_color = "#F44336"
            bg_color = "#4a2d2d"
        elif status == "installing":
            border_color = "#FF9800"
            bg_color = "#4a3d2d"
        else:
            border_color = "#666666"
            bg_color = "#2d2d2d"
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                color: #ffffff;
                padding: 5px;
            }}
            
            #status-icon {{
                font-size: 20px;
                margin-right: 10px;
            }}
            
            #step-name {{
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
            }}
            
            #step-description {{
                font-size: 12px;
                color: #cccccc;
                line-height: 1.3;
            }}
            
            #step-progress {{
                background-color: #3c3c3c;
                border: 1px solid {border_color};
                border-radius: 5px;
                text-align: center;
            }}
            
            #step-progress::chunk {{
                background-color: {border_color};
                border-radius: 4px;
            }}
        """)
    
    def get_status_icon(self) -> str:
        """Get the status icon for the step."""
        status = self.step_info.get("status", "pending")
        
        icons = {
            "pending": "⏳",
            "installing": "⚡",
            "completed": "✓",
            "error": "✗",
            "skipped": "⏭"
        }
        
        return icons.get(status, "⏳")
    
    def update_status(self, status: str, progress: int = 0):
        """Update the step status."""
        self.step_info["status"] = status
        self.step_info["progress"] = progress
        
        self.status_label.setText(self.get_status_icon())
        
        if status == "installing" and not hasattr(self, "progress_bar"):
            self.progress_bar = QProgressBar()
            self.progress_bar.setObjectName("step-progress")
            self.progress_bar.setMaximumWidth(100)
            self.progress_bar.setValue(progress)
            self.layout().addWidget(self.progress_bar)
        elif hasattr(self, "progress_bar"):
            self.progress_bar.setValue(progress)
        
        self.setup_styling()


class CommandExecutor(QThread):
    """Thread for executing commands in the background."""
    
    output_received = Signal(str)
    command_finished = Signal(int)  # Exit code
    
    def __init__(self, command: str):
        super().__init__()
        self.command = command
        self.process = None
    
    def run(self):
        """Execute the command."""
        try:
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output in real-time
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.output_received.emit(line.strip())
            
            # Wait for process to finish
            exit_code = self.process.wait()
            self.command_finished.emit(exit_code)
            
        except Exception as e:
            self.output_received.emit(f"Error executing command: {e}")
            self.command_finished.emit(1)
    
    def stop(self):
        """Stop the command execution."""
        if self.process:
            self.process.terminate()


class EnhancedTerminalConsole(QWidget):
    """
    Enhanced Terminal Console for CONFIGO GUI application.
    
    Features:
    - Dual-pane layout (timeline + terminal)
    - Real-time log streaming
    - Syntax highlighting
    - Progress tracking
    - Command execution
    - Error highlighting
    """
    
    # Signals
    step_completed = Signal(str, bool)  # step_name, success
    command_executed = Signal(str, int)  # command, exit_code
    
    def __init__(self):
        super().__init__()
        self.timeline_steps = []
        self.current_command = None
        self.command_history = []
        self.setup_ui()
        self.setup_connections()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the enhanced terminal console UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self.setup_header(layout)
        
        # Main content area
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Timeline
        self.setup_timeline_panel(content_splitter)
        
        # Right panel - Terminal
        self.setup_terminal_panel(content_splitter)
        
        content_splitter.setSizes([400, 600])
        layout.addWidget(content_splitter)
    
    def setup_header(self, layout):
        """Setup the header section."""
        header = QFrame()
        header.setObjectName("terminal-header")
        header.setMaximumHeight(60)
        
        header_layout = QHBoxLayout(header)
        
        # Icon and title
        icon_label = QLabel("🖥️")
        icon_label.setObjectName("terminal-icon")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel("Enhanced Terminal Console")
        title_label.setObjectName("terminal-title")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Control buttons
        clear_button = QPushButton("🗑️ Clear")
        clear_button.setObjectName("clear-button")
        clear_button.clicked.connect(self.clear_terminal)
        header_layout.addWidget(clear_button)
        
        layout.addWidget(header)
    
    def setup_timeline_panel(self, splitter):
        """Setup the timeline panel."""
        timeline_widget = QWidget()
        timeline_layout = QVBoxLayout(timeline_widget)
        
        # Timeline header
        header_label = QLabel("Installation Timeline")
        header_label.setObjectName("timeline-header")
        timeline_layout.addWidget(header_label)
        
        # Timeline scroll area
        self.timeline_scroll = QScrollArea()
        self.timeline_scroll.setWidgetResizable(True)
        self.timeline_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.timeline_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Timeline widget
        self.timeline_widget = QWidget()
        self.timeline_layout = QVBoxLayout(self.timeline_widget)
        self.timeline_layout.setAlignment(Qt.AlignTop)
        self.timeline_layout.setSpacing(5)
        
        self.timeline_scroll.setWidget(self.timeline_widget)
        timeline_layout.addWidget(self.timeline_scroll)
        
        splitter.addWidget(timeline_widget)
    
    def setup_terminal_panel(self, splitter):
        """Setup the terminal panel."""
        terminal_widget = QWidget()
        terminal_layout = QVBoxLayout(terminal_widget)
        
        # Terminal output
        self.terminal_output = QTextEdit()
        self.terminal_output.setObjectName("terminal-output")
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setFont(QFont("Consolas", 10))
        
        # Apply syntax highlighting
        self.terminal_highlighter = TerminalHighlighter(self.terminal_output.document())
        
        terminal_layout.addWidget(self.terminal_output)
        
        # Command input area
        input_container = QFrame()
        input_container.setObjectName("command-input-container")
        input_container.setMaximumHeight(80)
        
        input_layout = QHBoxLayout(input_container)
        
        # Command prompt
        prompt_label = QLabel("$")
        prompt_label.setObjectName("command-prompt")
        input_layout.addWidget(prompt_label)
        
        # Command input
        self.command_input = QLineEdit()
        self.command_input.setObjectName("command-input")
        self.command_input.setPlaceholderText("Enter command...")
        self.command_input.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.command_input)
        
        # Execute button
        execute_button = QPushButton("Execute")
        execute_button.setObjectName("execute-button")
        execute_button.clicked.connect(self.execute_command)
        input_layout.addWidget(execute_button)
        
        terminal_layout.addWidget(input_container)
        
        splitter.addWidget(terminal_widget)
    
    def setup_connections(self):
        """Setup signal connections."""
        pass  # Will be connected by parent widget
    
    def setup_styling(self):
        """Apply styling to the enhanced terminal console."""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            
            #terminal-header {
                background-color: #2c2c2c;
                border-bottom: 1px solid #3c3c3c;
                padding: 10px;
            }
            
            #terminal-icon {
                font-size: 24px;
                margin-right: 10px;
            }
            
            #terminal-title {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #clear-button {
                background-color: #666666;
                border: none;
                border-radius: 15px;
                color: #ffffff;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            #clear-button:hover {
                background-color: #777777;
            }
            
            #timeline-header {
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                margin: 10px;
            }
            
            #terminal-output {
                background-color: #0d1117;
                border: 1px solid #30363d;
                border-radius: 5px;
                color: #c9d1d9;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                padding: 10px;
            }
            
            #command-input-container {
                background-color: #2c2c2c;
                border-top: 1px solid #3c3c3c;
                padding: 10px;
            }
            
            #command-prompt {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                color: #00ff00;
                font-weight: bold;
                margin-right: 10px;
            }
            
            #command-input {
                background-color: #0d1117;
                border: 1px solid #30363d;
                border-radius: 5px;
                color: #c9d1d9;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                padding: 8px 12px;
            }
            
            #command-input:focus {
                border-color: #0066cc;
            }
            
            #execute-button {
                background-color: #0066cc;
                border: none;
                border-radius: 5px;
                color: #ffffff;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            #execute-button:hover {
                background-color: #0077ee;
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
    
    def add_timeline_step(self, step_info: Dict[str, Any]):
        """Add a new step to the timeline."""
        step_widget = TimelineStep(step_info)
        self.timeline_steps.append(step_widget)
        self.timeline_layout.addWidget(step_widget)
    
    def update_timeline_step(self, step_name: str, status: str, progress: int = 0):
        """Update a timeline step."""
        for step in self.timeline_steps:
            if step.step_info.get("name") == step_name:
                step.update_status(status, progress)
                break
    
    def add_terminal_output(self, text: str, timestamp: bool = True):
        """Add text to the terminal output."""
        if timestamp:
            timestamp_str = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            text = f"{timestamp_str} {text}"
        
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.terminal_output.setTextCursor(cursor)
        self.terminal_output.insertPlainText(text + "\n")
        
        # Auto-scroll to bottom
        self.terminal_output.verticalScrollBar().setValue(
            self.terminal_output.verticalScrollBar().maximum()
        )
    
    def execute_command(self):
        """Execute the current command."""
        command = self.command_input.text().strip()
        if not command:
            return
        
        # Add command to history
        self.command_history.append(command)
        
        # Display command in terminal
        self.add_terminal_output(f"$ {command}")
        
        # Execute command in background thread
        self.current_command = CommandExecutor(command)
        self.current_command.output_received.connect(self.add_terminal_output)
        self.current_command.command_finished.connect(self.on_command_finished)
        self.current_command.start()
        
        # Clear input
        self.command_input.clear()
    
    def on_command_finished(self, exit_code: int):
        """Handle command completion."""
        if exit_code == 0:
            self.add_terminal_output("Command completed successfully.", False)
        else:
            self.add_terminal_output(f"Command failed with exit code {exit_code}.", False)
        
        self.command_executed.emit(self.current_command.command, exit_code)
        self.current_command = None
    
    def clear_terminal(self):
        """Clear the terminal output."""
        self.terminal_output.clear()
    
    def get_command_history(self) -> List[str]:
        """Get the command history."""
        return self.command_history.copy()
    
    def stop_current_command(self):
        """Stop the currently running command."""
        if self.current_command:
            self.current_command.stop()
            self.current_command.wait()
            self.current_command = None 