# CONFIGO GUI - Modern Desktop Application

A beautiful, modern desktop application for intelligent development environment setup. Built with PySide6 and featuring glassmorphism effects, smooth animations, and seamless integration with the CONFIGO CLI backend.

![CONFIGO GUI](https://img.shields.io/badge/Version-1.0.0-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.5.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🧠 What is CONFIGO GUI?

CONFIGO GUI is a modern, cross-platform desktop application that provides an intelligent interface for setting up development environments. It combines the power of Google's Gemini LLM with a beautiful, glassmorphic UI to deliver a premium development experience.

### Key Features

- **🎨 Modern Glassmorphism Design**: Beautiful glass-like effects with blur and transparency
- **🧠 AI-Powered Intelligence**: Uses Google Gemini for intelligent tool recommendations
- **💾 Persistent Memory**: Remembers your preferences and installation history
- **🔧 Self-Healing**: Automatically fixes installation failures using AI
- **🎯 Domain-Aware**: Understands different development domains (AI/ML, Web, DevOps, etc.)
- **📱 Natural Language Input**: Describe your environment needs in plain English
- **🌐 Portal Orchestration**: Automated login portal management
- **✅ Post-Installation Validation**: Ensures everything works correctly

## 🪟 Features of the Desktop App

### 🎨 Modern UI Components

- **Glassmorphism Cards**: Beautiful glass-like cards with blur effects
- **Smooth Animations**: Framer Motion-like transitions and hover effects
- **Dark Theme**: Modern dark theme optimized for developers
- **Responsive Layout**: Adapts to different screen sizes
- **Toast Notifications**: Elegant notification system

### 🧩 Smart Navigation

- **Sidebar Navigation**: Clean sidebar with glassmorphism effects
- **View Transitions**: Smooth transitions between different views
- **Progress Tracking**: Real-time progress with animated progress bars
- **Status Indicators**: Clear success/error status for each operation

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

## 🎨 Tech Stack

### Frontend
- **PySide6**: Modern Qt for Python framework
- **qdarktheme**: Beautiful dark theme support
- **QGraphicsBlurEffect**: Glassmorphism blur effects
- **QPropertyAnimation**: Smooth animations and transitions
- **Custom CSS**: Modern styling with gradients and shadows

### Backend Integration
- **CLI Submodule**: External CLI repo as git submodule
- **InstallEngine**: Wrapper that interfaces with CLI logic
- **Async Threading**: Background processing for installations
- **Memory System**: Persistent storage with JSON

### Development Tools
- **pytest**: Comprehensive testing framework
- **black**: Code formatting
- **flake8**: Code linting
- **PyInstaller**: Executable packaging

## 🧩 Integration with CLI

CONFIGO GUI integrates seamlessly with the CONFIGO CLI backend through a clean submodule architecture:

```
GUI Application
├── gui/                    # All GUI app logic
│   ├── main.py            # GUI launcher
│   ├── views/             # All screens/pages
│   ├── components/        # Reusable UI components
│   ├── themes/            # Dark mode, glass styles
│   ├── animations/        # Loading effects
│   └── backend/           # Wrappers that interface with CLI
│       └── install_engine.py
├── cli_submodule/         # External CLI repo as git submodule
│   └── (CLI logic)
└── configo_gui_launcher.py
```

### Backend Interface

The `InstallEngine` class provides a clean interface to the CLI:

- **Plan Generation**: Uses CLI's LLM agent for intelligent planning
- **Installation Execution**: Leverages CLI's shell executor and validator
- **Memory Management**: Integrates with CLI's persistent memory system
- **System Detection**: Uses CLI's system inspector and tool detector

## 🔧 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git (for submodule management)
- CONFIGO CLI submodule

### Quick Start

1. **Clone the repository with submodules**
   ```bash
   git clone --recursive https://github.com/KumarCySec/Configo.git
   cd Configo
   ```

2. **Run the secure setup script**
   ```bash
   python setup.py
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r gui/requirements.txt
   ```

5. **Configure your API keys** (follow the setup script instructions)

6. **Run the application**
   ```bash
   python configo_gui_launcher.py
   ```

### Development Setup

For development and testing:

```bash
# Install with development dependencies
pip install -r gui/requirements.txt

# Run tests
pytest gui/tests/

# Format code
black gui/

# Lint code
flake8 gui/
```

### Environment Variables

🔐 **SECURITY SETUP**: CONFIGO requires API keys for AI features. Follow these steps to set up securely:

1. **Copy the template file**:
   ```bash
   cp .env.template .env
   ```

2. **Add your API keys** to the `.env` file:
   ```env
   # Required: Google Gemini API key
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   
   # Optional: Mem0 API key for enhanced memory
   MEM0_API_KEY=your_actual_mem0_api_key_here
   
   # Optional: Logging level
   LOG_LEVEL=INFO
   ```

3. **Get your API keys**:
   - **Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **Mem0 API**: [Mem0.ai](https://mem0.ai)

⚠️ **IMPORTANT SECURITY NOTES**:
- Never commit your `.env` file to version control
- Keep your API keys secure and private
- Rotate API keys regularly
- Use different keys for development and production

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gui

# Run specific test file
pytest gui/tests/test_main_window.py

# Run with verbose output
pytest -v
```

### Test Structure

```
gui/tests/
├── test_main_window.py     # Main window tests
├── test_welcome_view.py    # Welcome view tests
├── test_env_selector.py    # Environment selector tests
├── test_install_plan.py    # Install plan tests
├── test_sidebar.py         # Sidebar component tests
├── test_toast.py           # Toast notification tests
└── test_install_engine.py  # Backend integration tests
```

### Test Environments

Use test environments to simulate install flows:

```bash
# Create test environment
python -m venv test_env

# Run tests in isolated environment
pytest --test-env=test_env
```

## 📦 Packaging

### Creating Executables

Using PyInstaller:

```bash
# Install PyInstaller
pip install PyInstaller

# Create executable
pyinstaller --onefile --windowed configo_gui_launcher.py

# Create with icon
pyinstaller --onefile --windowed --icon=gui/assets/icon.ico configo_gui_launcher.py
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

## 🎁 Screenshots

### Welcome Screen
![Welcome Screen](gui/assets/screenshots/welcome.png)

### Environment Selector
![Environment Selector](gui/assets/screenshots/environment.png)

### Installation Progress
![Installation Progress](gui/assets/screenshots/install.png)

## 🔒 Security

### API Key Management

CONFIGO uses API keys for AI features. Here are the security best practices:

#### ✅ Secure Practices
- **Environment Variables**: Always use `.env` files for API keys
- **Template Files**: Use `.env.template` for safe configuration examples
- **Git Ignore**: `.env` files are automatically ignored by git
- **Key Rotation**: Rotate API keys regularly
- **Environment Separation**: Use different keys for dev/staging/production

#### ❌ Security Risks to Avoid
- **Never commit API keys** to version control
- **Don't share API keys** in code or documentation
- **Avoid hardcoding keys** in source code
- **Don't use the same key** across multiple projects

#### 🔐 Advanced Security
For production deployments, consider:
- **AWS Secrets Manager** or **Google Secret Manager**
- **HashiCorp Vault** for enterprise environments
- **Docker secrets** for containerized deployments
- **Kubernetes secrets** for orchestrated environments

### Reporting Security Issues

If you discover a security vulnerability, please:
1. **Do not create a public issue**
2. **Email directly**: security@configo.dev
3. **Include details** about the vulnerability
4. **Allow time** for assessment and fix

We take security seriously and will respond promptly to all reports.

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

## 🙌 Credits

**Kishore Kumar S** (ECE 2027, GCE Erode)

- **Original CONFIGO CLI**: The intelligent backend that powers this GUI
- **PySide6**: For the excellent Qt framework
- **qdarktheme**: For the beautiful dark theme
- **Python Community**: For the amazing ecosystem

## 📞 Support

- **Documentation**: [https://configo.dev/docs](https://configo.dev/docs)
- **Issues**: [GitHub Issues](https://github.com/KumarCySec/Configo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/KumarCySec/Configo/discussions)
- **Email**: kishore.kumar@configo.dev

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Complete GUI implementation with glassmorphism effects
- Integration with CONFIGO CLI backend
- Cross-platform support
- Modern dark theme
- Real-time progress tracking
- Toast notification system
- Memory management
- Error handling

---

**Made with ❤️ by Kishore Kumar S**

_Built with 💡 by the CONFIGO Team_ 