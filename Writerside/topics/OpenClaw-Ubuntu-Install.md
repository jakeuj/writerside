# 在 Ubuntu 上安裝 OpenClaw

OpenClaw 是一個個人 AI 助理，可以在您自己的設備上運行。本指南將說明如何在 Ubuntu 系統上安裝和設定 OpenClaw。

## 專案資訊

- **官方網站**: [openclaw.ai](https://openclaw.ai)
- **GitHub**: [openclaw/openclaw](https://github.com/openclaw/openclaw)
- **授權**: MIT License

## 系統需求

- **作業系統**: Ubuntu 20.04 或更新版本
- **Node.js**: 版本 22 或更新
- **記憶體**: 建議至少 2GB RAM
- **磁碟空間**: 至少 1GB 可用空間

## 安裝步驟

### 1. 安裝 Node.js 22+

首先，確保系統已安裝 Node.js 22 或更新版本：

```bash
# 使用 NodeSource 安裝 Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 驗證安裝
node --version
npm --version
```

### 2. 安裝 OpenClaw (推薦方式)

使用 npm 全域安裝 OpenClaw：

```bash
npm install -g openclaw@latest
```

或使用 pnpm：

```bash
# 先安裝 pnpm
npm install -g pnpm

# 安裝 OpenClaw
pnpm add -g openclaw@latest
```

### 3. 執行安裝精靈

OpenClaw 提供互動式安裝精靈，會引導您完成設定：

```bash
openclaw onboard --install-daemon
```

安裝精靈會協助您：

- 設定 Gateway (控制平面)
- 配置工作區 (workspace)
- 連接通訊頻道 (WhatsApp、Telegram、Slack 等)
- 安裝技能 (skills)

### 4. 設定系統服務 (systemd)

安裝精靈會自動設定 systemd 使用者服務，讓 Gateway 保持運行：

```bash
# 檢查服務狀態
systemctl --user status openclaw-gateway

# 啟動服務
systemctl --user start openclaw-gateway

# 設定開機自動啟動
systemctl --user enable openclaw-gateway
```

## 從原始碼安裝 (開發用)

如果您想從原始碼建置，建議使用 pnpm：

```bash
# 安裝必要工具
sudo apt-get update
sudo apt-get install -y git build-essential

# 複製專案
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 安裝相依套件
pnpm install

# 建置 UI
pnpm ui:build

# 建置專案
pnpm build

# 執行安裝精靈
pnpm openclaw onboard --install-daemon
```

### 開發模式 (自動重載)

```bash
# 啟動 Gateway 並監聽 TypeScript 變更
pnpm gateway:watch
```

## 基本使用

### 啟動 Gateway

```bash
openclaw gateway --port 18789 --verbose
```

### 發送訊息

```bash
openclaw message send --to +1234567890 --message "Hello from OpenClaw"
```

### 與助理對話

```bash
openclaw agent --message "Ship checklist" --thinking high
```

## 設定檔

OpenClaw 的設定檔位於 `~/.openclaw/openclaw.json`。

最小設定範例：

```json
{
  "agent": {
    "model": "anthropic/claude-opus-4-6"
  }
}
```

## 疑難排解

### 檢查系統健康狀態

```bash
openclaw doctor
```

### 查看日誌

```bash
# 查看 systemd 服務日誌
journalctl --user -u openclaw-gateway -f
```

### 常見問題

1. **權限錯誤**: 確保使用者有權限存取 `~/.openclaw` 目錄
2. **連接埠衝突**: 預設使用 18789 埠，可透過 `--port` 參數更改
3. **Node.js 版本過舊**: 必須使用 Node.js 22 或更新版本

## 更新 OpenClaw

```bash
# 更新到最新穩定版
openclaw update --channel stable

# 更新到 beta 版
openclaw update --channel beta
```

## 參考資源

- [官方文件](https://docs.openclaw.ai)
- [入門指南](https://github.com/openclaw/openclaw#getting-started)
- [設定參考](https://github.com/openclaw/openclaw/blob/main/docs/configuration.md)
- [Discord 社群](https://discord.gg/openclaw)
