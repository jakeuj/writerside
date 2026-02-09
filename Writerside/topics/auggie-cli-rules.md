# Auggie CLI Rules 設定指南

Auggie CLI 支援自訂規則和指引，讓 AI 助手能夠根據專案的編碼規範、慣例和偏好提供更精準的協助。

## 核心概念

**結論先講**：使用者層級的規則資料夾位於 `~/.augment/rules/`，系統會遞迴搜尋所有 `.md` 檔案作為全域規則。

## 支援的規則檔案

Auggie 會按照以下優先順序載入規則檔案：

1. **自訂規則檔案**（透過 `--rules` 參數）：`/path/to/custom-rules.md`
2. **CLAUDE.md**：與 Claude Code 等 AI 工具相容
3. **AGENTS.md**：與 Cursor 等 AI 開發工具相容
4. **工作區指引**：`<workspace_root>/.augment/guidelines.md`（舊版格式）
5. **工作區規則資料夾**：`<workspace_root>/.augment/rules/` - 遞迴搜尋 `.md` 檔案
6. **使用者規則資料夾**：`~/.augment/rules/` - 遞迴搜尋 `.md` 檔案（全域規則）

## 使用者規則 vs 工作區規則

| 範圍 | 位置 | 適用範圍 |
|------|------|----------|
| 使用者規則 | `~/.augment/rules/` | 所有工作區 |
| 工作區規則 | `<workspace_root>/.augment/rules/` | 僅限當前專案 |

### 使用者規則（User Rules）

- 儲存在家目錄，適用於所有專案
- 用於個人偏好、編碼風格指引或跨專案的通用慣例
- **永遠視為 `always_apply` 類型**，自動包含在每個提示中
- 不支援 frontmatter 配置

### 工作區規則（Workspace Rules）

- 儲存在專案儲存庫中，僅適用於特定專案
- 用於專案特定的指引，可透過版本控制與團隊共享
- 支援 frontmatter 配置（見下方說明）

## 規則檔案格式

規則檔案應使用 Markdown 格式撰寫，以自然語言描述指引。建議結構如下：

```markdown
# 專案指引

## 程式碼風格
- 所有新的 JavaScript 檔案使用 TypeScript
- 遵循程式碼庫中現有的命名慣例
- 為所有公開函式和類別添加 JSDoc 註解

## 架構
- 遵循程式碼庫中建立的 MVC 模式
- 將業務邏輯放在服務類別中
- 保持控制器精簡，專注於請求/回應處理

## 測試
- 為所有新函式撰寫單元測試
- 維持測試覆蓋率在 80% 以上
- 使用 Jest 作為測試框架

## 相依性
- 優先使用內建的 Node.js 模組
- 使用 npm 進行套件管理
- 在 package.json 中為生產相依性固定確切版本
```

## Frontmatter 配置（僅限工作區規則）

工作區規則資料夾 `<workspace_root>/.augment/rules/` 中的檔案支援 frontmatter 配置：

| 欄位 | 用途 | 選項 | 預設值 |
|------|------|------|--------|
| `type` | 控制規則何時套用 | `always_apply`, `agent_requested` | `always_apply` |
| `description` | 規則用途的簡短描述（`agent_requested` 類型必填） | 任何文字 | 無 |

### 規則類型

- **`always_apply`**：規則內容自動包含在每個使用者提示中
- **`agent_requested`**：根據 `description` 欄位，在相關時自動偵測並附加規則

> **注意**：CLI 中尚不支援手動規則（manual）。目前工作區規則會被視為 `always_apply`。`manual` 類型僅在 IDE 擴充功能中有效，可使用 `@` 提及選擇性附加規則。

### Frontmatter 範例 {id="frontmatter-examples"}

永遠套用的規則：

```markdown
---
type: always_apply
---

# TypeScript 指引

- 在所有 TypeScript 檔案中使用嚴格模式
- 為所有函式定義明確的回傳類型
- 除非絕對必要，否則避免使用 `any` 類型
```

代理請求的規則：

```markdown
---
type: agent_requested
description: React 元件開發模式和最佳實踐
---

# React 元件指引

- 使用帶有 hooks 的函式元件
- 為 props 實作適當的 TypeScript 介面
- 遵循 src/components/ 中建立的資料夾結構
```

## 階層式規則

除了工作區層級的規則外，Auggie 還支援透過在子目錄中放置 `AGENTS.md` 和 `CLAUDE.md` 檔案來實現階層式規則。

### 運作方式

1. 當你處理某個檔案時，Augment 會在該檔案的目錄中尋找 `AGENTS.md` 和 `CLAUDE.md`
2. 然後向上遍歷目錄樹，檢查每個父目錄中的這些檔案
3. 所有發現的規則都會包含在該工作階段的上下文中
4. 搜尋會在工作區根目錄停止（因為工作區根目錄的規則已經單獨載入）

### 目錄結構範例

```
my-project/
  AGENTS.md                  <- 永遠包含（工作區根目錄）
  src/
    AGENTS.md                <- 在 src/ 或子目錄中工作時包含
    frontend/
      AGENTS.md              <- 在 src/frontend/ 中工作時包含
      App.tsx
    backend/
      AGENTS.md              <- 在 src/backend/ 中工作時包含
      server.ts
  tests/
    AGENTS.md                <- 僅在 tests/ 中工作時包含
```

當處理 `src/frontend/App.tsx` 時：
- 載入 `src/frontend/AGENTS.md`（當前目錄）
- 載入 `src/AGENTS.md`（父目錄）
- 透過標準規則載入工作區根目錄的 `AGENTS.md`
- **不會**載入 `src/backend/AGENTS.md` 和 `tests/AGENTS.md`（不同分支）

### 使用案例

- **框架特定指引**：在前端目錄放置 React 特定規則，在後端目錄放置 Node.js 規則
- **模組特定慣例**：在 API 目錄中定義 API 設計模式
- **測試特定規則**：添加僅在撰寫測試時適用的測試慣例
- **團隊界限**：不同團隊可以在各自的目錄中維護自己的編碼標準

## 最佳實踐

1. **具體明確**：提供清晰、可操作的指引，而非模糊的建議
2. **使用範例**：在描述模式或慣例時包含程式碼範例
3. **保持更新**：隨著專案演進定期審查和更新規則
4. **簡潔扼要**：專注於最重要的指引，避免讓 AI 不知所措
5. **測試指引**：透過範例請求驗證 Auggie 是否遵循你的規則

## 命令列參數

你可以在啟動 Auggie 時指定自訂規則檔案：

```bash
auggie --rules /path/to/custom-rules.md
```

這會將指定的規則附加到自動載入的任何工作區指引中。

## 相關資源

- [Skills](https://docs.augmentcode.com/cli/skills) - 使用專業領域知識擴展能力
- [Rules & Guidelines for Agent and Chat](https://docs.augmentcode.com/configuration/rules) - 在 VSCode 和 JetBrains IDE 中配置規則
- [CLI Reference](https://docs.augmentcode.com/cli/cli-reference) - 完整的命令列參考
- [Custom Commands](https://docs.augmentcode.com/cli/custom-commands) - 建立可重複使用的命令範本

## 參考文件

- 官方文檔：https://docs.augmentcode.com/cli/rules

