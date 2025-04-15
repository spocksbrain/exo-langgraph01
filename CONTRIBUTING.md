# Contributing to exo

Thank you for your interest in contributing to exo! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to foster an open and welcoming environment.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your feature or bug fix
5. Make your changes
6. Run tests to ensure your changes don't break existing functionality
7. Commit your changes
8. Push to your fork
9. Submit a pull request

## Development Environment

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/exo.git
cd exo

# Run the setup script
# On Linux/macOS
./exo/setup.sh

# On Windows
.\exo\setup.bat

# Edit the .env file with your API keys and configuration
```

## Project Structure

- `exo/core/`: Core agent system and orchestration
- `exo/api/`: FastAPI-based API layer
- `exo/interfaces/`: Multiple user interfaces (CLI, Web, Electron)
- `exo/knowledge/`: Knowledge graph and vector database integration
- `exo/mcp/`: Model Context Protocol server implementation
- `prompts/`: Prompt templates for the agents
- `data/`: Data files for the system
- `logs/`: Log files for the system

## Coding Standards

- Follow PEP 8 for Python code
- Use type hints for function parameters and return values
- Write docstrings for all functions, classes, and modules
- Use meaningful variable and function names
- Keep functions small and focused on a single task
- Write unit tests for all new functionality

## Pull Request Process

1. Ensure your code follows the coding standards
2. Update the documentation to reflect any changes
3. Add or update tests as necessary
4. Update the README.md with details of changes to the interface
5. The pull request will be merged once it has been reviewed and approved by a maintainer

## Adding New Features

When adding new features:

1. First, open an issue to discuss the feature
2. Get approval from the maintainers before starting work
3. Follow the coding standards
4. Add appropriate tests
5. Update the documentation

## Reporting Bugs

When reporting bugs:

1. Use the GitHub issue tracker
2. Describe the bug in detail
3. Include steps to reproduce the bug
4. Include information about your environment (OS, Python version, etc.)
5. If possible, include a minimal code example that reproduces the bug

## Feature Requests

When requesting features:

1. Use the GitHub issue tracker
2. Describe the feature in detail
3. Explain why the feature would be useful
4. Provide examples of how the feature would be used

## License

By contributing to exo, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
