"""
API routes for the exo multi-agent system.

This module provides the RESTful API endpoints for interacting with the exo system.
"""
import logging
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel

from exo.core.system import ExoSystem, get_system


# Configure logging
logger = logging.getLogger(__name__)


# Create router
router = APIRouter(tags=["api"])


# Request and response models
class UserInputRequest(BaseModel):
    """Request model for user input."""
    
    text: str
    metadata: Optional[Dict[str, Any]] = None


class UserInputResponse(BaseModel):
    """Response model for user input."""
    
    response: str
    handled_by: str
    error: Optional[str] = None


class DesktopContextRequest(BaseModel):
    """Request model for desktop context."""
    
    context_data: Dict[str, Any]


class SystemStatusResponse(BaseModel):
    """Response model for system status."""
    
    status: str
    agents: List[str]
    version: str = "0.1.0"


# Dependency to get the exo system
def get_exo_system() -> ExoSystem:
    """Get the exo system instance.
    
    Returns:
        ExoSystem instance
    """
    return get_system()


@router.post("/input", response_model=UserInputResponse)
async def process_input(
    request: UserInputRequest,
    system: ExoSystem = Depends(get_exo_system),
) -> UserInputResponse:
    """Process user input.
    
    Args:
        request: User input request
        system: ExoSystem instance
        
    Returns:
        Response from the system
    """
    logger.info(f"Received user input: {request.text[:50]}...")
    
    try:
        result = await system.process_user_input(request.text, request.metadata)
        
        # Check for errors
        if "error" in result:
            return UserInputResponse(
                response="",
                handled_by="error",
                error=result["error"],
            )
        
        return UserInputResponse(
            response=result.get("response", ""),
            handled_by=result.get("handled_by", "unknown"),
        )
    except Exception as e:
        logger.exception("Error processing user input")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/desktop-context")
async def update_desktop_context(
    request: DesktopContextRequest,
    system: ExoSystem = Depends(get_exo_system),
):
    """Update desktop context.
    
    Args:
        request: Desktop context request
        system: ExoSystem instance
        
    Returns:
        Success message
    """
    logger.info("Received desktop context update")
    
    try:
        system.capture_desktop_context(request.context_data)
        return {"status": "success"}
    except Exception as e:
        logger.exception("Error updating desktop context")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=SystemStatusResponse)
async def get_status(
    system: ExoSystem = Depends(get_exo_system),
) -> SystemStatusResponse:
    """Get system status.
    
    Args:
        system: ExoSystem instance
        
    Returns:
        System status
    """
    return SystemStatusResponse(
        status="running",
        agents=system.get_agent_ids(),
    )


@router.post("/reset")
async def reset_system(
    background_tasks: BackgroundTasks,
    system: ExoSystem = Depends(get_exo_system),
):
    """Reset the system.
    
    Args:
        background_tasks: FastAPI background tasks
        system: ExoSystem instance
        
    Returns:
        Success message
    """
    logger.info("Resetting system")
    
    # Reset the system in the background
    background_tasks.add_task(reset_system_task)
    
    return {"status": "resetting"}


async def reset_system_task():
    """Reset the system in the background."""
    # For the PoC, we'll just create a new system instance
    # In a real implementation, we would properly clean up resources
    global _system_instance
    _system_instance = None
    _ = get_system()
