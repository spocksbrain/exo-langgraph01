"""
Primary Interface Agent (PIA) for the exo multi-agent system.

The PIA serves as the user's primary point of contact with the entire system.
It processes user input, captures desktop context, and delegates tasks to appropriate agents.
"""
import asyncio
from typing import Dict, Any, List, Optional, Callable, Union

import autogen
from autogen import Agent, AssistantAgent, UserProxyAgent

from exo.config import AGENT_CONFIG
from exo.core.agent import BaseAgent, Message


class PrimaryInterfaceAgent(BaseAgent):
    """Primary Interface Agent for the exo multi-agent system."""
    
    def __init__(
        self,
        cnc_agent=None,
        domain_agents=None,
        system_prompt: Optional[str] = None,
    ):
        """Initialize the Primary Interface Agent.
        
        Args:
            cnc_agent: Command & Control Agent
            domain_agents: Dictionary of domain agents
            system_prompt: Custom system prompt
        """
        config = AGENT_CONFIG["pia"]
        super().__init__(
            agent_id="pia",
            name=config["name"],
            description=config["description"],
            model=config["model"],
            system_prompt=system_prompt,
        )
        
        self.cnc_agent = cnc_agent
        self.domain_agents = domain_agents or {}
        self.conversation_history = []
        self.desktop_context = None
        self.voice_mode_active = False
        
        # Initialize autogen assistant agent
        # Replace spaces with underscores in the name for autogen (which doesn't allow spaces)
        autogen_name = self.name.replace(" ", "_")
        self.assistant = AssistantAgent(
            name=autogen_name,
            system_message=self.system_prompt,
            llm_config=self.llm_config,
        )
        
        # Initialize user proxy for autogen
        self.user_proxy = UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False},
        )
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the PIA."""
        base_prompt = super()._get_default_system_prompt()
        return base_prompt + """
You are the primary point of contact for users interacting with the exo system.
Your responsibilities include:

1. Processing user input (text, voice, or multimodal)
2. Capturing and interpreting desktop context for tasks
3. Directing desktop control for simple tasks
4. Delegating complex tasks to appropriate agents
5. Maintaining conversation history and context

You should maintain a conversational, helpful tone in all interactions.
Proactively offer assistance when context indicates it would be helpful.
Request clarification when user intentions are ambiguous.
Provide clear, concise feedback about task progress.
"""
    
    def _process_message(self, message: Message) -> None:
        """Process a received message.
        
        Args:
            message: Message to process
        """
        # Add to conversation history
        self.conversation_history.append(message)
        
        # If message is from user, process it
        if message.from_agent == "user":
            asyncio.create_task(self.process_user_input(message.content, message.metadata))
    
    async def process_user_input(self, input_text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process user input and determine appropriate action.
        
        Args:
            input_text: User input text
            metadata: Additional metadata about the input
            
        Returns:
            Response to the user
        """
        # Check for empty input
        if not input_text or input_text.strip() == "":
            return {
                "response": "I didn't receive any input. Please type a message.",
                "handled_by": "pia"
            }
        
        metadata = metadata or {}
        input_type = metadata.get("input_type", "text")
        
        # Capture desktop context if available
        if "desktop_context" in metadata:
            self.desktop_context = metadata["desktop_context"]
        
        # Determine if this is a simple query or a complex task
        task_complexity = self._determine_task_complexity(input_text)
        
        try:
            if task_complexity == "simple":
                # Handle simple queries directly
                response = await self._handle_simple_query(input_text)
                return {"response": response, "handled_by": "pia"}
            else:
                # Delegate to appropriate agent
                return await self._delegate_task(input_text, task_complexity)
        except Exception as e:
            # Handle any errors during processing
            import logging
            logging.exception(f"Error processing input: {input_text}")
            return {
                "response": f"I encountered an error while processing your request: {str(e)}",
                "handled_by": "pia",
                "error": str(e)
            }
    
    def _determine_task_complexity(self, input_text: str) -> str:
        """Determine the complexity of a user task.
        
        Args:
            input_text: User input text
            
        Returns:
            Task complexity: "simple", "domain_specific", or "multi_domain"
        """
        # For the PoC, use a simple heuristic
        # In a real implementation, this would use more sophisticated NLP
        
        # Check for domain-specific keywords
        code_keywords = ["code", "program", "function", "class", "script", "develop"]
        system_keywords = ["click", "type", "desktop", "window", "screenshot", "automate"]
        
        has_code_keywords = any(keyword in input_text.lower() for keyword in code_keywords)
        has_system_keywords = any(keyword in input_text.lower() for keyword in system_keywords)
        
        if has_code_keywords and has_system_keywords:
            return "multi_domain"
        elif has_code_keywords:
            return "domain_specific:software_engineer"
        elif has_system_keywords:
            return "domain_specific:system_control"
        else:
            return "simple"
    
    async def _handle_simple_query(self, input_text: str) -> str:
        """Handle a simple query directly.
        
        Args:
            input_text: User input text
            
        Returns:
            Response to the user
        """
        # Use autogen to generate a response
        self.user_proxy.initiate_chat(
            self.assistant,
            message=input_text,
        )
        
        # Extract the last assistant message
        chat_history = self.user_proxy.chat_history[self.assistant]
        last_message = chat_history[-1]["content"] if chat_history else "I'm sorry, I couldn't process that request."
        
        return last_message
    
    async def _delegate_task(self, input_text: str, task_complexity: str) -> Dict[str, Any]:
        """Delegate a task to the appropriate agent.
        
        Args:
            input_text: User input text
            task_complexity: Task complexity classification
            
        Returns:
            Task result
        """
        if task_complexity.startswith("domain_specific:"):
            # Extract domain from complexity
            domain = task_complexity.split(":")[1]
            
            # Check if we have this domain agent
            if domain in self.domain_agents:
                agent = self.domain_agents[domain]
                result = await agent.handle_task(input_text, {"desktop_context": self.desktop_context})
                return {"response": result.get("response", "Task completed"), "handled_by": domain}
            else:
                # Fallback to CNC if domain agent not available
                if self.cnc_agent:
                    result = await self.cnc_agent.handle_task(input_text, {"desktop_context": self.desktop_context})
                    return {"response": result.get("response", "Task completed"), "handled_by": "cnc"}
                else:
                    return {"response": "I don't have the capability to handle that task yet.", "handled_by": "pia"}
        else:
            # Multi-domain task, delegate to CNC
            if self.cnc_agent:
                result = await self.cnc_agent.handle_task(input_text, {"desktop_context": self.desktop_context})
                return {"response": result.get("response", "Task completed"), "handled_by": "cnc"}
            else:
                return {"response": "I don't have the capability to handle complex tasks yet.", "handled_by": "pia"}
    
    def capture_desktop_context(self, context_data: Dict[str, Any]) -> None:
        """Capture desktop context for use in task processing.
        
        Args:
            context_data: Desktop context data (e.g., screenshot, active window)
        """
        self.desktop_context = context_data
    
    async def handle_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle a task assigned to the agent.
        
        Args:
            task: Task description
            context: Additional context for the task
            
        Returns:
            Task result
        """
        # For PIA, this is the same as processing user input
        return await self.process_user_input(task, context)
