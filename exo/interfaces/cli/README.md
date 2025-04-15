# exo CLI Interface

This is the command-line interface for the exo multi-agent system. It provides a terminal-based interface for interacting with the exo system.

## Features

- Simple, text-based interface
- Rich text formatting with syntax highlighting
- Command history
- Markdown rendering
- Thinking animation

## Usage

```bash
# Run the CLI interface
python -m exo.interfaces.cli

# Run with debug logging
python -m exo.interfaces.cli --debug
```

## Commands

Once in the CLI interface, you can:

- Type any message to interact with the exo system
- Type `exit` or `quit` to exit the CLI

## Architecture

The CLI interface is built with:

- **Click**: Command-line interface creation kit
- **Rich**: Library for rich text and beautiful formatting in the terminal
- **asyncio**: For asynchronous I/O

## Components

- **main.py**: Main CLI application
- **__main__.py**: Entry point for the CLI interface

## Customization

You can customize the CLI interface by:

- Modifying the prompt in `config.py`
- Updating the display functions in `main.py`
- Adding new commands to the CLI interface
