"""
Base agent class for the exo multi-agent system.
"""
import time
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable

import autogen
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Message model for agent communication."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    from_agent: str
    to_agent: Optional[str] = None
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class AgentState(BaseModel):
    """State model for agent."""
    
    agent_id: str
    name: str
    description: str
    is_active: bool = True
    memory: List[Message] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseAgent(ABC):
    """Base agent class for all agents in the exo system."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        description: str,
        model: str,
        system_prompt: Optional[str] = None,
    ):
        """Initialize the base agent.
        
        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name for the agent
            description: Description of the agent's purpose
            model: LLM model to use for the agent
            system_prompt: System prompt for the agent
        """
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.model = model
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        
        # Initialize state
        self.state = AgentState(
            agent_id=agent_id,
            name=name,
            description=description,
        )
        
        # Initialize autogen config
        from exo.config import OPENAI_API_KEY
        
        # Base configuration
        config = {"model": model, "api_key": OPENAI_API_KEY}

        # Models that don't support temperature parameter (like o3-mini)
        no_temperature_models = ["o3-mini", "claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]

        # Set temperature based on model support
        if any(model_name in model.lower() for model_name in no_temperature_models):
            # Explicitly set temperature to None for unsupported models
            config["temperature"] = None
        else:
            # Set default temperature for supported models
            config["temperature"] = 0.1

        self.llm_config = {
            "config_list": [config],
            # Ensure temperature is passed correctly, even if None
            "temperature": config["temperature"],
        }
        
        # Initialize callbacks
        self.on_message_callbacks: List[Callable[[Message], None]] = []
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the agent."""
        return f"""You are {self.name}, {self.description}.
        
You are part of the exo multi-agent system, a hierarchical arrangement of specialized AI agents
working in concert to handle complex tasks across multiple domains.

Your agent ID is {self.agent_id}.
"""
    
    def add_message_to_memory(self, message: Message) -> None:
        """Add a message to the agent's memory.
        
        Args:
            message: Message to add to memory
        """
        self.state.memory.append(message)
    
    def create_message(self, content: str, to_agent: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Message:
        """Create a new message from this agent.
        
        Args:
            content: Message content
            to_agent: Recipient agent ID (if any)
            metadata: Additional metadata for the message
            
        Returns:
            Message object
        """
        return Message(
            from_agent=self.agent_id,
            to_agent=to_agent,
            content=content,
            metadata=metadata or {},
        )
    
    def register_on_message_callback(self, callback: Callable[[Message], None]) -> None:
        """Register a callback to be called when a message is received.
        
        Args:
            callback: Function to call with the message
        """
        self.on_message_callbacks.append(callback)
    
    def receive_message(self, message: Message) -> None:
        """Process a received message.
        
        Args:
            message: Message received by the agent
        """
        # Add to memory
        self.add_message_to_memory(message)
        
        # Call registered callbacks
        for callback in self.on_message_callbacks:
            callback(message)
        
        # Process the message
        self._process_message(message)
    
    @abstractmethod
    def _process_message(self, message: Message) -> None:
        """Process a received message (to be implemented by subclasses).
        
        Args:
            message: Message to process
        """
        pass
    
    @abstractmethod
    async def handle_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle a task assigned to the agent.
        
        Args:
            task: Task description
            context: Additional context for the task
            
        Returns:
            Task result
        """
        pass
