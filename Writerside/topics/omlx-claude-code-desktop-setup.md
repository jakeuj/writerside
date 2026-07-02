# 在 oMLX 設定 Claude Code Desktop 與 CLI 使用本地模型

<web-summary>說明如何在 oMLX 設定 claude-* 模型別名，讓 Claude Code Desktop 與 Claude Code CLI 直接連線到本地 macOS Apple Silicon 上運行的 Claude 系列模型，包含 API 連線設定、環境變數與 cc-switch 模型切換工具。</web-summary>

在 macOS Apple Silicon 上用 oMLX 伺服器提供本地 Claude 模型時，只需要在 oMLX 將模型別名命名為 `claude-*` 格式，Claude Code Desktop 與 CLI 就能直接偵測並使用。

<tldr>
- **模型別名**：oMLX 內設定為 `claude-opus-4`、`claude-sonnet-4` 等 `claude-*` 格式即可被 Claude Code 自動識別。
- **Desktop 連線**：Developer → Configure Third-Party Inference，base URL 設 `http://127.0.0.1:8000`。
- **CLI 啟動**：用 `omlx launch claude` 或直接設定 `ANTHROPIC_*` 環境變數執行。
- **模型切換**：可搭配 [cc-switch](https://github.com/farion1231/cc-switch) 快速切換不同模型名稱。
</tldr>

## 前置條件

- macOS Apple Silicon Mac（M1 / M2 / M3 / M4）
- 已安裝 [oMLX](https://github.com/ml-explore/oMLX) 伺服器
- 已下載 Claude 系列 MLX 格式模型（如 Ornith、Ornith-Qwen 等兼容模型）
- Claude Code Desktop 或 Claude Code CLI 已安裝

## 設定模型別名

Claude Code 系列工具會透過 OpenAI 相容 API 連線到本地伺服器，並根據模型 ID 判斷要使用哪種模型。oMLX 預設的模型名稱不一定符合 Claude Code 的預期格式，因此需要設定別名。

1. 打開 oMLX，進入 **Model Settings**。

![model_settings.png](model_settings.png)

1. 為目標模型設定別名，名稱必須符合 `claude-*` 格式。

![model_alias.png](model_alias.png)

- 例如：`claude-opus-4`、`claude-sonnet-4`、`claude-haiku-4`
- 別名會作為 API 請求時的 model ID，Claude Code 會依此判斷型號。

## Claude Code Desktop 設定

1. 打開 Claude Code Desktop，點選上方選單 **Help** → **Troubleshooting** → 勾選 **Enable Developer Mode**。

![claude_troub.png](claude_troub.png)

1. 啟用後上方會出現 **Developer** 選單，點擊 **Developer** → **Configure Third-Party Inference...**。

![claude_dev.png](claude_dev.png)

1. 在 **Connection** 頁面填入以下設定：

- **Base URL**：`http://127.0.0.1:8000`
- **API Key**：你在 oMLX 設定的密碼（authentication token）
- **Model ID**：在 oMLX 設定的模型別名，例如 `claude-opus-4`
- **Display Name**（選填）：設定原始模型名稱，方便在 UI 中辨識實際使用的模型

![claude_setting.png](claude_setting.png)

1. 儲存後重新啟動 Claude Code Desktop，即可開始使用本地模型。

## Claude Code CLI 設定

oMLX 內建整合模式，設定完成後可以直接用以下指令啟動 Claude Code CLI：

```bash
omlx launch claude
```

![claude_cli.png](claude_cli.png)

如果要手動指定環境變數啟動，可以使用：

```bash
ANTHROPIC_BASE_URL='http://127.0.0.1:8000' 
ANTHROPIC_AUTH_TOKEN='你的密碼' 
ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4' 
ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4' 
ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4' 
API_TIMEOUT_MS=3000000 
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 
claude
```

> **提示**：`ANTHROPIC_DEFAULT_*_MODEL` 可對應到你在 oMLX 設定的實際模型別名，格式為 `claude-*`。如果 oMLX 中的別名與預設值不同，請調整為實際的別名名稱。

## 搭配 cc-switch 切換模型

如果需要在不同 Claude 模型之間快速切換，可以額外安裝 [cc-switch](https://github.com/farion1231/cc-switch)。這個工具允許你在 Claude Code 執行時動態修改模型名稱對應，不必重新設定連線。

## 常見問題

- **連不上本地伺服器**：確認 oMLX 伺服器正在執行，且 `http://127.0.0.1:8000` 可以存取。可在瀏覽器開啟該 URL 測試。
- **API Key 驗證失敗**：確認填入的密碼與 oMLX 設定的 authentication token 一致。
- **模型識別錯誤**：Claude Code 會根據 model ID 判斷模型類型，確保別名符合 `claude-*` 格式。
- **回應速度較慢**：本地模型的回應速度取決於 Mac 的記憶體與模型大小，35B 以上模型可能需要較長等待時間。

## 相關文章

- [Codex App 搭配 oMLX 伺服器運行 Qwen3.6 35B 設定筆記](codex-app-omlx-qwen3-6-setup.md)
- [Apple Silicon MLX 工具選型](apple-silicon-mlx-local-llm-tools.md)
