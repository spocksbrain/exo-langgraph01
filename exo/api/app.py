"""
FastAPI application for the exo multi-agent system.

This module provides the main FastAPI application that serves as the API layer
for the exo system, allowing various interfaces to interact with the core system.
"""
import logging
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from exo.config import API_HOST, API_PORT, API_DEBUG
from exo.core.system import get_system, ExoSystem


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title="exo API",
    description="API for the exo multi-agent system",
    version="0.1.0",
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get the exo system
def get_exo_system() -> ExoSystem:
    """Get the exo system instance.
    
    Returns:
        ExoSystem instance
    """
    return get_system()


# Import routes
from exo.api.routes import router as api_router
from exo.api.websocket import router as ws_router

# Include routers
app.include_router(api_router, prefix="/api")
app.include_router(ws_router)


@app.get("/")
async def root():
    """Root endpoint.
    
    Returns:
        Basic information about the API
    """
    return {
        "name": "exo API",
        "version": "0.1.0",
        "description": "API for the exo multi-agent system",
    }


def start_api_server():
    """Start the API server."""
    import uvicorn
    
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(
        "exo.api.app:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_DEBUG,
    )


if __name__ == "__main__":
    start_api_server()
