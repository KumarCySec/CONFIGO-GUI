"""
CONFIGO GUI - Error Handler Widget
==================================

The error handler widget component for CONFIGO GUI application.
Displays errors and provides error recovery options.

Author: CONFIGO Team
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QTextEdit, QGroupBox,
    QSizePolicy, QSpacerItem, QMessageBox, QDialog,
    QDialogButtonBox, QScrollArea, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor


class ErrorDialog(QDialog):
    """
    Custom error dialog for displaying detailed error information.
    
    Features:
    - Error details with stack trace
    - Recovery suggestions
    - Action buttons
    """
    
    def __init__(self, error_title: str, error_message: str, error_details: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error - CONFIGO")
        self.setModal(True)
        self.setMinimumSize(600, 400)
        
        self.setup_ui(error_title, error_message, error_details)
        self.setup_styling()
    
    def setup_ui(self, error_title: str, error_message: str, error_details: str):
        """Initialize the error dialog UI."""
        layout = QVBoxLayout(self)
        
        # Error icon and title
        header_layout = QHBoxLayout()
        
        error_icon = QLabel("❌")
        error_icon.setObjectName("error-icon")
        header_layout.addWidget(error_icon)
        
        title_label = QLabel(error_title)
        title_label.setObjectName("error-title")
        header_layout.addWidget(title_label)
        
        layout.addLayout(header_layout)
        
        # Error message
        message_label = QLabel(error_message)
        message_label.setObjectName("error-message")
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        # Error details (collapsible)
        if error_details:
            details_group = QGroupBox("Error Details")
            details_group.setObjectName("details-group")
            details_group.setCheckable(True)
            details_group.setChecked(False)
            
            details_text = QTextEdit()
            details_text.setObjectName("details-text")
            details_text.setPlainText(error_details)
            details_text.setReadOnly(True)
            details_text.setMaximumHeight(150)
            details_group.layout().addWidget(details_text)
            
            layout.addWidget(details_group)
        
        # Recovery suggestions
        suggestions_group = QGroupBox("Recovery Suggestions")
        suggestions_group.setObjectName("suggestions-group")
        
        suggestions_text = QTextEdit()
        suggestions_text.setObjectName("suggestions-text")
        suggestions_text.setPlainText(self.get_recovery_suggestions(error_message))
        suggestions_text.setReadOnly(True)
        suggestions_text.setMaximumHeight(100)
        suggestions_group.layout().addWidget(suggestions_text)
        
        layout.addWidget(suggestions_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        retry_button = QPushButton("🔄 Retry")
        retry_button.setObjectName("retry-button")
        retry_button.clicked.connect(self.accept)
        button_layout.addWidget(retry_button)
        
        ignore_button = QPushButton("⏭️ Ignore")
        ignore_button.setObjectName("ignore-button")
        ignore_button.clicked.connect(self.reject)
        button_layout.addWidget(ignore_button)
        
        button_layout.addStretch()
        
        close_button = QPushButton("❌ Close")
        close_button.setObjectName("close-button")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def setup_styling(self):
        """Apply custom styling to the error dialog."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            
            #error-icon {
                font-size: 24px;
                color: #ff4444;
            }
            
            #error-title {
                font-size: 18px;
                font-weight: bold;
                color: #ff4444;
            }
            
            #error-message {
                font-size: 14px;
                color: #ffffff;
                line-height: 1.5;
                padding: 10px;
                background-color: #1e1e1e;
                border-radius: 6px;
            }
            
            QGroupBox {
                font-size: 14px;
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
            
            #details-text, #suggestions-text {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 6px;
                color: #ffffff;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                padding: 8px;
            }
            
            #retry-button, #ignore-button, #close-button {
                background-color: #404040;
                border: none;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 16px;
            }
            
            #retry-button:hover {
                background-color: #0066cc;
            }
            
            #ignore-button:hover {
                background-color: #ffaa00;
            }
            
            #close-button:hover {
                background-color: #ff4444;
            }
        """)
    
    def get_recovery_suggestions(self, error_message: str) -> str:
        """Get recovery suggestions based on error message."""
        error_lower = error_message.lower()
        
        suggestions = []
        
        if "permission" in error_lower or "access denied" in error_lower:
            suggestions.extend([
                "• Run the application with administrator privileges",
                "• Check file and folder permissions",
                "• Ensure you have write access to the installation directory"
            ])
        
        if "network" in error_lower or "connection" in error_lower:
            suggestions.extend([
                "• Check your internet connection",
                "• Verify firewall settings",
                "• Try using a different network"
            ])
        
        if "not found" in error_lower or "missing" in error_lower:
            suggestions.extend([
                "• Verify the file or tool exists",
                "• Check the installation path",
                "• Reinstall the missing component"
            ])
        
        if "timeout" in error_lower:
            suggestions.extend([
                "• Check your internet connection speed",
                "• Try again in a few minutes",
                "• Increase timeout settings if available"
            ])
        
        if not suggestions:
            suggestions = [
                "• Check the error details above for more information",
                "• Try restarting the application",
                "• Contact support if the problem persists"
            ]
        
        return "\n".join(suggestions)


class ErrorHandlerWidget(QWidget):
    """
    Error handler widget for CONFIGO GUI application.
    
    Features:
    - Error log display
    - Error recovery options
    - Error statistics
    - Error filtering
    """
    
    # Signals
    error_retry_requested = Signal(str)  # Emitted when retry is requested
    error_ignored = Signal(str)  # Emitted when error is ignored
    
    def __init__(self):
        super().__init__()
        self.errors = []
        self.setup_ui()
        self.setup_connections()
        self.setup_styling()
    
    def setup_ui(self):
        """Initialize the error handler UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header section
        self.setup_header_section(main_layout)
        
        # Error display section
        self.setup_error_display_section(main_layout)
        
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
        title_label = QLabel("Error Handler")
        title_label.setObjectName("title-label")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Error tracking and recovery management")
        subtitle_label.setObjectName("subtitle-label")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_frame)
    
    def setup_error_display_section(self, main_layout):
        """Create the error display section."""
        # Error display container
        error_group = QGroupBox("Error Log")
        error_group.setObjectName("error-group")
        error_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        error_layout = QVBoxLayout(error_group)
        
        # Error list
        self.error_list = QListWidget()
        self.error_list.setObjectName("error-list")
        self.error_list.itemDoubleClicked.connect(self.on_error_double_clicked)
        error_layout.addWidget(self.error_list)
        
        main_layout.addWidget(error_group)
    
    def setup_controls_section(self, main_layout):
        """Create the controls section."""
        # Controls container
        controls_group = QGroupBox("Error Controls")
        controls_group.setObjectName("controls-group")
        controls_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        controls_layout = QVBoxLayout(controls_group)
        
        # Top row controls
        top_controls = QHBoxLayout()
        
        # Retry selected button
        self.retry_button = QPushButton("🔄 Retry Selected")
        self.retry_button.setObjectName("retry-button")
        self.retry_button.clicked.connect(self.on_retry_selected)
        top_controls.addWidget(self.retry_button)
        
        # Ignore selected button
        self.ignore_button = QPushButton("⏭️ Ignore Selected")
        self.ignore_button.setObjectName("ignore-button")
        self.ignore_button.clicked.connect(self.on_ignore_selected)
        top_controls.addWidget(self.ignore_button)
        
        # Clear errors button
        self.clear_button = QPushButton("🗑️ Clear All")
        self.clear_button.setObjectName("clear-button")
        self.clear_button.clicked.connect(self.on_clear_errors)
        top_controls.addWidget(self.clear_button)
        
        controls_layout.addLayout(top_controls)
        
        # Bottom row controls
        bottom_controls = QHBoxLayout()
        
        # Error statistics
        self.stats_label = QLabel("No errors recorded")
        self.stats_label.setObjectName("stats-label")
        bottom_controls.addWidget(self.stats_label)
        
        bottom_controls.addStretch()
        
        # Export errors button
        self.export_button = QPushButton("📁 Export Errors")
        self.export_button.setObjectName("export-button")
        self.export_button.clicked.connect(self.on_export_errors)
        bottom_controls.addWidget(self.export_button)
        
        controls_layout.addLayout(bottom_controls)
        
        main_layout.addWidget(controls_group)
    
    def setup_connections(self):
        """Setup signal connections."""
        # Connect error list selection
        self.error_list.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Connect buttons
        self.retry_button.clicked.connect(self.on_retry_selected)
        self.ignore_button.clicked.connect(self.on_ignore_selected)
        self.clear_button.clicked.connect(self.on_clear_errors)
        self.export_button.clicked.connect(self.on_export_errors)
    
    def setup_styling(self):
        """Apply custom styling to the error handler widget."""
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
            
            #error-list {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            
            #error-list::item {
                padding: 10px;
                border-bottom: 1px solid #404040;
            }
            
            #error-list::item:hover {
                background-color: #404040;
            }
            
            #error-list::item:selected {
                background-color: #0066cc;
            }
            
            #retry-button, #ignore-button, #clear-button, #export-button {
                background-color: #404040;
                border: none;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 16px;
            }
            
            #retry-button:hover {
                background-color: #0066cc;
            }
            
            #ignore-button:hover {
                background-color: #ffaa00;
            }
            
            #clear-button:hover, #export-button:hover {
                background-color: #505050;
            }
            
            #retry-button:disabled, #ignore-button:disabled {
                background-color: #2a2a2a;
                color: #666666;
            }
            
            #stats-label {
                font-size: 14px;
                color: #cccccc;
            }
        """)
    
    def add_error(self, error_title: str, error_message: str, error_details: str = "", error_type: str = "error"):
        """Add an error to the error log."""
        from datetime import datetime
        
        error_info = {
            'title': error_title,
            'message': error_message,
            'details': error_details,
            'type': error_type,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'active'
        }
        
        self.errors.append(error_info)
        
        # Create list item
        item_text = f"[{error_info['timestamp']}] {error_title}"
        item = QListWidgetItem(item_text)
        item.setData(Qt.UserRole, error_info)
        
        # Set icon based on error type
        type_icons = {
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        item.setIcon(QIcon(type_icons.get(error_type, '❌')))
        
        self.error_list.addItem(item)
        self.update_statistics()
    
    def get_selected_error(self):
        """Get the currently selected error."""
        current_item = self.error_list.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None
    
    def update_statistics(self):
        """Update error statistics display."""
        total_errors = len(self.errors)
        active_errors = len([e for e in self.errors if e['status'] == 'active'])
        ignored_errors = len([e for e in self.errors if e['status'] == 'ignored'])
        
        if total_errors == 0:
            self.stats_label.setText("No errors recorded")
        else:
            self.stats_label.setText(
                f"Total: {total_errors} | Active: {active_errors} | Ignored: {ignored_errors}"
            )
    
    def on_selection_changed(self):
        """Handle error selection changes."""
        selected_error = self.get_selected_error()
        
        # Update button states
        has_selection = selected_error is not None
        self.retry_button.setEnabled(has_selection)
        self.ignore_button.setEnabled(has_selection)
    
    def on_error_double_clicked(self, item):
        """Handle error double-click."""
        error_info = item.data(Qt.UserRole)
        self.show_error_dialog(error_info)
    
    def show_error_dialog(self, error_info: dict):
        """Show detailed error dialog."""
        dialog = ErrorDialog(
            error_info['title'],
            error_info['message'],
            error_info['details'],
            self
        )
        
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            # Retry requested
            self.error_retry_requested.emit(error_info['title'])
        elif result == QDialog.Rejected:
            # Ignore requested
            self.mark_error_ignored(error_info)
    
    def mark_error_ignored(self, error_info: dict):
        """Mark an error as ignored."""
        error_info['status'] = 'ignored'
        
        # Update list item
        for i in range(self.error_list.count()):
            item = self.error_list.item(i)
            if item.data(Qt.UserRole) == error_info:
                item.setIcon(QIcon('⏭️'))
                break
        
        self.error_ignored.emit(error_info['title'])
        self.update_statistics()
    
    def on_retry_selected(self):
        """Handle retry selected button click."""
        selected_error = self.get_selected_error()
        if selected_error:
            self.error_retry_requested.emit(selected_error['title'])
    
    def on_ignore_selected(self):
        """Handle ignore selected button click."""
        selected_error = self.get_selected_error()
        if selected_error:
            self.mark_error_ignored(selected_error)
    
    def on_clear_errors(self):
        """Handle clear errors button click."""
        reply = QMessageBox.question(
            self,
            "Clear Errors",
            "Are you sure you want to clear all error logs?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.error_list.clear()
            self.errors.clear()
            self.update_statistics()
    
    def on_export_errors(self):
        """Handle export errors button click."""
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Errors",
            "configo_errors.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for error in self.errors:
                        f.write(f"[{error['timestamp']}] {error['title']}\n")
                        f.write(f"Message: {error['message']}\n")
                        if error['details']:
                            f.write(f"Details: {error['details']}\n")
                        f.write(f"Status: {error['status']}\n")
                        f.write("-" * 50 + "\n")
                
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Errors exported to: {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Failed to export errors: {str(e)}"
                )
    
    def get_error_count(self) -> int:
        """Get the total number of errors."""
        return len(self.errors)
    
    def get_active_error_count(self) -> int:
        """Get the number of active errors."""
        return len([e for e in self.errors if e['status'] == 'active'])
    
    def get_ignored_error_count(self) -> int:
        """Get the number of ignored errors."""
        return len([e for e in self.errors if e['status'] == 'ignored']) 