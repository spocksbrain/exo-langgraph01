#!/usr/bin/env python
"""
Run script for the exo multi-agent system.

This script provides a simple way to run the exo system with all interfaces.
"""
import os
import sys
import argparse
import logging

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
    
    # Check if the virtual environment is activated
    if not os.environ.get("VIRTUAL_ENV"):
        logger.warning("Virtual environment not activated. It's recommended to activate it first.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != "y":
            logger.info("Exiting. Please activate the virtual environment and try again.")
            sys.exit(0)
    
    # Run the exo system
    logger.info(f"Running exo with interface: {args.interface}")
    
    try:
        # Import the exo.__main__ module functions
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
    except ImportError:
        logger.error("Failed to import exo. Please make sure it's installed.")
        logger.info("You can install it with: pip install -e .")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error running exo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
