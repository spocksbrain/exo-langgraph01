# exo Documentation

This directory contains the documentation for the exo multi-agent system.

## Building the Documentation

### Prerequisites

Before building the documentation, make sure you have the following prerequisites:

- Python 3.10 or higher
- Sphinx
- sphinx-rtd-theme
- sphinx-autodoc-typehints
- myst-parser

You can install the required packages using pip:

```bash
pip install -r dev-requirements.txt
```

### Building

To build the documentation, run the following command from the `docs` directory:

```bash
# On Linux/macOS
make html

# On Windows
make.bat html
```

This will build the HTML documentation in the `build/html` directory.

### Live Preview

You can also use the `livehtml` target to start a live preview server that will automatically rebuild the documentation when you make changes:

```bash
# On Linux/macOS
make livehtml

# On Windows
make.bat livehtml
```

This will start a server at http://localhost:8000 that will automatically rebuild the documentation when you make changes.

### Other Formats

You can also build the documentation in other formats:

```bash
# PDF
make pdf

# EPUB
make epub

# LaTeX
make latex

# Man pages
make man

# Texinfo
make texinfo

# Plain text
make text
```

## Documentation Structure

The documentation is organized as follows:

- `source/index.rst`: The main index file.
- `source/introduction.rst`: Introduction to the exo system.
- `source/installation.rst`: Installation instructions.
- `source/quickstart.rst`: Quickstart guide.
- `source/architecture.rst`: Architecture overview.
- `source/core.rst`: Core system documentation.
- `source/api.rst`: API documentation.
- `source/knowledge.rst`: Knowledge system documentation.
- `source/mcp.rst`: MCP server documentation.
- `source/interfaces.rst`: Interfaces documentation.
- `source/development.rst`: Development guide.
- `source/contributing.rst`: Contributing guide.
- `source/changelog.rst`: Changelog.

## Adding New Documentation

To add new documentation, create a new `.rst` file in the `source` directory and add it to the appropriate toctree in `index.rst` or another file.

For example, to add a new file called `advanced.rst`, create the file in the `source` directory and add it to the toctree in `index.rst`:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   quickstart
   architecture
   core
   api
   knowledge
   mcp
   interfaces
   development
   advanced
   contributing
   changelog
```

## Documentation Style Guide

When writing documentation, follow these guidelines:

- Use reStructuredText (RST) format for all documentation files.
- Use Markdown format for README files.
- Use sentence case for headings.
- Use present tense and active voice.
- Use code blocks for code examples.
- Use admonitions for notes, warnings, and tips.
- Use cross-references to link to other parts of the documentation.
- Use images sparingly and only when they add value.
- Use tables for tabular data.
- Use lists for enumerated or bulleted items.
