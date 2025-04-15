MCP Server
=========

This guide provides information about the Model Context Protocol (MCP) server of the exo multi-agent system.

Overview
-------

The Model Context Protocol (MCP) server provides additional capabilities to the exo system, such as:

- **Desktop Control**: Control the user's desktop, including mouse and keyboard input.
- **File System Access**: Access the user's file system for reading and writing files.
- **Application Control**: Launch and control applications on the user's system.
- **System Information**: Access information about the user's system, such as hardware, operating system, and installed applications.

These capabilities allow the exo system to interact with the user's environment in a more powerful way.

Components
---------

The MCP server consists of the following components:

Server
~~~~~

The Server module provides the FastAPI application for the MCP server. It:

- Initializes the FastAPI application
- Registers tools and resources
- Handles requests for tools and resources

.. code-block:: python

    from exo.mcp.server import app, register_tool, register_resource

    # Register a tool
    @register_tool(
        name="hello_world",
        description="Say hello to the world",
        schema={"type": "object", "properties": {"name": {"type": "string"}}},
    )
    def hello_world(name="World"):
        return {"message": f"Hello, {name}!"}

    # Register a resource
    @register_resource(
        uri="system_info",
        description="Get system information",
    )
    def system_info():
        import platform
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    # Run the server
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)

Client
~~~~~

The Client module provides a client for interacting with the MCP server. It:

- Connects to the MCP server
- Executes tools
- Accesses resources

.. code-block:: python

    from exo.mcp.client import MCPClient

    # Create a client
    client = MCPClient("http://localhost:8001")

    # Execute a tool
    result = client.execute_tool("hello_world", {"name": "John"})
    print(result)  # {"message": "Hello, John!"}

    # Access a resource
    result = client.access_resource("system_info")
    print(result)  # {"system": "Linux", "release": "5.15.0", ...}

Desktop Control
~~~~~~~~~~~~~

The Desktop Control module provides a client for controlling the user's desktop. It:

- Controls the mouse
- Controls the keyboard
- Takes screenshots
- Gets screen information

.. code-block:: python

    from exo.mcp.client import DesktopControlClient

    # Create a client
    client = DesktopControlClient()

    # Move the mouse
    client.move_mouse(100, 100)

    # Click the mouse
    client.click(100, 100)

    # Type text
    client.type_text("Hello, world!")

    # Take a screenshot
    screenshot = client.take_screenshot()

    # Get screen information
    screen_info = client.get_screen_info()

Tools and Resources
-----------------

The MCP server provides a number of tools and resources:

Tools
~~~~~

- **click_element**: Click at a specific position on the screen.
- **move_mouse**: Move the mouse to a specific position on the screen.
- **type_text**: Type text on the keyboard.
- **take_screenshot**: Take a screenshot of the screen.
- **get_screen_info**: Get information about the screen.
- **read_file**: Read a file from the file system.
- **write_file**: Write a file to the file system.
- **list_files**: List files in a directory.
- **launch_application**: Launch an application.
- **close_application**: Close an application.
- **get_active_window**: Get the active window.
- **switch_window**: Switch to a different window.

Resources
~~~~~~~~

- **system_info**: Get information about the system.
- **clipboard**: Get the contents of the clipboard.
- **environment_variables**: Get the environment variables.
- **user_info**: Get information about the user.
- **network_info**: Get information about the network.
- **disk_info**: Get information about the disk.
- **memory_info**: Get information about the memory.
- **cpu_info**: Get information about the CPU.
- **gpu_info**: Get information about the GPU.
- **battery_info**: Get information about the battery.

Usage
-----

To use the MCP server, you can either use the server directly or use the client.

Using the Server
~~~~~~~~~~~~~

The server provides a FastAPI application that you can run:

.. code-block:: python

    from exo.mcp.server import app

    # Run the server
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)

You can also use the command-line interface:

.. code-block:: bash

    python -m exo.mcp

Using the Client
~~~~~~~~~~~~~

The client provides a high-level interface to the MCP server:

.. code-block:: python

    from exo.mcp.client import MCPClient

    # Create a client
    client = MCPClient("http://localhost:8001")

    # Execute a tool
    result = client.execute_tool("hello_world", {"name": "John"})
    print(result)  # {"message": "Hello, John!"}

    # Access a resource
    result = client.access_resource("system_info")
    print(result)  # {"system": "Linux", "release": "5.15.0", ...}

Using the Desktop Control Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The desktop control client provides a high-level interface for controlling the user's desktop:

.. code-block:: python

    from exo.mcp.client import DesktopControlClient

    # Create a client
    client = DesktopControlClient()

    # Move the mouse
    client.move_mouse(100, 100)

    # Click the mouse
    client.click(100, 100)

    # Type text
    client.type_text("Hello, world!")

    # Take a screenshot
    screenshot = client.take_screenshot()

    # Get screen information
    screen_info = client.get_screen_info()

Customization
-----------

You can customize the MCP server by:

- Registering custom tools
- Registering custom resources
- Extending the client

Registering Custom Tools
~~~~~~~~~~~~~~~~~~~~~

You can register custom tools using the register_tool decorator:

.. code-block:: python

    from exo.mcp.server import register_tool

    @register_tool(
        name="custom_tool",
        description="A custom tool",
        schema={"type": "object", "properties": {"param": {"type": "string"}}},
    )
    def custom_tool(param="default"):
        # Custom tool implementation
        return {"result": f"Custom tool: {param}"}

Registering Custom Resources
~~~~~~~~~~~~~~~~~~~~~~~~

You can register custom resources using the register_resource decorator:

.. code-block:: python

    from exo.mcp.server import register_resource

    @register_resource(
        uri="custom_resource",
        description="A custom resource",
    )
    def custom_resource():
        # Custom resource implementation
        return {"result": "Custom resource"}

Extending the Client
~~~~~~~~~~~~~~~~

You can extend the client by subclassing the MCPClient class:

.. code-block:: python

    from exo.mcp.client import MCPClient

    class CustomClient(MCPClient):
        def __init__(self, base_url="http://localhost:8001"):
            super().__init__(base_url)

        def custom_method(self, param):
            # Custom method implementation
            return self.execute_tool("custom_tool", {"param": param})

API Reference
-----------

Server
~~~~~

.. code-block:: python

    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, create_model
    from typing import Dict, Any, Callable, Optional, List, Type

    app = FastAPI(
        title="exo MCP Server",
        description="Model Context Protocol server for the exo system",
        version="0.1.0",
    )

    tools = {}
    resources = {}

    def register_tool(name, description, schema, handler=None):
        """Register a tool with the MCP server.

        Args:
            name (str): The name of the tool.
            description (str): The description of the tool.
            schema (Dict): The JSON schema for the tool's input.
            handler (Callable): The handler function for the tool.

        Returns:
            Callable: The decorator function.
        """
        def decorator(func):
            tools[name] = {
                "name": name,
                "description": description,
                "schema": schema,
                "handler": func,
            }
            return func

        if handler:
            return decorator(handler)
        return decorator

    def register_resource(uri, description, handler=None):
        """Register a resource with the MCP server.

        Args:
            uri (str): The URI of the resource.
            description (str): The description of the resource.
            handler (Callable): The handler function for the resource.

        Returns:
            Callable: The decorator function.
        """
        def decorator(func):
            resources[uri] = {
                "uri": uri,
                "description": description,
                "handler": func,
            }
            return func

        if handler:
            return decorator(handler)
        return decorator

    @app.get("/")
    async def root():
        """Get information about the MCP server."""
        return {
            "name": "exo MCP Server",
            "version": "0.1.0",
            "description": "Model Context Protocol server for the exo system",
        }

    @app.get("/tools")
    async def get_tools():
        """Get the available tools."""
        return {
            "tools": [
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "schema": tool["schema"],
                }
                for tool in tools.values()
            ]
        }

    @app.get("/resources")
    async def get_resources():
        """Get the available resources."""
        return {
            "resources": [
                {
                    "uri": resource["uri"],
                    "description": resource["description"],
                }
                for resource in resources.values()
            ]
        }

    @app.post("/tools/{tool_name}")
    async def execute_tool(tool_name: str, data: Dict[str, Any] = None):
        """Execute a tool.

        Args:
            tool_name (str): The name of the tool to execute.
            data (Dict[str, Any]): The input data for the tool.

        Returns:
            Dict[str, Any]: The result of the tool execution.
        """
        if tool_name not in tools:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        tool = tools[tool_name]
        handler = tool["handler"]

        try:
            result = handler(**(data or {}))
            return {"result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/resources/{resource_uri}")
    async def access_resource(resource_uri: str):
        """Access a resource.

        Args:
            resource_uri (str): The URI of the resource to access.

        Returns:
            Dict[str, Any]: The resource data.
        """
        if resource_uri not in resources:
            raise HTTPException(status_code=404, detail=f"Resource '{resource_uri}' not found")

        resource = resources[resource_uri]
        handler = resource["handler"]

        try:
            result = handler()
            return {"result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

Client
~~~~~

.. code-block:: python

    import requests
    import time
    from typing import Dict, Any, List, Optional

    class MCPClient:
        """Client for the MCP server."""

        def __init__(self, base_url="http://localhost:8001"):
            """Initialize the client.

            Args:
                base_url (str): The base URL of the MCP server.
            """
            self.base_url = base_url
            self.tools_cache = {}
            self.resources_cache = {}
            self.last_cache_update = 0

        def _update_cache(self):
            """Update the tools and resources cache."""
            if time.time() - self.last_cache_update < 60:
                return

            # Update tools cache
            response = requests.get(f"{self.base_url}/tools")
            response.raise_for_status()
            data = response.json()
            self.tools_cache = {tool["name"]: tool for tool in data["tools"]}

            # Update resources cache
            response = requests.get(f"{self.base_url}/resources")
            response.raise_for_status()
            data = response.json()
            self.resources_cache = {resource["uri"]: resource for resource in data["resources"]}

            self.last_cache_update = time.time()

        def get_tools(self) -> List[Dict[str, Any]]:
            """Get the available tools.

            Returns:
                List[Dict[str, Any]]: The available tools.
            """
            response = requests.get(f"{self.base_url}/tools")
            response.raise_for_status()
            data = response.json()
            return data["tools"]

        def get_resources(self) -> List[Dict[str, Any]]:
            """Get the available resources.

            Returns:
                List[Dict[str, Any]]: The available resources.
            """
            response = requests.get(f"{self.base_url}/resources")
            response.raise_for_status()
            data = response.json()
            return data["resources"]

        def execute_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """Execute a tool.

            Args:
                tool_name (str): The name of the tool to execute.
                arguments (Dict[str, Any]): The arguments for the tool.

            Returns:
                Dict[str, Any]: The result of the tool execution.
            """
            self._update_cache()
            if tool_name not in self.tools_cache:
                raise ValueError(f"Tool '{tool_name}' not found")

            response = requests.post(f"{self.base_url}/tools/{tool_name}", json=arguments or {})
            response.raise_for_status()
            return response.json()

        def access_resource(self, resource_uri: str) -> Dict[str, Any]:
            """Access a resource.

            Args:
                resource_uri (str): The URI of the resource to access.

            Returns:
                Dict[str, Any]: The resource data.
            """
            self._update_cache()
            if resource_uri not in self.resources_cache:
                raise ValueError(f"Resource '{resource_uri}' not found")

            response = requests.get(f"{self.base_url}/resources/{resource_uri}")
            response.raise_for_status()
            return response.json()

    class DesktopControlClient(MCPClient):
        """Client for desktop control."""

        def __init__(self, base_url="http://localhost:8001"):
            """Initialize the client.

            Args:
                base_url (str): The base URL of the MCP server.
            """
            super().__init__(base_url)

        def move_mouse(self, x: int, y: int) -> Dict[str, Any]:
            """Move the mouse to a specific position.

            Args:
                x (int): The x coordinate.
                y (int): The y coordinate.

            Returns:
                Dict[str, Any]: The result of the operation.
            """
            return self.execute_tool("move_mouse", {"x": x, "y": y})

        def click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> Dict[str, Any]:
            """Click at a specific position.

            Args:
                x (int): The x coordinate.
                y (int): The y coordinate.
                button (str): The mouse button to click.
                clicks (int): The number of clicks.

            Returns:
                Dict[str, Any]: The result of the operation.
            """
            return self.execute_tool("click_element", {
                "x": x,
                "y": y,
                "button": button,
                "clicks": clicks,
            })

        def type_text(self, text: str) -> Dict[str, Any]:
            """Type text on the keyboard.

            Args:
                text (str): The text to type.

            Returns:
                Dict[str, Any]: The result of the operation.
            """
            return self.execute_tool("type_text", {"text": text})

        def take_screenshot(self) -> Dict[str, Any]:
            """Take a screenshot of the screen.

            Returns:
                Dict[str, Any]: The screenshot data.
            """
            return self.execute_tool("take_screenshot")

        def get_screen_info(self) -> Dict[str, Any]:
            """Get information about the screen.

            Returns:
                Dict[str, Any]: The screen information.
            """
            return self.execute_tool("get_screen_info")
