# exo MCP Server

This is the Model Context Protocol (MCP) server for the exo multi-agent system. It provides a standardized interface for desktop control and other capabilities.

## Features

- Standardized interface for desktop control
- Tool registration and discovery
- Resource access
- RESTful API for tool execution
- Security considerations for sensitive operations

## Usage

```bash
# Run the MCP server
python -m exo.mcp

# Run with debug logging
python -m exo.mcp --debug
```

## API Endpoints

### Tools

- `GET /tools`: Get available tools
- `POST /tools/{tool_name}`: Execute a tool

### Resources

- `GET /resources`: Get available resources
- `GET /resources/{resource_uri}`: Access a resource

## Available Tools

- `click_element`: Click at a specific position
- `move_mouse`: Move the mouse to a specific position
- `type_text`: Type text
- `press_key`: Press a key
- `capture_screen`: Capture the screen
- `get_screen_size`: Get the screen size
- `get_mouse_position`: Get the current mouse position

## Available Resources

- `screen`: Current screen capture
- `screen_size`: Screen size
- `mouse_position`: Current mouse position

## Architecture

The MCP server is built with:

- **FastAPI**: Modern, fast web framework for building APIs
- **PyAutoGUI**: Cross-platform GUI automation
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server

## Components

- **server.py**: Main MCP server implementation
- **client.py**: Client for interacting with the MCP server
- **__main__.py**: Entry point for the MCP server

## Communication

The MCP server communicates with:

1. **Clients**: Web interface, Electron app, and other clients
2. **Desktop Environment**: For desktop control operations

## Security

The MCP server includes security considerations for sensitive operations:

- Tool registration with schemas for validation
- Permission checks for sensitive operations
- Logging of all operations

## Customization

You can customize the MCP server by:

- Adding new tools to `server.py`
- Adding new resources to `server.py`
- Updating the MCP server configuration in `config.py`
