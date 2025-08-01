"""
CONFIGO GUI - Setup Configuration
=================================

Setup configuration for the CONFIGO GUI desktop application.
Provides packaging and distribution options.

Author: CONFIGO Team
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements_file = this_directory / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="configo-gui",
    version="1.0.0",
    author="CONFIGO Team",
    author_email="team@configo.dev",
    description="CONFIGO GUI - Intelligent Development Environment Setup Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/configo/configo-gui",
    project_urls={
        "Bug Tracker": "https://github.com/configo/configo-gui/issues",
        "Documentation": "https://configo.dev/docs",
        "Source Code": "https://github.com/configo/configo-gui",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Systems Administration",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "packaging": [
            "PyInstaller>=5.0.0",
            "fbs>=0.9.0",
        ],
        "enhanced": [
            "pyside6-lottie>=1.0.0",
            "chromadb>=0.4.0",
            "sentence-transformers>=2.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "configo-gui=configo_gui.main:main",
        ],
        "gui_scripts": [
            "configo-gui=configo_gui.main:main",
        ],
    },
    keywords=[
        "development",
        "environment",
        "setup",
        "automation",
        "ai",
        "gui",
        "desktop",
        "tools",
        "installation",
    ],
    package_data={
        "configo_gui": [
            "assets/*",
            "ui/*.ui",
            "templates/*",
        ],
    },
    data_files=[
        ("share/applications", ["configo-gui.desktop"]),
        ("share/icons/hicolor/256x256/apps", ["assets/icon.png"]),
        ("share/configo-gui", ["configo_gui/assets/"]),
    ],
    zip_safe=False,
) 