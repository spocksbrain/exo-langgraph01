"""
Main entry point for the exo multi-agent system.

This module allows running the exo system with different interfaces:
- CLI: python -m exo cli
- API: python -m exo api
- Web: python -m exo web
- MCP: python -m exo mcp
- Electron: python -m exo electron
"""
import argparse
import logging
import os
import sys
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_cli():
    """Run the CLI interface."""
    from exo.interfaces.cli.main import main
    main()


def run_api():
    """Run the API server."""
    from exo.api.app import start_api_server
    start_api_server()


def run_web():
    """Run the web interface."""
    import subprocess
    import os
    
    # Change to the web directory
    web_dir = os.path.join(os.path.dirname(__file__), "interfaces", "web")
    
    # Check if node_modules exists
    if not os.path.exists(os.path.join(web_dir, "node_modules")):
        logger.info("Installing web dependencies...")
        subprocess.run(["npm", "install"], cwd=web_dir, check=True)
    
    # Run the web interface
    logger.info("Starting web interface...")
    subprocess.run(["npm", "run", "dev"], cwd=web_dir, check=True)


def run_mcp():
    """Run the MCP server."""
    from exo.mcp.server import start_mcp_server
    start_mcp_server()


def run_electron():
    """Run the Electron app."""
    from exo.interfaces.electron.__main__ import run_electron_app
    run_electron_app()


def run_all():
    """Run the API server, MCP server, and Electron app."""
    import threading
    import time
    
    # Start the API server in a separate thread
    api_thread = threading.Thread(target=run_api)
    api_thread.daemon = True
    api_thread.start()
    
    # Start the MCP server in a separate thread
    mcp_thread = threading.Thread(target=run_mcp)
    mcp_thread.daemon = True
    mcp_thread.start()
    
    # Wait for the servers to start
    logger.info("Waiting for servers to start...")
    time.sleep(2)
    
    # Run the Electron app
    run_electron()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="exo multi-agent system")
    parser.add_argument(
        "interface",
        choices=["cli", "api", "web", "mcp", "electron", "all"],
        help="Interface to run",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    
    args = parser.parse_args()
    
    # Configure logging
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
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


if __name__ == "__main__":
    main()
