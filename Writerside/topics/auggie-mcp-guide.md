# Auggie MCP 使用指南

## 目錄

- [什麼是 MCP](#what-is-mcp)
- [配置方式](#config-methods)
- [常用命令](#common-commands)
- [配置範例](#config-examples)
- [故障排除](#troubleshooting)

---

## 什麼是 MCP {id="what-is-mcp"}

**MCP (Model Context Protocol)** 是一個開放協議,用於將 AI 模型連接到不同的數據源和工具。

### MCP 的用途 {id="mcp-purpose"}

- 訪問本地或遠程數據庫
- 運行自動化瀏覽器測試
- 發送消息到 Slack
- 與各種 API 集成
- 執行自定義工具和腳本

---

## 配置方式 {id="config-methods"}

### 方式 1: 使用 settings.json (推薦)

配置文件位置: `~/.augment/settings.json`

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    },
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### 方式 2: 使用 Auggie CLI 命令

```bash
# 添加 MCP 服務器
auggie mcp add <name> [options]

# 從 JSON 添加
auggie mcp add-json <name> <json>

# 列出所有服務器
auggie mcp list

# 刪除服務器
auggie mcp remove <name>
```

### 方式 3: 使用命令行參數

```bash
auggie --mcp-config=mcp.json "你的問題"
```

---

## 常用命令 {id="common-commands"}

### 添加 MCP 服務器 {id="add-mcp-server"}

#### Stdio 傳輸 (本地可執行文件)

```bash
# 完整語法
auggie mcp add chrome-devtools \
  --command npx \
  --args "chrome-devtools-mcp@latest"

# 簡化語法
auggie mcp add chrome-devtools -- npx chrome-devtools-mcp@latest

# 帶環境變量
auggie mcp add context7 \
  --command npx \
  --args "-y @upstash/context7-mcp@latest" \
  --env CONTEXT7_API_KEY=your_key
```

#### SSE 傳輸 (Server-Sent Events)

```bash
# 完整語法
auggie mcp add weather-api \
  --transport sse \
  --url https://weather-mcp.example.com/sse

# 簡化語法
auggie mcp add weather-api --transport sse https://weather-mcp.example.com/sse
```

#### HTTP 傳輸 (帶認證頭)

```bash
# 單個 header
auggie mcp add renderMCP \
  --transport http \
  --url https://mcp.render.com/mcp \
  --header "Authorization:Bearer YOUR_TOKEN"

# 多個 headers
auggie mcp add api-service \
  --transport http \
  --url https://api.example.com/mcp \
  --header "Authorization:Bearer YOUR_TOKEN" \
  --header "X-Custom-Header:custom-value"
```

### 從 JSON 添加

```bash
# Stdio 傳輸
auggie mcp add-json weather-api '{
  "type": "stdio",
  "command": "/path/to/weather-cli",
  "args": ["--api-key", "abc123"],
  "env": {"CACHE_DIR": "/tmp"}
}'

# HTTP 傳輸
auggie mcp add-json renderMCP '{
  "type": "http",
  "url": "https://mcp.render.com/mcp",
  "headers": {"Authorization": "Bearer ABC_XYZ_123"}
}'
```

### 管理 MCP 服務器 {id="manage-mcp-servers"}

```bash
# 列出所有配置的服務器 (表格格式)
auggie mcp list

# 列出服務器 (JSON 格式)
auggie mcp list --json

# 刪除服務器
auggie mcp remove chrome-devtools

# 替換現有服務器 (不提示)
auggie mcp add chrome-devtools --command npx --args "..." --replace

# 檢查 MCP 狀態
auggie --mcp-status
```

---

## 配置範例 {id="config-examples"}

### Chrome DevTools MCP

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    }
  }
}
```

```bash
auggie mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

### Context7 MCP (HTTP)

```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

```bash
auggie mcp add context7 \
  --transport http \
  --url https://mcp.context7.com/mcp \
  --header "CONTEXT7_API_KEY:YOUR_API_KEY"
```

### Weather API (SSE)

```json
{
  "mcpServers": {
    "weather": {
      "type": "sse",
      "url": "https://weather-mcp.example.com/v1",
      "headers": {
        "X-API-Key": "your_weather_api_key",
        "Content-Type": "application/json"
      }
    }
  }
}
```

```bash
auggie mcp add weather \
  --transport sse \
  --url https://weather-mcp.example.com/v1 \
  --header "X-API-Key:your_weather_api_key"
```

### Render MCP (HTTP with Bearer Token)

```json
{
  "mcpServers": {
    "renderMCP": {
      "type": "http",
      "url": "https://mcp.render.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_API_KEY>"
      }
    }
  }
}
```

```bash
auggie mcp add renderMCP \
  --transport http \
  --url https://mcp.render.com/mcp \
  --header "Authorization:Bearer YOUR_API_KEY"
```

### GitLab MR MCP (本地工具)

```json
{
  "mcpServers": {
    "gitlab-mr-mcp": {
      "command": "node",
      "args": ["/path/to/gitlab-mr-mcp/index.js"],
      "env": {
        "MR_MCP_GITLAB_TOKEN": "your_gitlab_token",
        "MR_MCP_GITLAB_HOST": "your_gitlab_host"
      }
    }
  }
}
```

```bash
auggie mcp add gitlab-mr-mcp \
  --command node \
  --args "/path/to/gitlab-mr-mcp/index.js" \
  --env MR_MCP_GITLAB_TOKEN=your_gitlab_token \
  --env MR_MCP_GITLAB_HOST=your_gitlab_host
```

---

## 傳輸類型說明

### 1. Stdio (標準輸入/輸出) {id="transport-stdio"}

- **用途**: 本地可執行文件或腳本
- **特點**: 通過標準輸入/輸出通信
- **配置**: 需要 `command` 和 `args`

```json
{
  "command": "npx",
  "args": ["chrome-devtools-mcp@latest"],
  "env": { "DEBUG": "true" }
}
```

### 2. SSE (Server-Sent Events) {id="transport-sse"}

- **用途**: 遠程服務器,支持實時事件流
- **特點**: 單向服務器推送
- **配置**: 需要 `type: "sse"` 和 `url`

```json
{
  "type": "sse",
  "url": "https://api.example.com/sse",
  "headers": { "X-API-Key": "key" }
}
```

### 3. HTTP {id="transport-http"}

- **用途**: 標準 HTTP API
- **特點**: 請求/響應模式
- **配置**: 需要 `type: "http"` 和 `url`

```json
{
  "type": "http",
  "url": "https://api.example.com/mcp",
  "headers": { "Authorization": "Bearer token" }
}
```

---

## 命令選項說明

### `auggie mcp add` 選項

| 選項 | 說明 | 範例 |
|------|------|------|
| `--command <path>` | 可執行文件路徑 (stdio) | `--command npx` |
| `--args <args>` | 命令參數 | `--args "chrome-devtools-mcp@latest"` |
| `-e, --env <KEY=VAL>` | 環境變量 (可重複) | `--env API_KEY=abc123` |
| `-t, --transport <type>` | 傳輸類型: stdio/sse/http | `--transport http` |
| `-u, --url <url>` | URL (sse/http 必需) | `--url https://api.example.com` |
| `-h, --header <KEY:VAL>` | HTTP header (可重複) | `--header "Authorization:Bearer token"` |
| `-r, --replace` | 覆蓋現有配置不提示 | `--replace` |
| `--json` | 輸出 JSON 格式 | `--json` |

---

## 使用場景

### 1. 開發環境配置 {id="usage-dev-config"}

```bash
# 添加開發工具
auggie mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
auggie mcp add context7 -- npx -y @upstash/context7-mcp

# 檢查配置
auggie mcp list
```

### 2. 生產環境配置 {id="usage-prod-config"}

```bash
# 使用環境變量保護敏感信息
export RENDER_API_KEY="your_secure_key"

auggie mcp add renderMCP \
  --transport http \
  --url https://mcp.render.com/mcp \
  --header "Authorization:Bearer $RENDER_API_KEY"
```

### 3. 臨時使用 MCP {id="usage-temp-mcp"}

```bash
# 使用臨時配置文件
cat > temp-mcp.json << EOF
{
  "mcpServers": {
    "test-server": {
      "command": "node",
      "args": ["./test-mcp.js"]
    }
  }
}
EOF

auggie --mcp-config=temp-mcp.json "測試問題"
```

---

## 故障排除 {id="troubleshooting"}

### 問題 1: MCP 服務器未顯示 {id="troubleshooting-problem-1"}

**症狀**: `auggie mcp list` 顯示為空

**解決方案**:
```bash
# 檢查配置文件是否存在
cat ~/.augment/settings.json

# 如果不存在,創建配置
mkdir -p ~/.augment
echo '{"mcpServers":{}}' > ~/.augment/settings.json

# 重新添加 MCP 服務器
auggie mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

### 問題 2: MCP 服務器連接失敗 {id="troubleshooting-problem-2"}

**症狀**: 使用 MCP 時出現連接錯誤

**解決方案**:
```bash
# 檢查 MCP 狀態
auggie --mcp-status

# 測試服務器是否可訪問 (HTTP/SSE)
curl -I https://mcp.example.com/mcp

# 檢查本地命令是否可執行 (stdio)
npx chrome-devtools-mcp@latest --version
```

### 問題 3: 環境變量未生效 {id="troubleshooting-problem-3"}

**症狀**: MCP 服務器無法讀取 API 密鑰

**解決方案**:
```bash
# 方法 1: 在配置中直接設置
auggie mcp add context7 \
  --command npx \
  --args "-y @upstash/context7-mcp@latest" \
  --env CONTEXT7_API_KEY=your_actual_key

# 方法 2: 在 settings.json 中設置
# 編輯 ~/.augment/settings.json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {
        "CONTEXT7_API_KEY": "your_actual_key"
      }
    }
  }
}
```

### 問題 4: 權限錯誤 {id="troubleshooting-problem-4"}

**症狀**: 無法執行 MCP 命令

**解決方案**:
```bash
# 檢查文件權限
ls -la ~/.augment/settings.json

# 修復權限
chmod 600 ~/.augment/settings.json

# 確保 npx 可用
which npx
npm install -g npx
```

---

## 最佳實踐

### 1. 安全性 {id="best-practice-security"}

- ✅ 使用環境變量存儲敏感信息
- ✅ 設置適當的文件權限 (`chmod 600`)
- ✅ 定期更新 MCP 服務器版本
- ❌ 不要在配置文件中硬編碼 API 密鑰
- ❌ 不要將 settings.json 提交到版本控制

### 2. 組織配置 {id="best-practice-organization"}

```
{
  "mcpServers": {
    // 開發工具
    "chrome-devtools": { ... },

    // API 服務
    "context7": { ... },
    "renderMCP": { ... },

    // 自定義工具
    "gitlab-mr-mcp": { ... }
  }
}
```

### 3. 命名規範 {id="best-practice-naming"}

- 使用描述性名稱: `chrome-devtools` 而不是 `cd`
- 使用小寫和連字符: `weather-api` 而不是 `WeatherAPI`
- 保持一致性: 所有 MCP 服務器使用相同的命名風格

### 4. 版本管理 {id="best-practice-versioning"}

```bash
# 使用特定版本而不是 @latest
auggie mcp add chrome-devtools -- npx chrome-devtools-mcp@1.2.3

# 或在 package.json 中管理
npm install chrome-devtools-mcp@1.2.3
auggie mcp add chrome-devtools -- npx chrome-devtools-mcp
```

---

## 進階用法

### 1. 批量添加 MCP 服務器 {id="advanced-batch-add"}

```bash
#!/bin/bash
# add-mcps.sh

# 添加多個 MCP 服務器
auggie mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
auggie mcp add context7 -- npx -y @upstash/context7-mcp@latest
auggie mcp add weather --transport sse https://weather-mcp.example.com/sse

echo "所有 MCP 服務器已添加"
auggie mcp list
```

### 2. 導出和導入配置 {id="advanced-export-import"}

```bash
# 導出當前配置
cp ~/.augment/settings.json ./mcp-backup.json

# 導入配置到新機器
cp ./mcp-backup.json ~/.augment/settings.json

# 或使用 auggie mcp add-json
cat mcp-backup.json | jq -r '.mcpServers | to_entries[] |
  "auggie mcp add-json \(.key) '\''\(.value | @json)'\''"' | bash
```

### 3. 條件性使用 MCP {id="advanced-conditional-mcp"}

```bash
# 僅在特定項目中使用特定 MCP
if [ -f "./project-mcp.json" ]; then
  auggie --mcp-config=./project-mcp.json "$@"
else
  auggie "$@"
fi
```

---

## 常見 MCP 服務器 {id="common-mcp-servers"}

### 官方和社區 MCP {id="official-community-mcp"}

| 名稱 | 類型 | 用途 | 安裝命令 |
|------|------|------|----------|
| Chrome DevTools | stdio | 瀏覽器自動化 | `npx chrome-devtools-mcp@latest` |
| Context7 | http | 上下文管理 | `npx -y @upstash/context7-mcp` |
| GitLab MR | stdio | GitLab 合併請求 | `npm install gitlab-mr-mcp` |
| Weather API | sse | 天氣數據 | 自定義 URL |
| Render | http | 部署管理 | `https://mcp.render.com/mcp` |

---

## 參考資源

- [Augment 官方文檔 - MCP 配置](https://docs.augmentcode.com/setup-augment/mcp)
- [Auggie CLI 文檔 - 集成和 MCP](https://docs.augmentcode.com/cli/integrations)
- [MCP 協議規範](https://modelcontextprotocol.io/)
- [Augment GitHub](https://github.com/augmentcode)

---

## 更新日誌

- **2026-01-28**: 初始版本創建
  - 添加基本配置說明
  - 添加常用命令範例
  - 添加故障排除指南
  - 添加最佳實踐建議

---

## 貢獻

如果您發現任何錯誤或有改進建議,請隨時更新此文檔!

---

**最後更新**: 2026-01-28
**版本**: 1.0.0

