Development
===========

This guide provides information about developing with the exo multi-agent system.

Development Environment
---------------------

To set up a development environment for exo, follow these steps:

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/exo-agents/exo.git
       cd exo

2. Install the package in development mode:

   .. code-block:: bash

       pip install -e .

3. Install development dependencies:

   .. code-block:: bash

       pip install -r dev-requirements.txt

4. Install pre-commit hooks:

   .. code-block:: bash

       pre-commit install

Project Structure
---------------

The exo codebase is organized as follows:

.. code-block:: text

    exo/
    ├── __init__.py
    ├── __main__.py
    ├── config.py
    ├── core/
    │   ├── __init__.py
    │   ├── agent.py
    │   ├── pia.py
    │   ├── cnc.py
    │   ├── domain_agents.py
    │   └── system.py
    ├── api/
    │   ├── __init__.py
    │   ├── app.py
    │   ├── routes.py
    │   └── websocket.py
    ├── knowledge/
    │   ├── __init__.py
    │   ├── init.py
    │   └── system.py
    ├── mcp/
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── client.py
    │   └── server.py
    └── interfaces/
        ├── __init__.py
        ├── cli/
        │   ├── __init__.py
        │   ├── __main__.py
        │   └── main.py
        ├── web/
        │   ├── __init__.py
        │   ├── components/
        │   ├── pages/
        │   └── styles/
        └── electron/
            ├── __init__.py
            ├── __main__.py
            ├── main.js
            ├── preload.js
            └── index.html

Development Workflow
------------------

The development workflow for exo is as follows:

1. Create a new branch for your feature or bug fix:

   .. code-block:: bash

       git checkout -b feature/your-feature-name

2. Make your changes to the codebase.

3. Run the tests to ensure your changes don't break existing functionality:

   .. code-block:: bash

       pytest

4. Run the linters to ensure your code follows the project's coding standards:

   .. code-block:: bash

       pre-commit run --all-files

5. Commit your changes:

   .. code-block:: bash

       git add .
       git commit -m "Add your feature or fix your bug"

6. Push your changes to your fork:

   .. code-block:: bash

       git push origin feature/your-feature-name

7. Create a pull request on GitHub.

Testing
------

exo uses pytest for testing. To run the tests, use the following command:

.. code-block:: bash

    pytest

To run the tests with coverage, use the following command:

.. code-block:: bash

    pytest --cov=exo

To run a specific test file, use the following command:

.. code-block:: bash

    pytest tests/test_core.py

To run a specific test class, use the following command:

.. code-block:: bash

    pytest tests/test_core.py::TestAgent

To run a specific test method, use the following command:

.. code-block:: bash

    pytest tests/test_core.py::TestAgent::test_init

Linting and Formatting
--------------------

exo uses several tools for linting and formatting:

- **black**: Code formatter
- **isort**: Import sorter
- **flake8**: Linter
- **mypy**: Type checker
- **pydocstyle**: Docstring style checker
- **pyupgrade**: Python syntax upgrader

To run all linters and formatters, use the following command:

.. code-block:: bash

    pre-commit run --all-files

To run a specific linter or formatter, use the following command:

.. code-block:: bash

    pre-commit run black --all-files

Documentation
-----------

exo uses Sphinx for documentation. To build the documentation, use the following command:

.. code-block:: bash

    cd docs
    make html

To view the documentation, open `docs/build/html/index.html` in your browser.

To build the documentation in other formats, use the following command:

.. code-block:: bash

    cd docs
    make <format>

Where `<format>` is one of the following:

- `html`: HTML format
- `pdf`: PDF format
- `epub`: EPUB format
- `latex`: LaTeX format
- `man`: Man pages
- `texinfo`: Texinfo format
- `text`: Plain text format

Continuous Integration
--------------------

exo uses GitHub Actions for continuous integration. The CI pipeline runs the following checks:

- **Tests**: Run the tests with pytest
- **Linting**: Run the linters with pre-commit
- **Type checking**: Run mypy for type checking
- **Documentation**: Build the documentation with Sphinx
- **Coverage**: Check the test coverage with pytest-cov

The CI pipeline runs on every push to the main branch and on every pull request.

Releasing
--------

To release a new version of exo, follow these steps:

1. Update the version number in `exo/__init__.py`.
2. Update the changelog in `CHANGELOG.md`.
3. Commit the changes:

   .. code-block:: bash

       git add .
       git commit -m "Bump version to X.Y.Z"

4. Tag the release:

   .. code-block:: bash

       git tag -a vX.Y.Z -m "Version X.Y.Z"

5. Push the changes and tags:

   .. code-block:: bash

       git push origin main
       git push origin vX.Y.Z

6. Create a new release on GitHub.
7. Build and upload the package to PyPI:

   .. code-block:: bash

       python -m build
       python -m twine upload dist/*

Docker
-----

exo can be run in a Docker container. To build the Docker image, use the following command:

.. code-block:: bash

    docker build -t exo-agents/exo .

To run the Docker container, use the following command:

.. code-block:: bash

    docker run -p 8000:8000 -p 8001:8001 -p 3000:3000 exo-agents/exo

Alternatively, you can use Docker Compose:

.. code-block:: bash

    docker-compose up

Contributing
----------

For more information about contributing to exo, see the :doc:`contributing` guide.
