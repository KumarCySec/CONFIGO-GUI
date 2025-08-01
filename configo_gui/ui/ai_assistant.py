"""
CONFIGO GUI - AI Assistant Panel
================================

The AI assistant panel component for CONFIGO GUI application.
Provides a chatbot interface for users to interact with the AI agent.

Features:
- Real-time chat interface
- AI-powered responses
- Context-aware suggestions
- Code highlighting
- Voice feedback (optional)

Author: CONFIGO Team
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QTextEdit, QLineEdit,
    QScrollArea, QSizePolicy, QSpacerItem,
    QSplitter, QListWidget, QListWidgetItem,
    QGroupBox, QGridLayout, QProgressBar
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QThread
from PySide6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QTextCursor, QSyntaxHighlighter, QTextCharFormat


class CodeHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for code blocks in chat messages."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_formats()
    
    def setup_formats(self):
        """Setup text formats for syntax highlighting."""
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#FF6B6B"))
        self.keyword_format.setFontWeight(QFont.Bold)
        
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#4ECDC4"))
        
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#95A5A6"))
        self.comment_format.setFontItalic(True)
        
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor("#F7DC6F"))
        
        # Python keywords
        self.keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
            'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
            'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
            'with', 'yield', 'True', 'False', 'None'
        ]
    
    def highlightBlock(self, text):
        """Highlight code syntax in the text block."""
        # Highlight keywords
        for keyword in self.keywords:
            index = 0
            while index < len(text):
                index = text.find(keyword, index)
                if index == -1:
                    break
                length = len(keyword)
                self.setFormat(index, length, self.keyword_format)
                index += length
        
        # Highlight strings
        import re
        string_pattern = r'"[^"]*"|\'[^\']*\''
        for match in re.finditer(string_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.string_format)
        
        # Highlight comments
        comment_pattern = r'#.*$'
        for match in re.finditer(comment_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.comment_format)
        
        # Highlight function calls
        function_pattern = r'\b\w+(?=\()'
        for match in re.finditer(function_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.function_format)


class ChatMessage(QWidget):
    """Individual chat message widget."""
    
    def __init__(self, message: str, is_user: bool = True, timestamp: Optional[datetime] = None):
        super().__init__()
        self.message = message
        self.is_user = is_user
        self.timestamp = timestamp or datetime.now()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the chat message UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Create message bubble
        bubble = QFrame()
        bubble.setObjectName("chat-bubble")
        bubble.setMaximumWidth(400)
        
        bubble_layout = QVBoxLayout(bubble)
        
        # Message text
        message_text = QTextEdit()
        message_text.setObjectName("message-text")
        message_text.setPlainText(self.message)
        message_text.setReadOnly(True)
        message_text.setMaximumHeight(150)
        message_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Apply syntax highlighting for code blocks
        if "```" in self.message:
            highlighter = CodeHighlighter(message_text.document())
        
        bubble_layout.addWidget(message_text)
        
        # Timestamp
        timestamp_label = QLabel(self.timestamp.strftime("%H:%M"))
        timestamp_label.setObjectName("timestamp-label")
        timestamp_label.setAlignment(Qt.AlignRight)
        bubble_layout.addWidget(timestamp_label)
        
        # Add bubble to layout with proper alignment
        if self.is_user:
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addStretch()
        
        # Apply styling
        self.setup_styling()
    
    def setup_styling(self):
        """Apply styling to the chat message."""
        user_style = """
            #chat-bubble {
                background-color: #0066cc;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
            }
            
            #message-text {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            
            #timestamp-label {
                color: #cccccc;
                font-size: 11px;
                margin-top: 5px;
            }
        """
        
        ai_style = """
            #chat-bubble {
                background-color: #2c3e50;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
                border: 1px solid #34495e;
            }
            
            #message-text {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            
            #timestamp-label {
                color: #95a5a6;
                font-size: 11px;
                margin-top: 5px;
            }
        """
        
        self.setStyleSheet(user_style if self.is_user else ai_style)


class AIAssistantPanel(QWidget):
    """
    AI Assistant Panel for CONFIGO GUI application.
    
    Features:
    - Real-time chat interface
    - AI-powered responses
    - Context-aware suggestions
    - Code highlighting
    - Voice feedback (optional)
    """
    
    # Signals
    message_sent = Signal(str)  # Emitted when user sends a message
    ai_response_received = Signal(str)  # Emitted when AI responds
    
    def __init__(self):
        super().__init__()
        self.chat_history = []
        self.setup_ui()
        self.setup_connections()
        self.setup_styling()
        
        # Add welcome message
        self.add_ai_message(
            "Hello! I'm your CONFIGO AI assistant. I can help you with:\n\n"
            "• Setting up development environments\n"
            "• Troubleshooting installation issues\n"
            "• Explaining tools and configurations\n"
            "• Providing code examples\n"
            "• Optimizing your setup\n\n"
            "Just ask me anything about your development environment!"
        )
    
    def setup_ui(self):
        """Initialize the AI assistant panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self.setup_header(layout)
        
        # Chat area
        self.setup_chat_area(layout)
        
        # Input area
        self.setup_input_area(layout)
        
        # Suggestions area
        self.setup_suggestions_area(layout)
    
    def setup_header(self, layout):
        """Setup the header section."""
        header = QFrame()
        header.setObjectName("assistant-header")
        header.setMaximumHeight(60)
        
        header_layout = QHBoxLayout(header)
        
        # AI icon and title
        icon_label = QLabel("🤖")
        icon_label.setObjectName("ai-icon")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel("AI Assistant")
        title_label.setObjectName("assistant-title")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Status indicator
        self.status_label = QLabel("● Online")
        self.status_label.setObjectName("status-indicator")
        header_layout.addWidget(self.status_label)
        
        layout.addWidget(header)
    
    def setup_chat_area(self, layout):
        """Setup the chat messages area."""
        # Chat container
        chat_container = QFrame()
        chat_container.setObjectName("chat-container")
        
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)
        
        # Scroll area for messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Messages widget
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setAlignment(Qt.AlignTop)
        self.messages_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.messages_widget)
        chat_layout.addWidget(self.scroll_area)
        
        layout.addWidget(chat_container)
    
    def setup_input_area(self, layout):
        """Setup the message input area."""
        input_container = QFrame()
        input_container.setObjectName("input-container")
        input_container.setMaximumHeight(120)
        
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(15, 10, 15, 10)
        
        # Message input
        self.message_input = QLineEdit()
        self.message_input.setObjectName("message-input")
        self.message_input.setPlaceholderText("Ask me anything about your development environment...")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setObjectName("send-button")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addWidget(input_container)
    
    def setup_suggestions_area(self, layout):
        """Setup the quick suggestions area."""
        suggestions_container = QFrame()
        suggestions_container.setObjectName("suggestions-container")
        suggestions_container.setMaximumHeight(80)
        
        suggestions_layout = QHBoxLayout(suggestions_container)
        suggestions_layout.setContentsMargins(15, 10, 15, 10)
        
        # Quick suggestion buttons
        suggestions = [
            "Setup Python environment",
            "Install Node.js tools",
            "Configure Docker",
            "Setup Git workflow"
        ]
        
        for suggestion in suggestions:
            button = QPushButton(suggestion)
            button.setObjectName("suggestion-button")
            button.clicked.connect(lambda checked, text=suggestion: self.send_suggestion(text))
            suggestions_layout.addWidget(button)
        
        suggestions_layout.addStretch()
        layout.addWidget(suggestions_container)
    
    def setup_connections(self):
        """Setup signal connections."""
        pass  # Will be connected by parent widget
    
    def setup_styling(self):
        """Apply styling to the AI assistant panel."""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            
            #assistant-header {
                background-color: #2c2c2c;
                border-bottom: 1px solid #3c3c3c;
                padding: 10px;
            }
            
            #ai-icon {
                font-size: 24px;
                margin-right: 10px;
            }
            
            #assistant-title {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #status-indicator {
                color: #4CAF50;
                font-size: 12px;
            }
            
            #chat-container {
                background-color: #1e1e1e;
                border: none;
            }
            
            #input-container {
                background-color: #2c2c2c;
                border-top: 1px solid #3c3c3c;
            }
            
            #message-input {
                background-color: #3c3c3c;
                border: 1px solid #4c4c4c;
                border-radius: 20px;
                padding: 10px 15px;
                color: #ffffff;
                font-size: 14px;
            }
            
            #message-input:focus {
                border-color: #0066cc;
            }
            
            #send-button {
                background-color: #0066cc;
                border: none;
                border-radius: 20px;
                color: #ffffff;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            
            #send-button:hover {
                background-color: #0077ee;
            }
            
            #suggestions-container {
                background-color: #2c2c2c;
                border-top: 1px solid #3c3c3c;
            }
            
            #suggestion-button {
                background-color: #3c3c3c;
                border: 1px solid #4c4c4c;
                border-radius: 15px;
                color: #ffffff;
                padding: 8px 15px;
                font-size: 12px;
            }
            
            #suggestion-button:hover {
                background-color: #4c4c4c;
                border-color: #0066cc;
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
    
    def add_user_message(self, message: str):
        """Add a user message to the chat."""
        chat_message = ChatMessage(message, is_user=True)
        self.messages_layout.addWidget(chat_message)
        self.chat_history.append({"role": "user", "content": message, "timestamp": datetime.now()})
        self.scroll_to_bottom()
    
    def add_ai_message(self, message: str):
        """Add an AI message to the chat."""
        chat_message = ChatMessage(message, is_user=False)
        self.messages_layout.addWidget(chat_message)
        self.chat_history.append({"role": "assistant", "content": message, "timestamp": datetime.now()})
        self.scroll_to_bottom()
    
    def send_message(self):
        """Send the current message."""
        message = self.message_input.text().strip()
        if message:
            self.add_user_message(message)
            self.message_input.clear()
            self.message_sent.emit(message)
    
    def send_suggestion(self, suggestion: str):
        """Send a quick suggestion."""
        self.add_user_message(suggestion)
        self.message_sent.emit(suggestion)
    
    def receive_ai_response(self, response: str):
        """Receive and display an AI response."""
        self.add_ai_message(response)
        self.ai_response_received.emit(response)
    
    def scroll_to_bottom(self):
        """Scroll the chat to the bottom."""
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))
    
    def clear_chat(self):
        """Clear the chat history."""
        for i in reversed(range(self.messages_layout.count())):
            widget = self.messages_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.chat_history.clear()
    
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """Get the chat history."""
        return self.chat_history.copy() 