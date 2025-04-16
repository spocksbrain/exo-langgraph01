"""
System initialization and management for the exo multi-agent system.

This module provides the main entry point for the exo system, initializing all agents
and providing a simple API for interacting with the system.
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional, Union, Callable

from exo.config import AGENT_CONFIG
from exo.core.agent import BaseAgent, Message
from exo.core.pia import PrimaryInterfaceAgent
from exo.core.cnc import CommandControlAgent
from exo.core.domain_agents import create_domain_agent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ExoSystem:
    """Main class for the exo multi-agent system."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the exo system.
        
        Args:
            openai_api_key: OpenAI API key (optional, can be set in environment)
        """
        self.agents: Dict[str, BaseAgent] = {}
        self.openai_api_key = openai_api_key
        
        # Initialize the system
        self._initialize_system()
    
    def _initialize_system(self) -> None:
        """Initialize all agents and connect them together."""
        logger.info("Initializing exo system...")
        
        # Create domain agents
        domain_agents = {}
        for domain in ["software_engineer", "system_control"]:
            agent = create_domain_agent(domain)
            if agent:
                domain_agents[domain] = agent
                self.agents[domain] = agent
                logger.info(f"Created domain agent: {domain}")
        
        # Create CNC agent
        cnc_agent = CommandControlAgent(domain_agents=domain_agents)
        self.agents["cnc"] = cnc_agent
        logger.info("Created Command & Control Agent")
        
        # Create PIA
        pia = PrimaryInterfaceAgent(cnc_agent=cnc_agent, domain_agents=domain_agents)
        self.agents["pia"] = pia
        logger.info("Created Primary Interface Agent")
        
        logger.info("Exo system initialization complete")
    
    async def process_user_input(self, input_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process user input through the Primary Interface Agent.
        
        Args:
            input_text: User input text
            metadata: Additional metadata about the input
            
        Returns:
            Response from the system
        """
        logger.info(f"Processing user input: {input_text[:50]}...")
        
        # Get the PIA
        pia = self.agents.get("pia")
        if not pia:
            logger.error("Primary Interface Agent not found")
            return {"error": "System not properly initialized"}

        # Directly process the input via PIA's handler method
        # Removed the redundant pia.receive_message(message) call
        try:
            # Directly await the PIA's processing method
            result = await pia.process_user_input(input_text, metadata)
            logger.info(f"Processed user input, handled by: {result.get('handled_by', 'unknown')}")
            return result
        except Exception as e:
            logger.exception("Error processing user input")
            return {"error": str(e)}
    
    def capture_desktop_context(self, context_data: Dict[str, Any]) -> None:
        """Capture desktop context for use in task processing.
        
        Args:
            context_data: Desktop context data (e.g., screenshot, active window)
        """
        # Get the PIA
        pia = self.agents.get("pia")
        if not pia:
            logger.error("Primary Interface Agent not found")
            return
        
        # Update the desktop context
        pia.capture_desktop_context(context_data)
        logger.info("Updated desktop context")
    
    def register_callback(self, agent_id: str, callback: Callable[[Message], None]) -> bool:
        """Register a callback for an agent.
        
        Args:
            agent_id: ID of the agent to register the callback for
            callback: Function to call when the agent receives a message
            
        Returns:
            True if the callback was registered, False otherwise
        """
        agent = self.agents.get(agent_id)
        if not agent:
            logger.error(f"Agent not found: {agent_id}")
            return False
        
        agent.register_on_message_callback(callback)
        logger.info(f"Registered callback for agent: {agent_id}")
        return True
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID.
        
        Args:
            agent_id: ID of the agent to get
            
        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(agent_id)
    
    def get_agent_ids(self) -> List[str]:
        """Get a list of all agent IDs.
        
        Returns:
            List of agent IDs
        """
        return list(self.agents.keys())


# Singleton instance
_system_instance: Optional[ExoSystem] = None


def get_system(openai_api_key: Optional[str] = None) -> ExoSystem:
    """Get the singleton instance of the exo system.
    
    Args:
        openai_api_key: OpenAI API key (optional, can be set in environment)
        
    Returns:
        ExoSystem instance
    """
    global _system_instance
    if _system_instance is None:
        _system_instance = ExoSystem(openai_api_key=openai_api_key)
    return _system_instance


async def process_user_input(input_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Process user input through the exo system.
    
    Args:
        input_text: User input text
        metadata: Additional metadata about the input
        
    Returns:
        Response from the system
    """
    system = get_system()
    return await system.process_user_input(input_text, metadata)


def capture_desktop_context(context_data: Dict[str, Any]) -> None:
    """Capture desktop context for use in task processing.
    
    Args:
        context_data: Desktop context data (e.g., screenshot, active window)
    """
    system = get_system()
    system.capture_desktop_context(context_data)
