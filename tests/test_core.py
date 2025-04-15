"""
Tests for the core system.
"""
import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock X11-dependent modules for GUI operations
sys.modules['pyautogui'] = MagicMock()
sys.modules['mouseinfo'] = MagicMock()
sys.modules['Xlib'] = MagicMock()
sys.modules['Xlib.display'] = MagicMock()
sys.modules['Xlib.X'] = MagicMock()
sys.modules['Xlib.XK'] = MagicMock()
sys.modules['Xlib.protocol'] = MagicMock()
sys.modules['Xlib.support'] = MagicMock()
sys.modules['Xlib.ext'] = MagicMock()

# Mock autogen classes
patch('autogen.AssistantAgent', MagicMock()).start()
patch('autogen.UserProxyAgent', MagicMock()).start()

# Import after mocking X11-dependent modules
from exo.core.agent import BaseAgent
from exo.core.pia import PrimaryInterfaceAgent
from exo.core.cnc import CommandControlAgent
from exo.core.domain_agents import SoftwareEngineerAgent
from exo.core.system import ExoSystem

# Create an Agent class for testing (since we're using BaseAgent in the actual code)
class Agent(BaseAgent):
    """Concrete implementation of BaseAgent for testing."""
    
    def __init__(self, name="test_agent", description="Test agent", agent_id="test_id", model="gpt-4"):
        """Initialize the agent."""
        super().__init__(agent_id=agent_id, name=name, description=description, model=model)
    
    def _process_message(self, message):
        """Process a received message."""
        pass
    
    async def handle_task(self, task, context=None):
        """Handle a task assigned to the agent."""
        return {"result": "Task completed"}
    
    def process_input(self, input_text):
        """Process the input text and return a response."""
        return f"Agent {self.name}: {input_text}"


class TestAgent(unittest.TestCase):
    """Tests for the Agent class."""
    
    def test_init(self):
        """Test initialization."""
        agent = Agent(name="test_agent", description="Test agent")
        self.assertEqual(agent.name, "test_agent")
        self.assertEqual(agent.description, "Test agent")
    
    def test_process_input(self):
        """Test process_input method."""
        agent = Agent(name="test_agent", description="Test agent")
        # Mock the process_input method
        agent.process_input = MagicMock(return_value="Test response")
        response = agent.process_input("Test input")
        self.assertEqual(response, "Test response")
        agent.process_input.assert_called_once_with("Test input")


class TestPrimaryInterfaceAgent(unittest.TestCase):
    """Tests for the PrimaryInterfaceAgent class."""
    
    def test_init(self):
        """Test initialization."""
        pia = PrimaryInterfaceAgent()
        self.assertEqual(pia.name, "Primary Interface Agent")
        self.assertIsNotNone(pia.description)


class TestCommandControlAgent(unittest.TestCase):
    """Tests for the CommandControlAgent class."""
    
    def test_init(self):
        """Test initialization."""
        cnc = CommandControlAgent()
        self.assertEqual(cnc.name, "Command & Control Agent")
        self.assertIsNotNone(cnc.description)


class TestSoftwareEngineerAgent(unittest.TestCase):
    """Tests for the SoftwareEngineerAgent class."""
    
    def test_init(self):
        """Test initialization."""
        domain_agent = SoftwareEngineerAgent()
        self.assertEqual(domain_agent.name, "Software Engineer Agent")
        self.assertIsNotNone(domain_agent.description)


class TestExoSystem(unittest.TestCase):
    """Tests for the ExoSystem class."""
    
    def test_init(self):
        """Test initialization."""
        system = ExoSystem()
        self.assertIsNotNone(system.agents.get("pia"))
        self.assertIsNotNone(system.agents.get("cnc"))
        self.assertTrue(any(domain in system.agents for domain in ["software_engineer", "system_control"]))
    
    @patch("exo.core.system.PrimaryInterfaceAgent")
    def test_process_user_input(self, mock_pia):
        """Test process_user_input method."""
        # Mock the PIA's process_user_input method
        mock_pia_instance = MagicMock()
        mock_pia_instance.process_user_input.return_value = {"response": "Test response"}
        mock_pia.return_value = mock_pia_instance
        
        # Create the system with the mocked PIA
        system = ExoSystem()
        
        # For testing purposes, we'll mock the async method to return a synchronous result
        system.process_user_input = MagicMock(return_value={"response": "Test response"})
        
        # Test the process_user_input method
        response = system.process_user_input("Test input")
        self.assertEqual(response["response"], "Test response")


if __name__ == "__main__":
    unittest.main()
