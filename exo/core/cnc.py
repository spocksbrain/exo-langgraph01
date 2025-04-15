"""
Command & Control Agent (CNC) for the exo multi-agent system.

The CNC agent is responsible for decomposing complex tasks into subtasks,
coordinating multiple domain agents, and aggregating results.
"""
import asyncio
from typing import Dict, Any, List, Optional, Tuple, Set

import autogen
from autogen import AssistantAgent, UserProxyAgent

from exo.config import AGENT_CONFIG
from exo.core.agent import BaseAgent, Message


class TaskNode:
    """Represents a node in the task dependency graph."""
    
    def __init__(self, task_id: str, domain: str, description: str):
        """Initialize a task node.
        
        Args:
            task_id: Unique identifier for the task
            domain: Domain this task belongs to
            description: Description of the task
        """
        self.task_id = task_id
        self.domain = domain
        self.description = description
        self.dependencies: Set[str] = set()  # Task IDs this task depends on
        self.dependents: Set[str] = set()    # Task IDs that depend on this task
        self.status = "pending"  # pending, in_progress, completed, failed
        self.result: Optional[Dict[str, Any]] = None
    
    def add_dependency(self, task_id: str) -> None:
        """Add a dependency for this task.
        
        Args:
            task_id: Task ID this task depends on
        """
        self.dependencies.add(task_id)
    
    def add_dependent(self, task_id: str) -> None:
        """Add a dependent for this task.
        
        Args:
            task_id: Task ID that depends on this task
        """
        self.dependents.add(task_id)
    
    def is_ready(self) -> bool:
        """Check if this task is ready to be executed.
        
        Returns:
            True if all dependencies are completed, False otherwise
        """
        return self.status == "pending" and not self.dependencies
    
    def mark_completed(self, result: Dict[str, Any]) -> None:
        """Mark this task as completed.
        
        Args:
            result: Result of the task
        """
        self.status = "completed"
        self.result = result
    
    def mark_failed(self, error: str) -> None:
        """Mark this task as failed.
        
        Args:
            error: Error message
        """
        self.status = "failed"
        self.result = {"error": error}


class TaskGraph:
    """Represents a directed acyclic graph of tasks with dependencies."""
    
    def __init__(self):
        """Initialize an empty task graph."""
        self.nodes: Dict[str, TaskNode] = {}
    
    def add_task(self, task_id: str, domain: str, description: str) -> TaskNode:
        """Add a task to the graph.
        
        Args:
            task_id: Unique identifier for the task
            domain: Domain this task belongs to
            description: Description of the task
            
        Returns:
            The created task node
        """
        node = TaskNode(task_id, domain, description)
        self.nodes[task_id] = node
        return node
    
    def add_dependency(self, dependent_id: str, dependency_id: str) -> None:
        """Add a dependency between two tasks.
        
        Args:
            dependent_id: ID of the dependent task
            dependency_id: ID of the dependency task
        """
        if dependent_id not in self.nodes or dependency_id not in self.nodes:
            raise ValueError(f"Task IDs must exist in the graph: {dependent_id}, {dependency_id}")
        
        dependent = self.nodes[dependent_id]
        dependency = self.nodes[dependency_id]
        
        dependent.add_dependency(dependency_id)
        dependency.add_dependent(dependent_id)
    
    def get_ready_tasks(self) -> List[TaskNode]:
        """Get all tasks that are ready to be executed.
        
        Returns:
            List of ready task nodes
        """
        return [node for node in self.nodes.values() if node.is_ready()]
    
    def mark_completed(self, task_id: str, result: Dict[str, Any]) -> List[str]:
        """Mark a task as completed and update dependencies.
        
        Args:
            task_id: ID of the completed task
            result: Result of the task
            
        Returns:
            List of task IDs that are now ready
        """
        if task_id not in self.nodes:
            raise ValueError(f"Task ID does not exist in the graph: {task_id}")
        
        node = self.nodes[task_id]
        node.mark_completed(result)
        
        # Remove this task from dependencies of dependent tasks
        newly_ready = []
        for dependent_id in node.dependents:
            dependent = self.nodes[dependent_id]
            dependent.dependencies.remove(task_id)
            if dependent.is_ready():
                newly_ready.append(dependent_id)
        
        return newly_ready
    
    def mark_failed(self, task_id: str, error: str) -> None:
        """Mark a task as failed.
        
        Args:
            task_id: ID of the failed task
            error: Error message
        """
        if task_id not in self.nodes:
            raise ValueError(f"Task ID does not exist in the graph: {task_id}")
        
        node = self.nodes[task_id]
        node.mark_failed(error)
    
    def is_complete(self) -> bool:
        """Check if all tasks in the graph are completed or failed.
        
        Returns:
            True if all tasks are completed or failed, False otherwise
        """
        return all(node.status in ["completed", "failed"] for node in self.nodes.values())
    
    def get_results(self) -> Dict[str, Any]:
        """Get the results of all completed tasks.
        
        Returns:
            Dictionary mapping task IDs to results
        """
        return {task_id: node.result for task_id, node in self.nodes.items() if node.status == "completed"}


class CommandControlAgent(BaseAgent):
    """Command & Control Agent for the exo multi-agent system."""
    
    def __init__(
        self,
        domain_agents=None,
        system_prompt: Optional[str] = None,
    ):
        """Initialize the Command & Control Agent.
        
        Args:
            domain_agents: Dictionary of domain agents
            system_prompt: Custom system prompt
        """
        config = AGENT_CONFIG["cnc"]
        super().__init__(
            agent_id="cnc",
            name=config["name"],
            description=config["description"],
            model=config["model"],
            system_prompt=system_prompt,
        )
        
        self.domain_agents = domain_agents or {}
        self.active_tasks: Dict[str, TaskGraph] = {}
        
        # Initialize autogen assistant agent for task decomposition
        # Replace spaces with underscores in the name for autogen (which doesn't allow spaces)
        autogen_name = self.name.replace(" ", "_")
        self.assistant = AssistantAgent(
            name=autogen_name,
            system_message=self._get_task_decomposition_prompt(),
            llm_config=self.llm_config,
        )
        
        # Initialize user proxy for autogen
        self.user_proxy = UserProxyAgent(
            name="TaskDecomposer",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False},
        )
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the CNC agent."""
        base_prompt = super()._get_default_system_prompt()
        return base_prompt + """
You are responsible for orchestrating complex tasks across multiple domain agents.
Your responsibilities include:

1. Decomposing complex tasks into subtasks across domains
2. Coordinating multiple domain agents on related subtasks
3. Managing dependencies between subtasks
4. Aggregating results from multiple agents
5. Ensuring consistency across domain agent outputs
6. Handling agent failures and contingencies

You should approach tasks analytically, breaking them down into logical components
and identifying the dependencies between them.
"""
    
    def _get_task_decomposition_prompt(self) -> str:
        """Get the prompt for task decomposition."""
        domains = ", ".join(self.domain_agents.keys()) if self.domain_agents else "software_engineer, system_control"
        
        return f"""You are an expert at breaking down complex tasks into smaller, domain-specific subtasks.
Available domains: {domains}

For each task, you should:
1. Identify the key components of the task
2. Determine which domain each component belongs to
3. Establish dependencies between components
4. Create a clear description for each subtask

Your output should be in the following JSON format:
```json
{{
  "subtasks": [
    {{
      "id": "unique_id",
      "domain": "domain_name",
      "description": "detailed_description",
      "dependencies": ["dependency_id1", "dependency_id2"]
    }},
    ...
  ]
}}
```

Each subtask should have:
- A unique ID (e.g., "task1", "task2")
- A domain from the available domains
- A clear, detailed description
- A list of dependencies (IDs of tasks that must be completed before this one)

The first tasks should have empty dependencies lists.
"""
    
    def _process_message(self, message: Message) -> None:
        """Process a received message.
        
        Args:
            message: Message to process
        """
        # For CNC, we don't need to do anything special with messages
        # They will be handled through the handle_task method
        pass
    
    async def decompose_task(self, task: str) -> Dict[str, Any]:
        """Decompose a complex task into subtasks.
        
        Args:
            task: Task description
            
        Returns:
            Dictionary containing subtasks with dependencies
        """
        # Use autogen to decompose the task
        self.user_proxy.initiate_chat(
            self.assistant,
            message=f"Decompose the following task into subtasks:\n\n{task}",
        )
        
        # Extract the last assistant message
        chat_history = self.user_proxy.chat_history[self.assistant]
        last_message = chat_history[-1]["content"] if chat_history else "{}"
        
        # Extract JSON from the message
        import json
        import re
        
        json_match = re.search(r'```json\n(.*?)\n```', last_message, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find any JSON object
            json_match = re.search(r'({.*})', last_message, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Fallback to simple task
                return {
                    "subtasks": [
                        {
                            "id": "task1",
                            "domain": "software_engineer" if "code" in task.lower() else "system_control",
                            "description": task,
                            "dependencies": []
                        }
                    ]
                }
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Fallback to simple task
            return {
                "subtasks": [
                    {
                        "id": "task1",
                        "domain": "software_engineer" if "code" in task.lower() else "system_control",
                        "description": task,
                        "dependencies": []
                    }
                ]
            }
    
    def build_task_graph(self, subtasks: List[Dict[str, Any]]) -> TaskGraph:
        """Build a task graph from subtasks.
        
        Args:
            subtasks: List of subtask dictionaries
            
        Returns:
            Task graph
        """
        graph = TaskGraph()
        
        # First pass: create all nodes
        for subtask in subtasks:
            graph.add_task(
                task_id=subtask["id"],
                domain=subtask["domain"],
                description=subtask["description"],
            )
        
        # Second pass: add dependencies
        for subtask in subtasks:
            for dependency_id in subtask.get("dependencies", []):
                if dependency_id in graph.nodes:
                    graph.add_dependency(subtask["id"], dependency_id)
        
        return graph
    
    async def execute_task_graph(self, task_id: str, graph: TaskGraph) -> Dict[str, Any]:
        """Execute a task graph.
        
        Args:
            task_id: ID of the overall task
            graph: Task graph to execute
            
        Returns:
            Aggregated results
        """
        # Store the active task
        self.active_tasks[task_id] = graph
        
        # Process tasks until the graph is complete
        while not graph.is_complete():
            # Get ready tasks
            ready_tasks = graph.get_ready_tasks()
            
            # Execute ready tasks in parallel
            if ready_tasks:
                # Mark tasks as in progress
                for task in ready_tasks:
                    task.status = "in_progress"
                
                # Execute tasks
                tasks = [self._execute_subtask(task) for task in ready_tasks]
                await asyncio.gather(*tasks)
            else:
                # No ready tasks, but graph is not complete
                # This could happen if there are circular dependencies
                # or if all remaining tasks are in progress
                await asyncio.sleep(0.1)
        
        # Aggregate results
        results = graph.get_results()
        
        # Clean up
        del self.active_tasks[task_id]
        
        return self._aggregate_results(results)
    
    async def _execute_subtask(self, task: TaskNode) -> None:
        """Execute a subtask.
        
        Args:
            task: Task to execute
        """
        try:
            # Get the domain agent
            if task.domain in self.domain_agents:
                agent = self.domain_agents[task.domain]
                
                # Execute the task
                result = await agent.handle_task(task.description)
                
                # Mark the task as completed
                task.mark_completed(result)
            else:
                # Domain agent not available
                task.mark_failed(f"Domain agent not available: {task.domain}")
        except Exception as e:
            # Mark the task as failed
            task.mark_failed(str(e))
    
    def _aggregate_results(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate results from multiple subtasks.
        
        Args:
            results: Dictionary mapping task IDs to results
            
        Returns:
            Aggregated results
        """
        # For the PoC, we'll just combine all responses
        aggregated_response = ""
        
        for task_id, result in results.items():
            if "error" in result:
                aggregated_response += f"Task {task_id} failed: {result['error']}\n\n"
            else:
                response = result.get("response", "")
                if response:
                    aggregated_response += f"{response}\n\n"
        
        return {"response": aggregated_response.strip()}
    
    async def handle_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle a task assigned to the agent.
        
        Args:
            task: Task description
            context: Additional context for the task
            
        Returns:
            Task result
        """
        # Generate a unique task ID
        import uuid
        task_id = str(uuid.uuid4())
        
        # Decompose the task
        decomposition = await self.decompose_task(task)
        
        # Build the task graph
        graph = self.build_task_graph(decomposition.get("subtasks", []))
        
        # Execute the task graph
        return await self.execute_task_graph(task_id, graph)
