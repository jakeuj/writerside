# GitHub Copilot Instructions - Writerside 技術筆記

這是一個使用 JetBrains Writerside 構建的中文技術筆記專案，內容涵蓋開發技術、雲端服務、AI 工具等多個技術領域。

## Configuration
- **Language**: Traditional Chinese (zh-tw)

## Shell Tools Usage Guidelines
⚠️ **IMPORTANT**: Use the following specialized tools instead of traditional Unix commands: (Install if missing)
| Task Type | Must Use | Do Not Use |
|-----------|----------|------------|
| Find Files | `fd` | `find`, `ls -R` |
| Search Text | `rg` (ripgrep) | `grep`, `ag` |
| Analyze Code Structure | `ast-grep` | `grep`, `sed` |
| Interactive Selection | `fzf` | Manual filtering |
| Process JSON | `jq` | `python -m json.tool` |
| Process YAML/XML | `yq` | Manual parsing |

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
4. **測試**：推送後檢查 GitHub Actions 建構是否成功
5. **驗證**：確認在 GitHub Pages 上的顯示效果

## 技術重點領域

當協助此專案時，重點關注這些技術領域的內容：
- **ABP Framework**：.NET 開發框架相關文檔
- **Flutter**：行動應用開發，特別是 iOS 憑證和 Azure AD 整合
- **雲端服務**：Azure、GCP、AWS 的服務設定和部署
- **容器化**：Docker 相關配置和最佳實務
- **開發工具**：JetBrains IDE、Git 工作流程