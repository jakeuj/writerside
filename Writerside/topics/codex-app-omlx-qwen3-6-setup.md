# Codex App 搭配 oMLX 伺服器運行 Qwen3.6 35B 設定筆記

<web-summary>說明如何在本機利用 oMLX 伺服器提供 Qwen3.6 35B 模型給 Codex App 使用，包含 sampling 設定、認證機制與模型目錄的對應關係。</web-summary>

將 Codex App 的模型提供者設定為 oMLX，利用本地伺服器運行 Qwen3.6 35B 模型，可在 MacBook Pro 上獲得穩定且低延遲的 AI 編程體驗。

## 問題描述

在本地 MacBook Pro 開發時，若想讓 Codex App 使用本地的 Qwen3.6 35B 模型而不是雲端 API，需要正確設定三個層級的檔案：`config.toml`（Codex App 主設定）、`model-catalogs/omlx.json`（模型目錄）與 `settings.json`（oMLX 伺服器設定）。

## 解決方案

Codex App 透過 `model_provider = "omlx"` 指示 oMLX 伺服器作為模型來源，並由 `model_catalog_json` 指向本地 JSON 檔。oMLX 伺服器則負責提供實際的推理服務，並透過 REST API 與 Codex App 溝通。

## 設定架構總覽

設定分成三個互相搭配的層級：

| 層級 | 設定檔 | 職責 |
|------|--------|------|
| Codex App 主設定 | `config.toml` | 指定使用哪種 provider 與哪個模型 |
| 模型目錄 | `model-catalogs/omlx.json` | 描述模型的規格、context window、基礎指示 |
| oMLX 伺服器 | `settings.json` | 控制伺服器行為：sampling、記憶體、快取、排程 |

這三個層級各司其職，讓使用者可以獨立調整每個面向，而不必全部重設。

## 操作步驟

### 1. 設定 Codex App 主設定

在 `~/.codex/config.toml` 中，核心的設定如下：

```toml
model = "Qwen3.6-35B-A3B"
model_provider = "omlx"
model_catalog_json = "/Users/user/.codex/model-catalogs/omlx.json"
```

`model` 欄位使用簡化後的 slug，`model_provider` 指明模型供應商，`model_catalog_json` 則指向包含完整模型規格與基礎指示的 JSON 目錄。

### 2. 設定 oMLX 伺服器

在 `~/.omlx/settings.json` 中，最重要的兩個區塊是 `sampling` 與 `auth`：

```jsonc
"sampling": {
    "max_context_window": 262144,
    "max_tokens": 32768,
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 20,
    "repetition_penalty": 1.0
}
```

| 參數 | 值 | 說明 |
|------|-----|------|
| `max_context_window` | 262144 | 最大上下文視窗（128K tokens） |
| `max_tokens` | 32768 | 單次回應最大 token 數 |
| `temperature` | 1.0 | 創意濃度，預設值 |
| `top_p` | 0.95 | 核采樣參數 |
| `top_k` | 20 | 前 K 高機率詞彙 |
| `repetition_penalty` | 1.0 | 無重複懲罰 |

伺服器同時支援多個 hostname 與自動啟動，並採用平衡模式（balanced）的 burst decode。

### 3. 設定模型目錄

`model-catalogs/omlx.json` 包含實際的模型規格：

```jsonc
{
  "slug": "Qwen3.6-35B-A3B",
  "display_name": "Qwen3.6 35B A3B",
  "context_window": 262144,
  "max_context_window": 262144,
  "effective_context_window_percent": 90,
  "auto_compact_token_limit": 220000,
  "input_modalities": ["text", "image"],
  "supports_parallel_tool_calls": true,
  "supports_image_detail_original": true,
  "truncation_policy": {
    "mode": "tokens",
    "limit": 240000
  },
  "base_instructions": "You are Codex, a local coding agent running in Codex App. You and the user share one workspace. Help the user complete software engineering tasks by reading the relevant files first, making small and well-scoped changes, and verifying your work when practical.\n\nUse the available tools to inspect files, run commands, edit code, and test changes. Prefer `rg` for searching. Preserve user changes and never revert unrelated work. Do not use destructive git commands unless the user explicitly asks.\n\nWhen editing code, follow the existing project style and keep changes focused. Use structured parsers or existing helpers when available. Add comments only when they clarify non-obvious logic.\n\nFor frontend work, build the actual usable interface, match the existing design system, ensure responsive layout, avoid overlapping text, and verify the result visually when possible.\n\nCommunicate in Traditional Chinese when the user writes Chinese, using Taiwan phrasing. Keep technical terms in English when appropriate. Be concise, practical, and proactive. If a task needs implementation, proceed with the change instead of only proposing a plan, unless the user is clearly asking for advice only."
}
```

模型支援文字與圖片輸入、並行工具呼叫，並具備 90% 的有效上下文視窗。截斷策略採用 token 模式，在 240K tokens 時觸發。

### auto_compact_token_limit 與 truncation_policy.limit 的關係

在模型目錄（`omlx.json`）中，`auto_compact_token_limit` 與 `truncation_policy.limit` 是兩個互相配合的設定，用以控制上下文視窗的管理策略：

| 設定 | 數值 | 角色 |
|------|------|------|
| `auto_compact_token_limit` | 220,000 | 自動壓縮（compaction）觸發閾值 |
| `truncation_policy.limit` | 240,000 | 硬截斷（truncation）極限值 |

當對話過程中 token 數持續上升時，系統會依序觸發以下兩個機制：

1. **自動壓縮（compaction）**：當 token 數達到 `auto_compact_token_limit`（例如 220K）時，系統會將舊的對話訊息「壓縮」成較短的摘要，保留其內容脈絡但不佔用完整空間。
2. **硬截斷（truncation）**：當 token 數超過 `truncation_policy.limit`（例如 240K）時，系統會強制移除最舊的訊息，不會再做摘要。

正確的關係式為：

```
auto_compact_token_limit < truncation_policy.limit < max_context_window
```

這樣設計的**三大原因**如下：

#### 1. 預先壓縮（Preemptive Compaction）

當 token 數達到 `auto_compact_token_limit` 時，系統會主動壓縮舊訊息。這與等到上下文滿掉才被迫切掉的做法不同——壓縮後的訊息會變成簡短版本保留在上下文裡，而非完全消失。

#### 2. 避免硬截斷（Prevents Hard Truncation）

如果 `auto_compact_token_limit` 等於或大於 `truncation_policy.limit`，系統可能還沒觸發自動壓縮就達到了極限，必須強制截斷。硬截斷會直接切掉舊訊息，可能遺失重要的對話脈絡。

#### 3. 緩衝區設計（Buffer Zone）

兩個數值之間形成一個緩衝區（在上面的例子中是 220K ~ 240K 之間約 20K 的差距）。在緩衝區內，系統有時間執行壓縮動作，而不是一抵達極限就立刻切掉訊息。

```
token 數上升
  │
  ├─ 220K (auto_compact_token_limit) ──→ 開始壓縮舊訊息成摘要
  │
  ├─ 240K (truncation_policy.limit) ──→ 若壓縮後仍超過，開始硬截斷
  │
  └─ 超過 240K ──→ 強制移除最舊的訊息
```

此設定確保系統能「主動出擊」管理上下文，而不只是被動地等待訊息被截斷。

## experimental_bearer_token 取代 env_key

傳統上，本地 API 伺服器需要透過環境變數（如 `OMLX_API_KEY`）傳遞 API 金鑰。這種方式在重新啟動應用時可能會遺失，需要重新設定。

在目前的設定中，oMLX provider 改為使用 `experimental_bearer_token` 直接內嵌 token 值：

```toml
[model_providers.omlx]
name = "oMLX"
base_url = "http://127.0.0.1:8000/v1"
# env_key = "OMLX_API_KEY"
experimental_bearer_token = "api_key_placeholder"
```

這種設計的好處包括：

- **不需要環境變數**：設定檔內直接寫死 token，重新啟動 Codex App 後仍維持連線。
- **便於除錯**：直接在 `config.toml` 內可見 token 值，不用額外檢查環境。
- **適合本地開發**：本地伺服器的金鑰通常不需頻繁更換，內嵌方式更簡便。

若要切換回傳統的 `env_key` 模式，只需解除註解 `env_key` 並註掉 `experimental_bearer_token` 即可。

## 補充說明

- oMLX 伺服器預設監聽 `127.0.0.1:8000`，使用 RESTful API 格式。
- 通訊協定採用 `responses` wire format，與 OpenAI-compatible 的 API 樣式一致。
- 記憶體管理採用 `balanced` 模式，預寫區域保留 80% 空間，並設定 16GB 的熱快取上限。
- 排程器預設限制為單請求處理（`max_concurrent_requests = 1`），適合本地資源有限的場景。

## 參考資料

- [Codex App 使用說明](https://openai.com/codex)
- [oMLX 本地模型服務](https://github.com/omlx)
- [Qwen3.6 35B 模型規格](https://huggingface.co/models)
