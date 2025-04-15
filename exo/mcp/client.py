"""
Model Context Protocol (MCP) client for interacting with MCP servers.

This module provides a client for interacting with MCP servers, allowing the system
to use tools and resources exposed by MCP servers.
"""
import json
import logging
import os
import time
from typing import Dict, Any, List, Optional, Union

import requests

from exo.config import MCP_SERVER_HOST, MCP_SERVER_PORT


# Configure logging
logger = logging.getLogger(__name__)


class MCPClient:
    """Client for interacting with MCP servers."""
    
    def __init__(self, server_url: str):
        """Initialize the MCP client.
        
        Args:
            server_url: URL of the MCP server
        """
        self.server_url = server_url
        self.tools_cache: Dict[str, Dict[str, Any]] = {}
        self.resources_cache: Dict[str, Dict[str, Any]] = {}
        self.last_cache_update = 0
        self.cache_ttl = 60  # 60 seconds
    
    def _refresh_cache(self) -> None:
        """Refresh the tools and resources cache."""
        # Check if cache is still valid
        now = time.time()
        if now - self.last_cache_update < self.cache_ttl:
            return
        
        # Refresh tools
        try:
            response = requests.get(f"{self.server_url}/tools")
            response.raise_for_status()
            tools_data = response.json()
            
            # Update cache
            self.tools_cache = {
                tool["name"]: tool
                for tool in tools_data.get("tools", [])
            }
        except Exception as e:
            logger.error(f"Error refreshing tools cache: {e}")
        
        # Refresh resources
        try:
            response = requests.get(f"{self.server_url}/resources")
            response.raise_for_status()
            resources_data = response.json()
            
            # Update cache
            self.resources_cache = {
                resource["uri"]: resource
                for resource in resources_data.get("resources", [])
            }
        except Exception as e:
            logger.error(f"Error refreshing resources cache: {e}")
        
        # Update cache timestamp
        self.last_cache_update = now
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools.
        
        Returns:
            List of available tools
        """
        self._refresh_cache()
        return list(self.tools_cache.values())
    
    def get_resources(self) -> List[Dict[str, Any]]:
        """Get available resources.
        
        Returns:
            List of available resources
        """
        self._refresh_cache()
        return list(self.resources_cache.values())
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        self._refresh_cache()
        
        # Check if tool exists
        if tool_name not in self.tools_cache:
            raise ValueError(f"Tool not found: {tool_name}")
        
        # Execute tool
        try:
            response = requests.post(
                f"{self.server_url}/tools/{tool_name}",
                json=arguments,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            raise
    
    def access_resource(self, resource_uri: str) -> Dict[str, Any]:
        """Access a resource.
        
        Args:
            resource_uri: URI of the resource to access
            
        Returns:
            Resource data
        """
        self._refresh_cache()
        
        # Check if resource exists
        if resource_uri not in self.resources_cache:
            raise ValueError(f"Resource not found: {resource_uri}")
        
        # Access resource
        try:
            response = requests.get(f"{self.server_url}/resources/{resource_uri}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error accessing resource {resource_uri}: {e}")
            raise


class DesktopControlClient(MCPClient):
    """Client for interacting with the desktop control MCP server."""
    
    def __init__(self, host: str = MCP_SERVER_HOST, port: int = MCP_SERVER_PORT):
        """Initialize the desktop control client.
        
        Args:
            host: MCP server host
            port: MCP server port
        """
        super().__init__(f"http://{host}:{port}")
    
    def click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> Dict[str, Any]:
        """Click at a specific position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            button: Mouse button to click ("left", "right", or "middle")
            clicks: Number of clicks
            
        Returns:
            Success message
        """
        return self.execute_tool("click_element", {
            "x": x,
            "y": y,
            "button": button,
            "clicks": clicks,
        })
    
    def move_mouse(self, x: int, y: int) -> Dict[str, Any]:
        """Move the mouse to a specific position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Success message
        """
        return self.execute_tool("move_mouse", {
            "x": x,
            "y": y,
        })
    
    def type_text(self, text: str) -> Dict[str, Any]:
        """Type text.
        
        Args:
            text: Text to type
            
        Returns:
            Success message
        """
        return self.execute_tool("type_text", {
            "text": text,
        })
    
    def press_key(self, key: str) -> Dict[str, Any]:
        """Press a key.
        
        Args:
            key: Key to press
            
        Returns:
            Success message
        """
        return self.execute_tool("press_key", {
            "key": key,
        })
    
    def capture_screen(self, region: Optional[List[int]] = None) -> Dict[str, Any]:
        """Capture the screen.
        
        Args:
            region: Region to capture [left, top, width, height]
            
        Returns:
            Screenshot as base64-encoded PNG
        """
        arguments = {}
        if region:
            arguments["region"] = region
        
        return self.execute_tool("capture_screen", arguments)
    
    def get_screen_size(self) -> Dict[str, Any]:
        """Get the screen size.
        
        Returns:
            Screen width and height
        """
        return self.execute_tool("get_screen_size", {})
    
    def get_mouse_position(self) -> Dict[str, Any]:
        """Get the current mouse position.
        
        Returns:
            Mouse X and Y coordinates
        """
        return self.execute_tool("get_mouse_position", {})


# Singleton instance
_desktop_client_instance: Optional[DesktopControlClient] = None


def get_desktop_client() -> DesktopControlClient:
    """Get the singleton instance of the desktop control client.
    
    Returns:
        DesktopControlClient instance
    """
    global _desktop_client_instance
    if _desktop_client_instance is None:
        _desktop_client_instance = DesktopControlClient()
    return _desktop_client_instance
