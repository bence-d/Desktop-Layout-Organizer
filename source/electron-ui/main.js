const { app, BrowserWindow, utilityProcess } = require('electron');
const { spawn, exec, execSync } = require('node:child_process');

let win = null;

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
    // start API server
    exec('assets\\api-server\\dist\\dhapi.exe', function (err, data) {
        if (err) {
            console.error(`[DHAPI] > Error: ${err.message}`);
            return;
        } else {
            console.log(`[DHAPI] > data`);
        }
    })

    // run the executable that kills the API server)
    win.on('close', () => {
        execSync('assets\\api-server\\dist\\terminate_api.exe', function (err, data) {
            if (err) {
                console.error(`[DHAPI] > Error: ${err.message}`);
                return;
            } else {
                console.log(`[DHAPI] > data`);
            }
        })
    });
}