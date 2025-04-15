"""
Tests for the MCP server.
"""
import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock pyautogui and other X11-dependent modules before importing server
sys.modules['pyautogui'] = MagicMock()
sys.modules['mouseinfo'] = MagicMock()
sys.modules['Xlib'] = MagicMock()
sys.modules['Xlib.display'] = MagicMock()
sys.modules['Xlib.X'] = MagicMock()
sys.modules['Xlib.XK'] = MagicMock()
sys.modules['Xlib.protocol'] = MagicMock()
sys.modules['Xlib.support'] = MagicMock()
sys.modules['Xlib.ext'] = MagicMock()

from fastapi.testclient import TestClient

from exo.mcp.server import app, register_tool, register_resource
from exo.mcp.client import MCPClient, DesktopControlClient


class TestMCPServer(unittest.TestCase):
    """Tests for the MCP server."""
    
    def setUp(self):
        """Set up the test client."""
        self.client = TestClient(app)
    
    def test_root(self):
        """Test the root endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "exo MCP Server")
        self.assertIn("version", data)
        self.assertIn("description", data)
    
    def test_get_tools(self):
        """Test the get_tools endpoint."""
        response = self.client.get("/tools")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("tools", data)
        self.assertIsInstance(data["tools"], list)
    
    def test_get_resources(self):
        """Test the get_resources endpoint."""
        response = self.client.get("/resources")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("resources", data)
        self.assertIsInstance(data["resources"], list)
    
    def test_register_tool(self):
        """Test the register_tool function."""
        # Create a mock handler
        mock_handler = MagicMock(return_value={"result": "success"})
        
        # Register a tool
        register_tool(
            name="test_tool",
            description="Test tool",
            handler=mock_handler,
            schema={"type": "object", "properties": {}},
        )
        
        # Test the tool endpoint
        response = self.client.post("/tools/test_tool", json={})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["result"], "success")
        
        # Check that the handler was called
        mock_handler.assert_called_once_with()
    
    def test_register_resource(self):
        """Test the register_resource function."""
        # Create a mock handler
        mock_handler = MagicMock(return_value={"result": "success"})
        
        # Register a resource
        register_resource(
            uri="test_resource",
            description="Test resource",
            handler=mock_handler,
        )
        
        # Test the resource endpoint
        response = self.client.get("/resources/test_resource")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["result"]["result"], "success")
        
        # Check that the handler was called
        mock_handler.assert_called_once_with()


class TestMCPClient(unittest.TestCase):
    """Tests for the MCPClient class."""
    
    def setUp(self):
        """Set up the test client."""
        self.client = MCPClient("http://localhost:8001")
    
    @patch("exo.mcp.client.requests.get")
    def test_get_tools(self, mock_get):
        """Test the get_tools method."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tools": [
                {
                    "name": "test_tool",
                    "description": "Test tool",
                    "schema": {"type": "object", "properties": {}},
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Test the get_tools method
        tools = self.client.get_tools()
        
        # Check that the request was made (note: we don't use assert_called_once_with because
        # the client may make multiple requests during cache updates)
        mock_get.assert_any_call("http://localhost:8001/tools")
        
        # Check the result
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0]["name"], "test_tool")
        self.assertEqual(tools[0]["description"], "Test tool")
    
    @patch("exo.mcp.client.requests.get")
    def test_get_resources(self, mock_get):
        """Test the get_resources method."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "resources": [
                {
                    "uri": "test_resource",
                    "description": "Test resource",
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Test the get_resources method
        resources = self.client.get_resources()
        
        # Check that the request was made (note: we don't use assert_called_once_with because
        # the client may make multiple requests during cache updates)
        mock_get.assert_any_call("http://localhost:8001/resources")
        
        # Check the result
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]["uri"], "test_resource")
        self.assertEqual(resources[0]["description"], "Test resource")
    
    @patch("exo.mcp.client.requests.post")
    def test_execute_tool(self, mock_post):
        """Test the execute_tool method."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Mock the tools cache
        self.client.tools_cache = {
            "test_tool": {
                "name": "test_tool",
                "description": "Test tool",
                "schema": {"type": "object", "properties": {}},
            }
        }
        self.client.last_cache_update = 9999999999  # Far in the future
        
        # Test the execute_tool method
        result = self.client.execute_tool("test_tool", {"param": "value"})
        
        # Check that the request was made
        mock_post.assert_called_once_with(
            "http://localhost:8001/tools/test_tool",
            json={"param": "value"},
        )
        
        # Check the result
        self.assertEqual(result, {"result": "success"})
    
    @patch("exo.mcp.client.requests.get")
    def test_access_resource(self, mock_get):
        """Test the access_resource method."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Mock the resources cache
        self.client.resources_cache = {
            "test_resource": {
                "uri": "test_resource",
                "description": "Test resource",
            }
        }
        self.client.last_cache_update = 9999999999  # Far in the future
        
        # Test the access_resource method
        result = self.client.access_resource("test_resource")
        
        # Check that the request was made
        mock_get.assert_called_once_with("http://localhost:8001/resources/test_resource")
        
        # Check the result
        self.assertEqual(result, {"result": "success"})


class TestDesktopControlClient(unittest.TestCase):
    """Tests for the DesktopControlClient class."""
    
    def setUp(self):
        """Set up the test client."""
        self.client = DesktopControlClient()
    
    @patch("exo.mcp.client.MCPClient.execute_tool")
    def test_click(self, mock_execute_tool):
        """Test the click method."""
        # Mock the execute_tool method
        mock_execute_tool.return_value = {"result": {"success": True}}
        
        # Test the click method
        result = self.client.click(100, 200, "left", 1)
        
        # Check that the execute_tool method was called
        mock_execute_tool.assert_called_once_with("click_element", {
            "x": 100,
            "y": 200,
            "button": "left",
            "clicks": 1,
        })
        
        # Check the result
        self.assertEqual(result, {"result": {"success": True}})
    
    @patch("exo.mcp.client.MCPClient.execute_tool")
    def test_move_mouse(self, mock_execute_tool):
        """Test the move_mouse method."""
        # Mock the execute_tool method
        mock_execute_tool.return_value = {"result": {"success": True}}
        
        # Test the move_mouse method
        result = self.client.move_mouse(100, 200)
        
        # Check that the execute_tool method was called
        mock_execute_tool.assert_called_once_with("move_mouse", {
            "x": 100,
            "y": 200,
        })
        
        # Check the result
        self.assertEqual(result, {"result": {"success": True}})
    
    @patch("exo.mcp.client.MCPClient.execute_tool")
    def test_type_text(self, mock_execute_tool):
        """Test the type_text method."""
        # Mock the execute_tool method
        mock_execute_tool.return_value = {"result": {"success": True}}
        
        # Test the type_text method
        result = self.client.type_text("Hello, world!")
        
        # Check that the execute_tool method was called
        mock_execute_tool.assert_called_once_with("type_text", {
            "text": "Hello, world!",
        })
        
        # Check the result
        self.assertEqual(result, {"result": {"success": True}})


if __name__ == "__main__":
    unittest.main()
