# Miniconda

安裝 Miniconda 在 Ubuntu 系統上是一個相對簡單的過程。以下是詳細的步驟：

1. **更新系統包**：
   首先，更新系統的軟體包列表，確保你擁有最新的軟體版本。

   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **下載 Miniconda 安裝腳本**：
   使用 `wget` 或 `curl` 下載最新版本的 Miniconda 安裝腳本。你可以從 Miniconda 的官方網站獲取下載鏈接。

   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   ```

3. **驗證下載文件（可選）**：
   你可以使用 SHA-256 校驗碼來驗證下載文件的完整性。官方網站會提供這個校驗碼。

   ```bash
   sha256sum Miniconda3-latest-Linux-x86_64.sh
   ```

   比較輸出的校驗碼與網站提供的校驗碼是否一致。

4. **運行安裝腳本**：
   使下載的腳本可執行並運行安裝程序。

   ```bash
   chmod +x Miniconda3-latest-Linux-x86_64.sh
   ./Miniconda3-latest-Linux-x86_64.sh -b -u
   ```

   按照屏幕上的提示進行安裝，通常包括接受許可協議、選擇安裝目錄等。

5. **初始化 Miniconda**：
   安裝完成後，你需要初始化 Miniconda，使其在每次啟動 shell 時自動加載。

```bash
echo 'export PATH=~/miniconda3/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

6. **驗證安裝**：
   驗證 Miniconda 是否已正確安裝，並檢查 conda 版本。

   ```bash
   conda --version
   ```

這樣，你就已經成功在 Ubuntu 上安裝了 Miniconda。隨後你可以使用 `conda` 命令來管理 Python 環境和包。