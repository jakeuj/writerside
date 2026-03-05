# OpenClaw 安裝與配置指南

OpenClaw 是一個強大的 AI 助手框架，可以透過 Telegram 遠端控制你的伺服器，執行各種系統指令。本指南將帶你完成從安裝到透過 iPhone Telegram 應用程式遠端查詢系統資訊的完整流程。

## 📋 前置需求

- Docker 和 Docker Compose
- Telegram 帳號
- Ollama（用於運行本地 LLM 模型）
- 具備 NVIDIA GPU 的伺服器（如需查詢顯卡資訊）

## ⚡ 快速啟動（Ollama Launch）

> **官方文檔**: [Ollama OpenClaw 整合文檔](https://docs.ollama.com/integrations/openclaw)

如果你已安裝 Ollama，最簡單的方式是使用 `ollama launch` 指令一鍵啟動 OpenClaw：

```bash
ollama launch openclaw
```

Ollama 會自動完成以下流程：

1. **安裝** — 若尚未安裝 OpenClaw，Ollama 會提示透過 npm 安裝
2. **安全確認** — 首次啟動時顯示工具存取權限的安全說明
3. **選擇模型** — 從選單中選擇本地或雲端模型
4. **初始化** — Ollama 配置 Provider、安裝 Gateway Daemon 並設定主要模型
5. **啟動 Gateway** — 在背景啟動 Gateway 並開啟 OpenClaw TUI

> **注意**：OpenClaw 需要較大的 Context Window，本地模型建議至少 64k tokens。請參考 [Context length 設定](https://docs.ollama.com/context-length)。
> **提示**：OpenClaw 前身為 Clawdbot，`ollama launch clawdbot` 仍可作為別名使用。

### 不啟動直接設定

若只需更換模型而不啟動 Gateway 和 TUI：

```bash
ollama launch openclaw --config
```

指定特定模型直接啟動：

```bash
ollama launch openclaw --model kimi-k2.5:cloud
```

若 Gateway 已在執行，會自動重啟以套用新模型。

### 推薦模型

**雲端模型**（需網路連線）：

- `kimi-k2.5:cloud` — 多模態推理與子代理支援
- `minimax-m2.5:cloud` — 快速、高效的程式碼與生產力任務
- `glm-5:cloud` — 推理與程式碼生成

**本地模型**：

- `glm-4.7-flash` — 本地推理與程式碼生成（需約 25 GB VRAM）

更多模型請至 [ollama.com/search](https://ollama.com/search?c=cloud) 查詢。

### 連接通訊應用程式

啟動後，執行以下指令連結 WhatsApp、Telegram、Slack、Discord 或 iMessage：

```bash
openclaw configure --section channels
```

### 停止 Gateway

```bash
openclaw gateway stop
```

---

## 🚀 Docker 安裝步驟（進階）

### 1. 安裝 Ollama

首先安裝 Ollama 來運行本地語言模型：

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama
```

啟動 Ollama 服務：

```bash
ollama serve
```

### 2. 下載並配置 AI 模型

使用 Ollama 下載 OpenClaw 官方推薦的模型：

```bash
# 官方推薦模型（選擇其中一個）

# Qwen3 Coder（推薦 - 專為程式碼和指令優化）
# 預設版本 (30B 模型，19GB，256K 上下文)
ollama pull qwen3-coder

# 或指定版本
ollama pull qwen3-coder:latest  # 30B 版本
ollama pull qwen3-coder:30b     # 30B 版本（與 latest 相同）

# GLM 4.7（輕量級高效能模型）
ollama pull glm-4.7

# GPT OSS 20B（大型開源模型）
ollama pull gpt-oss:20b
```

> **模型規格參考**:
>
> - `qwen3-coder:30b` - 19GB, 256K 上下文長度, 文字輸入
> - 詳細資訊: [Ollama qwen3-coder 模型庫](https://ollama.com/library/qwen3-coder)

驗證模型是否成功安裝：

```bash
ollama list
```

測試模型運行：

```bash
# 使用 qwen3-coder 測試
ollama run qwen3-coder "你好，請介紹自己"
```

### 3. 安裝 OpenClaw

訪問 [OpenClaw 官方網站](https://openclaw.ai/) 獲取最新安裝指令。

使用 Docker Compose 安裝（推薦）：

```bash
# 創建專案目錄
mkdir openclaw && cd openclaw

# 下載 docker-compose.yml
curl -O https://openclaw.ai/docker-compose.yml

# 編輯配置檔案
nano docker-compose.yml
```

基本 `docker-compose.yml` 配置範例：

```yaml
version: '3.8'

services:
  openclaw:
    image: openclaw/openclaw:latest
    container_name: openclaw
    restart: unless-stopped
    environment:
      - OLLAMA_HOST=http://host.docker.internal:11434
      - MODEL_NAME=qwen3-coder  # 使用官方推薦模型
    volumes:
      - ./data:/app/data
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - "8080:8080"
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

啟動 OpenClaw 服務：

```bash
docker-compose up -d
```

檢查服務狀態：

```bash
docker-compose logs -f
```

## 🤖 設定 Telegram Bot 與配對 {id="telegram-bot-setup"}

### 1. 創建 Telegram Bot

1. 在 Telegram 中搜尋 `@BotFather`
2. 發送 `/newbot` 命令
3. 按照提示設定 Bot 名稱和使用者名稱
4. 保存 BotFather 提供的 **API Token**（格式：`123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`）

### 2. 配置 Telegram Bot Token

將你的 Telegram Bot Token 添加到 OpenClaw 配置：

```bash
# 方法 1: 環境變數（在 docker-compose.yml 中添加）
environment:
  - TELEGRAM_BOT_TOKEN=你的Bot Token

# 方法 2: 透過指令設定
docker exec -it openclaw openclaw config set telegram.bot_token "你的Bot Token"
```

重啟服務使配置生效：

```bash
docker-compose restart
```

## 📱 配對 Telegram Bot（重要）{id="telegram-bot-pairing"}

> **官方文檔參考**: [OpenClaw Pairing 配對指南](https://docs.openclaw.ai/channels/pairing)

### 1. 在 Telegram 應用中獲取配對碼

1. 開啟 iPhone 上的 Telegram 應用（小飛機 App）
2. 搜尋並開啟你剛創建的 Bot（使用 Bot 的使用者名稱，例如 `@YourBotName_bot`）
3. 發送 `/start` 命令

Bot 會自動回覆並顯示配對碼，類似：

```text
Welcome to OpenClaw! 🤖

Your pairing code is: ABCD-1234-EFGH-5678

Please run this command on your server to complete pairing:
openclaw pair verify ABCD-1234-EFGH-5678

This code will expire in 10 minutes.
```

### 2. 在伺服器端驗證配對碼 {id="verify-pairing-server"}

複製 Bot 顯示的配對碼，然後在 OpenClaw 伺服器上執行驗證指令：

```bash
# 使用 Bot 提供的配對碼進行配對
docker exec -it openclaw openclaw pair verify ABCD-1234-EFGH-5678
```

成功配對後，終端會顯示：

```text
✅ Pairing successful!
User @your_telegram_username is now authorized.
```

同時，Telegram Bot 也會發送確認訊息：

```text
✅ Pairing successful!
You can now send commands to control your server.
```

### 3. 檢查配對狀態

查看已配對的用戶清單：

```bash
# 查看所有已授權的用戶
docker exec -it openclaw openclaw pair list

# 或查看配對詳細資訊
docker exec -it openclaw openclaw user list
```

## 💻 使用範例

### 查詢 NVIDIA 顯卡資訊

配對成功後，在 Telegram 中直接向 Bot 發送自然語言指令：

```text
查詢顯卡資訊
```

或

```text
顯示 nvidia-smi
```

Bot 會執行 `nvidia-smi` 指令並返回結果：

```text
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03             Driver Version: 535.129.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 4090        Off | 00000000:01:00.0  On |                  Off |
|  0%   45C    P8              20W / 450W |   1234MiB / 24564MiB |      2%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
```

### 其他實用指令範例

```text
# 系統資源監控
顯示 CPU 和記憶體使用情況

# Docker 容器管理
列出所有運行中的容器

# 磁碟空間檢查
檢查磁碟使用量

# 服務狀態檢查
查看服務狀態
```

## 🔒 安全性設定

### 限制指令執行權限

編輯 OpenClaw 配置檔案以限制可執行的指令：

```bash
docker exec -it openclaw nano /app/config/permissions.yml
```

範例配置：

```yaml
permissions:
  allowed_commands:
    - nvidia-smi
    - docker ps
    - df -h
    - free -h
    - uptime
  blocked_commands:
    - rm
    - shutdown
    - reboot
```

### 設定用戶白名單

只允許特定 Telegram 用戶使用：

```bash
docker exec -it openclaw openclaw user add @your_telegram_username
```

## 🛠️ 故障排除

### Ollama 連線問題

如果 OpenClaw 無法連接到 Ollama：

```bash
# 檢查 Ollama 是否運行
curl http://localhost:11434/api/version

# 檢查 Docker 網路
docker network inspect bridge
```

### Bot 無回應 {id="bot-no-response"}

1. 檢查 Bot Token 是否正確設定
2. 確認 OpenClaw 容器正在運行：

   ```bash
   docker ps | grep openclaw
   ```

3. 查看錯誤日誌：

   ```bash
   docker logs openclaw --tail 100
   ```

### 配對碼過期

配對碼通常在 10 分鐘後過期。如果過期，請重新執行配對流程：

1. 在 Telegram Bot 中重新發送 `/start` 獲取新的配對碼
2. 在伺服器上使用新的配對碼執行驗證：

   ```bash
   docker exec -it openclaw openclaw pair verify 新的配對碼
   ```

### 無法獲取配對碼

如果 Bot 沒有回應或無法顯示配對碼：

1. 確認 Bot Token 已正確設定在 OpenClaw 配置中
2. 檢查 OpenClaw 服務是否正常運行
3. 重啟 OpenClaw 服務：

   ```bash
   docker-compose restart
   ```

## 📚 進階配置

### 自訂模型參數

調整模型的運行參數以優化性能：

```yaml
environment:
  - MODEL_NAME=qwen3-coder  # 或 glm-4.7, gpt-oss:20b
  - MODEL_TEMPERATURE=0.7
  - MODEL_MAX_TOKENS=2048
  - MODEL_CONTEXT_LENGTH=4096
```

### 設定多個 Bot {id="multiple-bots"}

可以為不同用途創建多個 Bot 實例：

```yaml
services:
  openclaw-admin:
    image: openclaw/openclaw:latest
    environment:
      - TELEGRAM_BOT_TOKEN=管理Bot Token
      - ROLE=admin
  
  openclaw-monitor:
    image: openclaw/openclaw:latest
    environment:
      - TELEGRAM_BOT_TOKEN=監控Bot Token
      - ROLE=monitor
```

## 🔗 相關資源

- [OpenClaw 官方網站](https://openclaw.ai/)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)
- [OpenClaw Pairing 配對指南](https://docs.openclaw.ai/channels/pairing) - 官方配對文檔
- [Ollama OpenClaw 整合文檔](https://docs.ollama.com/integrations/openclaw) - 官方整合指南
- [Ollama qwen3-coder 模型庫](https://ollama.com/library/qwen3-coder) - 模型詳細規格
- [Ollama 官方文檔](https://ollama.com/docs)
- [Telegram Bot API 文檔](https://core.telegram.org/bots/api)

## 📝 總結

透過以上步驟，你已經成功：

1. ✅ 安裝並配置 Ollama 與官方推薦模型（qwen3-coder / glm-4.7 / gpt-oss:20b）
2. ✅ 部署 OpenClaw 伺服器
3. ✅ 創建並配對 Telegram Bot
4. ✅ 在 iPhone Telegram 應用中遠端控制伺服器

現在你可以隨時隨地透過 Telegram 查詢伺服器狀態、管理服務，享受 AI 驅動的智能運維體驗！
