# exo Electron Desktop App

This is the Electron desktop application for the exo multi-agent system. It provides a native desktop interface for interacting with the exo system.

## Features

- Native desktop application for Windows, macOS, and Linux
- Integrated API and MCP servers
- Animated dot UI for visual feedback
- Settings for configuring the Python environment
- Real-time communication with the exo system

## Development

### Prerequisites

- Node.js 16+
- npm or yarn
- Electron

### Installation

```bash
# Install dependencies
npm install
```

### Running

```bash
# Run in development mode
npm run dev

# Run in production mode
npm start
```

### Building

```bash
# Build for current platform
npm run build

# Build for specific platforms
npm run build -- --win
npm run build -- --mac
npm run build -- --linux
```

## Architecture

The Electron app consists of the following components:

- **main.js**: Main Electron process that manages the application lifecycle and spawns the API and MCP servers
- **preload.js**: Preload script that exposes a secure API to the renderer process
- **index.html**: Main UI for the application
- **assets/**: Icons and other assets

## Communication

The Electron app communicates with the exo system through:

1. **WebSocket**: For real-time communication with the API server
2. **IPC**: For communication between the renderer process and the main process

## Configuration

The app stores configuration in the user's application data directory using electron-store. This includes:

- Python executable path
- API server configuration
- MCP server configuration
