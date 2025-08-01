"""
CONFIGO GUI - Memory View Widget
================================

The memory view widget component for CONFIGO GUI application.
Displays session history, memory management, and user preferences.

Author: CONFIGO Team
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QListWidget, QListWidgetItem,
    QGroupBox, QSizePolicy, QSpacerItem, QTextEdit,
    QLineEdit, QComboBox, QCheckBox, QMessageBox,
    QTabWidget, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QIcon, QPixmap


class MemoryViewWidget(QWidget):
    """
    Memory view widget for CONFIGO GUI application.
    
    Features:
    - Session history display
    - Memory management
    - User preferences
    - Tool usage statistics
    """
    
    # Signals
    memory_cleared = Signal()  # Emitted when memory is cleared
    preference_updated = Signal(str, str)  # Emitted when a preference is updated
    
    def __init__(self):
        super().__init__()
        self.session_history = []
        self.user_preferences = {}
        self.tool_statistics = {}
        self.setup_ui()
        self.setup_connections()
        self.setup_styling()
        self.load_sample_data()
    
    def setup_ui(self):
        """Initialize the memory view UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header section
        self.setup_header_section(main_layout)
        
        # Tab widget for different sections
        self.setup_tab_widget(main_layout)
    
    def setup_header_section(self, main_layout):
        """Create the header section."""
        # Header container
        header_frame = QFrame()
        header_frame.setObjectName("header-frame")
        header_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title_label = QLabel("Memory & History")
        title_label.setObjectName("title-label")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Session history and user preferences")
        subtitle_label.setObjectName("subtitle-label")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_frame)
    
    def setup_tab_widget(self, main_layout):
        """Create the tab widget for different sections."""
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("memory-tabs")
        
        # Session History Tab
        self.setup_session_history_tab()
        
        # User Preferences Tab
        self.setup_preferences_tab()
        
        # Tool Statistics Tab
        self.setup_statistics_tab()
        
        # Memory Management Tab
        self.setup_memory_management_tab()
        
        main_layout.addWidget(self.tab_widget)
    
    def setup_session_history_tab(self):
        """Create the session history tab."""
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.setObjectName("history-list")
        history_layout.addWidget(self.history_list)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.clear_history_button = QPushButton("🗑️ Clear History")
        self.clear_history_button.setObjectName("clear-history-button")
        self.clear_history_button.clicked.connect(self.on_clear_history)
        controls_layout.addWidget(self.clear_history_button)
        
        self.export_history_button = QPushButton("📁 Export History")
        self.export_history_button.setObjectName("export-history-button")
        self.export_history_button.clicked.connect(self.on_export_history)
        controls_layout.addWidget(self.export_history_button)
        
        controls_layout.addStretch()
        history_layout.addLayout(controls_layout)
        
        self.tab_widget.addTab(history_widget, "📋 Session History")
    
    def setup_preferences_tab(self):
        """Create the user preferences tab."""
        preferences_widget = QWidget()
        preferences_layout = QVBoxLayout(preferences_widget)
        
        # Preferences table
        self.preferences_table = QTableWidget()
        self.preferences_table.setObjectName("preferences-table")
        self.preferences_table.setColumnCount(3)
        self.preferences_table.setHorizontalHeaderLabels(["Preference", "Value", "Actions"])
        preferences_layout.addWidget(self.preferences_table)
        
        # Add preference controls
        add_layout = QHBoxLayout()
        
        self.pref_name_input = QLineEdit()
        self.pref_name_input.setPlaceholderText("Preference name")
        add_layout.addWidget(self.pref_name_input)
        
        self.pref_value_input = QLineEdit()
        self.pref_value_input.setPlaceholderText("Preference value")
        add_layout.addWidget(self.pref_value_input)
        
        self.add_pref_button = QPushButton("➕ Add")
        self.add_pref_button.setObjectName("add-pref-button")
        self.add_pref_button.clicked.connect(self.on_add_preference)
        add_layout.addWidget(self.add_pref_button)
        
        preferences_layout.addLayout(add_layout)
        
        self.tab_widget.addTab(preferences_widget, "⚙️ User Preferences")
    
    def setup_statistics_tab(self):
        """Create the tool statistics tab."""
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        
        # Statistics table
        self.stats_table = QTableWidget()
        self.stats_table.setObjectName("stats-table")
        self.stats_table.setColumnCount(4)
        self.stats_table.setHorizontalHeaderLabels(["Tool", "Installations", "Success Rate", "Last Used"])
        stats_layout.addWidget(self.stats_table)
        
        # Summary
        self.stats_summary = QLabel("Loading statistics...")
        self.stats_summary.setObjectName("stats-summary")
        stats_layout.addWidget(self.stats_summary)
        
        self.tab_widget.addTab(stats_widget, "📊 Tool Statistics")
    
    def setup_memory_management_tab(self):
        """Create the memory management tab."""
        memory_widget = QWidget()
        memory_layout = QVBoxLayout(memory_widget)
        
        # Memory info
        memory_info_group = QGroupBox("Memory Information")
        memory_info_group.setObjectName("memory-info-group")
        memory_layout.addWidget(memory_info_group)
        
        memory_info_layout = QVBoxLayout(memory_info_group)
        
        self.memory_info_label = QLabel("Loading memory information...")
        self.memory_info_label.setObjectName("memory-info-label")
        memory_info_layout.addWidget(self.memory_info_label)
        
        # Memory controls
        memory_controls_group = QGroupBox("Memory Controls")
        memory_controls_group.setObjectName("memory-controls-group")
        memory_layout.addWidget(memory_controls_group)
        
        memory_controls_layout = QVBoxLayout(memory_controls_group)
        
        # Clear memory button
        self.clear_memory_button = QPushButton("🗑️ Clear All Memory")
        self.clear_memory_button.setObjectName("clear-memory-button")
        self.clear_memory_button.clicked.connect(self.on_clear_memory)
        memory_controls_layout.addWidget(self.clear_memory_button)
        
        # Export memory button
        self.export_memory_button = QPushButton("📁 Export Memory")
        self.export_memory_button.setObjectName("export-memory-button")
        self.export_memory_button.clicked.connect(self.on_export_memory)
        memory_controls_layout.addWidget(self.export_memory_button)
        
        # Memory settings
        settings_layout = QHBoxLayout()
        
        self.auto_save_check = QCheckBox("Auto-save memory")
        self.auto_save_check.setObjectName("auto-save-check")
        self.auto_save_check.setChecked(True)
        settings_layout.addWidget(self.auto_save_check)
        
        self.memory_limit_label = QLabel("Memory limit:")
        settings_layout.addWidget(self.memory_limit_label)
        
        self.memory_limit_combo = QComboBox()
        self.memory_limit_combo.setObjectName("memory-limit-combo")
        self.memory_limit_combo.addItems(["1 MB", "10 MB", "100 MB", "1 GB", "Unlimited"])
        self.memory_limit_combo.setCurrentText("100 MB")
        settings_layout.addWidget(self.memory_limit_combo)
        
        memory_controls_layout.addLayout(settings_layout)
        
        self.tab_widget.addTab(memory_widget, "💾 Memory Management")
    
    def setup_connections(self):
        """Setup signal connections."""
        # Connect buttons
        self.clear_history_button.clicked.connect(self.on_clear_history)
        self.export_history_button.clicked.connect(self.on_export_history)
        self.add_pref_button.clicked.connect(self.on_add_preference)
        self.clear_memory_button.clicked.connect(self.on_clear_memory)
        self.export_memory_button.clicked.connect(self.on_export_memory)
        
        # Connect settings
        self.auto_save_check.toggled.connect(self.on_auto_save_toggled)
        self.memory_limit_combo.currentTextChanged.connect(self.on_memory_limit_changed)
    
    def setup_styling(self):
        """Apply custom styling to the memory view widget."""
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
            
            #memory-tabs {
                background-color: #2b2b2b;
            }
            
            QTabWidget::pane {
                border: 2px solid #404040;
                border-radius: 8px;
                background-color: #2b2b2b;
            }
            
            QTabBar::tab {
                background-color: #404040;
                color: #ffffff;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            
            QTabBar::tab:selected {
                background-color: #0066cc;
            }
            
            QTabBar::tab:hover {
                background-color: #505050;
            }
            
            #history-list, #preferences-table, #stats-table {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            
            #history-list::item {
                padding: 8px;
                border-bottom: 1px solid #404040;
            }
            
            #history-list::item:hover {
                background-color: #404040;
            }
            
            QTableWidget {
                gridline-color: #404040;
            }
            
            QTableWidget::item {
                padding: 8px;
            }
            
            QTableWidget::item:selected {
                background-color: #0066cc;
            }
            
            QHeaderView::section {
                background-color: #404040;
                color: #ffffff;
                padding: 8px;
                border: none;
            }
            
            #clear-history-button, #export-history-button, #add-pref-button,
            #clear-memory-button, #export-memory-button {
                background-color: #404040;
                border: none;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 16px;
            }
            
            #clear-history-button:hover, #export-history-button:hover, #add-pref-button:hover,
            #clear-memory-button:hover, #export-memory-button:hover {
                background-color: #505050;
            }
            
            #clear-history-button:pressed, #export-history-button:pressed, #add-pref-button:pressed,
            #clear-memory-button:pressed, #export-memory-button:pressed {
                background-color: #0066cc;
            }
            
            QLineEdit {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 12px;
            }
            
            QLineEdit:focus {
                border-color: #0066cc;
            }
            
            QComboBox {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 12px;
            }
            
            QComboBox:focus {
                border-color: #0066cc;
            }
            
            QCheckBox {
                font-size: 14px;
                color: #cccccc;
            }
            
            #memory-info-label, #stats-summary {
                font-size: 14px;
                color: #cccccc;
                line-height: 1.5;
            }
        """)
    
    def load_sample_data(self):
        """Load sample data for demonstration."""
        # Sample session history
        sample_history = [
            "2024-01-15 10:30 - Python web development environment setup",
            "2024-01-15 11:45 - Installed Django and PostgreSQL",
            "2024-01-14 14:20 - React development environment setup",
            "2024-01-14 16:10 - Installed Node.js and npm packages",
            "2024-01-13 09:15 - AI/ML environment setup",
            "2024-01-13 11:30 - Installed TensorFlow and Jupyter"
        ]
        
        for entry in sample_history:
            item = QListWidgetItem(entry)
            self.history_list.addItem(item)
        
        # Sample user preferences
        sample_preferences = {
            "Default Python Version": "3.11",
            "Preferred Package Manager": "pip",
            "Auto-install Dependencies": "true",
            "Theme": "dark",
            "Log Level": "INFO"
        }
        
        self.user_preferences = sample_preferences
        self.update_preferences_table()
        
        # Sample tool statistics
        sample_stats = {
            "Python": {"installations": 15, "success_rate": "93%", "last_used": "2024-01-15"},
            "Node.js": {"installations": 8, "success_rate": "88%", "last_used": "2024-01-14"},
            "Docker": {"installations": 12, "success_rate": "92%", "last_used": "2024-01-13"},
            "Git": {"installations": 20, "success_rate": "95%", "last_used": "2024-01-15"}
        }
        
        self.tool_statistics = sample_stats
        self.update_statistics_table()
        
        # Update memory info
        self.update_memory_info()
    
    def update_preferences_table(self):
        """Update the preferences table."""
        self.preferences_table.setRowCount(len(self.user_preferences))
        
        for row, (key, value) in enumerate(self.user_preferences.items()):
            # Preference name
            name_item = QTableWidgetItem(key)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.preferences_table.setItem(row, 0, name_item)
            
            # Preference value
            value_item = QTableWidgetItem(value)
            self.preferences_table.setItem(row, 1, value_item)
            
            # Actions button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            delete_button = QPushButton("🗑️")
            delete_button.setObjectName("delete-pref-button")
            delete_button.clicked.connect(lambda checked, k=key: self.on_delete_preference(k))
            actions_layout.addWidget(delete_button)
            
            self.preferences_table.setCellWidget(row, 2, actions_widget)
    
    def update_statistics_table(self):
        """Update the statistics table."""
        self.stats_table.setRowCount(len(self.tool_statistics))
        
        for row, (tool, stats) in enumerate(self.tool_statistics.items()):
            # Tool name
            name_item = QTableWidgetItem(tool)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.stats_table.setItem(row, 0, name_item)
            
            # Installations
            installs_item = QTableWidgetItem(str(stats["installations"]))
            installs_item.setFlags(installs_item.flags() & ~Qt.ItemIsEditable)
            self.stats_table.setItem(row, 1, installs_item)
            
            # Success rate
            success_item = QTableWidgetItem(stats["success_rate"])
            success_item.setFlags(success_item.flags() & ~Qt.ItemIsEditable)
            self.stats_table.setItem(row, 2, success_item)
            
            # Last used
            last_used_item = QTableWidgetItem(stats["last_used"])
            last_used_item.setFlags(last_used_item.flags() & ~Qt.ItemIsEditable)
            self.stats_table.setItem(row, 3, last_used_item)
        
        # Update summary
        total_installations = sum(stats["installations"] for stats in self.tool_statistics.values())
        avg_success_rate = sum(float(stats["success_rate"].rstrip('%')) for stats in self.tool_statistics.values()) / len(self.tool_statistics)
        
        self.stats_summary.setText(
            f"Total installations: {total_installations} | "
            f"Average success rate: {avg_success_rate:.1f}% | "
            f"Tools tracked: {len(self.tool_statistics)}"
        )
    
    def update_memory_info(self):
        """Update the memory information display."""
        total_history = self.history_list.count()
        total_preferences = len(self.user_preferences)
        total_tools = len(self.tool_statistics)
        
        memory_info = f"""
        Memory Usage Summary:
        • Session History Entries: {total_history}
        • User Preferences: {total_preferences}
        • Tool Statistics: {total_tools}
        • Estimated Memory Size: ~2.5 MB
        • Last Updated: {self.get_current_timestamp()}
        """
        
        self.memory_info_label.setText(memory_info)
    
    def get_current_timestamp(self):
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def on_clear_history(self):
        """Handle clear history button click."""
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to clear all session history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.history_list.clear()
            self.session_history.clear()
            self.update_memory_info()
    
    def on_export_history(self):
        """Handle export history button click."""
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export History",
            "configo_history.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for i in range(self.history_list.count()):
                        item = self.history_list.item(i)
                        f.write(item.text() + '\n')
                
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"History exported to: {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Failed to export history: {str(e)}"
                )
    
    def on_add_preference(self):
        """Handle add preference button click."""
        name = self.pref_name_input.text().strip()
        value = self.pref_value_input.text().strip()
        
        if name and value:
            self.user_preferences[name] = value
            self.update_preferences_table()
            self.update_memory_info()
            
            # Clear inputs
            self.pref_name_input.clear()
            self.pref_value_input.clear()
            
            # Emit signal
            self.preference_updated.emit(name, value)
        else:
            QMessageBox.warning(self, "Invalid Input", "Please provide both name and value.")
    
    def on_delete_preference(self, key: str):
        """Handle delete preference button click."""
        if key in self.user_preferences:
            del self.user_preferences[key]
            self.update_preferences_table()
            self.update_memory_info()
    
    def on_clear_memory(self):
        """Handle clear memory button click."""
        reply = QMessageBox.question(
            self,
            "Clear Memory",
            "Are you sure you want to clear all memory data? This will reset all history, preferences, and statistics.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.history_list.clear()
            self.session_history.clear()
            self.user_preferences.clear()
            self.tool_statistics.clear()
            
            self.update_preferences_table()
            self.update_statistics_table()
            self.update_memory_info()
            
            self.memory_cleared.emit()
    
    def on_export_memory(self):
        """Handle export memory button click."""
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Memory",
            "configo_memory.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                import json
                
                memory_data = {
                    "session_history": [self.history_list.item(i).text() for i in range(self.history_list.count())],
                    "user_preferences": self.user_preferences,
                    "tool_statistics": self.tool_statistics,
                    "export_timestamp": self.get_current_timestamp()
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(memory_data, f, indent=2)
                
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Memory exported to: {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Failed to export memory: {str(e)}"
                )
    
    def on_auto_save_toggled(self, checked: bool):
        """Handle auto-save checkbox toggle."""
        # In a real implementation, this would save the setting
        pass
    
    def on_memory_limit_changed(self, limit: str):
        """Handle memory limit combo box change."""
        # In a real implementation, this would update the memory limit
        pass 