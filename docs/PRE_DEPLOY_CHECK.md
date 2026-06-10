# 部署前檢查指南

## 🎯 目的

在推送到 GitHub 前，於本地檢查常見問題，避免 `deploy.yml` 建構失敗。

## ⚡ 快速使用

### 方法 1: 手動執行（推薦新手）

每次推送前執行：

```bash
npm run pre-deploy
```

如果檢查通過，就可以安心推送：

```bash
git push
```

### 方法 2: 自動執行（推薦熟手）

一次性安裝 Git hook：

```bash
npm run install-hooks
```

之後每次 `git push` 都會自動檢查。如果檢查失敗，推送會被阻止。

**跳過檢查**（不建議）：

```bash
git push --no-verify
```

## 📋 檢查項目

部署前檢查腳本會驗證：

1. **Markdown 格式** - 使用 markdownlint-cli2
2. **配置文件存在** - writerside.cfg, hi.tree, buildprofiles.xml
3. **TOC 結構正確** - hi.tree 的 XML 格式（需要 xmllint）

站台 SEO 檔案（`robots.txt`、`CNAME`、sitemap 線上 URL）需要部署後再驗證，因為它們是否可抓取取決於 GitHub Pages artifact。

## 🔧 只修復 Markdown 格式

如果只想修復 Markdown 格式問題：

```bash
# 自動修復
npm run lint:md:fix

# 檢查
npm run lint:md
```

## ⚠️ 重要說明

### 本地檢查 vs GitHub Actions

- **本地檢查**：快速檢查常見格式問題，節省時間
- **GitHub Actions**：完整的 Writerside 建構和測試（權威）

本地檢查通過 ≠ GitHub Actions 一定通過，但可以減少大部分錯誤。

### deploy.yml 失敗的常見原因

1. **Markdown 語法錯誤** ✅ 本地可檢查
2. **hi.tree 結構錯誤** ✅ 本地可檢查
3. **圖片路徑錯誤** ⚠️ 本地難以檢查（需要實際建構）
4. **Writerside 特定語法問題** ⚠️ 需要 Writerside 工具檢查
5. **站台根目錄檔案缺失** ⚠️ 部署後檢查 `robots.txt`、`CNAME` 是否存在

### SEO / Sitemap 部署後檢查

這個 repo 的正式網址是 `https://jakeuj.com/<topic-web-file-name>.html`，不是 `/writerside/master/`。

部署完成後可檢查：

```bash
curl -I https://jakeuj.com/robots.txt
curl -I https://jakeuj.com/sitemap.xml
curl -I https://jakeuj.com/sitemap-index.xml
curl -L https://jakeuj.com/sitemap.xml | grep -o '/writerside/master/' | head
```

正常情況：

- `robots.txt` 回傳 200，內容包含 `Sitemap: https://jakeuj.com/sitemap.xml`
- `sitemap.xml` 回傳 200
- `sitemap-index.xml` 回傳 404 是預期狀態，因為目前站台使用單一 sitemap
- sitemap 不應包含 `/writerside/master/`
- 首頁與高優先文章的 `meta name="description"`、`og:description`、`twitter:description` 與 Schema `description` 不應是空字串
- `og:image` 應指向 `https://jakeuj.com/images/og-image.png`，且圖片回傳 200

Search Console 應提交 `https://jakeuj.com/sitemap.xml`。只有在 sitemap 超過 50,000 URLs、未壓縮超過 50MB，或刻意拆成多個 sitemap 時，才需要改用 sitemap index。

## 🚀 建議工作流程

```bash
# 1. 編輯文檔
vim Writerside/topics/my-article.md

# 2. 更新 TOC（如果是新文章）
vim Writerside/hi.tree

# 3. 部署前檢查
npm run pre-deploy

# 4. 如果有問題，自動修復
npm run lint:md:fix

# 5. 再次檢查
npm run pre-deploy

# 6. 提交推送
git add .
git commit -m "docs: 新增文章"
git push
```

## 📚 相關文檔

- [Markdown Lint 使用指南](MARKDOWN_LINT.md)
- [快速修復指南](QUICK_FIX_GUIDE.md)

## 💡 提示

- 安裝 `xmllint` 以檢查 hi.tree 格式：`brew install libxml2`
- 使用 JetBrains Writerside IDE 可以獲得更好的本地預覽和驗證
