const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const url = require('url');
const { spawn } = require('child_process');
const Store = require('electron-store');

// Initialize store
const store = new Store();

// Keep a global reference of the window object
let mainWindow;
let apiProcess;
let mcpProcess;

// Command-line arguments
const isDev = process.argv.includes('--dev');

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, 'preload.js'),
    },
    icon: path.join(__dirname, 'assets/icon.png'),
  });

  // Load the index.html of the app
  if (isDev) {
    // In development, load from localhost
    mainWindow.loadURL('http://localhost:3000');
    
    // Open the DevTools
    mainWindow.webContents.openDevTools();
  } else {
    // In production, load the built app
    mainWindow.loadURL(
      url.format({
        pathname: path.join(__dirname, 'build/index.html'),
        protocol: 'file:',
        slashes: true,
      })
    );
  }

  // Emitted when the window is closed
  mainWindow.on('closed', function () {
    // Dereference the window object
    mainWindow = null;
    
    // Kill the API and MCP processes
    if (apiProcess) {
      apiProcess.kill();
    }
    
    if (mcpProcess) {
      mcpProcess.kill();
    }
  });
}

// Start the API server
function startApiServer() {
  // Get Python executable path
  const pythonPath = store.get('pythonPath', 'python');
  
  // Start the API server
  apiProcess = spawn(pythonPath, ['-m', 'exo', 'api']);
  
  apiProcess.stdout.on('data', (data) => {
    console.log(`API stdout: ${data}`);
  });
  
  apiProcess.stderr.on('data', (data) => {
    console.error(`API stderr: ${data}`);
  });
  
  apiProcess.on('close', (code) => {
    console.log(`API process exited with code ${code}`);
  });
}

// Start the MCP server
function startMcpServer() {
  // Get Python executable path
  const pythonPath = store.get('pythonPath', 'python');
  
  // Start the MCP server
  mcpProcess = spawn(pythonPath, ['-m', 'exo', 'mcp']);
  
  mcpProcess.stdout.on('data', (data) => {
    console.log(`MCP stdout: ${data}`);
  });
  
  mcpProcess.stderr.on('data', (data) => {
    console.error(`MCP stderr: ${data}`);
  });
  
  mcpProcess.on('close', (code) => {
    console.log(`MCP process exited with code ${code}`);
  });
}

// This method will be called when Electron has finished initialization
app.whenReady().then(() => {
  // Start the API and MCP servers
  startApiServer();
  startMcpServer();
  
  // Create the window
  createWindow();
  
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (mainWindow === null) createWindow();
  });
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

// IPC handlers
ipcMain.on('select-python-path', async (event) => {
  const result = await dialog.showOpenDialog({
    properties: ['openFile'],
    filters: [
      { name: 'Python', extensions: ['exe', ''] },
    ],
  });
  
  if (!result.canceled && result.filePaths.length > 0) {
    const pythonPath = result.filePaths[0];
    store.set('pythonPath', pythonPath);
    event.reply('python-path-selected', pythonPath);
  }
});

ipcMain.on('get-python-path', (event) => {
  const pythonPath = store.get('pythonPath', 'python');
  event.reply('python-path', pythonPath);
});

ipcMain.on('restart-servers', () => {
  // Kill existing processes
  if (apiProcess) {
    apiProcess.kill();
  }
  
  if (mcpProcess) {
    mcpProcess.kill();
  }
  
  // Start new processes
  startApiServer();
  startMcpServer();
});
