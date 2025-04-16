# exo Multi-Agent System

A proof-of-concept implementation of the "exo" multi-agent AI system, featuring a hierarchical arrangement of specialized AI agents working in concert to handle complex tasks across multiple domains.

## Overview

The exo system consists of:

- **Primary Interface Agent (PIA)**: User-facing component handling all direct interactions
- **Command & Control Agent (CNC)**: Orchestrates complex multi-domain tasks
- **Domain Agents**: Specialized for specific functions (Software Engineering, System Control, etc.)
- **Knowledge System**: Dual-memory architecture with knowledge graph and vector database
- **Multiple Interfaces**: CLI, Web, and Electron desktop app

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│       ┌───────────────────────────────────────────┐         │
│       │   Primary Interface & Management Agent    │         │
│       │               (PIA)                       │         │
│       └─────────────────┬─────────────────────────┘         │
│                         │                                   │
│                         ▼                                   │
│       ┌───────────────────────────────────────────┐         │
│       │     Command & Control Agent (CNC)         │         │
│       └──────┬─────────────────┬──────────────┬───┘         │
│              │                 │              │             │
│              ▼                 ▼              ▼             │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐   │
│  │ Domain Agent 1 │ │ Domain Agent 2 │ │ Domain Agent n │   │
│  └────────────────┘ └────────────────┘ └────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 Knowledge System                     │    │
│  │  ┌─────────────────────┐  ┌─────────────────────┐   │    │
│  │  │   Knowledge Graph   │  │   Vector Database   │   │    │
│  │  │  (Long-term Memory) │  │ (Short-term Memory) │   │    │
│  │  └─────────────────────┘  └─────────────────────┘   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+ and npm (required for Web and Electron interfaces)
- OpenAI API key
- Python setuptools, pip, and wheel (automatically installed by setup scripts)

### Installation

There are three ways to install and run the exo system:

#### Option 1: Using the Setup Scripts (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/spocksbrain/exo-langgraph01.git
cd exo-langgraph01
```

2. Run the setup script from the root directory of the project:
```bash
# On Linux/macOS
chmod +x exo/setup.sh  # Make the script executable if needed
./exo/setup.sh

# On Windows
.\exo\setup.bat
```

The setup script will:
- Create a virtual environment
- Install required Python packages
- Install the exo package in development mode
- Create a .env file from the template

#### Option 2: Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/spocksbrain/exo-langgraph01.git
cd exo-langgraph01
```

2. Create and activate a virtual environment:
```bash
# On Linux/macOS
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install the package in development mode:
```bash
# Install dependencies and the package
pip install -e .
```

4. Create a .env file:
```bash
cp exo/.env.example .env
```

#### Option 3: Using run_without_install.py (If Installation Fails)

If you're experiencing issues with package installation, you can use the `run_without_install.py` script that bypasses the need for installing the package:

1. Clone the repository (if you haven't already):
```bash
git clone https://github.com/spocksbrain/exo-langgraph01.git
cd exo-langgraph01
```

2. Create and activate a virtual environment (if you haven't already):
```bash
# On Linux/macOS
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install the requirements:
```bash
pip install -r exo/requirements.txt
```

4. Create a .env file:
```bash
cp exo/.env.example .env
```

5. Run the system using the special script:
```bash
python run_without_install.py cli
```

This method modifies the Python path directly to include the current directory, bypassing the need for package installation.

### Configuration

Edit the `.env` file with your API keys and configuration:
- `OPENAI_API_KEY`: Your OpenAI API key (required, must start with "sk-" not "sk-ant-")
- `EXO_DEFAULT_MODEL` or `DEFAULT_MODEL`: The OpenAI model to use (default: "gpt-4-turbo")
- `EXO_NEO4J_URI` or `NEO4J_URI`: URI for Neo4j database (optional, for knowledge graph)
- `EXO_NEO4J_USER` or `NEO4J_USER`: Username for Neo4j database (optional)
- `EXO_NEO4J_PASSWORD` or `NEO4J_PASSWORD`: Password for Neo4j database (optional)

Note: The system will look for a `.env` file in the root directory first, then in the `exo/` directory.
Both formats (with or without the `EXO_` prefix) are supported for backward compatibility.

**Important**: Make sure to use an OpenAI API key (starting with "sk-"), not an Anthropic API key (starting with "sk-ant-"). The system uses the OpenAI API for its LLM functionality.

### Troubleshooting Installation

If you encounter any issues during installation, here are some common solutions:

#### ModuleNotFoundError: No module named 'autogen'
The project requires the `autogen` package (not `autogen-agentchat`). This should be automatically installed by the setup script, but you can manually install it with:
```bash
# From the root directory
pip install -r exo/requirements.txt

# Or directly install autogen
pip install autogen
```

#### ModuleNotFoundError: No module named 'setuptools'
If you get this error when running `setup.py`, it means the setuptools package is missing. Install it with:
```bash
pip install setuptools
```
The updated setup scripts should automatically handle this for you.

#### Import errors with autogen version compatibility
If you see errors related to imports from `autogen.oai.client`, there might be a version compatibility issue. Try:

1. Using the `run_without_install.py` script, which includes fixes for these issues
2. Or pull the latest code with `git pull origin main` which contains the necessary fixes

#### Node.js and npm issues (Web and Electron interfaces)
If you encounter issues with the Web or Electron interfaces:

1. Make sure Node.js (v16+) and npm are installed:
```bash
node --version
npm --version
```

2. If you get errors about missing dependencies, try manually installing them:
```bash
# For Web interface
cd exo/interfaces/web
npm install

# For Electron interface
cd exo/interfaces/electron
npm install
```

3. If you see errors about port conflicts when running the Web interface, you can specify a different port:
```bash
cd exo/interfaces/web
npm run dev -- -p 3001
```

#### Deprecation Warnings
You may see deprecation warnings about license classifiers when running setup.py directly. This is normal and can be ignored. We've updated the project to use pyproject.toml for modern Python packaging, which addresses these warnings.

Note: You should not run `python setup.py` directly without any commands. Instead, use `pip install -e .` to install the package in development mode.

#### Repeating Response Loop Issues
If you encounter a problem where the system repeatedly generates the same response or gets stuck in a loop, the issue has been fixed in the latest code. Pull the latest changes with:
```bash
git pull origin main
```

### Running the System

There are multiple ways to run the exo system:

#### 1. Using run_without_install.py (Recommended for Installation Issues)

```bash
python run_without_install.py [interface] [--debug]
```

Where `[interface]` is one of: `cli`, `api`, `web`, `mcp`, `electron`, or `all`.

This method is particularly useful if you're experiencing import issues with the traditional installation.

#### 2. Using the Module-Based Execution

This is the primary way to run the system when installed correctly:

```bash
# Activate the virtual environment first
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate.bat  # On Windows

# Run the desired interface
python -m exo [interface]
```

Where `[interface]` is one of:
- `cli`: Command-line interface
- `api`: API server
- `web`: Web interface
- `mcp`: Model Context Protocol server
- `electron`: Electron desktop app
- `all`: Run API, MCP, and Electron interfaces together

#### 3. Using the Run Script

The run.py script provides a wrapper around the module-based execution with additional checks:

```bash
python run.py [interface] [--debug]
```

Where `[interface]` is one of: `cli`, `api`, `web`, `mcp`, `electron`, or `all` (default).

For example:
```bash
# Run the CLI interface
python run.py cli

# Run the web interface with debug logging
python run.py web --debug
```

Note: When running the web interface or Electron app, the API server will be automatically started in the background.

#### 4. Interface-Specific Execution

You can also run specific interfaces directly:

```bash
# CLI Interface
python -m exo.interfaces.cli

# API Server
python -m exo.api.app

# MCP Server
python -m exo.mcp

# Electron App
python -m exo.interfaces.electron
```

#### 5. Development Server for Web Interface

For web development, you can run the Next.js development server directly:

```bash
cd exo/interfaces/web
npm run dev
```

## Project Structure

- `exo/core/`: Core agent system and orchestration
- `exo/api/`: FastAPI-based API layer
- `exo/interfaces/`: Multiple user interfaces (CLI, Web, Electron)
- `exo/knowledge/`: Knowledge graph and vector database integration
- `exo/mcp/`: Model Context Protocol server implementation

## Recent Updates

- **Fixed repeating responses issue**: Removed redundant message processing in the Primary Interface Agent
- **Improved compatibility with autogen versions**: Updated import statements to work with autogen 0.8.6+
- **Added `run_without_install.py`**: New script that can run the system without formal package installation
- **Enhanced error handling**: Better diagnostics and recovery from API and import errors

## Features

- **Multi-Agent Architecture**: Hierarchical arrangement of specialized agents
- **Task Decomposition**: Breaking complex tasks into subtasks
- **Knowledge Persistence**: Dual-memory system for context retention
- **Multiple Interfaces**: CLI, Web, and Electron desktop app
- **Animated Dot UI**: Visual representation of system state

## License

MIT
