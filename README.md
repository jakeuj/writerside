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
2. 打開 `Writerside/hi.tree`，把新文章加到對應的 `<toc-element>`（不加會很難在導覽中找到）
3. 圖片放到 `Writerside/images/`，在 Markdown 內以相對路徑引用（依 Writerside 規則）
4. **部署前檢查**：`npm run pre-deploy`（檢查 Markdown 格式和配置文件）
5. 本機預覽確認沒問題後再推送

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
> 這個專案是標準 Writerside 結構；最穩定的方式是用 JetBrains Writerside IDE 直接開啟並 Build。

### 方法 A：使用 JetBrains Writerside（建議）
1. 用 JetBrains IDE（支援 Writerside 的版本）開啟此 repo
2. 開啟 `Writerside/writerside.cfg`
3. 在 IDE 內執行 **Build / Preview**（依你的 IDE 版本，命名可能略有不同）

### 方法 B：CI（GitHub Actions）
此 repo 通常會透過 GitHub Actions 在推送到主要分支後自動建置並部署到 GitHub Pages。

如果你在這個 repo 找不到 `.github/workflows/`，代表 workflow 可能在別處維護、或尚未加入；但不影響本機用 Writerside 產出與預覽。

## 常見問題
- **新增文章後側邊欄沒出現？**
  通常是忘了更新 `Writerside/hi.tree`。
- **圖片顯示不出來？**
  確認圖片放在 `Writerside/images/`，並檢查 Markdown 的引用路徑與檔名大小寫。
