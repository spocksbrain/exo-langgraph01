Quickstart
==========

This guide will help you get started with the exo multi-agent system.

Running exo
----------

After :doc:`installation`, you can run exo using one of the following methods:

Using the CLI
~~~~~~~~~~~~

The simplest way to run exo is using the CLI:

.. code-block:: bash

    python -m exo.interfaces.cli

This will start the CLI interface, which allows you to interact with the exo system through the command line.

Using the Web Interface
~~~~~~~~~~~~~~~~~~~~~

To run exo with the web interface:

.. code-block:: bash

    python -m exo.interfaces.web

This will start the web server, which you can access at http://localhost:3000 in your browser.

Using the Electron App
~~~~~~~~~~~~~~~~~~~~

To run exo with the Electron desktop app:

.. code-block:: bash

    python -m exo.interfaces.electron

This will start the Electron app, which provides a native desktop experience.

Using the API Server
~~~~~~~~~~~~~~~~~~

To run exo as an API server:

.. code-block:: bash

    python -m exo.api

This will start the API server, which you can access at http://localhost:8000.

Using the MCP Server
~~~~~~~~~~~~~~~~~~

To run exo with the MCP server:

.. code-block:: bash

    python -m exo.mcp

This will start the MCP server, which provides desktop control and other capabilities.

Using the Run Script
~~~~~~~~~~~~~~~~~~

The easiest way to run exo is using the run script, which allows you to run multiple components at once:

.. code-block:: bash

    python run.py --interface all

This will start all interfaces (CLI, Web, Electron, API, and MCP).

You can also specify which interfaces to run:

.. code-block:: bash

    python run.py --interface cli web

This will start the CLI and Web interfaces.

Basic Usage
----------

Once you have exo running, you can interact with it through the chosen interface.

CLI Interface
~~~~~~~~~~~

In the CLI interface, you can type commands and receive responses:

.. code-block:: bash

    > Hello, exo!
    Hello! How can I help you today?

    > What can you do?
    I can help you with a wide range of tasks, including:
    - Answering questions
    - Providing information
    - Performing calculations
    - Writing code
    - And much more!

    > Exit
    Goodbye!

Web Interface
~~~~~~~~~~~

In the web interface, you can type messages in the chat box and receive responses.

Electron Interface
~~~~~~~~~~~~~~~

In the Electron interface, you can type messages in the chat box and receive responses. The Electron interface also provides additional capabilities, such as desktop control.

API Interface
~~~~~~~~~~~

The API interface provides a RESTful API for interacting with the exo system. You can use tools like curl or Postman to send requests to the API:

.. code-block:: bash

    curl -X POST -H "Content-Type: application/json" -d '{"text": "Hello, exo!"}' http://localhost:8000/api/input

This will send a message to the exo system and receive a response.

MCP Interface
~~~~~~~~~~~

The MCP interface provides a Model Context Protocol server for desktop control and other capabilities. You can use the MCP client to interact with the MCP server:

.. code-block:: python

    from exo.mcp.client import MCPClient

    client = MCPClient()
    result = client.execute_tool("click_element", {"x": 100, "y": 100})
    print(result)

This will click at the specified coordinates on the screen.

Advanced Usage
-------------

exo provides a number of advanced features that you can use to customize its behavior.

Configuration
~~~~~~~~~~~

You can configure exo by editing the `.env` file in the root directory of the project. See the :doc:`installation` guide for more information.

Custom Domain Agents
~~~~~~~~~~~~~~~~~

You can create custom domain agents to extend the capabilities of exo. See the :doc:`core` guide for more information.

Custom Tools
~~~~~~~~~~

You can create custom tools to extend the capabilities of exo. See the :doc:`mcp` guide for more information.

Custom Interfaces
~~~~~~~~~~~~~~

You can create custom interfaces to interact with exo. See the :doc:`interfaces` guide for more information.

Next Steps
---------

Now that you have started using exo, you can:

- :doc:`architecture`: Learn more about the exo system architecture.
- :doc:`core`: Learn more about the core system.
- :doc:`api`: Learn more about the API layer.
- :doc:`knowledge`: Learn more about the knowledge system.
- :doc:`mcp`: Learn more about the MCP server.
- :doc:`interfaces`: Learn more about the interfaces.
- :doc:`development`: Learn more about developing with exo.
