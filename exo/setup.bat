@echo off
REM Setup script for the exo multi-agent system on Windows

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Ensuring pip and setuptools are up to date...
pip install --upgrade pip setuptools wheel

echo Installing dependencies...
REM Make sure we're using the correct path to requirements.txt
if exist exo\requirements.txt (
    pip install -r exo\requirements.txt
) else if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo Error: requirements.txt not found
    exit /b 1
)

echo Installing exo in development mode...
pip install -e .

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env with your API keys and configuration
)

echo Setup complete!
echo To activate the virtual environment, run: venv\Scripts\activate.bat
echo To run the CLI interface: python -m exo cli
echo To run the API server: python -m exo api
echo To run the web interface: python -m exo web
echo To run the MCP server: python -m exo mcp
echo To run the Electron app: python -m exo electron
echo To run all interfaces: python -m exo all

pause
