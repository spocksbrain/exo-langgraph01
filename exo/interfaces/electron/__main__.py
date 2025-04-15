"""
Entry point for the exo Electron app.

This module allows running the Electron app as a module:
python -m exo.interfaces.electron
"""
import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_electron_app():
    """Run the Electron app."""
    # Get the directory of this file
    electron_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if node_modules exists
    if not os.path.exists(os.path.join(electron_dir, "node_modules")):
        logger.info("Installing Electron dependencies...")
        subprocess.run(["npm", "install"], cwd=electron_dir, check=True)
    
    # Run the Electron app
    logger.info("Starting Electron app...")
    subprocess.run(["npm", "start"], cwd=electron_dir, check=True)


if __name__ == "__main__":
    run_electron_app()
