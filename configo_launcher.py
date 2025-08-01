#!/usr/bin/env python3
"""
CONFIGO Launcher - Main Entry Point
====================================

This is the main entry point for CONFIGO, the Autonomous AI Setup Agent.
It handles command-line arguments, initializes the agent, and orchestrates
the different modes of operation.

Author: Kishore Kumar S
"""

import sys
import os
import argparse
import logging
from typing import Optional, List

# Add the configo package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'configo'))

from configo import ConfigoAgent
from configo.ui.banner import display_full_banner, display_quick_banner
from configo.utils import Logger
from configo.errors import ConfigoError, handle_error

def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        verbose: Whether to enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('configo.log'),
            logging.StreamHandler()
        ]
    )

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="CONFIGO - Autonomous AI Setup Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  configo setup                    # Set up development environment
  configo install discord          # Install Discord application
  configo chat                     # Enter interactive chat mode
  configo scan                     # Scan current project
  configo portal                   # Manage login portals
        """
    )
    
    # Main command
    parser.add_argument(
        'command',
        nargs='?',
        default='setup',
        choices=['setup', 'install', 'chat', 'scan', 'portal', 'status', 'help', 'version'],
        help='Command to execute'
    )
    
    # Command-specific arguments
    parser.add_argument(
        'args',
        nargs='*',
        help='Additional arguments for the command'
    )
    
    # Global options
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--simple-banner',
        action='store_true',
        help='Use simple banner instead of ASCII art'
    )
    
    parser.add_argument(
        '--api-key',
        help='LLM API key (overrides environment variable)'
    )
    
    parser.add_argument(
        '--project-path',
        help='Path to project directory for analysis'
    )
    
    parser.add_argument(
        '--domain',
        choices=['ai_ml', 'web_dev', 'data_science', 'devops'],
        help='Domain hint for tool recommendations'
    )
    
    return parser.parse_args()

def main() -> int:
    """
    Main entry point for CONFIGO.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Set up logging
        setup_logging(args.verbose)
        logger = Logger(__name__)
        
        # Display banner
        if args.simple_banner:
            display_quick_banner()
        else:
            display_full_banner()
        
        # Initialize agent
        logger.info("Initializing CONFIGO agent")
        agent = ConfigoAgent(api_key=args.api_key)
        
        # Execute command
        if args.command == 'setup':
            return _handle_setup(agent, args)
        elif args.command == 'install':
            return _handle_install(agent, args)
        elif args.command == 'chat':
            return _handle_chat(agent, args)
        elif args.command == 'scan':
            return _handle_scan(agent, args)
        elif args.command == 'portal':
            return _handle_portal(agent, args)
        elif args.command == 'status':
            return _handle_status(agent, args)
        elif args.command == 'help':
            return _handle_help(args)
        elif args.command == 'version':
            return _handle_version(args)
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 130
    except Exception as e:
        error_info = handle_error(e)
        print(f"\n❌ Error: {error_info['message']}")
        if args.verbose:
            print(f"Details: {error_info}")
        return 1

def _handle_setup(agent: ConfigoAgent, args: argparse.Namespace) -> int:
    """Handle setup command."""
    try:
        print("🚀 Setting up development environment...")
        
        result = agent.setup_environment(
            project_path=args.project_path,
            domain_hint=args.domain
        )
        
        if result['success']:
            print("✅ Environment setup completed successfully!")
            
            # Display results
            env_info = result.get('environment', {})
            print(f"📊 Environment: {env_info.get('os_name', 'Unknown')} {env_info.get('os_version', 'Unknown')}")
            
            installation_results = result.get('installation_results', {})
            successful = installation_results.get('successful', [])
            failed = installation_results.get('failed', [])
            
            if successful:
                print(f"✅ Successfully installed: {', '.join(successful)}")
            
            if failed:
                print(f"❌ Failed to install: {len(failed)} tools")
                for failure in failed:
                    print(f"   - {failure.get('name', 'Unknown')}: {failure.get('error', 'Unknown error')}")
            
            return 0
        else:
            print("❌ Environment setup failed!")
            return 1
            
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        return 1

def _handle_install(agent: ConfigoAgent, args: argparse.Namespace) -> int:
    """Handle install command."""
    try:
        if not args.args:
            print("❌ Please specify an application to install.")
            print("Example: configo install discord")
            return 1
        
        app_name = args.args[0]
        print(f"📦 Installing {app_name}...")
        
        result = agent.install_app(app_name)
        
        if result['success']:
            print(f"✅ {app_name} installed successfully!")
            return 0
        else:
            print(f"❌ Failed to install {app_name}: {result.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"❌ Installation failed: {str(e)}")
        return 1

def _handle_chat(agent: ConfigoAgent, args: argparse.Namespace) -> int:
    """Handle chat command."""
    try:
        print("💬 Entering chat mode...")
        print("Type 'exit' to quit, 'help' for assistance.")
        print()
        
        agent.chat_mode()
        return 0
        
    except Exception as e:
        print(f"❌ Chat mode failed: {str(e)}")
        return 1

def _handle_scan(agent: ConfigoAgent, args: argparse.Namespace) -> int:
    """Handle scan command."""
    try:
        project_path = args.project_path or '.'
        print(f"🔍 Scanning project at: {project_path}")
        
        # This would use the environment detector to analyze the project
        # For now, we'll just show a placeholder
        print("📁 Project analysis completed")
        print("   - Project type: Unknown")
        print("   - Languages: Unknown")
        print("   - Frameworks: Unknown")
        
        return 0
        
    except Exception as e:
        print(f"❌ Scan failed: {str(e)}")
        return 1

def _handle_portal(agent: ConfigoAgent, args: argparse.Namespace) -> int:
    """Handle portal command."""
    try:
        print("🌐 Portal management mode...")
        print("This feature is under development.")
        return 0
        
    except Exception as e:
        print(f"❌ Portal mode failed: {str(e)}")
        return 1

def _handle_status(agent: ConfigoAgent, args: argparse.Namespace) -> int:
    """Handle status command."""
    try:
        print("📊 CONFIGO Status")
        print("=================")
        
        # Get memory stats
        memory_stats = agent.memory.get_memory_stats()
        
        print(f"📈 Total sessions: {memory_stats.get('total_sessions', 0)}")
        print(f"📦 Total installations: {memory_stats.get('total_installations', 0)}")
        print(f"✅ Successful installations: {memory_stats.get('successful_installations', 0)}")
        print(f"📊 Success rate: {memory_stats.get('success_rate', 0)*100:.1f}%")
        print(f"🧠 Memory system: {'Available' if memory_stats.get('mem0_available') else 'Local only'}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Status check failed: {str(e)}")
        return 1

def _handle_help(args: argparse.Namespace) -> int:
    """Handle help command."""
    print("""
CONFIGO - Autonomous AI Setup Agent
===================================

Commands:
  setup              Set up development environment
  install <app>      Install specific application
  chat               Enter interactive chat mode
  scan               Scan current project
  portal             Manage login portals
  status             Show system status
  help               Show this help
  version            Show version information

Options:
  --verbose          Enable verbose logging
  --simple-banner    Use simple banner
  --api-key KEY      LLM API key
  --project-path PATH Project directory path
  --domain DOMAIN    Domain hint (ai_ml, web_dev, data_science, devops)

Examples:
  configo setup
  configo install discord
  configo chat
  configo scan --project-path ./my-project
    """)
    return 0

def _handle_version(args: argparse.Namespace) -> int:
    """Handle version command."""
    from configo import __version__, __author__
    
    print(f"CONFIGO Version {__version__}")
    print(f"Author: {__author__}")
    print("Autonomous AI Setup Agent")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 