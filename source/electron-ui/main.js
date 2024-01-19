const { app, BrowserWindow, utilityProcess } = require('electron');
const { spawn, exec } = require('node:child_process');

let win = null;
const foreignPythonProcesses = []; // PIDs of Python processes that were already running before the API Server was started
let ownPythonProcesses = []; // PIDs of Python processes that were started by the API Server

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
const startAPI = async () => {   
    let apiReady = false; // disables PID checking after the PIDs of the API Server have been found

    // Check all Python processes before starting the API Server
    getAllPythonPIDs(foreignPythonProcesses, async () => {
        if (process.env.NODE_ENV == 'development') {
            spawn('pythonw', ['./assets/api-server/dhapi.py']);
        } else {
            // Path to the executable when the app is built
            spawn('pythonw', ['./resources/assets/api-server/dhapi.py']);
        }

        // Wait until 3 additional Python procecces have been started
        while (ownPythonProcesses.length < 3) {

            // Check all Python processes every 100ms after starting the API Server
            getAllPythonPIDs(ownPythonProcesses, () => {

                let tempOwnPythonProcesses = []; // By saving the PIDs in a temporary array, we can remove them from the original array without causing problems. (You shouldn't remove items from a list when iterating it) 

                // Remove processes that were already running before the API Server was started
                for (let i = 0; i < ownPythonProcesses.length; i++) {
                    const pid = ownPythonProcesses[i];
                    if (!foreignPythonProcesses.includes(pid)) {
                        tempOwnPythonProcesses.push(pid);
                    }
                }

                ownPythonProcesses = tempOwnPythonProcesses;
            });

            // sleep for 100ms
            await new Promise(r => setTimeout(r, 100));
        } 
    });

    win.on('close', () => {
        // Kill all owned Python processes
        for (let i = 0; i < ownPythonProcesses.length; i++) {
            exec('taskkill /t /f /pid ' + ownPythonProcesses[i]);
        }
    });
}   

/**
 * Requests all Python PIDs from the Windows Task Manager.
 * @param {actList} the list to store the requested python PIDs in.
 * @param {callback} the function to call after the PIDs have been requested and saved.
 */
function getAllPythonPIDs(actList, callback) {
    exec('tasklist /FI "IMAGENAME eq pythonw.exe" /FO csv', (error, stdout) => {
        if (error) {
            console.error(`Error: ${error.message}`);
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
            actList.push(pid);
        }

        callback();
    });

}


