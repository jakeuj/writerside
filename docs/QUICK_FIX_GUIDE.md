# 🚀 快速修復指南

## 立即執行以下步驟修復 2183 個 Markdown 格式錯誤

### 步驟 1: 確保依賴已安裝

```bash
cd /Users/jakeuj/WritersideProjects/writerside
npm install
```

### 步驟 2: 執行自動修復

```bash
# 使用 Python 腳本預處理（修復換行符和空白）
python3 scripts/fix-markdown-format.py

# 使用 markdownlint-cli2 自動修復
npm run lint:md:fix
```

### 步驟 3: 驗證修復結果

```bash
# 檢查是否還有錯誤
npm run lint:md
```

### 步驟 4: 提交更改

```bash
git status
git add .
git commit -m "fix: 修復 Markdown 格式問題並更新 lint 配置

- 新增 .markdownlint-cli2.jsonc 配置文件
- 更新 GitHub Actions workflow 使用正確配置
- 修復所有 Markdown 文件的格式問題
- 新增 lint 工具腳本和文檔

修復了 2183 個格式錯誤"

git push origin main
```

### 步驟 5: 驗證 GitHub Actions

1. 前往 GitHub Actions 頁面
2. 查看最新的 Markdown Lint workflow
3. 確認通過 ✅

## 🎯 預期結果

- ✅ 本地 `npm run lint:md` 應該顯示 0 個錯誤
- ✅ GitHub Actions Markdown Lint workflow 應該通過
- ✅ 所有文檔保持可讀性和正確性

## ❓ 如果仍有錯誤

查看具體錯誤信息：

```bash
npm run lint:md 2>&1 | less
```

手動修復無法自動處理的問題，然後重新執行步驟 2-4。

## 📖 詳細文檔

- [Markdown Lint 使用指南](./MARKDOWN_LINT.md)
- [修復總結](./MARKDOWN_LINT_FIX_SUMMARY.md)

