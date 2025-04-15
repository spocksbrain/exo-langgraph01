Installation
============

This guide will help you install the exo multi-agent system.

Prerequisites
------------

Before installing exo, make sure you have the following prerequisites:

- Python 3.10 or higher
- pip (Python package installer)
- Node.js 18 or higher (for web and Electron interfaces)
- npm (Node.js package manager)
- Git

For the knowledge system, you'll also need:

- Neo4j (for the knowledge graph)

Installation Methods
------------------

There are several ways to install exo:

1. Using pip (recommended)
2. From source
3. Using Docker

Using pip
~~~~~~~~~

The easiest way to install exo is using pip:

.. code-block:: bash

    pip install exo-agents

This will install the exo package and its dependencies.

From Source
~~~~~~~~~~

To install exo from source, follow these steps:

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/exo-agents/exo.git
       cd exo

2. Install the package in development mode:

   .. code-block:: bash

       pip install -e .

3. Install development dependencies (optional):

   .. code-block:: bash

       pip install -r dev-requirements.txt

Using Docker
~~~~~~~~~~~

exo can also be installed using Docker:

1. Pull the Docker image:

   .. code-block:: bash

       docker pull exo-agents/exo:latest

2. Run the Docker container:

   .. code-block:: bash

       docker run -p 8000:8000 -p 8001:8001 -p 3000:3000 exo-agents/exo:latest

Alternatively, you can use Docker Compose:

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/exo-agents/exo.git
       cd exo

2. Run Docker Compose:

   .. code-block:: bash

       docker-compose up

Configuration
------------

After installing exo, you need to configure it:

1. Create a `.env` file in the root directory of the project:

   .. code-block:: bash

       cp .env.example .env

2. Edit the `.env` file to set your configuration options:

   .. code-block:: bash

       # OpenAI API Key
       OPENAI_API_KEY=your_openai_api_key_here

       # API Server Configuration
       API_HOST=localhost
       API_PORT=8000

       # MCP Server Configuration
       MCP_SERVER_HOST=localhost
       MCP_SERVER_PORT=8001

       # Knowledge System Configuration
       # Neo4j Configuration
       NEO4J_URI=bolt://localhost:7687
       NEO4J_USER=neo4j
       NEO4J_PASSWORD=password

       # Vector Database Configuration
       VECTOR_DB_PATH=./data/vector_db

       # Data Directory
       DATA_DIR=./data

       # Logging Configuration
       LOG_LEVEL=INFO
       LOG_FILE=./logs/exo.log

       # Web Interface Configuration
       WEB_PORT=3000

       # Electron App Configuration
       ELECTRON_DEV_MODE=true

       # Agent Configuration
       DEFAULT_MODEL=gpt-4o
       SYSTEM_PROMPT_TEMPLATE_PATH=./prompts/system_prompt.txt
       USER_PROMPT_TEMPLATE_PATH=./prompts/user_prompt.txt

Neo4j Setup
----------

exo uses Neo4j for the knowledge graph. You can install Neo4j locally or use a cloud service like Neo4j Aura.

Local Installation
~~~~~~~~~~~~~~~~

1. Download and install Neo4j Desktop from https://neo4j.com/download/
2. Create a new database with the following settings:
   - Name: exo
   - Password: password (or set your own password and update the `.env` file)
3. Start the database

Cloud Installation
~~~~~~~~~~~~~~~~

1. Sign up for Neo4j Aura at https://neo4j.com/cloud/aura/
2. Create a new database
3. Update the `.env` file with the connection details

Verification
-----------

To verify that exo is installed correctly, run the following command:

.. code-block:: bash

    python -m exo --version

This should display the version of exo that you have installed.

Next Steps
---------

Now that you have installed exo, you can:

- :doc:`quickstart`: Get started with the exo system.
- :doc:`architecture`: Learn more about the exo system architecture.
