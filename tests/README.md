# exo Tests

This directory contains tests for the exo multi-agent system.

## Test Files

- **test_core.py**: Tests for the core system
- **test_api.py**: Tests for the API layer
- **test_knowledge.py**: Tests for the knowledge system
- **test_mcp.py**: Tests for the MCP server

## Running Tests

You can run the tests using pytest:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=exo

# Run a specific test file
pytest tests/test_core.py

# Run a specific test class
pytest tests/test_core.py::TestAgent

# Run a specific test method
pytest tests/test_core.py::TestAgent::test_init
```

## Writing Tests

When writing tests, follow these guidelines:

1. Use unittest for test classes and methods
2. Use descriptive names for test classes and methods
3. Use docstrings to describe what each test is testing
4. Use assertions to verify expected behavior
5. Use mocks to isolate the code being tested
6. Use patches to replace external dependencies

Example:

```python
import unittest
from unittest.mock import MagicMock, patch

from exo.core.agent import Agent


class TestAgent(unittest.TestCase):
    """Tests for the Agent class."""
    
    def test_init(self):
        """Test initialization."""
        agent = Agent(name="test_agent", description="Test agent")
        self.assertEqual(agent.name, "test_agent")
        self.assertEqual(agent.description, "Test agent")
    
    @patch("exo.core.agent.some_external_function")
    def test_with_mock(self, mock_function):
        """Test with a mock."""
        # Set up the mock
        mock_function.return_value = "mocked_result"
        
        # Create the agent
        agent = Agent(name="test_agent", description="Test agent")
        
        # Call the method that uses the external function
        result = agent.some_method()
        
        # Check that the external function was called
        mock_function.assert_called_once_with()
        
        # Check the result
        self.assertEqual(result, "mocked_result")
```

## Test Coverage

The CI/CD pipeline runs tests with coverage and fails if the coverage is below a certain threshold. You can check the coverage locally by running:

```bash
pytest --cov=exo --cov-report=html
```

This will generate an HTML coverage report in the `htmlcov` directory. Open `htmlcov/index.html` in a browser to view the report.
