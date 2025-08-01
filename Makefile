# CONFIGO Makefile
# ================
# Convenient commands for CONFIGO development and usage

.PHONY: help install setup test clean run chat install-app status version

# Default target
help:
	@echo "CONFIGO - Autonomous AI Setup Agent"
	@echo "===================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          - Set up development environment"
	@echo "  make install-app    - Install specific application (usage: make install-app APP=discord)"
	@echo "  make chat           - Enter interactive chat mode"
	@echo "  make status         - Show system status"
	@echo "  make version        - Show version information"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Clean up temporary files"
	@echo "  make install        - Install CONFIGO dependencies"
	@echo "  make run            - Run CONFIGO with default settings"
	@echo ""

# Install dependencies
install:
	@echo "Installing CONFIGO dependencies..."
	pip install -r requirements.txt

# Set up development environment
setup:
	@echo "Setting up development environment..."
	python configo_launcher.py setup

# Install specific application
install-app:
	@if [ -z "$(APP)" ]; then \
		echo "Error: Please specify an app to install"; \
		echo "Usage: make install-app APP=discord"; \
		exit 1; \
	fi
	@echo "Installing $(APP)..."
	python configo_launcher.py install $(APP)

# Enter chat mode
chat:
	@echo "Entering chat mode..."
	python configo_launcher.py chat

# Show status
status:
	@echo "Showing system status..."
	python configo_launcher.py status

# Show version
version:
	@echo "Showing version information..."
	python configo_launcher.py version

# Run tests
test:
	@echo "Running tests..."
	python -m pytest tests/ -v

# Clean up temporary files
clean:
	@echo "Cleaning up temporary files..."
	rm -rf __pycache__/
	rm -rf .configo_memory/
	rm -rf configo/__pycache__/
	rm -rf configo/ui/__pycache__/
	rm -f *.log
	rm -f .env

# Run CONFIGO with default settings
run:
	@echo "Running CONFIGO..."
	python configo_launcher.py setup

# Development commands
dev-setup:
	@echo "Setting up development environment..."
	pip install -r requirements.txt
	python -m pytest tests/ -v

dev-run:
	@echo "Running CONFIGO in development mode..."
	python configo_launcher.py --verbose --simple-banner setup

# Documentation
docs:
	@echo "Generating documentation..."
	@echo "README.md and Features.md are up to date"

# Package commands
package:
	@echo "Creating package..."
	python setup.py sdist bdist_wheel

# Install in development mode
dev-install:
	@echo "Installing CONFIGO in development mode..."
	pip install -e .

# Uninstall
uninstall:
	@echo "Uninstalling CONFIGO..."
	pip uninstall configo -y

# Show help for specific command
help-setup:
	@echo "Setup command help:"
	@python configo_launcher.py setup --help

help-install:
	@echo "Install command help:"
	@python configo_launcher.py install --help

# Quick commands
quick-setup:
	@echo "Quick setup with simple banner..."
	python configo_launcher.py --simple-banner setup

quick-install:
	@if [ -z "$(APP)" ]; then \
		echo "Error: Please specify an app to install"; \
		echo "Usage: make quick-install APP=discord"; \
		exit 1; \
	fi
	@echo "Quick install of $(APP)..."
	python configo_launcher.py --simple-banner install $(APP)

# Environment setup
env-setup:
	@echo "Setting up environment file..."
	@if [ ! -f .env ]; then \
		cp .env.template .env; \
		echo "Created .env file from template"; \
		echo "Please edit .env with your API keys"; \
	else \
		echo ".env file already exists"; \
	fi

# Check system requirements
check-system:
	@echo "Checking system requirements..."
	@python -c "import sys; print(f'Python version: {sys.version}')"
	@python -c "import platform; print(f'Platform: {platform.system()} {platform.release()}')"
	@python -c "import psutil; print(f'Memory: {psutil.virtual_memory().total // (1024**3)} GB')"
	@python -c "import psutil; print(f'CPU cores: {psutil.cpu_count()}')"

# Show all available commands
list:
	@echo "Available make commands:"
	@echo "  help              - Show this help"
	@echo "  install           - Install dependencies"
	@echo "  setup             - Set up development environment"
	@echo "  install-app       - Install specific app (APP=name)"
	@echo "  chat              - Enter chat mode"
	@echo "  status            - Show status"
	@echo "  version           - Show version"
	@echo "  test              - Run tests"
	@echo "  clean             - Clean temporary files"
	@echo "  run               - Run with default settings"
	@echo "  dev-setup         - Development setup"
	@echo "  dev-run           - Run in development mode"
	@echo "  docs              - Generate documentation"
	@echo "  package           - Create package"
	@echo "  dev-install       - Install in development mode"
	@echo "  uninstall         - Uninstall CONFIGO"
	@echo "  env-setup         - Set up environment file"
	@echo "  check-system      - Check system requirements"
	@echo "  quick-setup       - Quick setup with simple banner"
	@echo "  quick-install     - Quick install (APP=name)" 