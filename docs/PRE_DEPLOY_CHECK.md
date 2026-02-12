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

