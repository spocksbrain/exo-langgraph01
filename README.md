# exo Multi-Agent System

A proof-of-concept implementation of the "exo" multi-agent AI system, featuring a hierarchical arrangement of specialized AI agents working in concert to handle complex tasks across multiple domains.

## Overview

The exo system consists of:

- **Primary Interface Agent (PIA)**: User-facing component handling all direct interactions
- **Command & Control Agent (CNC)**: Orchestrates complex multi-domain tasks
- **Domain Agents**: Specialized for specific functions (Software Engineering, System Control, etc.)
- **Knowledge System**: Dual-memory architecture with knowledge graph and vector database
- **Multiple Interfaces**: CLI, Web, and Electron desktop app

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│       ┌───────────────────────────────────────────┐         │
│       │   Primary Interface & Management Agent    │         │
│       │               (PIA)                       │         │
│       └─────────────────┬─────────────────────────┘         │
│                         │                                   │
│                         ▼                                   │
│       ┌───────────────────────────────────────────┐         │
│       │     Command & Control Agent (CNC)         │         │
│       └──────┬─────────────────┬──────────────┬───┘         │
│              │                 │              │             │
│              ▼                 ▼              ▼             │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐   │
│  │ Domain Agent 1 │ │ Domain Agent 2 │ │ Domain Agent n │   │
│  └────────────────┘ └────────────────┘ └────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 Knowledge System                     │    │
│  │  ┌─────────────────────┐  ┌─────────────────────┐   │    │
│  │  │   Knowledge Graph   │  │   Vector Database   │   │    │
│  │  │  (Long-term Memory) │  │ (Short-term Memory) │   │    │
│  │  └─────────────────────┘  └─────────────────────┘   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+ (for Web and Electron interfaces)
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/example/exo.git
cd exo
```

2. Run the setup script:
```bash
# On Linux/macOS
./exo/setup.sh

# On Windows
.\exo\setup.bat
```

3. Edit the `.env` file with your API keys and configuration.

### Running the System

#### CLI Interface

```bash
python -m exo cli
```

#### API Server

```bash
python -m exo api
```

#### Web Interface

```bash
python -m exo web
```

#### MCP Server

```bash
python -m exo mcp
```

#### Electron Desktop App

```bash
python -m exo electron
```

#### All Interfaces

```bash
python -m exo all
```

## Project Structure

- `exo/core/`: Core agent system and orchestration
- `exo/api/`: FastAPI-based API layer
- `exo/interfaces/`: Multiple user interfaces (CLI, Web, Electron)
- `exo/knowledge/`: Knowledge graph and vector database integration
- `exo/mcp/`: Model Context Protocol server implementation

## Features

- **Multi-Agent Architecture**: Hierarchical arrangement of specialized agents
- **Task Decomposition**: Breaking complex tasks into subtasks
- **Knowledge Persistence**: Dual-memory system for context retention
- **Multiple Interfaces**: CLI, Web, and Electron desktop app
- **Animated Dot UI**: Visual representation of system state

## License

MIT
