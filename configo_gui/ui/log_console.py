"""
CONFIGO GUI - Log Console Widget
================================

The log console widget component for CONFIGO GUI application.
Displays real-time log messages with syntax highlighting and filtering.

Author: CONFIGO Team
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QTextEdit, QLineEdit,
    QComboBox, QCheckBox, QGroupBox, QSizePolicy,
    QScrollArea, QSplitter, QMenu, QSpacerItem
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal, QTimer, QThread
from PySide6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QSyntaxHighlighter, QTextDocument


class LogHighlighter(QSyntaxHighlighter):
    """
    Syntax highlighter for log messages.
    
    Features:
    - Error messages in red
    - Success messages in green
    - Warning messages in yellow
    - Info messages in blue
    - Timestamps in gray
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_formats()
    
    def setup_formats(self):
        """Setup text formats for different log levels."""
        self.formats = {}
        
        # Error format (red)
        error_format = QTextCharFormat()
        error_format.setForeground(QColor("#ff4444"))
        error_format.setFontWeight(QFont.Bold)
        self.formats['error'] = error_format
        
        # Success format (green)
        success_format = QTextCharFormat()
        success_format.setForeground(QColor("#00cc00"))
        self.formats['success'] = success_format
        
        # Warning format (yellow)
        warning_format = QTextCharFormat()
        warning_format.setForeground(QColor("#ffaa00"))
        self.formats['warning'] = warning_format
        
        # Info format (blue)
        info_format = QTextCharFormat()
        info_format.setForeground(QColor("#0066cc"))
        self.formats['info'] = info_format
        
        # Timestamp format (gray)
        timestamp_format = QTextCharFormat()
        timestamp_format.setForeground(QColor("#888888"))
        self.formats['timestamp'] = timestamp_format
    
    def highlightBlock(self, text):
        """Highlight a block of text based on log level."""
        # Check for error messages
        if any(keyword in text.lower() for keyword in ['error', 'failed', 'exception', 'traceback']):
            self.setFormat(0, len(text), self.formats['error'])
        # Check for success messages
        elif any(keyword in text.lower() for keyword in ['success', 'installed', 'completed', 'done']):
            self.setFormat(0, len(text), self.formats['success'])
        # Check for warning messages
        elif any(keyword in text.lower() for keyword in ['warning', 'warn', 'deprecated']):
            self.setFormat(0, len(text), self.formats['warning'])
        # Check for info messages
        elif any(keyword in text.lower() for keyword in ['info', 'installing', 'downloading']):
            self.setFormat(0, len(text), self.formats['info'])
        # Check for timestamps
        elif text.strip().startswith('[') and ']' in text:
            # Highlight timestamp part
            end_bracket = text.find(']')
            if end_bracket > 0:
                self.setFormat(0, end_bracket + 1, self.formats['timestamp'])


class LogConsoleWidget(QWidget):
    """
    Log console widget for CONFIGO GUI application.
    
    Features:
    - Real-time log display
    - Syntax highlighting
    - Log filtering
    - Auto-scroll
    - Clear functionality
    - Export capability
    """
    
    # Signals
    log_cleared = Signal()  # Emitted when logs are cleared
    
    def __init__(self):
        super().__init__()
        self.log_messages = []
        self.setup_ui()
        self.setup_connections()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the log console UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header section
        self.setup_header_section(main_layout)
        
        # Controls section
        self.setup_controls_section(main_layout)
        
        # Log display section
        self.setup_log_display_section(main_layout)
    
    def setup_header_section(self, main_layout):
        """Create the header section."""
        # Header container
        header_frame = QFrame()
        header_frame.setObjectName("header-frame")
        header_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel("Log Console")
        title_label.setObjectName("title-label")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Real-time installation and system logs")
        subtitle_label.setObjectName("subtitle-label")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_frame)
    
    def setup_controls_section(self, main_layout):
        """Create the controls section."""
        # Controls container
        controls_group = QGroupBox("Controls")
        controls_group.setObjectName("controls-group")
        controls_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        controls_layout = QVBoxLayout(controls_group)
        
        # Top row controls
        top_controls = QHBoxLayout()
        
        # Filter input
        filter_label = QLabel("Filter:")
        filter_label.setObjectName("filter-label")
        top_controls.addWidget(filter_label)
        
        self.filter_input = QLineEdit()
        self.filter_input.setObjectName("filter-input")
        self.filter_input.setPlaceholderText("Filter logs...")
        self.filter_input.textChanged.connect(self.on_filter_changed)
        top_controls.addWidget(self.filter_input)
        
        # Log level filter
        level_label = QLabel("Level:")
        level_label.setObjectName("level-label")
        top_controls.addWidget(level_label)
        
        self.level_combo = QComboBox()
        self.level_combo.setObjectName("level-combo")
        self.level_combo.addItems(["All", "Error", "Warning", "Info", "Success"])
        self.level_combo.currentTextChanged.connect(self.on_level_changed)
        top_controls.addWidget(self.level_combo)
        
        controls_layout.addLayout(top_controls)
        
        # Bottom row controls
        bottom_controls = QHBoxLayout()
        
        # Auto-scroll checkbox
        self.auto_scroll_check = QCheckBox("Auto-scroll")
        self.auto_scroll_check.setObjectName("auto-scroll-check")
        self.auto_scroll_check.setChecked(True)
        bottom_controls.addWidget(self.auto_scroll_check)
        
        # Clear button
        self.clear_button = QPushButton("🗑️ Clear")
        self.clear_button.setObjectName("clear-button")
        self.clear_button.clicked.connect(self.on_clear_clicked)
        bottom_controls.addWidget(self.clear_button)
        
        # Export button
        self.export_button = QPushButton("📁 Export")
        self.export_button.setObjectName("export-button")
        self.export_button.clicked.connect(self.on_export_clicked)
        bottom_controls.addWidget(self.export_button)
        
        # Add spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        bottom_controls.addItem(spacer)
        
        controls_layout.addLayout(bottom_controls)
        
        main_layout.addWidget(controls_group)
    
    def setup_log_display_section(self, main_layout):
        """Create the log display section."""
        # Log display container
        log_group = QGroupBox("Log Messages")
        log_group.setObjectName("log-group")
        log_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        log_layout = QVBoxLayout(log_group)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setObjectName("log-text")
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        
        # Set monospace font
        font = QFont("Consolas", 10)
        self.log_text.setFont(font)
        
        # Apply syntax highlighter
        self.highlighter = LogHighlighter(self.log_text.document())
        
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_group)
    
    def setup_connections(self):
        """Setup signal connections."""
        # Connect filter input
        self.filter_input.textChanged.connect(self.on_filter_changed)
        
        # Connect level combo
        self.level_combo.currentTextChanged.connect(self.on_level_changed)
        
        # Connect clear button
        self.clear_button.clicked.connect(self.on_clear_clicked)
        
        # Connect export button
        self.export_button.clicked.connect(self.on_export_clicked)
    
    def setup_styling(self):
        """Apply custom styling to the log console widget."""
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
            
            #filter-label, #level-label {
                font-size: 14px;
                color: #cccccc;
            }
            
            #filter-input {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 12px;
            }
            
            #filter-input:focus {
                border-color: #0066cc;
            }
            
            #level-combo {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 12px;
            }
            
            #level-combo:focus {
                border-color: #0066cc;
            }
            
            #auto-scroll-check {
                font-size: 14px;
                color: #cccccc;
            }
            
            #clear-button, #export-button {
                background-color: #404040;
                border: none;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 16px;
            }
            
            #clear-button:hover, #export-button:hover {
                background-color: #505050;
            }
            
            #clear-button:pressed, #export-button:pressed {
                background-color: #0066cc;
            }
            
            #log-text {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #ffffff;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
    
    def add_log_message(self, message: str, level: str = "info"):
        """Add a log message to the console."""
        from datetime import datetime
        
        # Create timestamp
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        
        # Create formatted message
        formatted_message = f"{timestamp} [{level.upper()}] {message}"
        
        # Add to internal list
        self.log_messages.append({
            'message': formatted_message,
            'level': level,
            'raw_message': message
        })
        
        # Apply filters
        if self.should_display_message(formatted_message, level):
            # Add to text widget
            cursor = self.log_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.log_text.setTextCursor(cursor)
            self.log_text.insertPlainText(formatted_message + "\n")
            
            # Auto-scroll if enabled
            if self.auto_scroll_check.isChecked():
                self.log_text.ensureCursorVisible()
    
    def should_display_message(self, message: str, level: str) -> bool:
        """Check if message should be displayed based on current filters."""
        # Check level filter
        current_level = self.level_combo.currentText()
        if current_level != "All" and level.lower() != current_level.lower():
            return False
        
        # Check text filter
        filter_text = self.filter_input.text().lower()
        if filter_text and filter_text not in message.lower():
            return False
        
        return True
    
    def on_filter_changed(self):
        """Handle filter text changes."""
        self.refresh_display()
    
    def on_level_changed(self):
        """Handle log level filter changes."""
        self.refresh_display()
    
    def refresh_display(self):
        """Refresh the log display based on current filters."""
        self.log_text.clear()
        
        for log_entry in self.log_messages:
            if self.should_display_message(log_entry['message'], log_entry['level']):
                self.log_text.append(log_entry['message'])
    
    def on_clear_clicked(self):
        """Handle clear button click."""
        self.log_messages.clear()
        self.log_text.clear()
        self.log_cleared.emit()
    
    def on_export_clicked(self):
        """Handle export button click."""
        from PySide6.QtWidgets import QFileDialog
        
        # Get save file path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Logs",
            "configo_logs.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for log_entry in self.log_messages:
                        f.write(log_entry['message'] + '\n')
                
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Logs exported to: {file_path}"
                )
            except Exception as e:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Failed to export logs: {str(e)}"
                )
    
    def get_log_count(self) -> int:
        """Get the total number of log messages."""
        return len(self.log_messages)
    
    def get_error_count(self) -> int:
        """Get the number of error messages."""
        return len([log for log in self.log_messages if log['level'] == 'error'])
    
    def get_warning_count(self) -> int:
        """Get the number of warning messages."""
        return len([log for log in self.log_messages if log['level'] == 'warning']) 