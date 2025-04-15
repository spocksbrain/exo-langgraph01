# exo Multi-Agent System

A proof-of-concept implementation of the "exo" multi-agent AI system, featuring a hierarchical arrangement of specialized AI agents working in concert to handle complex tasks across multiple domains.

## Architecture

The system consists of:

- **Primary Interface Agent (PIA)**: User-facing component handling all direct interactions
- **Command & Control Agent (CNC)**: Orchestrates complex multi-domain tasks
- **Domain Agents**: Specialized for specific functions (Software Engineering, System Control, etc.)
- **Knowledge System**: Dual-memory architecture with knowledge graph and vector database
- **Multiple Interfaces**: Electron desktop app, CLI, and web interface

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+ (for Electron and Web interfaces)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Usage

### CLI Interface

```bash
python -m exo.interfaces.cli
```

### Web Interface

```bash
cd exo/interfaces/web
npm install
npm run dev
```

### Electron Desktop App

```bash
cd exo/interfaces/electron
npm install
npm start
```

## Development

The project follows a modular architecture:

- `core/`: Core agent system and orchestration
- `api/`: FastAPI-based API layer
- `interfaces/`: Multiple user interfaces (CLI, Web, Electron)
- `knowledge/`: Knowledge graph and vector database integration
- `mcp/`: Model Context Protocol server implementation

## License

MIT
