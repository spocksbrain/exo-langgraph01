Core System
===========

This guide provides information about the core system of the exo multi-agent system.

Overview
-------

The core system is the central component of the exo multi-agent system. It provides the agent architecture, task orchestration, and system management.

Components
---------

The core system consists of the following components:

Agent
~~~~~

The Agent class is the base class for all agents in the system. It provides the basic functionality for agents, such as:

- Name and description
- Input processing
- Response generation
- Task execution

.. code-block:: python

    from exo.core.agent import Agent

    # Create an agent
    agent = Agent(name="test_agent", description="Test agent")

    # Process input
    response = agent.process_input("Hello, world!")

Primary Interface Agent (PIA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Primary Interface Agent (PIA) is the user-facing component that handles all direct interactions with the user. It is responsible for:

- Understanding user requests
- Generating appropriate responses
- Delegating complex tasks to the Command & Control Agent
- Maintaining conversation context
- Providing a consistent user experience

.. code-block:: python

    from exo.core.pia import PrimaryInterfaceAgent

    # Create a PIA
    pia = PrimaryInterfaceAgent()

    # Process input
    response = pia.process_input("Hello, world!")

Command & Control Agent (CNC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Command & Control Agent (CNC) is responsible for orchestrating complex multi-domain tasks. It:

- Breaks down complex tasks into subtasks
- Assigns subtasks to appropriate domain agents
- Monitors task progress
- Aggregates results from domain agents
- Reports back to the PIA

.. code-block:: python

    from exo.core.cnc import CommandAndControlAgent

    # Create a CNC
    cnc = CommandAndControlAgent()

    # Process input
    response = cnc.process_input("Create a web scraper for news articles")

Domain Agents
~~~~~~~~~~~

Domain Agents are specialized for specific functions. They:

- Execute domain-specific tasks
- Provide domain expertise
- Report results back to the CNC
- Maintain domain-specific knowledge

.. code-block:: python

    from exo.core.domain_agents import DomainAgent

    # Create a domain agent
    domain_agent = DomainAgent(name="software_engineer", description="Software engineering expert")

    # Process input
    response = domain_agent.process_input("Write a Python function to calculate Fibonacci numbers")

System
~~~~~~

The System class is the main entry point for the exo system. It:

- Initializes the agents
- Manages the system state
- Processes user input
- Generates responses

.. code-block:: python

    from exo.core.system import ExoSystem

    # Create the exo system
    system = ExoSystem()

    # Process input
    response = system.process_input("Hello, world!")

    # Get the current state
    state = system.get_state()

    # Reset the system
    system.reset()

Usage
-----

To use the core system, you can either use the ExoSystem class directly or use the individual agent classes.

Using the ExoSystem Class
~~~~~~~~~~~~~~~~~~~~~~~

The ExoSystem class provides a high-level interface to the exo system:

.. code-block:: python

    from exo.core.system import ExoSystem

    # Create the exo system
    system = ExoSystem()

    # Process input
    response = system.process_input("Hello, world!")

    # Get the current state
    state = system.get_state()

    # Reset the system
    system.reset()

Using the Agent Classes
~~~~~~~~~~~~~~~~~~~~

You can also use the individual agent classes directly:

.. code-block:: python

    from exo.core.pia import PrimaryInterfaceAgent
    from exo.core.cnc import CommandAndControlAgent
    from exo.core.domain_agents import DomainAgent

    # Create the agents
    pia = PrimaryInterfaceAgent()
    cnc = CommandAndControlAgent()
    domain_agent = DomainAgent(name="software_engineer", description="Software engineering expert")

    # Process input with the PIA
    response = pia.process_input("Hello, world!")

    # Process input with the CNC
    response = cnc.process_input("Create a web scraper for news articles")

    # Process input with a domain agent
    response = domain_agent.process_input("Write a Python function to calculate Fibonacci numbers")

Customization
-----------

You can customize the core system by:

- Creating custom domain agents
- Modifying the PIA behavior
- Updating the CNC orchestration
- Extending the base agent class

Creating Custom Domain Agents
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create custom domain agents by subclassing the DomainAgent class:

.. code-block:: python

    from exo.core.domain_agents import DomainAgent

    class SoftwareEngineerAgent(DomainAgent):
        def __init__(self):
            super().__init__(name="software_engineer", description="Software engineering expert")

        def process_input(self, input_text):
            # Custom processing logic
            return f"Software Engineer: {input_text}"

Modifying the PIA Behavior
~~~~~~~~~~~~~~~~~~~~~~~

You can modify the PIA behavior by subclassing the PrimaryInterfaceAgent class:

.. code-block:: python

    from exo.core.pia import PrimaryInterfaceAgent

    class CustomPIA(PrimaryInterfaceAgent):
        def __init__(self):
            super().__init__()

        def process_input(self, input_text):
            # Custom processing logic
            return f"Custom PIA: {input_text}"

Updating the CNC Orchestration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can update the CNC orchestration by subclassing the CommandAndControlAgent class:

.. code-block:: python

    from exo.core.cnc import CommandAndControlAgent

    class CustomCNC(CommandAndControlAgent):
        def __init__(self):
            super().__init__()

        def process_input(self, input_text):
            # Custom processing logic
            return f"Custom CNC: {input_text}"

Extending the Base Agent Class
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can extend the base agent class by subclassing the Agent class:

.. code-block:: python

    from exo.core.agent import Agent

    class CustomAgent(Agent):
        def __init__(self, name, description):
            super().__init__(name=name, description=description)

        def process_input(self, input_text):
            # Custom processing logic
            return f"Custom Agent: {input_text}"

API Reference
-----------

Agent
~~~~~

.. code-block:: python

    class Agent:
        """Base class for all agents in the system."""

        def __init__(self, name, description):
            """Initialize the agent.

            Args:
                name (str): The name of the agent.
                description (str): The description of the agent.
            """
            self.name = name
            self.description = description

        def process_input(self, input_text):
            """Process the input text and return a response.

            Args:
                input_text (str): The input text to process.

            Returns:
                str: The response text.
            """
            # Default implementation
            return f"Agent {self.name}: {input_text}"

PrimaryInterfaceAgent
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class PrimaryInterfaceAgent(Agent):
        """Primary Interface Agent (PIA) for the exo system."""

        def __init__(self):
            """Initialize the PIA."""
            super().__init__(name="primary_interface_agent", description="Primary Interface Agent (PIA) for the exo system")

        def process_input(self, input_text):
            """Process the input text and return a response.

            Args:
                input_text (str): The input text to process.

            Returns:
                str: The response text.
            """
            # PIA-specific implementation
            return f"PIA: {input_text}"

CommandAndControlAgent
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class CommandAndControlAgent(Agent):
        """Command & Control Agent (CNC) for the exo system."""

        def __init__(self):
            """Initialize the CNC."""
            super().__init__(name="command_and_control_agent", description="Command & Control Agent (CNC) for the exo system")

        def process_input(self, input_text):
            """Process the input text and return a response.

            Args:
                input_text (str): The input text to process.

            Returns:
                str: The response text.
            """
            # CNC-specific implementation
            return f"CNC: {input_text}"

DomainAgent
~~~~~~~~~

.. code-block:: python

    class DomainAgent(Agent):
        """Domain Agent for the exo system."""

        def __init__(self, name, description):
            """Initialize the domain agent.

            Args:
                name (str): The name of the domain agent.
                description (str): The description of the domain agent.
            """
            super().__init__(name=name, description=description)

        def process_input(self, input_text):
            """Process the input text and return a response.

            Args:
                input_text (str): The input text to process.

            Returns:
                str: The response text.
            """
            # Domain agent-specific implementation
            return f"Domain Agent {self.name}: {input_text}"

ExoSystem
~~~~~~~

.. code-block:: python

    class ExoSystem:
        """Main system class for the exo system."""

        def __init__(self):
            """Initialize the exo system."""
            self.pia = PrimaryInterfaceAgent()
            self.cnc = CommandAndControlAgent()
            self.domain_agents = {}

        def process_input(self, input_text):
            """Process the input text and return a response.

            Args:
                input_text (str): The input text to process.

            Returns:
                str: The response text.
            """
            # System-specific implementation
            return self.pia.process_input(input_text)

        def get_state(self):
            """Get the current state of the system.

            Returns:
                dict: The current state of the system.
            """
            return {
                "pia": self.pia,
                "cnc": self.cnc,
                "domain_agents": self.domain_agents,
            }

        def reset(self):
            """Reset the system."""
            self.pia = PrimaryInterfaceAgent()
            self.cnc = CommandAndControlAgent()
            self.domain_agents = {}
