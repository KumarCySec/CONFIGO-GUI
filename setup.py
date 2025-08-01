#!/usr/bin/env python3
"""
CONFIGO Setup Script
====================

Secure setup script for CONFIGO AI Setup Agent.
This script helps users configure the project securely.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional


class ConfigoSetup:
    """Secure setup utility for CONFIGO project."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.env_template = self.project_root / ".env.template"
        self.env_file = self.project_root / ".env"
        
    def print_banner(self):
        """Print professional setup banner."""
        print("=" * 60)
        print("🔧 CONFIGO AI Setup Agent - Secure Configuration")
        print("=" * 60)
        print("This script will help you configure CONFIGO securely.")
        print("Follow the prompts to set up your environment safely.\n")
    
    def check_existing_env(self) -> bool:
        """Check if .env file already exists."""
        if self.env_file.exists():
            print("⚠️  Found existing .env file")
            response = input("Do you want to backup and recreate it? (y/N): ").lower()
            if response == 'y':
                backup_path = self.env_file.with_suffix('.env.backup')
                shutil.copy2(self.env_file, backup_path)
                print(f"✅ Backed up to {backup_path}")
                return False
            else:
                print("ℹ️  Keeping existing .env file")
                return True
        return False
    
    def create_env_file(self) -> bool:
        """Create .env file from template."""
        if not self.env_template.exists():
            print("❌ .env.template not found!")
            return False
        
        try:
            shutil.copy2(self.env_template, self.env_file)
            print("✅ Created .env file from template")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    
    def validate_git_ignore(self) -> bool:
        """Validate that .env is properly ignored by git."""
        gitignore_path = self.project_root / ".gitignore"
        if not gitignore_path.exists():
            print("❌ .gitignore not found!")
            return False
        
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        if '.env' in content and '!.env.template' in content:
            print("✅ .env properly ignored by git")
            return True
        else:
            print("⚠️  .env may not be properly ignored by git")
            return False
    
    def check_api_keys(self) -> dict:
        """Check for API keys in the environment."""
        keys = {
            'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
            'MEM0_API_KEY': os.getenv('MEM0_API_KEY'),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY')
        }
        
        print("\n🔑 API Key Status:")
        for key, value in keys.items():
            if value and value != "your_gemini_api_key_here":
                print(f"  ✅ {key}: Found (masked)")
            else:
                print(f"  ❌ {key}: Not set")
        
        return keys
    
    def provide_setup_instructions(self):
        """Provide setup instructions to user."""
        print("\n📋 Setup Instructions:")
        print("1. Edit your .env file with your actual API keys:")
        print(f"   nano {self.env_file}")
        print("\n2. Get your API keys:")
        print("   - Gemini API: https://makersuite.google.com/app/apikey")
        print("   - Mem0 API: https://mem0.ai")
        print("\n3. Verify setup:")
        print("   python -c \"from core.ai import ConfigoAI; print('✅ Setup complete')\"")
    
    def security_reminders(self):
        """Display security reminders."""
        print("\n🔒 Security Reminders:")
        print("✅ .env file is ignored by git")
        print("✅ Never commit API keys to version control")
        print("✅ Rotate API keys regularly")
        print("✅ Use different keys for development and production")
        print("✅ Keep your .env file secure and private")
    
    def run(self):
        """Run the complete setup process."""
        self.print_banner()
        
        # Check git ignore
        if not self.validate_git_ignore():
            print("❌ Security issue: .env not properly ignored")
            return False
        
        # Check existing .env
        if self.check_existing_env():
            print("ℹ️  Using existing .env file")
        else:
            # Create new .env file
            if not self.create_env_file():
                return False
        
        # Check API keys
        self.check_api_keys()
        
        # Provide instructions
        self.provide_setup_instructions()
        
        # Security reminders
        self.security_reminders()
        
        print("\n🎉 Setup complete! Follow the instructions above to configure your API keys.")
        return True


def main():
    """Main setup function."""
    try:
        setup = ConfigoSetup()
        success = setup.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 