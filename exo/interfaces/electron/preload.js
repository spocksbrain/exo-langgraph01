// Preload script for the Electron app
const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld(
  'api', {
    selectPythonPath: () => {
      ipcRenderer.send('select-python-path');
    },
    getPythonPath: () => {
      ipcRenderer.send('get-python-path');
    },
    restartServers: () => {
      ipcRenderer.send('restart-servers');
    },
    onPythonPathSelected: (callback) => {
      ipcRenderer.on('python-path-selected', (_, path) => callback(path));
    },
    onPythonPath: (callback) => {
      ipcRenderer.on('python-path', (_, path) => callback(path));
    }
  }
);
