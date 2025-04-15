API Layer
=========

This guide provides information about the API layer of the exo multi-agent system.

Overview
-------

The API layer provides a RESTful interface for interacting with the exo system. It handles:

- User input processing
- Response generation
- System status monitoring
- WebSocket connections for real-time communication

Components
---------

The API layer consists of the following components:

App
~~~

The App module provides the FastAPI application for the API layer. It:

- Initializes the FastAPI application
- Configures CORS
- Includes the API routes
- Configures middleware

.. code-block:: python

    from exo.api.app import app

    # Run the app
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

Routes
~~~~~~

The Routes module provides the API routes for the API layer. It:

- Defines the API endpoints
- Handles request validation
- Processes user input
- Generates responses

.. code-block:: python

    from exo.api.routes import router

    # Add the router to the app
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)

WebSocket
~~~~~~~~

The WebSocket module provides WebSocket support for the API layer. It:

- Handles WebSocket connections
- Processes user input
- Generates responses
- Sends real-time updates

.. code-block:: python

    from exo.api.websocket import websocket_endpoint

    # Add the WebSocket endpoint to the app
    from fastapi import FastAPI
    app = FastAPI()
    app.add_websocket_route("/ws", websocket_endpoint)

API Endpoints
-----------

The API layer provides the following endpoints:

Root
~~~~

The root endpoint provides information about the API.

.. code-block:: http

    GET /

Response:

.. code-block:: json

    {
        "message": "Welcome to the exo API"
    }

Status
~~~~~~

The status endpoint provides information about the system status.

.. code-block:: http

    GET /api/status

Response:

.. code-block:: json

    {
        "status": "ok",
        "version": "0.1.0",
        "timestamp": "2025-04-15T16:32:30Z"
    }

Input
~~~~~

The input endpoint processes user input and returns a response.

.. code-block:: http

    POST /api/input

Request:

.. code-block:: json

    {
        "text": "Hello, world!",
        "metadata": {
            "source": "web"
        }
    }

Response:

.. code-block:: json

    {
        "response": "Hello! How can I help you today?",
        "metadata": {
            "timestamp": "2025-04-15T16:32:30Z"
        }
    }

Reset
~~~~~

The reset endpoint resets the system.

.. code-block:: http

    POST /api/reset

Response:

.. code-block:: json

    {
        "status": "success",
        "message": "System reset successful"
    }

WebSocket
~~~~~~~~

The WebSocket endpoint provides real-time communication with the system.

.. code-block:: http

    WebSocket /ws

Messages:

.. code-block:: json

    {
        "type": "input",
        "text": "Hello, world!",
        "metadata": {
            "source": "web"
        }
    }

Responses:

.. code-block:: json

    {
        "type": "response",
        "text": "Hello! How can I help you today?",
        "metadata": {
            "timestamp": "2025-04-15T16:32:30Z"
        }
    }

Usage
-----

To use the API layer, you can either use the FastAPI application directly or use the API endpoints.

Using the FastAPI Application
~~~~~~~~~~~~~~~~~~~~~~~~~~

The FastAPI application provides a high-level interface to the API layer:

.. code-block:: python

    from exo.api.app import app

    # Run the app
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

Using the API Endpoints
~~~~~~~~~~~~~~~~~~~

You can also use the API endpoints directly:

.. code-block:: python

    import requests

    # Get the status
    response = requests.get("http://localhost:8000/api/status")
    print(response.json())

    # Process input
    response = requests.post(
        "http://localhost:8000/api/input",
        json={"text": "Hello, world!", "metadata": {"source": "web"}}
    )
    print(response.json())

    # Reset the system
    response = requests.post("http://localhost:8000/api/reset")
    print(response.json())

Using the WebSocket
~~~~~~~~~~~~~~~~

You can also use the WebSocket endpoint:

.. code-block:: python

    import websockets
    import json
    import asyncio

    async def connect():
        async with websockets.connect("ws://localhost:8000/ws") as websocket:
            # Send input
            await websocket.send(json.dumps({
                "type": "input",
                "text": "Hello, world!",
                "metadata": {"source": "web"}
            }))

            # Receive response
            response = await websocket.recv()
            print(json.loads(response))

    asyncio.run(connect())

Customization
-----------

You can customize the API layer by:

- Adding new API endpoints
- Modifying existing API endpoints
- Adding middleware
- Configuring CORS

Adding New API Endpoints
~~~~~~~~~~~~~~~~~~~~

You can add new API endpoints by adding new routes to the router:

.. code-block:: python

    from fastapi import APIRouter
    from exo.api.routes import router

    @router.get("/api/custom")
    async def custom_endpoint():
        return {"message": "Custom endpoint"}

Modifying Existing API Endpoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can modify existing API endpoints by overriding the route handlers:

.. code-block:: python

    from fastapi import APIRouter
    from exo.api.routes import router

    @router.get("/api/status", include_in_schema=False)
    async def custom_status():
        return {"status": "custom", "version": "0.1.0", "timestamp": "2025-04-15T16:32:30Z"}

Adding Middleware
~~~~~~~~~~~~~~

You can add middleware to the FastAPI application:

.. code-block:: python

    from fastapi import FastAPI
    from exo.api.app import app

    @app.middleware("http")
    async def custom_middleware(request, call_next):
        # Custom middleware logic
        response = await call_next(request)
        return response

Configuring CORS
~~~~~~~~~~~~~

You can configure CORS for the FastAPI application:

.. code-block:: python

    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from exo.api.app import app

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

API Reference
-----------

App
~~~

.. code-block:: python

    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from exo.api.routes import router

    app = FastAPI(
        title="exo API",
        description="API for the exo multi-agent system",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

Routes
~~~~~~

.. code-block:: python

    from fastapi import APIRouter, Depends, HTTPException
    from pydantic import BaseModel
    from typing import Dict, Any, Optional
    from datetime import datetime
    from exo.core.system import ExoSystem, get_exo_system

    router = APIRouter()

    class InputRequest(BaseModel):
        text: str
        metadata: Optional[Dict[str, Any]] = None

    class InputResponse(BaseModel):
        response: str
        metadata: Optional[Dict[str, Any]] = None

    @router.get("/")
    async def root():
        return {"message": "Welcome to the exo API"}

    @router.get("/api/status")
    async def status():
        return {
            "status": "ok",
            "version": "0.1.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    @router.post("/api/input", response_model=InputResponse)
    async def input(request: InputRequest, system: ExoSystem = Depends(get_exo_system)):
        response = system.process_input(request.text)
        return {
            "response": response,
            "metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        }

    @router.post("/api/reset")
    async def reset(system: ExoSystem = Depends(get_exo_system)):
        system.reset()
        return {
            "status": "success",
            "message": "System reset successful",
        }

WebSocket
~~~~~~~~

.. code-block:: python

    from fastapi import WebSocket, WebSocketDisconnect
    from typing import Dict, Any, Optional
    from datetime import datetime
    import json
    from exo.core.system import ExoSystem, get_exo_system

    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        system = get_exo_system()
        try:
            while True:
                data = await websocket.receive_text()
                data = json.loads(data)
                if data["type"] == "input":
                    response = system.process_input(data["text"])
                    await websocket.send_text(json.dumps({
                        "type": "response",
                        "text": response,
                        "metadata": {
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                        },
                    }))
        except WebSocketDisconnect:
            pass
