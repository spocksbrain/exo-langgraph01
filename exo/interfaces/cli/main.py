"""
Command-line interface for the exo multi-agent system.

This module provides a simple CLI for interacting with the exo system.
"""
import asyncio
import logging
import os
import sys
from typing import Dict, Any, List, Optional, Tuple

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.text import Text

from exo.config import CLI_CONFIG
from exo.core.system import get_system, process_user_input


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Create console
console = Console()


def display_welcome():
    """Display welcome message."""
    console.print(Panel.fit(
        "[bold blue]exo[/bold blue] [bold]Multi-Agent System[/bold]\n\n"
        "Type your message and press Enter to interact with the system.\n"
        "Type [bold]exit[/bold] or [bold]quit[/bold] to exit.",
        title="Welcome",
        border_style="blue",
    ))


def display_response(response: str, handled_by: str):
    """Display a response from the system.
    
    Args:
        response: Response text
        handled_by: Agent that handled the request
    """
    # Check if the response contains code blocks
    if "```" in response:
        # Display as markdown
        console.print(Markdown(response))
    else:
        # Display as plain text
        console.print(Panel.fit(
            response,
            title=f"Response from {handled_by}",
            border_style="green",
        ))


def display_error(error: str):
    """Display an error message.
    
    Args:
        error: Error message
    """
    console.print(Panel.fit(
        error,
        title="Error",
        border_style="red",
    ))


def display_thinking():
    """Display a thinking animation."""
    with console.status("[bold blue]Thinking...[/bold blue]", spinner="dots"):
        # This will be replaced by the actual response
        yield


def save_history(input_text: str):
    """Save input to history file.
    
    Args:
        input_text: User input text
    """
    history_file = CLI_CONFIG["history_file"]
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    
    # Append to history file
    with open(history_file, "a") as f:
        f.write(f"{input_text}\n")


def load_history() -> List[str]:
    """Load history from file.
    
    Returns:
        List of history items
    """
    history_file = CLI_CONFIG["history_file"]
    
    if not os.path.exists(history_file):
        return []
    
    with open(history_file, "r") as f:
        return [line.strip() for line in f.readlines()]


async def process_input(input_text: str) -> Tuple[str, str]:
    """Process user input and return the response.
    
    Args:
        input_text: User input text
        
    Returns:
        Tuple of (response, handled_by)
    """
    # Process the input
    result = await process_user_input(input_text)
    
    # Check for errors
    if "error" in result:
        return result["error"], "error"
    
    # Print the raw result for debugging
    print(f"Result from process_user_input: {result}")
    
    return result.get("response", ""), result.get("handled_by", "unknown")


async def main_loop():
    """Main CLI loop."""
    display_welcome()
    
    # Load history
    history = load_history()
    
    while True:
        # Get user input
        input_text = Prompt.ask(
            f"[bold blue]{CLI_CONFIG['prompt']}[/bold blue]",
            console=console,
        )
        
        # Check for exit command
        if input_text.lower() in ["exit", "quit"]:
            console.print("[bold blue]Goodbye![/bold blue]")
            break
        
        # Save to history
        save_history(input_text)
        
        # Display thinking animation
        for _ in display_thinking():
            # Process the input
            response, handled_by = await process_input(input_text)
            
            # Display the response
            if handled_by == "error":
                display_error(response)
            else:
                display_response(response, handled_by)


@click.command()
@click.option("--debug", is_flag=True, help="Enable debug logging")
def main(debug: bool):
    """Command-line interface for the exo multi-agent system."""
    # Configure logging
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run the main loop
    asyncio.run(main_loop())


if __name__ == "__main__":
    main()
