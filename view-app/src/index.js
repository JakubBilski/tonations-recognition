const { app, BrowserWindow } = require('electron');
let path = require('path');
let url = require('url')
const {ipcMain} = require('electron')  

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) { // eslint-disable-line global-require
  app.quit();
}

const process = require('child_process');
var executablePath = ".\\main.exe";
var parameters = ["--http"];

var child = process.spawn(executablePath, parameters); 
child.on('error', function(err) {
  console.log('stderr: <'+err+'>' );
});

child.stdout.on('data', function (data) {
  console.log(data);
});

child.stderr.on('data', function (data) {
  console.log('stderr: <'+data+'>' );
});

child.on('close', function (code) {
    if (code == 0)
      console.log('child process complete.');
    else
      console.log('child process exited with code ' + code);
});

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 1000,
    height: 600,
    minWidth: 800,
    webPreferences: {
      enableRemoteModule: true,
      nodeIntegration: false,
      contextIsolation: false,
    preload: path.join(__dirname, "open_dialog.js")}
    
  });
  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));
  
  mainWindow.setMenuBarVisibility(false);
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  child.kill()
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.

