#!/usr/bin/env python3
"""
Test script to verify imports work correctly.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("Testing imports...")

try:
    from ui.themes.glass_theme import GlassTheme
    print("✅ GlassTheme imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import GlassTheme: {e}")

try:
    from ui.themes.animations import AnimationManager
    print("✅ AnimationManager imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import AnimationManager: {e}")

try:
    from ui.themes.modern_styles import ModernStyles
    print("✅ ModernStyles imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import ModernStyles: {e}")

try:
    from ui.components.glass_card import GlassCard
    print("✅ GlassCard imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import GlassCard: {e}")

try:
    from ui.components.animated_button import AnimatedButton
    print("✅ AnimatedButton imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import AnimatedButton: {e}")

try:
    from ui.modern_main_window import ModernMainWindow
    print("✅ ModernMainWindow imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import ModernMainWindow: {e}")

print("Import test completed!") 