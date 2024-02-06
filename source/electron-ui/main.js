const { app, BrowserWindow, utilityProcess } = require('electron');
const { spawn, exec, execSync } = require('node:child_process');
const path = require('node:path');

let win = null;
let apiServerPath = "";

const createWindow = () => {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        frame: true,
        icon: 'img/squid-logo-3.0.ico'
    }
)

// win.webContents.openDevTools()
win.removeMenu()

win.loadFile('index.html')
}

app.whenReady().then(() => {
    createWindow();
    startAPI();
})

/**
 * Handles the API Server, start it kills it upon closing the application
 * Checks the PIDs of the API Server and kills them when the window is closed.
 */
const startAPI = () => {  

    var env = process.env.NODE_ENV || 'production';

    if (env === 'production') {
        apiServerPath = path.join(__dirname, '..', 'assets', 'api-server', 'dist');
    } else {
        apiServerPath = path.join(__dirname, 'assets', 'api-server', 'dist');
    }

    // I assume execSync works with absolute paths, since the built version of the application is throwing error not finding the assets folder...
    // prepend spaces in the path to avoid errors
    apiServerPath = `"${apiServerPath}"`;


    // start API server
    exec(path.join(apiServerPath, 'dhapi.exe'), function (err, data) {
        if (err) {
            console.error(`[DHAPI] > Error: ${err.message}`);
            return;
        } else {
            console.log(`[DHAPI] > data`);
        }
    })

    // run the executable that kills the API server
    win.on('close', () => {
        execSync(path.join(apiServerPath, 'terminate_api.exe'), function (err, data) {
            if (err) {
                console.error(`[DHAPI] > Error: ${err.message}`);
                return;
            } else {
                console.log(`[DHAPI] > data`);
            }
        })
    });
}