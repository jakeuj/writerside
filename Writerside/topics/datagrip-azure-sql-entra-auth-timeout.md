# DataGrip 連線 Azure SQL：Microsoft Entra Default 驗證 20 秒逾時排錯

<web-summary>DataGrip 使用 Microsoft Entra ID Default 連線 Azure SQL 出現 switchIfEmpty 20 秒逾時時，可從 macOS GUI PATH 與 Azure CLI 自動更新輸出污染快速定位並修復。</web-summary>

DataGrip 使用 `Microsoft Entra ID Default` 連線 Azure SQL 時，如果出現以下錯誤，先不要調高 SQL timeout，也不要急著修改 firewall 或資料庫權限：

```text
Did not observe any item or terminal signal within 20000ms in 'switchIfEmpty'
(and no fallback has been configured).
```

這通常表示 Microsoft JDBC Driver 在等待 `DefaultAzureCredential` 取得 access token。本次實際遇到兩層問題：DataGrip 的 macOS GUI process 起初找不到 Homebrew 安裝的 `az`；補好 GUI `PATH` 後，Azure CLI 的 auto-upgrade warning 又污染了原本應是 JSON 的輸出。最後關閉 Azure CLI auto-upgrade，並透過 Homebrew 更新 Azure CLI 後恢復正常。

> 本文已將 server、database、tenant、subscription、帳號與本機路徑去識別化。驗證 access token 時只輸出 metadata，不要把 token 寫進終端紀錄或文章。

## 快速修復

如果 `az` 是用 Homebrew 安裝，而且 DataGrip 由 Finder、Dock 或 JetBrains Toolbox 啟動，可依序處理。

先讓之後登入的 macOS GUI user domain 能找到 Azure CLI：

```bash
sudo launchctl config user path "/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin"
```

這項設定需要重新開機才會完整套用。重開機後，再關閉 Azure CLI auto-upgrade，並交由原本的 Homebrew 更新：

```bash
az config set auto-upgrade.enable=no
brew update
brew upgrade azure-cli
az version --query '"azure-cli"' -o tsv
```

最後確認 Azure SQL token 指令只輸出乾淨的 JSON，再回 DataGrip 執行 **Test Connection**：

```bash
az account get-access-token \
  --resource https://database.windows.net/ \
  --query '{tenant:tenant,subscription:subscription,expiresOn:expires_on}' \
  -o json
```

## 為什麼是固定 20 秒

`ActiveDirectoryDefault` 會使用 Azure Identity 的 `DefaultAzureCredential` credential chain。不同 JDBC 與 Azure Identity 版本包含的 credential 與順序可能不同；Azure CLI 是其中一種可能來源。

Microsoft JDBC Driver 13.2.1 的 `SQLServerSecurityUtility` 對 DefaultAzureCredential token request 設有 20,000 ms 上限。因此 credential chain 卡住時，外層常只看到 Reactor 的 `switchIfEmpty` 逾時訊息。單獨調高 DataGrip 的 `loginTimeout` 不會移除這個版本內部的 20 秒 token wait cap。

先記錄 DataGrip log 中的 JDBC Driver 與 Azure Identity 版本，再套用版本相關判斷；後續版本的實作可能改變。

## 第一步：從 DataGrip log 確認故障層

在 DataGrip 使用 **Help > Show Log in Finder** 開啟 log 目錄，或在 macOS 搜尋目前的 JetBrains logs：

```bash
rg -n -C 12 \
  "switchIfEmpty|getDefaultAzureCredAuthToken|Auth provider:|DatabaseConnectionEstablisher" \
  "$HOME/Library/Logs/JetBrains" \
  --glob 'idea.log*'
```

以下訊號代表問題發生在 token acquisition：

- `SQLServerSecurityUtility.getDefaultAzureCredAuthToken`
- `Auth provider: ms-azure-active-directory-default`
- `switchIfEmpty` 與 `20000ms`

DataGrip 顯示 DBMS、driver 或 Azure SQL effective version，只能證明 client 已取得部分連線資訊，不能據此判定 Microsoft Entra 驗證已完成。

如果錯誤已變成 `Login failed for user '<token-identified principal>'`，代表 token acquisition 大致成功，下一步應檢查 Azure SQL 的 Microsoft Entra administrator、contained database user、目標 database 與 roles，而不是繼續調整 `PATH`。

## 第二步：分開驗證登入狀態與網路

先確認目前 Azure CLI 使用的 account、subscription 與 tenant。輸出可辨識資訊前，仍應留意終端紀錄與分享範圍：

```bash
az account show \
  --query '{subscription:name,subscriptionId:id,tenantId:tenantId,user:user.name}' \
  -o json
```

再用不包含 access token 的查詢確認 Azure SQL token 能否取得：

```bash
az account get-access-token \
  --resource https://database.windows.net/ \
  --query '{tenant:tenant,subscription:subscription,expiresOn:expires_on}' \
  -o json
```

把 server endpoint 設為測試變數，另外確認 DNS 與 TCP 1433：

```bash
SQL_SERVER_FQDN="example.database.windows.net"

dig +short "$SQL_SERVER_FQDN"
nc -vz -G 5 "$SQL_SERVER_FQDN" 1433
```

token acquisition 與 TCP reachability 是兩道不同的 gate。兩者分開測試，才不會在 credential 失敗時誤改 network，或在 network timeout 時反覆重登 Azure CLI。

## 第三步：確認 DataGrip 的 GUI PATH

在 Terminal 執行 `az` 成功，不代表 Finder、Dock 或 JetBrains Toolbox 啟動的 DataGrip 也找得到它。Terminal 會載入 shell 設定；GUI app 通常繼承 macOS `launchd` 提供的環境，不會讀取 `.zshrc`。

先確認 Azure CLI 的實際位置與 GUI user domain 的 `PATH`：

```bash
command -v az
launchctl getenv PATH
```

Apple Silicon 上以 Homebrew 安裝的 Azure CLI 通常位於 `/opt/homebrew/bin/az`。如果 GUI `PATH` 沒有 `/opt/homebrew/bin`，可設定未來 user domain 的預設值：

```bash
sudo launchctl config user path "/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin"
```

### `launchctl config user path` 的影響

這不是只修改 DataGrip，而是修改之後由該 macOS user domain 啟動之服務與 GUI apps 的預設 `PATH`，並且需要重新開機才能完整生效。

主要副作用如下：

- 所有從該 user domain 啟動的 GUI apps 都可能看到新增的指令目錄。
- `PATH` 的先後順序決定同名指令採用哪一份；把 macOS system directories 放前面，可降低 Homebrew 指令意外覆蓋系統指令的風險。
- 已經執行中的 Toolbox、DataGrip 或 helper process 不會自動取得新環境，必須在重新開機後重新啟動。
- 後續如果移除 Homebrew，殘留的路徑通常只會造成無效搜尋，但仍應同步整理設定。

重開機後，可檢查執行中的 DataGrip 是否真的繼承新值：

```bash
datagrip_pid=$(pgrep -f '/DataGrip.app/Contents/MacOS/datagrip' | head -n 1)

ps eww -p "$datagrip_pid" -o command= \
  | tr ' ' '\n' \
  | rg '^PATH='
```

### Toolbox shell script 有沒有用

JetBrains Toolbox 產生的 shell script 適合從 Terminal 用短指令開啟 IDE；這時 DataGrip 會繼承 Terminal 的 `PATH`。但它不會改變從 Toolbox GUI、Finder 或 Dock 啟動 DataGrip 時的環境，因此不能單獨解決 GUI launch 的 `PATH` 問題。

也不要直接修改 Toolbox 自動產生的 launcher，因為 Toolbox 更新時可能重新產生檔案。如果只想影響 DataGrip，不想改整個 user domain，可以自行建立 per-app wrapper，在 wrapper 裡 export `PATH` 後直接執行 DataGrip binary。

若不需要 `DefaultAzureCredential` 的無提示登入，也可以在 DataGrip 改選 `Microsoft Entra ID Interactive`，透過 browser 完成授權，避開依賴本機 Azure CLI 的這條 credential path。

## 第四步：檢查 Azure CLI 輸出是否被污染

如果 DataGrip 已看得到 `az`，但仍出現同一個 20 秒錯誤，檢查 auto-upgrade 設定：

```bash
az config get auto-upgrade
```

當 `auto-upgrade.enable=yes`，Azure CLI 在偵測到新版本時可能先輸出 warning，例如：

```text
WARNING: New Azure CLI version available. Running 'az upgrade' to update automatically.
WARNING: Unable to prompt for auto upgrade as no tty available.
```

Azure Identity 透過 child process 呼叫 `az account get-access-token` 時，預期收到可解析的 JSON。若前面混入 warning，解析可能失敗並出現類似訊息：

```text
Unrecognized token 'WARNING'
```

關閉 auto-upgrade，讓 machine-readable command output 保持穩定：

```bash
az config set auto-upgrade.enable=no
```

Microsoft 文件也提醒，upgrade prompt 與 output messages 可能中斷變數接值或 automation flow。`auto-upgrade.prompt=no` 只是不要求確認，仍可能顯示 upgrade warning；對 JSON consumer 而言，停用 auto-upgrade 並由 package manager 主動更新較穩定。

如果 Azure CLI 原本由 Homebrew 安裝，就繼續使用同一個 package manager 更新：

```bash
brew update
brew upgrade azure-cli
az version --query '"azure-cli"' -o tsv
```

## 驗證順序

修正後依序驗證：

1. `az account get-access-token` 只回傳 JSON，前面沒有 auto-upgrade warning。
2. metadata 中的 tenant 與 subscription 是預期環境。
3. DNS 與 TCP 1433 可達。
4. 重新執行 DataGrip **Test Connection**。
5. 若仍失敗，只看最新一次連線測試對應的 log block。
6. 如果錯誤內容改變，依新的 layer 排查，不要繼續重複修改 `PATH`。

## 常見錯誤邊界

- `getDefaultAzureCredAuthToken` 加上 `switchIfEmpty`：優先檢查 token credential chain、GUI `PATH` 與 Azure CLI output。
- `Login failed for user '<token-identified principal>'`：token 已送到 SQL，改查 database user、Microsoft Entra administrator、database 與 roles。
- DNS 或 TCP timeout：改查 firewall、Private Endpoint、VPN、routing 與 port 1433。
- Certificate 或 hostname validation error：獨立檢查 TLS；不要把 `trustServerCertificate=true` 當預設解法。
- 只增加 `loginTimeout`：無法解決 JDBC Driver 13.2.1 內部的 20 秒 token wait cap。
- 只建立 Toolbox shell script：無法改變從 GUI 啟動 DataGrip 的 `PATH`。

## 參考資料

- [DataGrip：連線 Azure SQL Database](https://www.jetbrains.com/help/datagrip/azure-sql-database.html)
- [Microsoft JDBC Driver：使用 Microsoft Entra 驗證連線](https://learn.microsoft.com/sql/connect/jdbc/connecting-using-azure-active-directory-authentication)
- [Microsoft Learn：更新 Azure CLI 與 auto-upgrade](https://learn.microsoft.com/cli/azure/update-azure-cli)
- [Microsoft JDBC Driver 13.2.1：SQLServerSecurityUtility.java](https://github.com/microsoft/mssql-jdbc/blob/v13.2.1/src/main/java/com/microsoft/sqlserver/jdbc/SQLServerSecurityUtility.java)
