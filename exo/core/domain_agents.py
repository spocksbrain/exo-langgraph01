"""
Domain-specific agents for the exo multi-agent system.

This module contains specialized agents for specific domains:
- Software Engineer Agent: For code generation and documentation
- System Control Agent: For desktop control and automation
"""
import asyncio
from typing import Dict, Any, List, Optional

import autogen
from autogen import AssistantAgent, UserProxyAgent

from exo.config import AGENT_CONFIG
from exo.core.agent import BaseAgent, Message


class SoftwareEngineerAgent(BaseAgent):
    """Software Engineer Agent for code generation and documentation."""
    
    def __init__(self, system_prompt: Optional[str] = None):
        """Initialize the Software Engineer Agent.
        
        Args:
            system_prompt: Custom system prompt
        """
        config = AGENT_CONFIG["software_engineer"]
        super().__init__(
            agent_id="software_engineer",
            name=config["name"],
            description=config["description"],
            model=config["model"],
            system_prompt=system_prompt,
        )
        
        # Initialize autogen assistant agent
        self.assistant = AssistantAgent(
            name=self.name,
            system_message=self.system_prompt,
            llm_config=self.llm_config,
        )
        
        # Initialize user proxy for autogen
        self.user_proxy = UserProxyAgent(
            name="CodeRequester",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False},
        )
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the Software Engineer Agent."""
        base_prompt = super()._get_default_system_prompt()
        return base_prompt + """
You are a highly skilled software engineer with expertise in multiple programming languages,
frameworks, and best practices. Your responsibilities include:

1. Code generation and refactoring
2. Technical documentation creation
3. Bug identification and fixing
4. Code review and optimization
5. Integration with version control systems

When given a task, you should:
1. Analyze the requirements thoroughly
2. Choose appropriate technologies and approaches
3. Write clean, efficient, and well-documented code
4. Provide explanations for your implementation decisions
5. Include tests where appropriate

Your code should follow best practices for the language/framework being used,
be maintainable, and handle edge cases appropriately.
"""
    
    def _process_message(self, message: Message) -> None:
        """Process a received message.
        
        Args:
            message: Message to process
        """
        # For domain agents, we don't need to do anything special with messages
        # They will be handled through the handle_task method
        pass
    
    async def handle_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle a task assigned to the agent.
        
        Args:
            task: Task description
            context: Additional context for the task
            
        Returns:
            Task result
        """
        context = context or {}
        
        # Prepare the prompt with context
        prompt = task
        if "desktop_context" in context and context["desktop_context"]:
            prompt = f"Context:\n{context['desktop_context']}\n\nTask:\n{task}"
        
        # Use autogen to generate a response
        self.user_proxy.initiate_chat(
            self.assistant,
            message=prompt,
        )
        
        # Extract the last assistant message
        chat_history = self.user_proxy.chat_history[self.assistant]
        last_message = chat_history[-1]["content"] if chat_history else "I couldn't complete the task."
        
        return {"response": last_message}


class SystemControlAgent(BaseAgent):
    """System Control Agent for desktop control and automation."""
    
    def __init__(self, system_prompt: Optional[str] = None):
        """Initialize the System Control Agent.
        
        Args:
            system_prompt: Custom system prompt
        """
        config = AGENT_CONFIG["system_control"]
        super().__init__(
            agent_id="system_control",
            name=config["name"],
            description=config["description"],
            model=config["model"],
            system_prompt=system_prompt,
        )
        
        # Initialize autogen assistant agent
        self.assistant = AssistantAgent(
            name=self.name,
            system_message=self.system_prompt,
            llm_config=self.llm_config,
        )
        
        # Initialize user proxy for autogen
        self.user_proxy = UserProxyAgent(
            name="SystemRequester",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False},
        )
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the System Control Agent."""
        base_prompt = super()._get_default_system_prompt()
        return base_prompt + """
You are a specialized agent for desktop control and automation. Your responsibilities include:

1. Interpreting user requests for desktop interactions
2. Generating code for UI automation
3. Capturing and analyzing desktop context
4. Performing system operations
5. Automating repetitive tasks

When given a task, you should:
1. Analyze what desktop interactions are needed
2. Generate appropriate automation code using PyAutoGUI or similar libraries
3. Consider security and permission implications
4. Provide clear explanations of what actions will be performed
5. Handle potential errors and edge cases

Your automation code should be safe, efficient, and respect user privacy and security.
"""
    
    def _process_message(self, message: Message) -> None:
        """Process a received message.
        
        Args:
            message: Message to process
        """
        # For domain agents, we don't need to do anything special with messages
        # They will be handled through the handle_task method
        pass
    
    async def handle_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle a task assigned to the agent.
        
        Args:
            task: Task description
            context: Additional context for the task
            
        Returns:
            Task result
        """
        context = context or {}
        
        # Prepare the prompt with context
        prompt = task
        if "desktop_context" in context and context["desktop_context"]:
            prompt = f"Context:\n{context['desktop_context']}\n\nTask:\n{task}"
        
        # Use autogen to generate a response
        self.user_proxy.initiate_chat(
            self.assistant,
            message=prompt,
        )
        
        # Extract the last assistant message
        chat_history = self.user_proxy.chat_history[self.assistant]
        last_message = chat_history[-1]["content"] if chat_history else "I couldn't complete the task."
        
        # For the PoC, we'll just return the response without actually executing desktop actions
        # In a real implementation, we would parse the response and execute the actions
        return {"response": last_message}


# Factory function to create domain agents
def create_domain_agent(domain: str, **kwargs) -> Optional[BaseAgent]:
    """Create a domain agent based on the domain name.
    
    Args:
        domain: Domain name
        **kwargs: Additional arguments to pass to the agent constructor
        
    Returns:
        Domain agent instance or None if domain is not supported
    """
    if domain == "software_engineer":
        return SoftwareEngineerAgent(**kwargs)
    elif domain == "system_control":
        return SystemControlAgent(**kwargs)
    else:
        return None
