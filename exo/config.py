"""
Configuration settings for the exo multi-agent system.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Base directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# API settings
API_HOST = os.getenv("EXO_API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("EXO_API_PORT", "8000"))
API_DEBUG = os.getenv("EXO_API_DEBUG", "False").lower() == "true"

# LLM settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL = os.getenv("EXO_DEFAULT_MODEL", "gpt-4-turbo")
EMBEDDING_MODEL = os.getenv("EXO_EMBEDDING_MODEL", "text-embedding-ada-002")

# Knowledge system settings
NEO4J_URI = os.getenv("EXO_NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("EXO_NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("EXO_NEO4J_PASSWORD", "password")
VECTOR_DB_PATH = DATA_DIR / "vector_db"

# Agent settings
AGENT_CONFIG: Dict[str, Dict[str, Any]] = {
    "pia": {
        "name": "Primary Interface Agent",
        "description": "User-facing agent handling all direct interactions",
        "model": DEFAULT_MODEL,
    },
    "cnc": {
        "name": "Command & Control Agent",
        "description": "Orchestrates complex multi-domain tasks",
        "model": DEFAULT_MODEL,
    },
    "software_engineer": {
        "name": "Software Engineer Agent",
        "description": "Specialized agent for code generation and documentation",
        "model": DEFAULT_MODEL,
    },
    "system_control": {
        "name": "System Control Agent",
        "description": "Specialized agent for desktop control and automation",
        "model": DEFAULT_MODEL,
    },
}

# Interface settings
CLI_CONFIG = {
    "prompt": "exo> ",
    "history_file": DATA_DIR / "cli_history.txt",
}

WEB_CONFIG = {
    "host": os.getenv("EXO_WEB_HOST", "127.0.0.1"),
    "port": int(os.getenv("EXO_WEB_PORT", "3000")),
}

ELECTRON_CONFIG = {
    "dev_server_port": int(os.getenv("EXO_ELECTRON_DEV_PORT", "3001")),
}

# MCP server settings
MCP_SERVER_HOST = os.getenv("EXO_MCP_HOST", "127.0.0.1")
MCP_SERVER_PORT = int(os.getenv("EXO_MCP_PORT", "5000"))

# Create a .env.example file if it doesn't exist
def create_env_example():
    env_example_path = BASE_DIR / ".env.example"
    if not env_example_path.exists():
        with open(env_example_path, "w") as f:
            f.write("""# API settings
EXO_API_HOST=127.0.0.1
EXO_API_PORT=8000
EXO_API_DEBUG=False

# LLM settings
OPENAI_API_KEY=your_openai_api_key_here
EXO_DEFAULT_MODEL=gpt-4-turbo
EXO_EMBEDDING_MODEL=text-embedding-ada-002

# Knowledge system settings
EXO_NEO4J_URI=bolt://localhost:7687
EXO_NEO4J_USER=neo4j
EXO_NEO4J_PASSWORD=password

# Interface settings
EXO_WEB_HOST=127.0.0.1
EXO_WEB_PORT=3000
EXO_ELECTRON_DEV_PORT=3001

# MCP server settings
EXO_MCP_HOST=127.0.0.1
EXO_MCP_PORT=5000
""")

create_env_example()
