# Contributing to CONFIGO

Thank you for your interest in contributing to CONFIGO! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Before You Start

1. **Read the documentation**:
   - [README.md](README.md) - Project overview and setup
   - [SECURITY.md](SECURITY.md) - Security guidelines
   - [FEATURES.md](FEATURES.md) - Feature documentation

2. **Set up your development environment**:
   ```bash
   git clone --recursive https://github.com/KumarCySec/Configo.git
   cd Configo
   python setup.py  # Secure setup
   python -m venv venv
   source venv/bin/activate
   pip install -r gui/requirements.txt
   ```

3. **Understand the project structure**:
   ```
   CONFIGO/
   ├── gui/                    # GUI application
   ├── cli_submodule/         # CLI backend (submodule)
   ├── core/                  # Core AI logic
   ├── ui/                    # Terminal UI components
   └── scripts/               # Utility scripts
   ```

## 🔒 Security Guidelines

### API Key Management

**NEVER commit API keys or sensitive data:**

- ✅ Use `.env` files for local development
- ✅ Use environment variables in CI/CD
- ✅ Use secrets managers in production
- ❌ Never hardcode API keys in source code
- ❌ Never commit `.env` files
- ❌ Never share API keys in issues or PRs

### Code Security

- **Input validation**: Always validate user inputs
- **Path sanitization**: Sanitize file paths before operations
- **Error handling**: Don't expose sensitive data in error messages
- **Dependency updates**: Keep dependencies updated for security patches

## 🚀 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Follow the coding standards:
- **Python**: Follow PEP 8 guidelines
- **Type hints**: Use type hints for function parameters and return values
- **Docstrings**: Add docstrings to all functions and classes
- **Tests**: Write tests for new functionality

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run specific test file
pytest gui/tests/test_your_feature.py

# Run with coverage
pytest --cov=gui

# Format code
black gui/

# Lint code
flake8 gui/
```

### 4. Commit Your Changes

Use conventional commit messages:

```bash
git commit -m "feat: add new AI-powered feature"
git commit -m "fix: resolve installation timeout issue"
git commit -m "docs: update security documentation"
git commit -m "test: add tests for new feature"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] **Tests pass**: All tests should pass
- [ ] **Code formatted**: Code is formatted with `black`
- [ ] **Linting passes**: No linting errors with `flake8`
- [ ] **Documentation updated**: Update relevant documentation
- [ ] **Security reviewed**: No security vulnerabilities introduced
- [ ] **API keys secure**: No API keys or sensitive data in code

### PR Description Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Security improvement
- [ ] Performance optimization

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Security
- [ ] No API keys or sensitive data exposed
- [ ] Input validation implemented
- [ ] Error handling doesn't expose sensitive data

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## 🧪 Testing Guidelines

### Writing Tests

```python
def test_new_feature():
    """Test the new feature functionality."""
    # Arrange
    expected = "expected_result"
    
    # Act
    result = new_feature()
    
    # Assert
    assert result == expected
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

### Test Best Practices

- **Isolation**: Each test should be independent
- **Mocking**: Mock external dependencies
- **Coverage**: Aim for >80% test coverage
- **Descriptive names**: Use descriptive test names
- **Edge cases**: Test both success and failure scenarios

## 🔧 Code Style

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines:

```python
# ✅ Good
def calculate_total(items: List[float]) -> float:
    """Calculate the total of all items."""
    return sum(items)

# ❌ Bad
def calc_total(items):
    return sum(items)
```

### File Organization

```python
# Standard imports
import os
import sys
from typing import List, Dict, Optional

# Third-party imports
import requests
from rich.console import Console

# Local imports
from core.ai import ConfigoAI
from ui.messages import MessageHandler
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `ConfigoAI`)
- **Functions**: `snake_case` (e.g., `setup_environment`)
- **Variables**: `snake_case` (e.g., `api_key`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)

## 🐛 Bug Reports

### Before Reporting

1. **Check existing issues**: Search for similar issues
2. **Reproduce the bug**: Ensure you can reproduce it consistently
3. **Check documentation**: Verify it's not a configuration issue

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- CONFIGO Version: [e.g., 1.0.0]

## Additional Information
Screenshots, logs, or other relevant information.
```

## 💡 Feature Requests

### Before Requesting

1. **Check existing features**: Ensure the feature doesn't already exist
2. **Search issues**: Check if it's already been requested
3. **Consider impact**: Think about the broader impact

### Feature Request Template

```markdown
## Feature Description
Clear description of the requested feature.

## Use Case
Why this feature would be useful.

## Proposed Implementation
How you think it could be implemented (optional).

## Alternatives Considered
Other approaches you considered (optional).
```

## 🔒 Security Issues

**DO NOT create public issues for security vulnerabilities.**

Instead:
1. **Email directly**: security@configo.dev
2. **Include details**: Description, steps to reproduce, impact
3. **Allow time**: For assessment and response

## 📞 Getting Help

- **Documentation**: Check the README and other docs
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions
- **Email**: kishore.kumar@configo.dev

## 🙏 Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor hall of fame

---

**Thank you for contributing to CONFIGO!** 🚀 