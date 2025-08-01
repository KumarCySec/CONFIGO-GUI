"""
CONFIGO GUI - Basic Test
Simple test to verify GUI components work
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path
parent_path = Path(__file__).parent.parent
sys.path.insert(0, str(parent_path))

def test_imports():
    """Test that all GUI components can be imported"""
    try:
        from gui.main import CONFIGOGUI
        from gui.views.welcome import WelcomeView
        from gui.views.env_selector import EnvironmentSelectorView
        from gui.views.install_plan import InstallPlanView
        from gui.components.sidebar import Sidebar
        from gui.components.toast import ToastManager
        from gui.themes.dark_theme import DarkTheme
        from gui.backend.install_engine import InstallEngine
        
        print("✅ All GUI components imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
        
def test_install_engine():
    """Test the install engine"""
    try:
        from gui.backend.install_engine import InstallEngine
        
        # Test environment validation
        engine = InstallEngine()
        env_info = engine.validate_environment()
        
        print(f"✅ Install engine initialized successfully")
        print(f"   CLI available: {env_info.get('cli_available', False)}")
        print(f"   Memory available: {env_info.get('memory_available', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Install engine error: {e}")
        return False
        
def test_mock_plan():
    """Test mock plan generation"""
    try:
        from gui.backend.install_engine import InstallEngine
        
        engine = InstallEngine()
        plan = engine._generate_mock_plan("Python development environment")
        
        print(f"✅ Mock plan generated successfully")
        print(f"   Tools: {plan.get('tools', [])}")
        print(f"   Commands: {len(plan.get('commands', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mock plan error: {e}")
        return False

def main():
    """Run basic tests"""
    print("🧪 Running CONFIGO GUI Basic Tests")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Install Engine", test_install_engine),
        ("Mock Plan Generation", test_mock_plan)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
            
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GUI is ready to run.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 