# Writerside 技術筆記

這個 repo 是用 **JetBrains Writerside** 維護的中文（zh-tw）技術筆記，內容涵蓋 .NET/ABP、Flutter、Docker、雲端服務、AI 工具等。

## 線上閱讀

- GitHub Pages：<https://jakeuj.github.io/writerside/default-topic.html>
- 自訂網域：<https://jakeuj.com/>（由 `CNAME` 指向）

## 專案結構（重點）

- `Writerside/topics/`：所有文章（Markdown）
- `Writerside/images/`：文章用圖片
- `Writerside/hi.tree`：目錄（TOC）樹狀結構，決定側邊欄與導覽
- `Writerside/writerside.cfg`：Writerside 專案設定（topics/images 位置、instance 設定）
- `Writerside/cfg/`：建置設定（主題、Analytics、搜尋等）
- `scripts/`：一些資料整理/產文的輔助腳本（跟 Writerside build 無強耦合）

## 新增/修改文章流程

1. 在 `Writerside/topics/` 新增或編輯 `*.md`
2. 先決定 topic 檔名、H1 標題與側欄顯示名稱
3. 打開 `Writerside/hi.tree`，把新文章加到對應的 `<toc-element>`（不加會很難在導覽中找到）
4. 如果 H1 太長，優先在 `hi.tree` 補較短的 `toc-title`，避免側欄 menu 太擠
5. 圖片放到 `Writerside/images/`，在 Markdown 內以相對路徑引用（依 Writerside 規則）
6. **部署前檢查**：`npm run pre-deploy`（檢查 Markdown 格式和配置文件）
7. 本機預覽確認沒問題後再推送

### Topic 檔名、標題與側欄名稱

- `Writerside/topics/*.md` 的檔名會影響預設的 web page name / URL，建議保持簡短、穩定、可讀。
- 目前這個 repo 的公開文章 URL，可概念化成 `https://jakeuj.com/` + `writerside/master/` + `<topic-web-file-name>.html`。
- Markdown 文章的第一個 `# H1` 是 topic title，會顯示成頁面主標題，也會被 Writerside 當成對應 TOC/menu 項目的標題。
- `Writerside/hi.tree` 的 `toc-title` 只影響側欄顯示名稱，不改 URL。
- 如果想避開中文 URL，新文章的 topic 檔名優先用 ASCII / English kebab-case，不要把中文或拼音當成預設 slug。
- 如果文章標題需要保留完整關鍵字，但側欄顯示太長，請在 `Writerside/hi.tree` 的 `<toc-element>` 上加 `toc-title`。
- 已發布文章如果改 topic 檔名，等於改變 URL；調整前要一併考慮 redirect 或舊連結更新，例如 `Writerside/redirection-rules.xml` 或 `accepts-web-file-names`。

對照範例：

| topic 檔名 | H1 | `toc-title` | 預期 URL |
| ------ | ------ | ------ | -------- |
| `azure-app-service-vnet-tcpping-timeout.md` | `# Azure App Service VNet Integration 經 S2S VPN 使用 tcpping timeout 排錯` | `VNet/S2S VPN timeout 排錯` | `/writerside/master/azure-app-service-vnet-tcpping-timeout.html` |
| `nswag-settings-httpclient-startup.md` | `# NSwag Settings 與 HttpClient Startup` | `NSwag + HttpClient Startup` | `/writerside/master/nswag-settings-httpclient-startup.html` |
| `windows-11-native-nvme-enable.md` | `# Windows 11 啟用 Native NVMe` | `啟用 Native NVMe` | `/writerside/master/windows-11-native-nvme-enable.html` |

範例：

```xml
<toc-element topic="windows-11-native-nvme-enable.md" toc-title="啟用 Native NVMe" />
```

## 部署前檢查（避免 CI/CD 失敗）

為了避免推送後 GitHub Actions 建構失敗，建議在本地先執行檢查：

### 手動檢查

```bash
# 完整的部署前檢查（推薦）
npm run pre-deploy

# 或只檢查 Markdown 格式
npm run lint:md:fix
```

### 自動檢查（推薦）

安裝 Git pre-push hook，在每次推送前自動檢查：

```bash
# 一次性安裝
npm run install-hooks
```

安裝後，每次 `git push` 前會自動執行檢查。如需跳過檢查：

```bash
git push --no-verify
```

## Markdown 格式檢查

專案使用 `markdownlint-cli2` 確保文檔格式一致性。

### 快速使用

```bash
# 安裝依賴
npm install

# 檢查格式
npm run lint:md

# 自動修復格式問題
npm run lint:md:fix
```

### 詳細說明

- 📖 [完整使用指南](docs/MARKDOWN_LINT.md)
- 🚀 [快速修復指南](docs/QUICK_FIX_GUIDE.md)
- 📋 [修復總結](docs/MARKDOWN_LINT_FIX_SUMMARY.md)

**注意**：本地 Markdown 檢查是輔助工具，主要的建構驗證仍由 GitHub Actions 的 Writerside 工具執行。

## 本機預覽與建置
>
> 這個專案是標準 Writerside 結構；最穩定的方式是用 JetBrains Writerside IDE 直接開啟並 Build。

### 方法 A：使用 JetBrains Writerside（建議）

1. 用 JetBrains IDE（支援 Writerside 的版本）開啟此 repo
2. 開啟 `Writerside/writerside.cfg`
3. 在 IDE 內執行 **Build / Preview**（依你的 IDE 版本，命名可能略有不同）

### 方法 B：CI（GitHub Actions）

此 repo 通常會透過 GitHub Actions 在推送到主要分支後自動建置並部署到 GitHub Pages。

如果你在這個 repo 找不到 `.github/workflows/`，代表 workflow 可能在別處維護、或尚未加入；但不影響本機用 Writerside 產出與預覽。

## 贊助

如果這些筆記對你有幫助，歡迎贊助支持：

- [PayPal.me/jakeuj](https://paypal.me/jakeuj)

## 常見問題

- **新增文章後側邊欄沒出現？**
  通常是忘了更新 `Writerside/hi.tree`。
- **側邊欄 menu 太長、不好閱讀？**
  不一定要縮短 H1；通常在 `Writerside/hi.tree` 補 `toc-title` 就可以只縮短側欄顯示名稱。
- **文章檔名要不要跟標題一樣長？**
  不建議。檔名會影響預設 URL，通常比 H1 更需要短、穩定、好維護。
- **圖片顯示不出來？**
  確認圖片放在 `Writerside/images/`，並檢查 Markdown 的引用路徑與檔名大小寫。
