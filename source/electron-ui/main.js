const { app, BrowserWindow, utilityProcess } = require('electron');
const { spawn, exec } = require('node:child_process');

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
 * Starts the API Server.
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

    // kill API server when window is closed
    win.on('close', () => {
        exec('tasklist /FI "IMAGENAME eq dhapi.exe" /FO csv', (error, stdout) => {
            if (err) {
                console.error(`Error: ${err.message}`);
                return;
            }
    
            const lines = stdout.split('\n');
    
            for (let i = 1; i < lines.length; i++) {
                const line = lines[i].trim();
    
                if (line.length === 0) {
                    continue;
                }
    
                const parts = line.split(',');
                const pid = parts[1];

                exec('taskkill /t /f /pid ' + pid);
            }
    
            callback();
        });

    });
}