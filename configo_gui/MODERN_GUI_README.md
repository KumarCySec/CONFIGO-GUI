# CONFIGO GUI - Modern Desktop Application

![CONFIGO GUI](https://img.shields.io/badge/CONFIGO-GUI-blue?style=for-the-badge&logo=python)
![Version](https://img.shields.io/badge/version-2.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge)

A modern, cross-platform GUI desktop application for CONFIGO, the Autonomous AI Setup Agent. Built with PySide6 (Qt for Python) featuring advanced glassmorphism effects, smooth animations, and a premium user experience.

## ✨ Features

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Transparent panels with blur effects
- **Smooth Animations**: Hover effects, transitions, and loading spinners
- **Modern Color Scheme**: Dark theme with gradient backgrounds
- **Responsive Layout**: Adaptive design for different screen sizes
- **Custom Typography**: Inter font family with proper hierarchy

### 🧠 AI-Powered Features
- **Environment Setup**: Intelligent detection and configuration
- **Visual Plan Rendering**: Animated timeline of installation steps
- **Real-time Console**: Syntax-highlighted log output
- **Portal Integration**: Seamless login flows for AI services
- **Memory Management**: Visual timeline of past sessions
- **Predictive Suggestions**: AI-powered recommendations

### ⚡ Performance & Reliability
- **Async Operations**: Non-blocking backend processes
- **Error Handling**: Graceful error recovery with modals
- **Status Updates**: Real-time progress indicators
- **Cross-platform**: Works on macOS, Linux, and Windows

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PySide6 6.6.0+
- CONFIGO CLI backend

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/configo-gui.git
cd configo-gui
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

### Development Setup

1. **Install development dependencies**
```bash
pip install -r requirements-dev.txt
```

2. **Run with debugging**
```bash
python main.py --debug
```

## 🏗️ Architecture

### File Structure
```
configo_gui/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── ui/
│   ├── modern_main_window.py    # Main window with glassmorphism
│   ├── themes/                  # Modern styling system
│   │   ├── glass_theme.py       # Glassmorphism theme
│   │   ├── animations.py        # Animation manager
│   │   └── modern_styles.py     # Component styles
│   ├── components/              # Reusable UI components
│   │   ├── glass_card.py        # Glassmorphism cards
│   │   ├── animated_button.py   # Animated buttons
│   │   └── loading_spinner.py   # Loading indicators
│   └── views/                   # Screen components
│       ├── welcome_screen.py    # Welcome screen
│       ├── environment_setup.py # Environment configuration
│       └── ...                  # Other screens
├── configo_core/           # Backend integration
├── assets/                 # Icons, fonts, images
└── docs/                   # Documentation
```

### Technology Stack

#### Frontend
- **PySide6**: Modern Qt for Python
- **Glassmorphism**: Blur effects and transparency
- **CSS-like Styling**: QSS for component styling
- **Animation System**: QPropertyAnimation for smooth transitions

#### Backend Integration
- **CONFIGO Core**: CLI agent integration
- **Async Processing**: QThread for background operations
- **Signal/Slot**: Qt's event system for communication

#### Modern Features
- **High DPI Support**: Retina and 4K display support
- **Dark Theme**: Modern color palette
- **Custom Fonts**: Inter font family
- **Responsive Design**: Adaptive layouts

## 🎨 UI Components

### Glass Card
```python
from ui.components.glass_card import GlassCard

card = GlassCard(
    title="Environment Setup",
    subtitle="Configure your development environment",
    theme=theme
)
```

### Animated Button
```python
from ui.components.animated_button import AnimatedButton

button = AnimatedButton(
    text="Start Setup",
    variant="primary",
    size="large",
    theme=theme
)
```

### Loading Spinner
```python
from ui.components.loading_spinner import LoadingSpinner

spinner = LoadingSpinner(
    text="Installing packages...",
    size=40,
    theme=theme
)
spinner.start()
```

## 🎭 Animation System

### Theme Integration
```python
from ui.themes.glass_theme import GlassTheme
from ui.themes.animations import AnimationManager

theme = GlassTheme()
animations = AnimationManager()

# Create fade animation
fade_anim = animations.create_fade_animation(
    widget, start_opacity=0.0, end_opacity=1.0, duration=300
)
```

### Hover Effects
```python
# Apply hover effect to button
hover_effects = animations.create_hover_effect(
    button, scale_factor=1.02, glow_color=theme.colors['primary']
)
```

## 🎨 Styling System

### Modern Styles
```python
from ui.themes.modern_styles import ModernStyles

styles = ModernStyles(theme)

# Apply glass card style
card.setStyleSheet(styles.get_glass_card_style())

# Apply modern button style
button.setStyleSheet(styles.get_modern_button_style("primary", "large"))
```

### Color Palette
```python
# Primary colors
primary = QColor(99, 102, 241)      # Indigo
secondary = QColor(168, 85, 247)    # Purple
accent = QColor(34, 197, 94)        # Green

# Neutral colors
background = QColor(15, 23, 42)     # Slate 900
surface = QColor(30, 41, 59)        # Slate 800
text_primary = QColor(248, 250, 252) # Slate 50
```

## 🔧 Development Guide

### Adding New Screens

1. **Create screen component**
```python
class MyScreen(QWidget):
    def __init__(self, theme=None):
        super().__init__()
        self.theme = theme
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Add your UI components
```

2. **Register in main window**
```python
# In modern_main_window.py
self.screens["my_screen"] = MyScreen(self.theme)
self.stacked_widget.addWidget(self.screens["my_screen"])
```

3. **Add navigation button**
```python
# In setup_sidebar method
button = AnimatedButton("🔧 My Screen", variant="ghost", theme=self.theme)
button.clicked.connect(lambda: self.navigate_to_screen("my_screen"))
```

### Creating Custom Components

1. **Extend base component**
```python
class MyCustomCard(GlassCard):
    def __init__(self, theme=None):
        super().__init__(title="My Card", theme=theme)
        self.setup_custom_content()
    
    def setup_custom_content(self):
        # Add custom content
        pass
```

2. **Add animations**
```python
def setup_animations(self):
    super().setup_animations()
    
    # Add custom animation
    self.custom_animation = QPropertyAnimation(self, b"geometry")
    self.custom_animation.setDuration(300)
```

### Styling Guidelines

1. **Use theme colors**
```python
# Good
color = self.theme.colors['primary']

# Avoid hardcoded colors
color = QColor(255, 0, 0)  # Don't do this
```

2. **Apply glass effects**
```python
# Apply glassmorphism
self.theme.apply_glass_effect_to_widget(widget)

# Add shadow
self.modern_styles.apply_shadow_effect(widget)
```

3. **Use modern typography**
```python
# Use theme fonts
label.setFont(self.theme.fonts['heading_medium'])
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=configo_gui

# Run specific test
pytest test_modern_main_window.py
```

### UI Testing
```python
# Test component creation
def test_glass_card():
    card = GlassCard(title="Test", theme=theme)
    assert card.title == "Test"
    assert card.isVisible()

# Test animations
def test_button_hover():
    button = AnimatedButton("Test", theme=theme)
    # Simulate hover
    button.enterEvent(None)
    assert button.is_hovered
```

## 📦 Packaging

### Creating Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main.py
```

### Creating Installer
```bash
# For Windows
pip install fbs
fbs freeze
fbs installer
```

## 🐛 Troubleshooting

### Common Issues

1. **Glass effect not working**
   - Ensure PySide6 version 6.6.0+
   - Check if graphics effects are supported
   - Verify transparency is enabled

2. **Animations not smooth**
   - Check if hardware acceleration is enabled
   - Reduce animation duration for better performance
   - Use simpler easing curves

3. **Fonts not loading**
   - Verify Inter font is installed
   - Check font file paths
   - Use fallback fonts

### Performance Optimization

1. **Reduce animation complexity**
```python
# Use simpler animations for better performance
animation.setDuration(200)  # Shorter duration
animation.setEasingCurve(QEasingCurve.Type.OutCubic)  # Simpler curve
```

2. **Optimize glass effects**
```python
# Reduce blur radius for better performance
self.theme.effects['glass_blur'] = 10  # Lower value
```

3. **Use efficient layouts**
```python
# Use QGridLayout for complex layouts
# Avoid nested QVBoxLayout/QHBoxLayout
```

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**
```bash
git checkout -b feature/modern-ui-component
```

3. **Make changes**
4. **Add tests**
5. **Submit pull request**

### Code Style

- Follow PEP 8 for Python code
- Use type hints
- Add docstrings for all functions
- Keep components modular and reusable

### UI/UX Guidelines

- Maintain glassmorphism design language
- Use consistent spacing and typography
- Ensure accessibility (keyboard navigation, screen readers)
- Test on different screen sizes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CONFIGO Team**: Original CONFIGO CLI development
- **Qt/PySide6**: Modern GUI framework
- **Inter Font**: Beautiful typography
- **Glassmorphism Design**: Modern UI inspiration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/configo-gui/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/configo-gui/discussions)
- **Documentation**: [Wiki](https://github.com/your-username/configo-gui/wiki)

---

**Made with ❤️ by the CONFIGO Team**

*Empowering developers with intelligent automation* 