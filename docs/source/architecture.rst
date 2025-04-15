Architecture
============

This guide provides an overview of the exo multi-agent system architecture.

System Overview
-------------

The exo system is built around a hierarchical agent architecture, with a knowledge system for memory and multiple interfaces for interaction.

.. code-block:: text

    +---------------------+
    |       User          |
    +---------------------+
              |
              v
    +---------------------+
    |     Interfaces      |
    | (CLI, Web, Electron)|
    +---------------------+
              |
              v
    +---------------------+
    |         API         |
    +---------------------+
              |
              v
    +---------------------+
    |    Primary Interface|
    |      Agent (PIA)    |
    +---------------------+
              |
              v
    +---------------------+
    |  Command & Control  |
    |    Agent (CNC)      |
    +---------------------+
              |
              v
    +---------------------+
    |    Domain Agents    |
    +---------------------+
              |
              v
    +---------------------+
    |   Knowledge System  |
    | (Graph + Vector DB) |
    +---------------------+
              |
              v
    +---------------------+
    |      MCP Server     |
    +---------------------+

Components
---------

The exo system consists of the following components:

Interfaces
~~~~~~~~~

The interfaces provide the user-facing components of the system:

- **CLI**: Command-line interface for quick access and scripting.
- **Web**: Browser-based interface for easy access from any device.
- **Electron**: Desktop application for a native experience with additional capabilities.

API
~~~

The API provides a RESTful interface for interacting with the exo system. It handles:

- User input processing
- Response generation
- System status monitoring
- WebSocket connections for real-time communication

Primary Interface Agent (PIA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The PIA is the user-facing component that handles all direct interactions with the user. It is responsible for:

- Understanding user requests
- Generating appropriate responses
- Delegating complex tasks to the Command & Control Agent
- Maintaining conversation context
- Providing a consistent user experience

Command & Control Agent (CNC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The CNC is responsible for orchestrating complex multi-domain tasks. It:

- Breaks down complex tasks into subtasks
- Assigns subtasks to appropriate domain agents
- Monitors task progress
- Aggregates results from domain agents
- Reports back to the PIA

Domain Agents
~~~~~~~~~~~

Domain Agents are specialized for specific functions. They:

- Execute domain-specific tasks
- Provide domain expertise
- Report results back to the CNC
- Maintain domain-specific knowledge

Knowledge System
~~~~~~~~~~~~~~

The Knowledge System provides a dual-memory architecture:

- **Knowledge Graph**: Long-term memory for storing structured information about entities, relationships, and concepts.
- **Vector Database**: Short-term memory for storing and retrieving unstructured information based on semantic similarity.

MCP Server
~~~~~~~~~

The Model Context Protocol (MCP) server provides additional capabilities to the exo system, such as:

- **Desktop Control**: Control the user's desktop, including mouse and keyboard input.
- **File System Access**: Access the user's file system for reading and writing files.
- **Application Control**: Launch and control applications on the user's system.
- **System Information**: Access information about the user's system, such as hardware, operating system, and installed applications.

Data Flow
--------

The data flow in the exo system follows this pattern:

1. The user interacts with the system through one of the interfaces.
2. The interface sends the user input to the API.
3. The API forwards the input to the PIA.
4. The PIA processes the input and either:
   a. Generates a response directly, or
   b. Delegates the task to the CNC.
5. If delegated to the CNC, it:
   a. Breaks down the task into subtasks.
   b. Assigns subtasks to appropriate domain agents.
   c. Monitors task progress.
   d. Aggregates results from domain agents.
   e. Reports back to the PIA.
6. The PIA generates a response based on the results.
7. The API sends the response back to the interface.
8. The interface displays the response to the user.

Throughout this process, the Knowledge System is used to:

- Store and retrieve conversation history.
- Store and retrieve user preferences.
- Store and retrieve domain-specific knowledge.
- Store and retrieve task history.

The MCP Server is used to:

- Control the user's desktop.
- Access the user's file system.
- Launch and control applications.
- Access system information.

Code Structure
------------

The exo codebase is organized as follows:

.. code-block:: text

    exo/
    ├── __init__.py
    ├── __main__.py
    ├── config.py
    ├── core/
    │   ├── __init__.py
    │   ├── agent.py
    │   ├── pia.py
    │   ├── cnc.py
    │   ├── domain_agents.py
    │   └── system.py
    ├── api/
    │   ├── __init__.py
    │   ├── app.py
    │   ├── routes.py
    │   └── websocket.py
    ├── knowledge/
    │   ├── __init__.py
    │   ├── init.py
    │   └── system.py
    ├── mcp/
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── client.py
    │   └── server.py
    └── interfaces/
        ├── __init__.py
        ├── cli/
        │   ├── __init__.py
        │   ├── __main__.py
        │   └── main.py
        ├── web/
        │   ├── __init__.py
        │   ├── components/
        │   ├── pages/
        │   └── styles/
        └── electron/
            ├── __init__.py
            ├── __main__.py
            ├── main.js
            ├── preload.js
            └── index.html

Design Patterns
-------------

The exo system uses several design patterns:

- **Singleton**: The Knowledge System and MCP Server are implemented as singletons to ensure only one instance exists.
- **Factory**: The Domain Agents are created using a factory pattern to allow for dynamic creation of agents.
- **Observer**: The CNC uses an observer pattern to monitor task progress.
- **Strategy**: The PIA uses a strategy pattern to determine how to handle user input.
- **Adapter**: The interfaces use an adapter pattern to convert between different data formats.
- **Facade**: The API provides a facade for the underlying system.
- **Command**: The MCP Server uses a command pattern to execute desktop control actions.
- **Mediator**: The CNC acts as a mediator between the PIA and Domain Agents.

Next Steps
---------

Now that you understand the exo system architecture, you can:

- :doc:`core`: Learn more about the core system.
- :doc:`api`: Learn more about the API layer.
- :doc:`knowledge`: Learn more about the knowledge system.
- :doc:`mcp`: Learn more about the MCP server.
- :doc:`interfaces`: Learn more about the interfaces.
- :doc:`development`: Learn more about developing with exo.
