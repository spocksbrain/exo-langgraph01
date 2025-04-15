Introduction
============

What is exo?
-----------

exo is a multi-agent system that provides a hierarchical arrangement of specialized AI agents working in concert to handle complex tasks across multiple domains. It is designed to be a flexible, extensible, and powerful system for building AI applications.

Key Features
-----------

- **Hierarchical Agent Architecture**: A structured system of specialized agents working together to solve complex problems.
- **Task Decomposition and Delegation**: Break down complex tasks into manageable subtasks and delegate them to appropriate agents.
- **Knowledge System**: Dual-memory architecture with a knowledge graph for long-term memory and a vector database for short-term memory.
- **Multiple Interfaces**: CLI, Web, and Electron desktop app interfaces for interacting with the system.
- **MCP Server**: Model Context Protocol server for desktop control and other capabilities.
- **Extensible Design**: Easy to add new domain agents, tools, and capabilities.

System Architecture
------------------

The exo system is built around a hierarchical agent architecture:

1. **Primary Interface Agent (PIA)**: The user-facing component that handles all direct interactions with the user.
2. **Command & Control Agent (CNC)**: Orchestrates complex multi-domain tasks by breaking them down and delegating to domain agents.
3. **Domain Agents**: Specialized for specific functions, providing domain expertise and executing domain-specific tasks.

This architecture allows for efficient task handling, with each agent focusing on its specific role:

- The PIA focuses on understanding user requests and generating appropriate responses.
- The CNC focuses on task decomposition, delegation, and coordination.
- Domain agents focus on executing specific tasks within their domains of expertise.

Knowledge System
---------------

The exo knowledge system provides a dual-memory architecture:

- **Knowledge Graph**: Long-term memory for storing structured information about entities, relationships, and concepts.
- **Vector Database**: Short-term memory for storing and retrieving unstructured information based on semantic similarity.

This dual-memory approach allows the system to maintain both structured knowledge (like user preferences, task history, and domain-specific information) and unstructured knowledge (like conversation history and document content).

Interfaces
---------

exo provides multiple interfaces for interacting with the system:

- **CLI**: Command-line interface for quick access and scripting.
- **Web**: Browser-based interface for easy access from any device.
- **Electron**: Desktop application for a native experience with additional capabilities.

These interfaces provide different ways to interact with the system, depending on the user's needs and preferences.

MCP Server
---------

The Model Context Protocol (MCP) server provides additional capabilities to the exo system, such as:

- **Desktop Control**: Control the user's desktop, including mouse and keyboard input.
- **File System Access**: Access the user's file system for reading and writing files.
- **Application Control**: Launch and control applications on the user's system.
- **System Information**: Access information about the user's system, such as hardware, operating system, and installed applications.

These capabilities allow the exo system to interact with the user's environment in a more powerful way.

Use Cases
--------

exo can be used for a wide range of applications, including:

- **Personal Assistant**: Help users with everyday tasks, such as scheduling, reminders, and information retrieval.
- **Research Assistant**: Help researchers with literature review, data analysis, and experiment design.
- **Software Development**: Help developers with coding, debugging, and documentation.
- **Content Creation**: Help content creators with writing, editing, and publishing.
- **Education**: Help students with learning, homework, and research.
- **Business**: Help businesses with customer service, data analysis, and decision-making.

Next Steps
---------

- :doc:`installation`: Install the exo system.
- :doc:`quickstart`: Get started with the exo system.
- :doc:`architecture`: Learn more about the exo system architecture.
