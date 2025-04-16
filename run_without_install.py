#!/usr/bin/env python
"""
Runtime helper for the exo multi-agent system without requiring installation.

This script modifies the Python path to include the current directory,
then imports and runs the exo system directly.
"""
import os
import sys
import logging
import argparse

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    # Print command line arguments for debugging
    print(f"Command line arguments: {sys.argv}")
    
    parser = argparse.ArgumentParser(description="Run the exo multi-agent system")
    parser.add_argument(
        "interface",
        nargs="?",
        choices=["cli", "api", "web", "mcp", "electron", "all"],
        default="all",
        help="Interface to run (default: all)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    
    args = parser.parse_args()
    print(f"Parsed arguments: interface={args.interface}, debug={args.debug}")
    
    # Configure logging
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check if we're in the right directory
    if not os.path.exists("exo"):
        logger.error("Please run this script from the root directory of the project")
        sys.exit(1)
    
    # Run the exo system
    logger.info(f"Running exo with interface: {args.interface}")
    
    try:
        # Import the exo.__main__ module functions
        # These imports will now work because we've added the current directory to sys.path
        from exo.__main__ import run_cli, run_api, run_web, run_mcp, run_electron, run_all
        
        # Run the selected interface
        if args.interface == "cli":
            run_cli()
        elif args.interface == "api":
            run_api()
        elif args.interface == "web":
            run_web()
        elif args.interface == "mcp":
            run_mcp()
        elif args.interface == "electron":
            run_electron()
        elif args.interface == "all":
            run_all()
        else:
            logger.error(f"Unknown interface: {args.interface}")
            sys.exit(1)
    except ImportError as e:
        logger.error(f"Failed to import exo modules: {e}")
        logger.error("This script should be run from the root directory of the project")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error running exo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
