"""
Tests for the API layer.
"""
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from exo.api.app import app
from exo.api.routes import router


class TestAPI(unittest.TestCase):
    """Tests for the API layer."""
    
    def setUp(self):
        """Set up the test client."""
        # Mock the get_system function to avoid the need for an OpenAI API key
        self.patcher1 = patch("exo.api.app.get_system")
        self.mock_get_system1 = self.patcher1.start()
        
        # Mock the get_system function in routes.py
        self.patcher2 = patch("exo.api.routes.get_system")
        self.mock_get_system2 = self.patcher2.start()
        
        # Mock the get_exo_system function in routes.py
        self.patcher3 = patch("exo.api.routes.get_exo_system")
        self.mock_get_exo_system = self.patcher3.start()
        
        # Create a mock system
        self.mock_system = MagicMock()
        self.mock_system.get_agent_ids.return_value = ["pia", "cnc", "software_engineer"]
        
        # Configure the mocks to return the mock system
        self.mock_get_system1.return_value = self.mock_system
        self.mock_get_system2.return_value = self.mock_system
        self.mock_get_exo_system.return_value = self.mock_system
        
        self.client = TestClient(app)
    
    def tearDown(self):
        """Clean up after tests."""
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()
    
    def test_root(self):
        """Test the root endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "exo API")
        self.assertEqual(data["version"], "0.1.0")
        self.assertEqual(data["description"], "API for the exo multi-agent system")
    
    def test_status(self):
        """Test the status endpoint."""
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "running")
        self.assertEqual(data["version"], "0.1.0")
        self.assertEqual(data["agents"], ["pia", "cnc", "software_engineer"])
    
    def test_input(self):
        """Test the input endpoint."""
        # Configure the mock system
        # Mock the async method to return a synchronous result
        async def mock_process_user_input(*args, **kwargs):
            return {"response": "Test response", "handled_by": "test"}
        
        self.mock_system.process_user_input = mock_process_user_input
        
        # Test the input endpoint
        response = self.client.post(
            "/api/input",
            json={"text": "Test input", "metadata": {"source": "test"}}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["response"], "Test response")
        self.assertEqual(data["handled_by"], "test")
    
    def test_reset(self):
        """Test the reset endpoint."""
        # Test the reset endpoint
        response = self.client.post("/api/reset")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "resetting")


if __name__ == "__main__":
    unittest.main()
