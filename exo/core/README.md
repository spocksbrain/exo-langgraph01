# exo Core System

This is the core system for the exo multi-agent system. It provides the central orchestration and agent management for the exo system.

## Features

- Hierarchical agent architecture
- Task decomposition and delegation
- Agent communication and coordination
- Knowledge system integration
- MCP server integration

## Components

### Primary Interface Agent (PIA)

The Primary Interface Agent (PIA) is the user-facing component that handles all direct interactions with the user. It is responsible for:

- Understanding user requests
- Generating appropriate responses
- Delegating complex tasks to the Command & Control Agent
- Maintaining conversation context
- Providing a consistent user experience

### Command & Control Agent (CNC)

The Command & Control Agent (CNC) is responsible for orchestrating complex multi-domain tasks. It:

- Breaks down complex tasks into subtasks
- Assigns subtasks to appropriate domain agents
- Monitors task progress
- Aggregates results from domain agents
- Reports back to the PIA

### Domain Agents

Domain Agents are specialized for specific functions. They:

- Execute domain-specific tasks
- Provide domain expertise
- Report results back to the CNC
- Maintain domain-specific knowledge

## Usage

```python
from exo.core.system import ExoSystem

# Create the exo system
system = ExoSystem()

# Process user input
response = system.process_input("Create a web scraper for news articles")

# Get the current state
state = system.get_state()

# Reset the system
system.reset()
```

## Architecture

The core system is built with:

- **LangChain**: For agent orchestration and task execution
- **Knowledge System**: For memory and context
- **MCP Server**: For desktop control and other capabilities

## Customization

You can customize the core system by:

- Adding new domain agents in `domain_agents.py`
- Modifying the PIA behavior in `pia.py`
- Updating the CNC orchestration in `cnc.py`
- Extending the base agent class in `agent.py`
- Updating the system configuration in `config.py`
