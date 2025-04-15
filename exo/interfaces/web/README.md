# exo Web Interface

This is the web interface for the exo multi-agent system. It provides a browser-based interface for interacting with the exo system.

## Features

- Modern, responsive web interface
- Real-time communication with the exo system
- Animated dot UI for visual feedback
- Markdown rendering for structured responses
- Code syntax highlighting

## Development

### Prerequisites

- Node.js 16+
- npm or yarn
- Next.js

### Installation

```bash
# Install dependencies
npm install
```

### Running

```bash
# Run in development mode
npm run dev

# Build for production
npm run build

# Run in production mode
npm start
```

## Architecture

The web interface is built with:

- **Next.js**: React framework for server-rendered applications
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library for React
- **WebSockets**: For real-time communication with the API server

## Components

- **AnimatedDot.js**: Animated dot component for visual feedback
- **Chat.js**: Main chat interface component
- **pages/index.js**: Main page component
- **pages/_app.js**: Next.js app component
- **styles/globals.css**: Global styles

## Communication

The web interface communicates with the exo system through:

1. **WebSocket**: For real-time communication with the API server
2. **REST API**: For non-real-time operations

## Customization

You can customize the web interface by:

- Modifying the Tailwind CSS configuration in `tailwind.config.js`
- Updating the global styles in `styles/globals.css`
- Modifying the components in the `components` directory
