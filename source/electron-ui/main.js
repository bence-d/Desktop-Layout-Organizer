const { app, BrowserWindow } = require('electron')

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        frame: true,
        icon: 'img/squid-logo.ico'
    }
)

//win.webContents.openDevTools()
win.removeMenu()

win.loadFile('index.html')
}

app.whenReady().then(() => {
    createWindow()
})