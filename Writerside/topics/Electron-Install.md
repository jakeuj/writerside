# Electron-Install

Auto Install Electron with .sh script

```bash

## 安裝 Electron

```bash
#!/bin/bash

# 檢查是否為 WSL
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null; then
    echo "Running on WSL"

    TAIWAN_MIRROR="http://tw.archive.ubuntu.com/ubuntu"

    # 檢查 /etc/apt/sources.list 是否包含台灣伺服器
    if ! grep -q "$TAIWAN_MIRROR" /etc/apt/sources.list; then
        echo "Updating sources.list to use Taiwan mirror..."
        sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
        sudo sed -i 's|deb http://archive|deb http://tw.archive|g' /etc/apt/sources.list
        sudo apt update
        sudo apt upgrade -y
    else
        echo "The sources.list is already using the Taiwan mirror."
    fi
    # 更新並安裝基本套件
    sudo apt install -y curl build-essential libnss3 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libgbm1 libasound2 \
    libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libxrandr2 libxrender1 libxtst6 \
    libxss1 libnss3 libasound2 xdg-utils dbus-user-session
else
    echo "Not running on WSL"
    # TODO: Add support for native Linux
fi

# 安裝 NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# 安裝 Node.js 和 npm
nvm install node
nvm use node

# 安裝 Yarn
npm install -g yarn

# 創建並初始化新的測試專案
mkdir -p ~/my-electron-app
cd ~/my-electron-app
yarn init -y

# 安裝 Electron
yarn add --dev electron

# 創建 index.js
cat <<EOL > index.js
const { app, BrowserWindow } = require('electron');

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  });

  win.loadFile('index.html');
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
EOL

# 創建 index.html
cat <<EOL > index.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Hello World!</title>
  </head>
  <body>
    <h1>Hello World!</h1>
  </body>
</html>
EOL

# 設置執行權限
chmod +x ~/my-electron-app/index.js

echo "環境配置完成，通過 'yarn electron .' 在 '~/my-electron-app' 目錄中運行。"

if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null; then
  echo "Running on WSL，重啟 Ubuntu 環境以啟動 D-Bus 會話服務。"
  sudo reboot
fi
```

## 執行

```bash
source ~/.bashrc
cd ~/my-electron-app
yarn electron .
```

![HelloWolrd.png](HelloWolrd.png){style="block"}

## 非 WSL 顯示遠端 Ubuntu 的 electron 畫面

1. 首先在自己電腦下載安裝執行 VcXsrv Windows X Server
    參照：[GUI-VcXsrv](GUI-VcXsrv.md)
    P.S. 記得 `Disable access control`

2. 從 Windows PoserShell ssh 到遠端 Ubuntu
    ```Shell
    ssh trx50@192.168.1.2
    ```
   P.S. 192.168.1.2 需改成實際遠端 IP

3. 設定 Ubuntu 環境變數 `DISPLAY` 到自己 Windows 的 IP
    ```bash
    export DISPLAY=192.168.1.3:0
    ```
    P.S. 192.168.1.3 需改成實際 Windows IP

4. 執行 electron 應用程式
    ```bash
    my-electron-app
    ```
   P.S. `my-electron-app` 為自己打包安裝後的應用程式名稱，不然 `yarn electron .` 也可以
   
這樣就會在 Windows 直接顯示遠端 Ubuntu 的 electron 畫面。

![xWindows.png](xWindows.png){style="block"}

## REF

這些套件在 WSL 2 (Windows Subsystem for Linux 2) 上的用途如下：

1. **curl**：用於從命令行傳輸數據的工具，支持多種協議（如 HTTP、FTP 等）。

2. **build-essential**：提供了編譯軟件所需的基本工具，包括 GCC 編譯器和相關的庫。

3. **libnss3**：網絡安全服務庫，用於支持 SSL/TLS。

4. **libatk1.0-0**：提供了無障礙工具包，允許無障礙技術與 GUI 應用程序交互。

5. **libatk-bridge2.0-0**：AT-SPI 的橋接庫，允許無障礙技術與 GTK 應用程序交互。

6. **libgtk-3-0**：GTK+ 3 圖形工具包庫，用於構建圖形用戶界面。

7. **libgbm1**：通用緩衝區管理器，提供抽象層來管理圖形內存。

8. **libasound2**：ALSA（高級 Linux 聲音架構）的庫，用於聲音設備的音頻處理。

9. **libx11-xcb1**：X11 協議的庫，支持 XCB（X 協議 C 語言綁定）。

10. **libxcomposite1**：X11 合成擴展庫，允許窗口的部分重繪。

11. **libxcursor1**：X 窗口系統的游標管理庫。

12. **libxdamage1**：X11 損壞通知擴展庫，提供窗口損壞的通知。

13. **libxfixes3**：X11 修正擴展庫，提供多種小的修正功能。

14. **libxi6**：X11 輸入設備擴展庫，支持多種輸入設備。

15. **libxrandr2**：X11 動態縮放和旋轉擴展庫，支持屏幕分辨率和方向的動態變更。

16. **libxrender1**：X11 渲染擴展庫，提供高效的圖形渲染功能。

17. **libxtst6**：X11 測試擴展庫，允許程序模擬用戶輸入。

18. **libxss1**：X11 螢幕保護擴展庫，管理螢幕保護程序。

19. **xdg-utils**：一組桌面獨立的命令行工具，用於整合桌面應用程序和工具。

20. **dbus-user-session**：用於啟動 D-Bus 會話服務的工具。

這些套件主要用於支持和運行圖形用戶界面應用程序，以及提供開發和編譯環境的基本功能。
在 WSL 2 上安裝這些套件，可以使 Linux 系統更好地支持各種應用程序的運行需求。