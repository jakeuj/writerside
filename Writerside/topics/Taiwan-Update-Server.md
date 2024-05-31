# Taiwan Update Server

可以的，你可以將 WSL 中的 Ubuntu 的 APT 更新伺服器改為台灣的伺服器。以下是具體步驟：

1. 打開 WSL 的 Ubuntu 終端機。

2. 編輯 APT 源列表檔案：
   ```bash
   sudo nano /etc/apt/sources.list
   ```

3. 將文件中的所有 URL 替換為台灣的更新伺服器。以下是台灣的 Ubuntu 更新伺服器 URL，可以用這些替換文件中的原有內容：

   ```
   deb http://tw.archive.ubuntu.com/ubuntu/ focal main restricted
   deb http://tw.archive.ubuntu.com/ubuntu/ focal-updates main restricted
   deb http://tw.archive.ubuntu.com/ubuntu/ focal universe
   deb http://tw.archive.ubuntu.com/ubuntu/ focal-updates universe
   deb http://tw.archive.ubuntu.com/ubuntu/ focal multiverse
   deb http://tw.archive.ubuntu.com/ubuntu/ focal-updates multiverse
   deb http://tw.archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse
   deb http://security.ubuntu.com/ubuntu focal-security main restricted
   deb http://security.ubuntu.com/ubuntu focal-security universe
   deb http://security.ubuntu.com/ubuntu focal-security multiverse
   ```

4. 保存文件並退出編輯器（在 Nano 中按 `Ctrl+X`，然後按 `Y`，最後按 `Enter`）。

5. 更新 APT 包清單：
   ```bash
   sudo apt update
   ```

這樣你就將 WSL 的 Ubuntu APT 更新伺服器改為台灣的伺服器了。