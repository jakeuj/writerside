# Auggie 使用者規則範例檔案

這是一個實際可用的使用者規則範例，適合放在 `~/.augment/rules/personal-preferences.md`。

## 完整範例檔案

將以下內容儲存為 `~/.augment/rules/personal-preferences.md`：

```markdown
# 個人開發偏好設定

## 系統環境
- **作業系統**：macOS 26 (ARM64 - Apple Silicon M4)
- **主要語言**：繁體中文（zh-tw）
- **回應風格**：使用台灣慣用的繁體中文，技術術語保留英文但提供中文說明

## Shell 工具偏好

### 必須使用的現代化工具
當需要執行以下任務時，優先使用現代化工具（如果尚未安裝，請先安裝）：

| 任務類型 | 必須使用 | 不要使用 |
|---------|---------|---------|
| 尋找檔案 | `fd` | `find`, `ls -R` |
| 搜尋文字 | `rg` (ripgrep) | `grep`, `ag` |
| 分析程式碼結構 | `ast-grep` | `grep`, `sed` |
| 互動式選擇 | `fzf` | 手動過濾 |
| 處理 JSON | `jq` | `python -m json.tool` |
| 處理 YAML/XML | `yq` | 手動解析 |

### 工具使用範例

**搜尋檔案**：
```bash
# 使用 fd 而非 find
fd "*.ts" src/
fd -e md -e txt  # 搜尋多種副檔名
fd -H ".env"     # 包含隱藏檔案
```

**搜尋內容**：
```bash
# 使用 ripgrep 而非 grep
rg "TODO" --type typescript
rg "function.*export" -g "*.ts"
rg -i "error" --stats  # 不區分大小寫並顯示統計
```

**處理 JSON**：
```bash
# 使用 jq 處理 JSON
cat package.json | jq '.dependencies'
jq -r '.version' package.json
```

**處理 YAML**：
```bash
# 使用 yq 處理 YAML
yq eval '.services.web.ports' docker-compose.yml
```

## 程式碼風格通用原則

### 命名慣例
- 使用有意義的變數名稱，避免單字母變數（除了迴圈索引 i, j, k）
- 函式名稱應該是動詞或動詞片語（如 `getUserData`, `calculateTotal`）
- 類別名稱使用名詞（如 `UserService`, `PaymentProcessor`）
- 常數使用全大寫加底線（如 `MAX_RETRY_COUNT`, `API_BASE_URL`）
- 布林值變數使用 `is`, `has`, `should` 等前綴（如 `isValid`, `hasPermission`）

### 註解原則
- 優先寫自解釋的程式碼，而非依賴註解
- 註解應該解釋「為什麼」而非「是什麼」
- 複雜的業務邏輯必須加上註解說明
- 公開的 API 必須有完整的文件註解（JSDoc, docstring 等）
- 移除被註解掉的程式碼，使用版本控制系統追蹤歷史

### 錯誤處理
- 永遠處理可能的錯誤情況，不要忽略例外
- 使用具體的錯誤類型，避免捕捉通用的 Exception
- 錯誤訊息應該提供足夠的上下文資訊
- 記錄錯誤時包含相關的變數值和堆疊追蹤
- 對於預期的錯誤，提供使用者友善的錯誤訊息

## 版本控制

### Git Commit 訊息格式
遵循 Conventional Commits 規範：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 類型**：
- `feat`: 新功能
- `fix`: 錯誤修正
- `docs`: 文件更新
- `style`: 程式碼格式調整（不影響功能）
- `refactor`: 重構
- `test`: 測試相關
- `chore`: 建置流程或輔助工具變更
- `perf`: 效能改善

**範例**：
```
feat(auth): 新增 OAuth 2.0 登入支援

- 實作 Google OAuth 登入流程
- 新增 token 刷新機制
- 更新使用者認證中介層

Closes #123
```

### 分支命名
- `feature/功能描述` - 新功能開發
- `bugfix/問題描述` - 錯誤修正
- `hotfix/緊急修正` - 緊急修正
- `refactor/重構描述` - 程式碼重構
- `docs/文件更新` - 文件更新

## 測試原則

- 為所有公開的函式和方法撰寫單元測試
- 測試名稱應該清楚描述測試情境（使用 `should` 或 `it should` 格式）
- 遵循 AAA 模式：Arrange（準備）、Act（執行）、Assert（驗證）
- 維持測試覆蓋率在 80% 以上
- 測試應該獨立且可重複執行
- 避免測試實作細節，專注於行為測試

## 安全性考量

- 永遠不要在程式碼中硬編碼敏感資訊（密碼、API 金鑰、私鑰等）
- 使用環境變數或安全的密鑰管理服務（如 AWS Secrets Manager, Azure Key Vault）
- 驗證和清理所有使用者輸入
- 使用參數化查詢或 ORM 防止 SQL 注入
- 定期更新相依套件以修補安全漏洞
- 實作適當的身份驗證和授權機制
- 敏感資料傳輸使用 HTTPS/TLS

## 效能最佳化

- 避免過早優化，先確保程式碼正確性和可讀性
- 使用適當的資料結構和演算法
- 對資料庫查詢進行索引優化
- 實作適當的快取策略（記憶體快取、Redis 等）
- 監控和記錄效能指標
- 對於大量資料處理，考慮分頁或串流處理
- 避免 N+1 查詢問題

## 文件撰寫

- README 應包含：專案簡介、安裝步驟、使用方式、貢獻指南
- API 文件應該完整且保持更新
- 複雜的架構決策應該記錄在 ADR（Architecture Decision Records）
- 使用 Markdown 格式撰寫文件
- 提供程式碼範例和使用案例
- 保持文件與程式碼同步更新
```

## 建立步驟

1. **建立目錄**（如果不存在）：
   ```bash
   mkdir -p ~/.augment/rules
   ```

2. **建立規則檔案**：
   ```bash
   touch ~/.augment/rules/personal-preferences.md
   ```

3. **編輯檔案**：
   使用您喜歡的編輯器將上述內容貼入檔案中

4. **驗證**：
   啟動 Auggie 並測試規則是否生效

## 進階技巧

### 多檔案組織

您可以將規則分成多個檔案，Auggie 會遞迴載入所有 `.md` 檔案：

```
~/.augment/rules/
├── 00-system-preferences.md      # 系統和語言偏好
├── 10-shell-tools.md              # Shell 工具偏好
├── 20-code-style.md               # 程式碼風格
├── 30-git-conventions.md          # Git 慣例
├── 40-testing.md                  # 測試原則
└── 50-security.md                 # 安全性指引
```

使用數字前綴可以控制載入順序（雖然通常不重要）。

### 語言特定規則

如果您經常使用特定程式語言，可以建立語言特定的規則檔案：

```
~/.augment/rules/
├── personal-preferences.md        # 通用偏好
├── typescript-style.md            # TypeScript 特定規則
├── python-style.md                # Python 特定規則
└── csharp-style.md                # C# 特定規則
```

## 相關資源

- [Auggie CLI Rules 設定指南](auggie-cli-rules.md)
- [Auggie MCP 整合指南](auggie-mcp-guide.md)

