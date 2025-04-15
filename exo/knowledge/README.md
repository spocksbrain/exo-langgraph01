# exo Knowledge System

This is the knowledge system for the exo multi-agent system. It provides a dual-memory architecture with a knowledge graph for long-term memory and a vector database for short-term memory.

## Features

- Dual-memory architecture
- Knowledge graph for long-term memory
- Vector database for short-term memory
- Conversation history storage
- Task tracking
- Entity relationship modeling

## Usage

```bash
# Initialize the knowledge system
python -m exo.knowledge.init

# Use the knowledge system in your code
from exo.knowledge.system import get_knowledge_system

# Get the knowledge system
knowledge_system = get_knowledge_system()

# Add a conversation to the vector store
conversation_id = knowledge_system.add_conversation("Hello, how can I help you?")

# Search for similar conversations
results = knowledge_system.search_conversations("help")

# Create a user task
task = knowledge_system.create_user_task("user123", "Create a web scraper")

# Assign a task to an agent
knowledge_system.assign_task_to_agent("task123", "software_engineer")

# Complete a task
knowledge_system.complete_task("task123", "Task completed successfully")
```

## Architecture

The knowledge system is built with:

- **Neo4j**: Graph database for knowledge graph
- **ChromaDB**: Vector database for vector storage
- **Pydantic**: Data validation and settings management

## Components

- **system.py**: Main knowledge system implementation
- **init.py**: Initialization script for the knowledge system

## Knowledge Graph

The knowledge graph stores:

- **Users**: User information and preferences
- **Agents**: Agent information and capabilities
- **Tasks**: Task information and status
- **Entities**: Domain-specific entities and relationships

## Vector Database

The vector database stores:

- **Conversations**: Conversation history with metadata
- **Embeddings**: Vector embeddings for semantic search

## Customization

You can customize the knowledge system by:

- Adding new node types to the knowledge graph
- Adding new relationship types to the knowledge graph
- Adding new collections to the vector database
- Updating the knowledge system configuration in `config.py`
