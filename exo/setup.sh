#!/bin/bash
# Setup script for the exo multi-agent system

# Exit on error
set -e

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install exo in development mode
echo "Installing exo in development mode..."
pip install -e .

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env with your API keys and configuration"
fi

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To run the CLI interface: python -m exo cli"
echo "To run the API server: python -m exo api"
echo "To run the web interface: python -m exo web"
echo "To run the MCP server: python -m exo mcp"
echo "To run the Electron app: python -m exo electron"
echo "To run all interfaces: python -m exo all"
