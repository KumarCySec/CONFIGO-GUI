"""
CONFIGO GUI - Portal Integration Widget
=======================================

The portal integration widget component for CONFIGO GUI application.
Manages login portals and browser integration for development services.

Author: CONFIGO Team
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QListWidget, QListWidgetItem,
    QGroupBox, QSizePolicy, QSpacerItem, QTextEdit,
    QLineEdit, QComboBox, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QTimer, QUrl
from PySide6.QtGui import QFont, QIcon, QPixmap, QDesktopServices


class PortalItem(QListWidgetItem):
    """
    Custom list item for portal entries.
    
    Features:
    - Portal name and description
    - Status indicator
    - URL information
    """
    
    def __init__(self, portal_info: dict):
        super().__init__()
        self.portal_info = portal_info
        self.setup_display()
    
    def setup_display(self):
        """Setup the display text and icon for the portal item."""
        name = self.portal_info.get('name', 'Unknown Portal')
        description = self.portal_info.get('description', '')
        status = self.portal_info.get('status', 'pending')
        
        # Set display text
        display_text = f"{name}"
        if description:
            display_text += f"\n{description}"
        
        self.setText(display_text)
        
        # Set status-based icon
        status_icons = {
            'pending': '⏳',
            'opened': '🌐',
            'completed': '✅',
            'failed': '❌'
        }
        
        icon = status_icons.get(status, '⏳')
        self.setIcon(QIcon(icon))


class PortalIntegrationWidget(QWidget):
    """
    Portal integration widget for CONFIGO GUI application.
    
    Features:
    - List of development portals
    - Browser integration
    - Portal status tracking
    - Manual portal management
    """
    
    # Signals
    portal_opened = Signal(str)  # Emitted when a portal is opened
    portal_completed = Signal(str)  # Emitted when a portal is marked as completed
    
    def __init__(self):
        super().__init__()
        self.portals = []
        self.setup_ui()
        self.setup_connections()
        self.setup_styling()
        self.load_default_portals()
    
    def setup_ui(self):
        """Initialize the portal integration UI components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header section
        self.setup_header_section(main_layout)
        
        # Portals section
        self.setup_portals_section(main_layout)
        
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
        title_label = QLabel("Portal Integration")
        title_label.setObjectName("title-label")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Manage login portals for development services")
        subtitle_label.setObjectName("subtitle-label")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_frame)
    
    def setup_portals_section(self, main_layout):
        """Create the portals section."""
        # Portals container
        portals_group = QGroupBox("Development Portals")
        portals_group.setObjectName("portals-group")
        portals_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        portals_layout = QVBoxLayout(portals_group)
        
        # Portals list
        self.portals_list = QListWidget()
        self.portals_list.setObjectName("portals-list")
        self.portals_list.itemDoubleClicked.connect(self.on_portal_double_clicked)
        portals_layout.addWidget(self.portals_list)
        
        main_layout.addWidget(portals_group)
    
    def setup_controls_section(self, main_layout):
        """Create the controls section."""
        # Controls container
        controls_group = QGroupBox("Portal Controls")
        controls_group.setObjectName("controls-group")
        controls_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        controls_layout = QVBoxLayout(controls_group)
        
        # Top row controls
        top_controls = QHBoxLayout()
        
        # Open selected button
        self.open_button = QPushButton("🌐 Open Selected")
        self.open_button.setObjectName("open-button")
        self.open_button.clicked.connect(self.on_open_selected)
        top_controls.addWidget(self.open_button)
        
        # Mark completed button
        self.complete_button = QPushButton("✅ Mark Completed")
        self.complete_button.setObjectName("complete-button")
        self.complete_button.clicked.connect(self.on_mark_completed)
        top_controls.addWidget(self.complete_button)
        
        # Refresh button
        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.setObjectName("refresh-button")
        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        top_controls.addWidget(self.refresh_button)
        
        controls_layout.addLayout(top_controls)
        
        # Bottom row controls
        bottom_controls = QHBoxLayout()
        
        # Add custom portal
        self.add_button = QPushButton("➕ Add Portal")
        self.add_button.setObjectName("add-button")
        self.add_button.clicked.connect(self.on_add_portal)
        bottom_controls.addWidget(self.add_button)
        
        # Remove portal
        self.remove_button = QPushButton("🗑️ Remove")
        self.remove_button.setObjectName("remove-button")
        self.remove_button.clicked.connect(self.on_remove_portal)
        bottom_controls.addWidget(self.remove_button)
        
        # Add spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        bottom_controls.addItem(spacer)
        
        controls_layout.addLayout(bottom_controls)
        
        main_layout.addWidget(controls_group)
    
    def setup_connections(self):
        """Setup signal connections."""
        # Connect portal list selection
        self.portals_list.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Connect buttons
        self.open_button.clicked.connect(self.on_open_selected)
        self.complete_button.clicked.connect(self.on_mark_completed)
        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        self.add_button.clicked.connect(self.on_add_portal)
        self.remove_button.clicked.connect(self.on_remove_portal)
    
    def setup_styling(self):
        """Apply custom styling to the portal integration widget."""
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
            
            #portals-list {
                background-color: #1e1e1e;
                border: 2px solid #404040;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            
            #portals-list::item {
                padding: 10px;
                border-bottom: 1px solid #404040;
            }
            
            #portals-list::item:hover {
                background-color: #404040;
            }
            
            #portals-list::item:selected {
                background-color: #0066cc;
            }
            
            #open-button, #complete-button, #refresh-button, #add-button, #remove-button {
                background-color: #404040;
                border: none;
                border-radius: 6px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 16px;
            }
            
            #open-button:hover, #complete-button:hover, #refresh-button:hover, #add-button:hover, #remove-button:hover {
                background-color: #505050;
            }
            
            #open-button:pressed, #complete-button:pressed, #refresh-button:pressed, #add-button:pressed, #remove-button:pressed {
                background-color: #0066cc;
            }
            
            #open-button:disabled, #complete-button:disabled, #remove-button:disabled {
                background-color: #2a2a2a;
                color: #666666;
            }
        """)
    
    def load_default_portals(self):
        """Load default development portals."""
        default_portals = [
            {
                'name': 'GitHub',
                'url': 'https://github.com',
                'description': 'Code hosting and version control',
                'status': 'pending'
            },
            {
                'name': 'ChatGPT',
                'url': 'https://chat.openai.com',
                'description': 'AI assistant for coding help',
                'status': 'pending'
            },
            {
                'name': 'Claude',
                'url': 'https://claude.ai',
                'description': 'Anthropic AI assistant',
                'status': 'pending'
            },
            {
                'name': 'Stack Overflow',
                'url': 'https://stackoverflow.com',
                'description': 'Developer Q&A community',
                'status': 'pending'
            },
            {
                'name': 'Docker Hub',
                'url': 'https://hub.docker.com',
                'description': 'Container registry and images',
                'status': 'pending'
            },
            {
                'name': 'PyPI',
                'url': 'https://pypi.org',
                'description': 'Python package index',
                'status': 'pending'
            },
            {
                'name': 'npm',
                'url': 'https://www.npmjs.com',
                'description': 'Node.js package registry',
                'status': 'pending'
            }
        ]
        
        for portal in default_portals:
            self.add_portal(portal)
    
    def add_portal(self, portal_info: dict):
        """Add a portal to the list."""
        self.portals.append(portal_info)
        item = PortalItem(portal_info)
        self.portals_list.addItem(item)
    
    def get_selected_portal(self):
        """Get the currently selected portal."""
        current_item = self.portals_list.currentItem()
        if current_item:
            return current_item.portal_info
        return None
    
    def update_portal_status(self, portal_name: str, status: str):
        """Update the status of a portal."""
        for i in range(self.portals_list.count()):
            item = self.portals_list.item(i)
            if item.portal_info['name'] == portal_name:
                item.portal_info['status'] = status
                item.setup_display()
                break
    
    def on_selection_changed(self):
        """Handle portal selection changes."""
        selected_portal = self.get_selected_portal()
        
        # Update button states
        has_selection = selected_portal is not None
        self.open_button.setEnabled(has_selection)
        self.complete_button.setEnabled(has_selection)
        self.remove_button.setEnabled(has_selection)
    
    def on_portal_double_clicked(self, item):
        """Handle portal double-click."""
        self.open_portal(item.portal_info)
    
    def on_open_selected(self):
        """Handle open selected button click."""
        selected_portal = self.get_selected_portal()
        if selected_portal:
            self.open_portal(selected_portal)
    
    def open_portal(self, portal_info: dict):
        """Open a portal in the default browser."""
        url = portal_info.get('url', '')
        if not url:
            QMessageBox.warning(self, "Invalid URL", "No URL specified for this portal.")
            return
        
        try:
            # Open URL in default browser
            QDesktopServices.openUrl(QUrl(url))
            
            # Update portal status
            portal_name = portal_info.get('name', '')
            self.update_portal_status(portal_name, 'opened')
            
            # Emit signal
            self.portal_opened.emit(portal_name)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open portal: {str(e)}")
    
    def on_mark_completed(self):
        """Handle mark completed button click."""
        selected_portal = self.get_selected_portal()
        if selected_portal:
            portal_name = selected_portal.get('name', '')
            self.update_portal_status(portal_name, 'completed')
            self.portal_completed.emit(portal_name)
    
    def on_refresh_clicked(self):
        """Handle refresh button click."""
        # Reset all portal statuses to pending
        for portal in self.portals:
            portal['status'] = 'pending'
        
        # Refresh the list display
        for i in range(self.portals_list.count()):
            item = self.portals_list.item(i)
            item.setup_display()
    
    def on_add_portal(self):
        """Handle add portal button click."""
        from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Portal")
        dialog.setModal(True)
        
        # Create form layout
        layout = QFormLayout(dialog)
        
        # Add form fields
        name_input = QLineEdit()
        name_input.setPlaceholderText("Portal name")
        layout.addRow("Name:", name_input)
        
        url_input = QLineEdit()
        url_input.setPlaceholderText("https://example.com")
        layout.addRow("URL:", url_input)
        
        desc_input = QLineEdit()
        desc_input.setPlaceholderText("Portal description")
        layout.addRow("Description:", desc_input)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        # Show dialog
        if dialog.exec() == QDialog.Accepted:
            name = name_input.text().strip()
            url = url_input.text().strip()
            description = desc_input.text().strip()
            
            if name and url:
                portal_info = {
                    'name': name,
                    'url': url,
                    'description': description,
                    'status': 'pending'
                }
                self.add_portal(portal_info)
            else:
                QMessageBox.warning(self, "Invalid Input", "Please provide both name and URL.")
    
    def on_remove_portal(self):
        """Handle remove portal button click."""
        selected_portal = self.get_selected_portal()
        if selected_portal:
            portal_name = selected_portal.get('name', '')
            
            # Confirm removal
            reply = QMessageBox.question(
                self,
                "Remove Portal",
                f"Are you sure you want to remove '{portal_name}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Remove from list
                self.portals = [p for p in self.portals if p['name'] != portal_name]
                
                # Remove from list widget
                current_row = self.portals_list.currentRow()
                if current_row >= 0:
                    self.portals_list.takeItem(current_row)
    
    def get_portal_count(self) -> int:
        """Get the total number of portals."""
        return len(self.portals)
    
    def get_completed_count(self) -> int:
        """Get the number of completed portals."""
        return len([p for p in self.portals if p.get('status') == 'completed'])
    
    def get_opened_count(self) -> int:
        """Get the number of opened portals."""
        return len([p for p in self.portals if p.get('status') == 'opened']) 