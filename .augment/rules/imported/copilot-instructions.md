---
type: "always_apply"
---

# GitHub Copilot Instructions - Writerside 技術筆記

這是一個使用 JetBrains Writerside 構建的中文技術筆記專案，內容涵蓋開發技術、雲端服務、AI 工具等多個技術領域。

## 專案架構

### 核心文件結構
- `Writerside/writerside.cfg` - 主要專案設定檔，定義了 topics、images 目錄和實例配置
- `Writerside/hi.tree` - 文件目錄結構樹狀圖，定義所有文檔的階層組織（TOC）
- `Writerside/cfg/buildprofiles.xml` - 建構配置，包含網站主題、Analytics、Algolia 搜索設定
- `Writerside/topics/` - 所有 Markdown 技術文檔的存放目錄
- `Writerside/images/` - 文檔中使用的所有圖片資源

### 發布流程
專案使用 GitHub Actions 自動化建構和發布到 GitHub Pages：
- 觸發條件：push 到 `main` 或 `master` 分支
- 建構工具：JetBrains Writerside Docker builder (`DOCKER_VERSION: '2025.04.8412'`)
- 測試：使用 `writerside-checker-action` 驗證文檔品質
- 發布：自動部署到 GitHub Pages (`https://jakeuj.github.io/writerside/`)
- 搜索：整合 Algolia 搜索功能

## 文檔撰寫規範

### 文檔組織原則
- **按技術領域分類**：ABP、Flutter、Azure、Docker、Python 等主要技術分類
- **支援中英混合**：技術名詞保持英文，說明使用繁體中文
- **問題導向**：多數文檔針對特定問題或安裝步驟提供解決方案

### 內容模式
- **安裝指南**：詳細的軟體安裝步驟和環境設定（如 `ABP.md`、`Docker-Install.md`）
- **問題排除**：常見錯誤和解決方案（如 `detected-dubious-ownership.md`）
- **配置範例**：實用的設定檔和程式碼片段
- **外部連結**：整合原有的點部落格文章連結

### 文檔元數據
- 使用 Writerside XML 格式的 TOC 元素
- 支援 `toc-title` 自訂顯示名稱
- 可使用 `href` 連結到外部資源
- 支援巢狀的多層級文檔結構

## 專案特色設定

### 品牌元素
- **主題色彩**：strawberry 粉紅色調
- **Logo**：初音未來圖示 (`hatsune-miku-seeklogo.svg`)
- **網站根目錄**：`https://jakeuj.com/`

### 整合服務
- **Algolia 搜索**：App ID `8VA5LCDZGD`，索引名稱 `Default`
- **Google Analytics**：透過 `analytics-head-script-file.js` 追蹤
- **社群連結**：包含 Blog、Facebook、GitHub、YouTube 等多個平台

## 新增或修改文檔時

1. **新增文檔**：在 `Writerside/topics/` 建立 `.md` 檔案
2. **更新目錄**：在 `Writerside/hi.tree` 中添加對應的 `<toc-element>` 項目
3. **圖片資源**：將圖片放在 `Writerside/images/` 目錄
4. **本地測試**：使用 Docker 或 Writerside IDE 在本地驗證文檔
5. **推送測試**：推送後檢查 GitHub Actions 建構是否成功
6. **驗證**：確認在 GitHub Pages 上的顯示效果

## 本地測試 Writerside 文檔

在推送到 GitHub 之前，可以在本地執行與 GitHub Actions 相同的檢查，避免 CI/CD 失敗。

### 方法一：使用 Docker 執行 Writerside 檢查

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

#### 查看檢查結果

```bash
# 使用 jq 格式化輸出
cat artifacts/report.json | jq

# 或只顯示錯誤
cat artifacts/report.json | jq '.errors'

# 或只顯示警告
cat artifacts/report.json | jq '.warnings'
```

### 方法二：使用 IntelliJ IDEA / Writerside IDE

1. 安裝 [Writerside IDE](https://www.jetbrains.com/writerside/) 或在 IntelliJ IDEA 中安裝 Writerside Plugin
2. 開啟專案
3. 執行：**Build → Build Documentation**
4. IDE 會在下方顯示具體的錯誤行數與問題

### 常見錯誤修復

#### MRK002: Source file syntax is corrupted

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

#### MRK003: Element ID is not unique

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

#### CTT004: Undefined variable

**原因**: URL 中的 URL 編碼字符（如 `%E6%B7%BB%E5%8A%A0`）被誤認為變數引用。

**修復方式**:
```markdown
# 方法 1: 使用 Markdown 連結語法
[ABP 官方教學](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0)

# 方法 2: 使用 {ignore-vars="true"} 屬性
<https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0>
{ignore-vars="true"}
```

### 參考資源

- [JetBrains 官方指南 - 本地測試 Writerside](https://www.jetbrains.com/help/writerside/testing-your-docs-locally.html)
- [writerside-checker-action GitHub Repository](https://github.com/JetBrains/writerside-checker-action)

## 技術重點領域

當協助此專案時，重點關注這些技術領域的內容：
- **ABP Framework**：.NET 開發框架相關文檔
- **Flutter**：行動應用開發，特別是 iOS 憑證和 Azure AD 整合
- **雲端服務**：Azure、GCP、AWS 的服務設定和部署
- **容器化**：Docker 相關配置和最佳實務
- **開發工具**：JetBrains IDE、Git 工作流程