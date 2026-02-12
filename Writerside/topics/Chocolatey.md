# Chocolatey

Chocolatey 是一個 Windows 的軟體包管理工具，專為簡化 Windows 環境下的軟體安裝、更新和管理而設計，類似於 Linux 平台的 apt 或 yum。Chocolatey 利用 PowerShell 和 NuGet 來實現自動化安裝和管理軟體包的功能，特別適合開發者和 IT 管理員使用。

![yarn.png](yarn.png){style="block"}

## 更新環境變數

使環境變數更新全局可用
使用 refreshenv 工具（適用於安裝 [Chocolatey](https://chocolatey.org/) 的系統）：

```shell
refreshenv
```

這個工具會自動重新加載環境變數。

### 主要功能

1. **軟體安裝**：可以快速安裝軟體，使用簡單的命令如 `choco install package_name`。
2. **軟體更新**：可以用 `choco upgrade` 更新已安裝的軟體。
3. **批次管理**：支援批次安裝或更新多個軟體。
4. **軟體移除**：透過 `choco uninstall package_name` 快速移除軟體。
5. **自動化腳本**：可以整合到部署腳本中，用於自動化環境建置。

### 如何安裝 Chocolatey

1. 開啟 PowerShell（以系統管理員身份執行）。
2. 執行以下命令來安裝 Chocolatey：

   ```shell
   Set-ExecutionPolicy Bypass -Scope Process -Force; `
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

3. 完成後，可以透過 `choco -v` 確認是否安裝成功。

### 常用命令

1. 安裝軟體：

   ```shell
   choco install package_name -y
   ```

   例如，安裝 Google Chrome：

   ```shell
   choco install googlechrome -y
   ```

2. 更新軟體：

   ```shell
   choco upgrade package_name -y
   ```

3. 列出已安裝的軟體包：

   ```shell
   choco list --localonly
   ```

4. 移除軟體：

   ```shell
   choco uninstall package_name -y
   ```

### 優勢

- 節省手動安裝軟體的時間。
- 支援多數常用軟體（如瀏覽器、開發工具等）。
- 易於整合到 CI/CD 流程或 IT 部署中。
- 可離線使用（需要預先下載包）。

如果你是開發者或 IT 管理人員，Chocolatey 是非常有價值的工具，尤其在大量電腦的環境建置中，能大幅提高效率。
