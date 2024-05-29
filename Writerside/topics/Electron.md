# Electron

使用 Electron 呼叫 Python 與 Shell Script

## 參考

[electronjs](https://www.electronjs.org/zh/docs/latest/tutorial/quick-start)

## 必要環境

- [Node.js](https://nodejs.org/en/download/package-manager)

## 建立專案

```bash
mkdir my-electron-app && cd my-electron-app
yarn init
yarn add --dev electron
```

## 執行

需要新增 `"start": "electron ."` 到 package.json 的 scripts 中。

package.json
```json
{
  "name": "my-electron-app",
  "version": "1.0.0",
  "description": "test",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "jakeuj",
  "license": "MIT",
  "devDependencies": {
    "electron": "^30.0.8"
  }
}

```

以後可以用以下命令執行

```bash
yarn start
```

## 執行 Python

script.py
```Python
# script.py
import sys
print("Hello from Python!")
sys.stdout.flush()
```

## 執行 Shell Script

```Bash
#!/bin/bash
echo "Hello from Shell Script!"
```

## HTML

index.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Electron App</title>
</head>
<body>
    <h1>Hello from Electron!</h1>
    <pre id="python-output"></pre>
    <pre id="shell-output"></pre>
    <script>
        const { ipcRenderer } = require('electron');
        ipcRenderer.on('python-output', (event, output) => {
            document.getElementById('python-output').innerText = output;
        });
        ipcRenderer.on('shell-output', (event, output) => {
            document.getElementById('shell-output').innerText = output;
        });
    </script>
</body>
</html>
```

## 主程式

mina.js
```JavaScript
const { app, BrowserWindow, ipcMain } = require('electron');
const { exec } = require('child_process');
const path = require('path');

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');

    // 執行 Python 腳本
    exec('python script.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
        // 將 Python 腳本的輸出發送到渲染進程
        mainWindow.webContents.send('python-output', stdout);
    });

    // 使用 Git Bash 執行 Shell 腳本
    exec('bash script.sh', { shell: 'C:\\Program Files\\Git\\bin\\bash.exe' }
        , (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
        // 將 Shell 腳本的輸出發送到渲染進程
        mainWindow.webContents.send('shell-output', stdout);
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
```

## 結果

應該可以在畫面上看到 Python 與 Shell Script 的輸出。