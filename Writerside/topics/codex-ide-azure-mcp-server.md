# Codex IDE 使用 Azure MCP Server

這篇筆記整理如何把 Azure MCP Server 接到 Codex IDE，並用實際查詢確認設定已經生效。

> 本文中的 subscription 名稱、subscription ID、tenant ID、resource group、email、路徑與查詢結果皆已去識別化，請替換成你自己的 Azure 環境資訊。

## 問題描述

Microsoft Learn 已經提供 Azure MCP Server 的安裝與 Manual Setup，但沒有直接用 `Codex IDE` 當主角說明。

這次實測後可以整理成一個很直接的結論：

- Codex CLI 與 Codex IDE extension 共用同一份 MCP 設定。
- 本機 `stdio` 模式下，Azure MCP Server 會直接使用你機器上的 Azure 認證。
- 在 macOS 上，最省事的做法通常是直接用 `npx` 啟動 `@azure/mcp`。

## 先講結論

如果你的環境已經有：

- `node`
- `npx`
- `az`
- 已完成 `az login`

那最簡單的設定方式就是：

```bash
codex mcp add azure -- npx -y @azure/mcp@latest server start
```

如果你想讓認證來源更明確，建議在 Codex 設定裡固定使用 Azure CLI credential：

```toml
[mcp_servers.azure]
command = "npx"
args = ["-y", "@azure/mcp@latest", "server", "start"]
startup_timeout_sec = 60

[mcp_servers.azure.env]
AZURE_TOKEN_CREDENTIALS = "AzureCliCredential"
```

## 前置條件

先確認本機有這些工具：

```bash
node --version
npx --version
az version
codex mcp --help
```

如果 Azure CLI 還沒登入，先完成登入並切到正確的 subscription：

```bash
az login
az account list -o table
az account set --subscription "<subscription-name-or-id>"
az account show -o json
```

如果你有多個 subscription，這一步很重要，因為後續 Azure MCP 查詢會沿用目前的 Azure 登入上下文。

## 操作步驟

### 1. 用 Codex CLI 新增 Azure MCP Server

```bash
codex mcp add azure -- npx -y @azure/mcp@latest server start
```

新增後可以立即確認：

```bash
codex mcp list
codex mcp get azure
```

如果你看到 `azure` 這個 server 已經出現在清單裡，就表示 Codex 已經讀到這筆設定。

### 2. 或直接編輯 `config.toml`

Codex 的 MCP 設定預設放在：

```text
~/.codex/config.toml
```

如果只想套用到特定專案，也可以使用專案內的：

```text
.codex/config.toml
```

可用的設定範例如下：

```toml
[mcp_servers.azure]
command = "npx"
args = ["-y", "@azure/mcp@latest", "server", "start"]
startup_timeout_sec = 60

[mcp_servers.azure.env]
AZURE_TOKEN_CREDENTIALS = "AzureCliCredential"
```

這裡把 `AZURE_TOKEN_CREDENTIALS` 固定成 `AzureCliCredential` 的好處是：

- 行為比較可預測
- 明確使用 `az login` 的登入狀態
- 比較不容易因為本機有多種 Azure credential source 而混淆

### 3. 驗證 Azure MCP 套件本身可以執行

如果想先確認 Azure MCP 套件本身沒問題，可以直接跑：

```bash
npx -y @azure/mcp@latest --help
```

如果要驗證它有沒有真的吃到目前 Azure CLI 的登入狀態，可以跑：

```bash
AZURE_TOKEN_CREDENTIALS=AzureCliCredential \
npx -y @azure/mcp@latest subscription list
```

預期會看到類似這樣的結果：

```json
{
  "status": 200,
  "message": "Success",
  "results": {
    "subscriptions": [
      {
        "subscriptionId": "<subscription-id-a>",
        "displayName": "<subscription-name-a>",
        "state": "Enabled",
        "tenantId": "<tenant-id>",
        "isDefault": true
      },
      {
        "subscriptionId": "<subscription-id-b>",
        "displayName": "<subscription-name-b>",
        "state": "Enabled",
        "tenantId": "<tenant-id>",
        "isDefault": false
      }
    ]
  }
}
```

### 4. 用 `codex exec` 做 smoke test

如果你想模擬「在 Codex 裡直接用自然語言查 Azure」的效果，可以跑：

```bash
codex exec \
  --skip-git-repo-check \
  --sandbox workspace-write \
  -C "<your-workspace>" \
  "請透過已設定的 MCP 工具列出我目前 Azure 預設 subscription 底下的前 5 個 resource groups，只回傳名稱與 location。"
```

只要你看到輸出裡有：

- `mcp: azure starting`
- `mcp: azure ready`

而且最後有成功回傳 resource groups，就表示 Codex 已經能透過 Azure MCP Server 進行查詢。

## 在 Codex IDE 裡怎麼問

設定完成後，Codex IDE 就可以直接用自然語言問 Azure：

- `列出我目前 Azure subscriptions`
- `幫我列出某個 subscription 底下所有 resource groups`
- `查某個 resource group 裡有哪些 App Service`
- `哪個 Azure resource 正在使用這個 subnet`

如果你的工作型態偏維運或盤點，這種問法通常比手寫 CLI 查詢更快。

## 常見問題

### 第一次啟動 Azure MCP 太慢

第一次用 `npx` 啟動時可能需要下載套件，建議在設定裡補：

```toml
startup_timeout_sec = 60
```

### `codex mcp list` 有 `azure`，但查不到 Azure 資源

先依序檢查：

1. `az login` 是否仍然有效
2. `az account show -o json` 是否切到正確 subscription
3. 目前登入的身份是否有足夠的 Azure RBAC 權限

### `Auth` 欄位顯示 `Unsupported`

這在本機 `stdio` 模式通常是正常現象。因為這種模式不是走 MCP 伺服器的 HTTP/OAuth inbound authentication，而是 Azure MCP Server 直接使用你本機可用的 Azure credential。

## 補充說明

- Codex CLI 與 Codex IDE extension 共用 MCP 設定，所以通常只需要設一次。
- 如果只是想快速開始，直接用 `codex mcp add azure -- npx -y @azure/mcp@latest server start` 就夠了。
- 如果你所在的機器同時有多種 Azure credential source，建議固定 `AZURE_TOKEN_CREDENTIALS = "AzureCliCredential"`，比較容易排查問題。

## 參考資料

- [開始使用 Azure MCP 伺服器 | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/developer/azure-mcp-server/get-started)
- [Azure MCP Server README](https://github.com/microsoft/mcp/blob/main/servers/Azure.Mcp.Server/README.md)
- [Authentication in Azure MCP Server](https://github.com/microsoft/mcp/blob/main/docs/Authentication.md)
- [Model Context Protocol | Codex](https://developers.openai.com/codex/mcp)
- [Configuration Reference | Codex](https://developers.openai.com/codex/config-reference)
