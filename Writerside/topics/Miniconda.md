# Miniconda

完整安裝步驟

1. **下載 Miniconda 安裝腳本**：
   首先，下載 Miniconda 安裝腳本：

   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/Miniconda3-latest-Linux-x86_64.sh
   ```

2. **運行安裝腳本**：
   使用 `bash` 運行安裝腳本，並使用 `-b` 標誌以無交互模式進行安裝，指定安裝目錄為 `/opt/miniconda3`：

   ```bash
   sudo bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -u -p /opt/miniconda3
   ```

-u 標誌表示更新已安裝的軟件包，以確保安裝的 Miniconda 版本是最新的。

1. **初始化 Conda**：
   初始化 Conda 來配置環境變數和 shell 設置：

   ```bash
   /opt/miniconda3/bin/conda init bash
   ```

2. **加載新的 PATH**：
   使當前 shell 會話加載新的 PATH 設置：

   ```bash
   source ~/.bashrc
   ```

3. **驗證安裝**：
   驗證 `conda` 是否已正確安裝並可用：

   ```bash
   conda --version
   ```

這樣，你應該可以在無交互模式下成功安裝 Miniconda 到 `/opt/miniconda3` 並配置系統 PATH，使 `conda` 命令可用。。
