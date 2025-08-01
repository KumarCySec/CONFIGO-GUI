# CONFIGO GUI - Intelligent Development Environment Setup Agent

A modern, cross-platform desktop application that provides an intelligent GUI for CONFIGO, the Autonomous AI Setup Agent. Built with PySide6 (Qt for Python), CONFIGO GUI offers a beautiful, developer-friendly interface for setting up development environments.

## 🚀 Features

### 🎨 Modern GUI Interface
- **Dark Theme**: Beautiful dark mode interface designed for developers
- **Responsive Design**: Adapts to different screen sizes and resolutions
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Intuitive Navigation**: Easy-to-use sidebar navigation

### 🧠 AI-Powered Environment Setup
- **Natural Language Input**: Describe your environment needs in plain English
- **Smart Suggestions**: AI-powered tool recommendations based on your input
- **Template Library**: Quick setup templates for common development stacks
- **Intelligent Planning**: Automatic generation of installation plans

### 📋 Visual Plan Management
- **Tool Cards**: Visual representation of tools to be installed
- **Progress Tracking**: Real-time progress updates for each installation step
- **Status Indicators**: Clear success/error status for each tool
- **Dependency Management**: Automatic handling of tool dependencies

### 🖥️ Real-Time Monitoring
- **Live Console**: Real-time log output with syntax highlighting
- **Progress Bars**: Visual progress tracking for installations
- **Error Handling**: Comprehensive error reporting and recovery suggestions
- **Status Updates**: Live updates on installation progress

### 🌐 Portal Integration
- **Development Portals**: Quick access to common development services
- **Browser Integration**: Automatic opening of login portals
- **Portal Management**: Add, remove, and manage custom portals
- **Status Tracking**: Track portal completion status

### 💾 Memory & History
- **Session History**: Track all previous environment setups
- **User Preferences**: Store and manage user preferences
- **Tool Statistics**: Track installation success rates and usage
- **Memory Export**: Export memory data for backup or analysis

### ⚡ Advanced Features
- **Async Operations**: Non-blocking installation processes
- **Error Recovery**: Intelligent error handling and retry mechanisms
- **System Integration**: Deep integration with existing CONFIGO backend
- **Plugin Support**: Extensible architecture for future enhancements

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- CONFIGO backend (optional, for full functionality)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/configo/configo-gui.git
   cd configo-gui
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python configo_gui/main.py
   ```

### Development Installation

For development and testing:

```bash
# Install with development dependencies
pip install -e .[dev]

# Run tests
pytest

# Format code
black configo_gui/

# Lint code
flake8 configo_gui/
```

### Package Installation

```bash
# Install from PyPI (when available)
pip install configo-gui

# Or install from source
pip install .
```

## 🎯 Usage

### Getting Started

1. **Launch the Application**
   - Run `configo-gui` from command line or double-click the executable
   - The application will start with the welcome screen

2. **Environment Setup**
   - Click "Start Setup" to begin
   - Describe your development environment needs
   - Choose from templates or enter custom requirements

3. **Review and Execute**
   - Review the generated installation plan
   - Click "Start Installation" to begin the setup process
   - Monitor progress in real-time

4. **Portal Management**
   - Access development portals from the Portals tab
   - Open login pages for services like GitHub, ChatGPT, etc.
   - Track portal completion status

### Navigation

- **🏠 Welcome**: Application welcome screen
- **⚙️ Environment Setup**: Configure your development environment
- **📋 Plan**: Review and manage installation plans
- **🖥️ Console**: View real-time logs and output
- **🌐 Portals**: Manage development service portals
- **💾 Memory**: View history and preferences

### Advanced Features

#### Custom Portal Management
- Add custom development portals
- Configure portal URLs and descriptions
- Track portal usage and completion

#### Memory Management
- View session history
- Manage user preferences
- Export memory data
- Clear memory when needed

#### Error Handling
- View detailed error information
- Get recovery suggestions
- Retry failed installations
- Ignore non-critical errors

## 🏗️ Architecture

### Component Structure

```
configo_gui/
├── main.py                 # Application entry point
├── ui/                     # UI components
│   ├── main_window.py      # Main window
│   ├── welcome_screen.py   # Welcome screen
│   ├── environment_setup.py # Environment setup
│   ├── plan_renderer.py    # Plan visualization
│   ├── log_console.py      # Log display
│   ├── portal_integration.py # Portal management
│   ├── memory_view.py      # Memory management
│   └── error_handler.py    # Error handling
├── configo_core/           # Backend integration
│   └── gui_agent.py       # GUI agent wrapper
├── assets/                 # Application assets
├── plugins/                # Plugin system
└── requirements.txt        # Dependencies
```

### Backend Integration

CONFIGO GUI integrates with the existing CONFIGO backend through the `ConfigoGUIAgent` class, which provides:

- **Async Communication**: Non-blocking backend operations
- **Signal-Based Updates**: Real-time UI updates via Qt signals
- **Error Handling**: Comprehensive error management
- **Memory Integration**: Seamless memory management

### Threading Model

- **Main Thread**: UI rendering and user interaction
- **Worker Threads**: Installation and backend operations
- **Signal/Slot Communication**: Thread-safe UI updates

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the application directory:

```env
# API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Application Settings
LOG_LEVEL=INFO
AUTO_SAVE_MEMORY=true
MEMORY_LIMIT=100MB

# Backend Configuration
CONFIGO_BACKEND_PATH=/path/to/configo/backend
```

### Application Settings

The application stores settings in:
- **User Preferences**: Application preferences and settings
- **Session History**: Previous environment setups
- **Tool Statistics**: Installation success rates and usage data

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=configo_gui

# Run specific test file
pytest tests/test_main_window.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── test_main_window.py     # Main window tests
├── test_welcome_screen.py  # Welcome screen tests
├── test_environment_setup.py # Environment setup tests
├── test_plan_renderer.py   # Plan renderer tests
├── test_log_console.py     # Log console tests
├── test_portal_integration.py # Portal integration tests
├── test_memory_view.py     # Memory view tests
├── test_error_handler.py   # Error handler tests
└── test_gui_agent.py      # GUI agent tests
```

## 📦 Packaging

### Creating Executables

Using PyInstaller:

```bash
# Install PyInstaller
pip install PyInstaller

# Create executable
pyinstaller --onefile --windowed configo_gui/main.py

# Create with icon
pyinstaller --onefile --windowed --icon=assets/icon.ico configo_gui/main.py
```

### Creating Installers

Using fbs:

```bash
# Install fbs
pip install fbs

# Initialize fbs project
fbs startproject

# Create installer
fbs freeze
fbs installer
```

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests for new functionality**
5. **Run tests and ensure they pass**
6. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
7. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
8. **Open a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

### Testing Guidelines

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Mock external dependencies
- Test both success and error cases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CONFIGO Team**: For the original CLI backend
- **Qt/PySide6**: For the excellent GUI framework
- **Python Community**: For the amazing ecosystem
- **Open Source Contributors**: For inspiration and tools

## 📞 Support

- **Documentation**: [https://configo.dev/docs](https://configo.dev/docs)
- **Issues**: [GitHub Issues](https://github.com/configo/configo-gui/issues)
- **Discussions**: [GitHub Discussions](https://github.com/configo/configo-gui/discussions)
- **Email**: team@configo.dev

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Complete GUI implementation
- Integration with CONFIGO backend
- Cross-platform support
- Modern dark theme
- Real-time progress tracking
- Portal integration
- Memory management
- Error handling

---

**Made with ❤️ by the CONFIGO Team** 