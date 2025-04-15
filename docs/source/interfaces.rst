Interfaces
==========

This guide provides information about the interfaces of the exo multi-agent system.

Overview
-------

The exo system provides multiple interfaces for interacting with the system:

- **CLI**: Command-line interface for quick access and scripting.
- **Web**: Browser-based interface for easy access from any device.
- **Electron**: Desktop application for a native experience with additional capabilities.

These interfaces provide different ways to interact with the system, depending on the user's needs and preferences.

CLI Interface
-----------

The CLI interface provides a command-line interface for interacting with the exo system. It:

- Provides a simple text-based interface
- Supports scripting and automation
- Offers quick access to the system

.. code-block:: python

    from exo.interfaces.cli.main import ExoCLI

    # Create the CLI
    cli = ExoCLI()

    # Run the CLI
    cli.run()

You can also use the command-line interface:

.. code-block:: bash

    python -m exo.interfaces.cli

Web Interface
-----------

The Web interface provides a browser-based interface for interacting with the exo system. It:

- Provides a modern web-based interface
- Supports access from any device with a web browser
- Offers a rich user experience

.. code-block:: python

    from exo.interfaces.web import run_web_interface

    # Run the web interface
    run_web_interface()

You can also use the command-line interface:

.. code-block:: bash

    python -m exo.interfaces.web

Electron Interface
---------------

The Electron interface provides a desktop application for interacting with the exo system. It:

- Provides a native desktop experience
- Supports desktop integration
- Offers additional capabilities

.. code-block:: python

    from exo.interfaces.electron import run_electron_app

    # Run the Electron app
    run_electron_app()

You can also use the command-line interface:

.. code-block:: bash

    python -m exo.interfaces.electron

Usage
-----

To use the interfaces, you can either use the interface directly or use the run script.

Using the Interfaces Directly
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the interfaces directly:

.. code-block:: python

    # CLI interface
    from exo.interfaces.cli.main import ExoCLI
    cli = ExoCLI()
    cli.run()

    # Web interface
    from exo.interfaces.web import run_web_interface
    run_web_interface()

    # Electron interface
    from exo.interfaces.electron import run_electron_app
    run_electron_app()

You can also use the command-line interface:

.. code-block:: bash

    # CLI interface
    python -m exo.interfaces.cli

    # Web interface
    python -m exo.interfaces.web

    # Electron interface
    python -m exo.interfaces.electron

Using the Run Script
~~~~~~~~~~~~~~~~

The easiest way to run the interfaces is using the run script, which allows you to run multiple interfaces at once:

.. code-block:: bash

    python run.py --interface all

This will start all interfaces (CLI, Web, Electron, API, and MCP).

You can also specify which interfaces to run:

.. code-block:: bash

    python run.py --interface cli web

This will start the CLI and Web interfaces.

CLI Interface
-----------

The CLI interface provides a command-line interface for interacting with the exo system.

Components
~~~~~~~~

The CLI interface consists of the following components:

Main
~~~~

The Main module provides the main entry point for the CLI interface. It:

- Initializes the CLI
- Handles user input
- Generates responses

.. code-block:: python

    from exo.interfaces.cli.main import ExoCLI

    # Create the CLI
    cli = ExoCLI()

    # Run the CLI
    cli.run()

Usage
~~~~

To use the CLI interface, you can either use the ExoCLI class directly or use the command-line interface.

Using the ExoCLI Class
~~~~~~~~~~~~~~~~~~

The ExoCLI class provides a high-level interface to the CLI interface:

.. code-block:: python

    from exo.interfaces.cli.main import ExoCLI

    # Create the CLI
    cli = ExoCLI()

    # Run the CLI
    cli.run()

Using the Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use the command-line interface:

.. code-block:: bash

    python -m exo.interfaces.cli

Customization
~~~~~~~~~~

You can customize the CLI interface by:

- Modifying the ExoCLI class
- Adding custom commands
- Changing the prompt

Modifying the ExoCLI Class
~~~~~~~~~~~~~~~~~~~~~

You can modify the ExoCLI class by subclassing it:

.. code-block:: python

    from exo.interfaces.cli.main import ExoCLI

    class CustomCLI(ExoCLI):
        def __init__(self):
            super().__init__()

        def run(self):
            # Custom run implementation
            print("Custom CLI")
            super().run()

Adding Custom Commands
~~~~~~~~~~~~~~~~~

You can add custom commands by adding methods to the ExoCLI class:

.. code-block:: python

    from exo.interfaces.cli.main import ExoCLI

    class CustomCLI(ExoCLI):
        def __init__(self):
            super().__init__()

        def do_custom(self, arg):
            """Custom command."""
            print(f"Custom command: {arg}")

Changing the Prompt
~~~~~~~~~~~~~~~

You can change the prompt by setting the prompt attribute:

.. code-block:: python

    from exo.interfaces.cli.main import ExoCLI

    class CustomCLI(ExoCLI):
        def __init__(self):
            super().__init__()
            self.prompt = "custom> "

Web Interface
-----------

The Web interface provides a browser-based interface for interacting with the exo system.

Components
~~~~~~~~

The Web interface consists of the following components:

Pages
~~~~~

The Pages directory contains the Next.js pages for the Web interface. It:

- Defines the page routes
- Handles page rendering
- Manages page state

.. code-block:: javascript

    // pages/index.js
    import React from 'react';
    import Chat from '../components/Chat';

    export default function Home() {
        return (
            <div>
                <h1>exo Web Interface</h1>
                <Chat />
            </div>
        );
    }

Components
~~~~~~~~~

The Components directory contains the React components for the Web interface. It:

- Defines the UI components
- Handles component logic
- Manages component state

.. code-block:: javascript

    // components/Chat.js
    import React, { useState } from 'react';

    export default function Chat() {
        const [messages, setMessages] = useState([]);
        const [input, setInput] = useState('');

        const handleSubmit = async (e) => {
            e.preventDefault();
            if (!input) return;

            // Add user message
            setMessages([...messages, { text: input, sender: 'user' }]);

            // Send message to API
            const response = await fetch('/api/input', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: input }),
            });
            const data = await response.json();

            // Add response message
            setMessages([...messages, { text: input, sender: 'user' }, { text: data.response, sender: 'exo' }]);
            setInput('');
        };

        return (
            <div>
                <div>
                    {messages.map((message, index) => (
                        <div key={index} className={message.sender}>
                            {message.text}
                        </div>
                    ))}
                </div>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type a message..."
                    />
                    <button type="submit">Send</button>
                </form>
            </div>
        );
    }

Styles
~~~~~~

The Styles directory contains the CSS styles for the Web interface. It:

- Defines the global styles
- Defines the component styles
- Manages the theme

.. code-block:: css

    /* styles/globals.css */
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }

    .user {
        background-color: #f0f0f0;
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
    }

    .exo {
        background-color: #e0f0ff;
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
    }

Usage
~~~~

To use the Web interface, you can either use the run_web_interface function directly or use the command-line interface.

Using the run_web_interface Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The run_web_interface function provides a high-level interface to the Web interface:

.. code-block:: python

    from exo.interfaces.web import run_web_interface

    # Run the web interface
    run_web_interface()

Using the Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use the command-line interface:

.. code-block:: bash

    python -m exo.interfaces.web

Customization
~~~~~~~~~~

You can customize the Web interface by:

- Modifying the pages
- Adding custom components
- Changing the styles

Modifying the Pages
~~~~~~~~~~~~~~~

You can modify the pages by editing the files in the pages directory:

.. code-block:: javascript

    // pages/index.js
    import React from 'react';
    import Chat from '../components/Chat';

    export default function Home() {
        return (
            <div>
                <h1>Custom Web Interface</h1>
                <Chat />
            </div>
        );
    }

Adding Custom Components
~~~~~~~~~~~~~~~~~~

You can add custom components by adding files to the components directory:

.. code-block:: javascript

    // components/CustomComponent.js
    import React from 'react';

    export default function CustomComponent() {
        return (
            <div>
                <h2>Custom Component</h2>
            </div>
        );
    }

Changing the Styles
~~~~~~~~~~~~~~

You can change the styles by editing the files in the styles directory:

.. code-block:: css

    /* styles/globals.css */
    body {
        font-family: 'Helvetica Neue', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f5f5f5;
    }

    .user {
        background-color: #e0e0e0;
        padding: 15px;
        margin: 15px;
        border-radius: 15px;
    }

    .exo {
        background-color: #d0e0ff;
        padding: 15px;
        margin: 15px;
        border-radius: 15px;
    }

Electron Interface
---------------

The Electron interface provides a desktop application for interacting with the exo system.

Components
~~~~~~~~

The Electron interface consists of the following components:

Main
~~~~

The Main module provides the main entry point for the Electron app. It:

- Initializes the Electron app
- Creates the browser window
- Handles app events

.. code-block:: javascript

    // main.js
    const { app, BrowserWindow } = require('electron');
    const path = require('path');

    function createWindow() {
        const win = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                preload: path.join(__dirname, 'preload.js'),
            },
        });

        win.loadFile('index.html');
    }

    app.whenReady().then(() => {
        createWindow();

        app.on('activate', () => {
            if (BrowserWindow.getAllWindows().length === 0) {
                createWindow();
            }
        });
    });

    app.on('window-all-closed', () => {
        if (process.platform !== 'darwin') {
            app.quit();
        }
    });

Preload
~~~~~~~

The Preload module provides the preload script for the Electron app. It:

- Exposes APIs to the renderer process
- Handles IPC communication
- Provides security

.. code-block:: javascript

    // preload.js
    const { contextBridge, ipcRenderer } = require('electron');

    contextBridge.exposeInMainWorld('api', {
        send: (channel, data) => {
            ipcRenderer.send(channel, data);
        },
        receive: (channel, func) => {
            ipcRenderer.on(channel, (event, ...args) => func(...args));
        },
    });

HTML
~~~~

The HTML file provides the HTML for the Electron app. It:

- Defines the page structure
- Includes the scripts
- Includes the styles

.. code-block:: html

    <!-- index.html -->
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>exo Electron Interface</title>
        <meta http-equiv="Content-Security-Policy" content="script-src 'self';">
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <h1>exo Electron Interface</h1>
        <div id="chat">
            <div id="messages"></div>
            <form id="message-form">
                <input type="text" id="message-input" placeholder="Type a message...">
                <button type="submit">Send</button>
            </form>
        </div>
        <script src="renderer.js"></script>
    </body>
    </html>

Usage
~~~~

To use the Electron interface, you can either use the run_electron_app function directly or use the command-line interface.

Using the run_electron_app Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The run_electron_app function provides a high-level interface to the Electron interface:

.. code-block:: python

    from exo.interfaces.electron import run_electron_app

    # Run the Electron app
    run_electron_app()

Using the Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use the command-line interface:

.. code-block:: bash

    python -m exo.interfaces.electron

Customization
~~~~~~~~~~

You can customize the Electron interface by:

- Modifying the main script
- Adding custom preload scripts
- Changing the HTML and CSS

Modifying the Main Script
~~~~~~~~~~~~~~~~~~~

You can modify the main script by editing the main.js file:

.. code-block:: javascript

    // main.js
    const { app, BrowserWindow } = require('electron');
    const path = require('path');

    function createWindow() {
        const win = new BrowserWindow({
            width: 1024,
            height: 768,
            webPreferences: {
                preload: path.join(__dirname, 'preload.js'),
            },
        });

        win.loadFile('index.html');
        win.webContents.openDevTools();
    }

    app.whenReady().then(() => {
        createWindow();

        app.on('activate', () => {
            if (BrowserWindow.getAllWindows().length === 0) {
                createWindow();
            }
        });
    });

    app.on('window-all-closed', () => {
        if (process.platform !== 'darwin') {
            app.quit();
        }
    });

Adding Custom Preload Scripts
~~~~~~~~~~~~~~~~~~~~~~~

You can add custom preload scripts by editing the preload.js file:

.. code-block:: javascript

    // preload.js
    const { contextBridge, ipcRenderer } = require('electron');

    contextBridge.exposeInMainWorld('api', {
        send: (channel, data) => {
            ipcRenderer.send(channel, data);
        },
        receive: (channel, func) => {
            ipcRenderer.on(channel, (event, ...args) => func(...args));
        },
        platform: process.platform,
    });

Changing the HTML and CSS
~~~~~~~~~~~~~~~~~~~

You can change the HTML and CSS by editing the index.html file and adding a styles.css file:

.. code-block:: html

    <!-- index.html -->
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Custom Electron Interface</title>
        <meta http-equiv="Content-Security-Policy" content="script-src 'self';">
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <h1>Custom Electron Interface</h1>
        <div id="chat">
            <div id="messages"></div>
            <form id="message-form">
                <input type="text" id="message-input" placeholder="Type a message...">
                <button type="submit">Send</button>
            </form>
        </div>
        <script src="renderer.js"></script>
    </body>
    </html>

.. code-block:: css

    /* styles.css */
    body {
        font-family: 'Helvetica Neue', sans-serif;
        margin: 0;
        padding: 20px;
        background-color: #f5f5f5;
    }

    h1 {
        color: #333;
    }

    #chat {
        margin-top: 20px;
    }

    #messages {
        height: 400px;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 10px;
        margin-bottom: 10px;
    }

    #message-form {
        display: flex;
    }

    #message-input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    button {
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        margin-left: 10px;
        cursor: pointer;
    }

    button:hover {
        background-color: #45a049;
    }
