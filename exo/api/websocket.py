"""
WebSocket handlers for the exo multi-agent system.

This module provides WebSocket endpoints for real-time communication with the exo system.
"""
import asyncio
import json
import logging
from typing import Dict, Any, List, Set, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel, Field

from exo.core.system import ExoSystem, get_system
from exo.core.agent import Message


# Configure logging
logger = logging.getLogger(__name__)


# Create router
router = APIRouter(tags=["websocket"])


# WebSocket message models
class WSMessage(BaseModel):
    """Base WebSocket message model."""
    
    type: str
    data: Dict[str, Any] = Field(default_factory=dict)


class WSUserInputMessage(WSMessage):
    """WebSocket message for user input."""
    
    type: str = "user_input"
    data: Dict[str, Any]


class WSResponseMessage(WSMessage):
    """WebSocket message for system response."""
    
    type: str = "response"
    data: Dict[str, Any]


class WSStatusMessage(WSMessage):
    """WebSocket message for system status updates."""
    
    type: str = "status"
    data: Dict[str, Any]


class WSErrorMessage(WSMessage):
    """WebSocket message for errors."""
    
    type: str = "error"
    data: Dict[str, Any]


# WebSocket connection manager
class ConnectionManager:
    """Manager for WebSocket connections."""
    
    def __init__(self):
        """Initialize the connection manager."""
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Connect a WebSocket client.
        
        Args:
            websocket: WebSocket connection
        """
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket client connected, total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client.
        
        Args:
            websocket: WebSocket connection
        """
        self.active_connections.remove(websocket)
        
        # Clean up last_messages for this websocket
        websocket_id = id(websocket)
        keys_to_remove = [key for key in last_messages if key.startswith(f"{websocket_id}:")]
        for key in keys_to_remove:
            del last_messages[key]
        
        logger.info(f"WebSocket client disconnected, total connections: {len(self.active_connections)}")
    
    async def send_message(self, websocket: WebSocket, message: WSMessage):
        """Send a message to a specific client.
        
        Args:
            websocket: WebSocket connection
            message: Message to send
        """
        await websocket.send_text(message.json())
    
    async def broadcast(self, message: WSMessage):
        """Broadcast a message to all connected clients.
        
        Args:
            message: Message to broadcast
        """
        for connection in self.active_connections:
            try:
                await connection.send_text(message.json())
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")


# Create connection manager
manager = ConnectionManager()


# Track the last message sent to each client to prevent duplicates
last_messages = {}

# Message handler for agent messages
async def handle_agent_message(websocket: WebSocket, message: Message):
    """Handle a message from an agent.
    
    Args:
        websocket: WebSocket connection
        message: Agent message
    """
    # Create a unique key for this websocket and message combination
    key = f"{id(websocket)}:{message.from_agent}:{message.to_agent}"
    
    # Check if this is a duplicate message
    if key in last_messages and last_messages[key] == message.content:
        logger.debug(f"Skipping duplicate message: {message.content[:50]}...")
        return
    
    # Store this message as the last one for this key
    last_messages[key] = message.content
    
    # Create a WebSocket message
    ws_message = WSResponseMessage(
        data={
            "from_agent": message.from_agent,
            "to_agent": message.to_agent,
            "content": message.content,
            "metadata": message.metadata,
        }
    )
    
    # Send the message to the client
    await manager.send_message(websocket, ws_message)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    system: ExoSystem = Depends(get_system),
):
    """WebSocket endpoint for real-time communication.
    
    Args:
        websocket: WebSocket connection
        system: ExoSystem instance
    """
    await manager.connect(websocket)
    
    # Register callbacks for agent messages
    for agent_id in system.get_agent_ids():
        system.register_callback(
            agent_id,
            lambda message, ws=websocket: asyncio.create_task(handle_agent_message(ws, message)),
        )
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                # Parse the message
                message_data = json.loads(data)
                message_type = message_data.get("type", "")
                
                if message_type == "user_input":
                    # Process user input
                    input_text = message_data.get("data", {}).get("text", "")
                    metadata = message_data.get("data", {}).get("metadata", {})
                    
                    # Process the input asynchronously
                    asyncio.create_task(
                        process_user_input(websocket, system, input_text, metadata)
                    )
                elif message_type == "desktop_context":
                    # Update desktop context
                    context_data = message_data.get("data", {}).get("context_data", {})
                    system.capture_desktop_context(context_data)
                    
                    # Send acknowledgement
                    await manager.send_message(
                        websocket,
                        WSStatusMessage(
                            data={"status": "desktop_context_updated"}
                        )
                    )
                else:
                    # Unknown message type
                    await manager.send_message(
                        websocket,
                        WSErrorMessage(
                            data={"error": f"Unknown message type: {message_type}"}
                        )
                    )
            except json.JSONDecodeError:
                # Invalid JSON
                await manager.send_message(
                    websocket,
                    WSErrorMessage(
                        data={"error": "Invalid JSON"}
                    )
                )
            except Exception as e:
                # Other error
                logger.exception("Error processing WebSocket message")
                await manager.send_message(
                    websocket,
                    WSErrorMessage(
                        data={"error": str(e)}
                    )
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def process_user_input(
    websocket: WebSocket,
    system: ExoSystem,
    input_text: str,
    metadata: Optional[Dict[str, Any]] = None,
):
    """Process user input and send the response.
    
    Args:
        websocket: WebSocket connection
        system: ExoSystem instance
        input_text: User input text
        metadata: Additional metadata
    """
    try:
        # Process the input
        result = await system.process_user_input(input_text, metadata)
        
        # Check for errors
        if "error" in result:
            await manager.send_message(
                websocket,
                WSErrorMessage(
                    data={"error": result["error"]}
                )
            )
            return
        
        # Send the response
        await manager.send_message(
            websocket,
            WSResponseMessage(
                data={
                    "response": result.get("response", ""),
                    "handled_by": result.get("handled_by", "unknown"),
                }
            )
        )
    except Exception as e:
        logger.exception("Error processing user input")
        await manager.send_message(
            websocket,
            WSErrorMessage(
                data={"error": str(e)}
            )
        )
