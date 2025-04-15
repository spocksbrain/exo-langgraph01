"""
Model Context Protocol (MCP) server implementation for desktop control.

This module provides a simple MCP server that exposes desktop control capabilities
through a standardized interface.
"""
import base64
import io
import json
import logging
import os
import time
from typing import Dict, Any, List, Optional, Callable, Union

import pyautogui
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageGrab

from exo.config import MCP_SERVER_HOST, MCP_SERVER_PORT


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title="exo MCP Server",
    description="Model Context Protocol server for desktop control",
    version="0.1.0",
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MCP tool registry
tools: Dict[str, Dict[str, Any]] = {}


# MCP resource registry
resources: Dict[str, Dict[str, Any]] = {}


def register_tool(
    name: str,
    description: str,
    handler: Callable,
    schema: Dict[str, Any],
) -> None:
    """Register a tool with the MCP server.
    
    Args:
        name: Tool name
        description: Tool description
        handler: Function to handle tool requests
        schema: JSON schema for tool arguments
    """
    tools[name] = {
        "name": name,
        "description": description,
        "handler": handler,
        "schema": schema,
    }
    logger.info(f"Registered tool: {name}")


def register_resource(
    uri: str,
    description: str,
    handler: Callable,
) -> None:
    """Register a resource with the MCP server.
    
    Args:
        uri: Resource URI
        description: Resource description
        handler: Function to handle resource requests
    """
    resources[uri] = {
        "uri": uri,
        "description": description,
        "handler": handler,
    }
    logger.info(f"Registered resource: {uri}")


@app.get("/")
async def root():
    """Root endpoint.
    
    Returns:
        Basic information about the MCP server
    """
    return {
        "name": "exo MCP Server",
        "version": "0.1.0",
        "description": "Model Context Protocol server for desktop control",
    }


@app.get("/tools")
async def get_tools():
    """Get available tools.
    
    Returns:
        List of available tools
    """
    return {
        "tools": [
            {
                "name": name,
                "description": tool["description"],
                "schema": tool["schema"],
            }
            for name, tool in tools.items()
        ]
    }


@app.post("/tools/{tool_name}")
async def execute_tool(tool_name: str, request: Request):
    """Execute a tool.
    
    Args:
        tool_name: Name of the tool to execute
        request: Request object containing tool arguments
        
    Returns:
        Tool result
    """
    if tool_name not in tools:
        raise HTTPException(status_code=404, detail=f"Tool not found: {tool_name}")
    
    # Get tool
    tool = tools[tool_name]
    
    # Parse arguments
    try:
        arguments = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Execute tool
    try:
        result = tool["handler"](**arguments)
        return {"result": result}
    except Exception as e:
        logger.exception(f"Error executing tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/resources")
async def get_resources():
    """Get available resources.
    
    Returns:
        List of available resources
    """
    return {
        "resources": [
            {
                "uri": uri,
                "description": resource["description"],
            }
            for uri, resource in resources.items()
        ]
    }


@app.get("/resources/{resource_uri:path}")
async def access_resource(resource_uri: str):
    """Access a resource.
    
    Args:
        resource_uri: URI of the resource to access
        
    Returns:
        Resource data
    """
    if resource_uri not in resources:
        raise HTTPException(status_code=404, detail=f"Resource not found: {resource_uri}")
    
    # Get resource
    resource = resources[resource_uri]
    
    # Execute handler
    try:
        result = resource["handler"]()
        return {"result": result}
    except Exception as e:
        logger.exception(f"Error accessing resource {resource_uri}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Desktop control tools

def click_element(x: int, y: int, button: str = "left", clicks: int = 1) -> Dict[str, Any]:
    """Click at a specific position.
    
    Args:
        x: X coordinate
        y: Y coordinate
        button: Mouse button to click ("left", "right", or "middle")
        clicks: Number of clicks
        
    Returns:
        Success message
    """
    pyautogui.click(x=x, y=y, button=button, clicks=clicks)
    return {"success": True, "message": f"Clicked at ({x}, {y}) with {button} button {clicks} times"}


def move_mouse(x: int, y: int) -> Dict[str, Any]:
    """Move the mouse to a specific position.
    
    Args:
        x: X coordinate
        y: Y coordinate
        
    Returns:
        Success message
    """
    pyautogui.moveTo(x=x, y=y)
    return {"success": True, "message": f"Moved mouse to ({x}, {y})"}


def type_text(text: str) -> Dict[str, Any]:
    """Type text.
    
    Args:
        text: Text to type
        
    Returns:
        Success message
    """
    pyautogui.write(text)
    return {"success": True, "message": f"Typed text: {text[:20]}..."}


def press_key(key: str) -> Dict[str, Any]:
    """Press a key.
    
    Args:
        key: Key to press
        
    Returns:
        Success message
    """
    pyautogui.press(key)
    return {"success": True, "message": f"Pressed key: {key}"}


def capture_screen(region: Optional[List[int]] = None) -> Dict[str, Any]:
    """Capture the screen.
    
    Args:
        region: Region to capture [left, top, width, height]
        
    Returns:
        Screenshot as base64-encoded PNG
    """
    # Capture screenshot
    if region:
        screenshot = ImageGrab.grab(bbox=tuple(region))
    else:
        screenshot = ImageGrab.grab()
    
    # Convert to base64
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    screenshot_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return {
        "success": True,
        "screenshot": screenshot_base64,
        "width": screenshot.width,
        "height": screenshot.height,
    }


def get_screen_size() -> Dict[str, Any]:
    """Get the screen size.
    
    Returns:
        Screen width and height
    """
    width, height = pyautogui.size()
    return {"success": True, "width": width, "height": height}


def get_mouse_position() -> Dict[str, Any]:
    """Get the current mouse position.
    
    Returns:
        Mouse X and Y coordinates
    """
    x, y = pyautogui.position()
    return {"success": True, "x": x, "y": y}


# Register tools
register_tool(
    name="click_element",
    description="Click at a specific position",
    handler=click_element,
    schema={
        "type": "object",
        "properties": {
            "x": {"type": "integer", "description": "X coordinate"},
            "y": {"type": "integer", "description": "Y coordinate"},
            "button": {"type": "string", "enum": ["left", "right", "middle"], "default": "left", "description": "Mouse button to click"},
            "clicks": {"type": "integer", "default": 1, "description": "Number of clicks"},
        },
        "required": ["x", "y"],
    },
)

register_tool(
    name="move_mouse",
    description="Move the mouse to a specific position",
    handler=move_mouse,
    schema={
        "type": "object",
        "properties": {
            "x": {"type": "integer", "description": "X coordinate"},
            "y": {"type": "integer", "description": "Y coordinate"},
        },
        "required": ["x", "y"],
    },
)

register_tool(
    name="type_text",
    description="Type text",
    handler=type_text,
    schema={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Text to type"},
        },
        "required": ["text"],
    },
)

register_tool(
    name="press_key",
    description="Press a key",
    handler=press_key,
    schema={
        "type": "object",
        "properties": {
            "key": {"type": "string", "description": "Key to press"},
        },
        "required": ["key"],
    },
)

register_tool(
    name="capture_screen",
    description="Capture the screen",
    handler=capture_screen,
    schema={
        "type": "object",
        "properties": {
            "region": {"type": "array", "items": {"type": "integer"}, "description": "Region to capture [left, top, width, height]"},
        },
    },
)

register_tool(
    name="get_screen_size",
    description="Get the screen size",
    handler=get_screen_size,
    schema={
        "type": "object",
        "properties": {},
    },
)

register_tool(
    name="get_mouse_position",
    description="Get the current mouse position",
    handler=get_mouse_position,
    schema={
        "type": "object",
        "properties": {},
    },
)


# Register resources
register_resource(
    uri="screen",
    description="Current screen capture",
    handler=lambda: capture_screen(),
)

register_resource(
    uri="screen_size",
    description="Screen size",
    handler=get_screen_size,
)

register_resource(
    uri="mouse_position",
    description="Current mouse position",
    handler=get_mouse_position,
)


def start_mcp_server():
    """Start the MCP server."""
    import uvicorn
    
    logger.info(f"Starting MCP server on {MCP_SERVER_HOST}:{MCP_SERVER_PORT}")
    uvicorn.run(
        "exo.mcp.server:app",
        host=MCP_SERVER_HOST,
        port=MCP_SERVER_PORT,
        reload=False,
    )


if __name__ == "__main__":
    start_mcp_server()
