---
type: "agent_requested"
description: "當需要本地測試 Writerside 文檔、執行文檔檢查、或修復 Writerside 建構錯誤和警告時，參考此規則"
---

# 本地測試 Writerside 文檔

在推送到 GitHub 之前，可以在本地執行與 GitHub Actions 相同的檢查，避免 CI/CD 失敗。

## 方法一：使用 Docker 執行 Writerside 檢查

在專案根目錄執行（與 `.idea` / `Writerside` 同層）：

```bash
# 方法 1: 使用 writerside-checker（推薦，與 GitHub Actions 一致）
docker run --rm \
  -v "$PWD":/docs \
  jetbrains/writerside-checker:2025.04.8412 \
  "Writerside/hi"

# 方法 2: 使用完整的 builder 進行建構和檢查
docker run --rm \
  -v "$PWD":/opt/sources \
  registry.jetbrains.team/p/writerside/builder/writerside-builder:2025.04.8412 \
  --instance "Writerside/hi" \
  --artifact "artifacts/webHelpHI2-all.zip" \
  --output "artifacts"
```

**參數說明**：
- `jetbrains/writerside-checker:2025.04.8412` - 使用與 GitHub Actions 相同的版本
- `"Writerside/hi"` - Writerside instance 名稱（對應 `writerside.cfg` 中的設定）
- 第二個參數可選：`true` 或 `false` 表示是否為 group instance（預設為 `false`）
- 執行後會在 `artifacts/` 目錄產生 `report.json`，包含所有錯誤和警告

**注意**：
- writerside-checker 會自動在 `artifacts/` 目錄下尋找或生成 `report.json`
- 如果 `artifacts/report.json` 不存在，checker 會先執行建構流程
- 確保專案根目錄有 `artifacts/` 目錄的寫入權限

### 查看檢查結果

```bash
# 使用 jq 格式化輸出
cat artifacts/report.json | jq

# 或只顯示錯誤
cat artifacts/report.json | jq '.errors'

# 或只顯示警告
cat artifacts/report.json | jq '.warnings'
```

## 方法二：使用 IntelliJ IDEA / Writerside IDE

1. 安裝 [Writerside IDE](https://www.jetbrains.com/writerside/) 或在 IntelliJ IDEA 中安裝 Writerside Plugin
2. 開啟專案
3. 執行：**Build → Build Documentation**
4. IDE 會在下方顯示具體的錯誤行數與問題

### 常見錯誤修復

### MRK002: Source file syntax is corrupted

**原因**: 未閉合的 XML/HTML 標籤，例如 `<T>`、`<int>` 被 Writerside 認為是 XML 而非 Markdown code。

**修復方式**:
```markdown
# 錯誤寫法
返回 IQueryable<T>

# 正確寫法
返回 `IQueryable<T>`
```

或使用程式碼區塊：
````markdown
```csharp
Func<T>
```
````

### MRK003: Element ID is not unique

**原因**: 多個標題產生了相同的 ID。

**修復方式**:
```markdown
# 錯誤寫法
### DTO
### DTO

# 正確寫法
### GetAuthorListDto - 獲取作者列表
### CreateAuthorDto - 創建作者
```

### CTT004: Undefined variable

**原因**: URL 中的 URL 編碼字符（如 `%E6%B7%BB%E5%8A%A0`）被誤認為變數引用。

**修復方式**:
```markdown
# 方法 1: 使用 Markdown 連結語法
[ABP 官方教學](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0)

# 方法 2: 使用 {ignore-vars="true"} 屬性
<https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0>
{ignore-vars="true"}
```

### MRK058: Large image in paragraph

**原因**: 大圖片被放在段落內，Writerside 預設會將大圖片渲染為區塊元素，可能導致排版問題。

**修復方式**:
```markdown
# 方法 1: 將圖片放在段落外（推薦）
# 在圖片前後加空行，使其成為獨立的區塊

這是一段文字。

![flutter-project.png](flutter-project.png)

這是另一段文字。

# 方法 2: 使用 style 屬性明確指定為行內元素
這是一段文字 ![flutter-project.png](flutter-project.png){ style="inline" } 繼續文字。

# 方法 3: 在列表中使用圖片時，添加適當縮排
1. 列表項目標題

   ![圖片說明](image.png)

   圖片說明文字
```

**參考文檔**: 詳細說明請參考 `Writerside/topics/MRK058-Large-image.md`

## 參考資源

- [JetBrains 官方指南 - 本地測試 Writerside](https://www.jetbrains.com/help/writerside/testing-your-docs-locally.html)
- [writerside-checker-action GitHub Repository](https://github.com/JetBrains/writerside-checker-action)