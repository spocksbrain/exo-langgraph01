"""
Entry point for the exo MCP server.

This module allows running the MCP server as a module:
python -m exo.mcp
"""
from exo.mcp.server import start_mcp_server


if __name__ == "__main__":
    start_mcp_server()
