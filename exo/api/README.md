# exo API Layer

This is the API layer for the exo multi-agent system. It provides a RESTful API and WebSocket interface for interacting with the exo system.

## Features

- RESTful API for interacting with the exo system
- WebSocket interface for real-time communication
- Automatic OpenAPI documentation
- CORS support for cross-origin requests
- Background task processing

## Usage

```bash
# Run the API server
python -m exo.api

# Run with debug logging
python -m exo.api --debug
```

## API Endpoints

### REST API

- `GET /api/status`: Get system status
- `POST /api/input`: Process user input
- `POST /api/desktop-context`: Update desktop context
- `POST /api/reset`: Reset the system

### WebSocket

- `WebSocket /ws`: WebSocket endpoint for real-time communication

## Architecture

The API layer is built with:

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server
- **WebSockets**: For real-time communication

## Components

- **app.py**: Main FastAPI application
- **routes.py**: API routes
- **websocket.py**: WebSocket handlers

## Communication

The API layer communicates with:

1. **Core System**: For processing user input and managing the system
2. **Clients**: Web interface, Electron app, and other clients

## Documentation

When the API server is running, you can access the OpenAPI documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Customization

You can customize the API layer by:

- Adding new endpoints to `routes.py`
- Modifying the WebSocket handlers in `websocket.py`
- Updating the API configuration in `config.py`
