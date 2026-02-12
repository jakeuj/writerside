# 🎯 調整總結：純本地檢查方案

## 問題理解

你的本意是：
- ✅ 在本機檢查 Markdown，避免 `deploy.yml` 失敗
- ❌ 不想增加額外的 CI/CD 檢查步驟（會導致更多失敗）

## ✅ 已完成的調整

### 1. 移除 GitHub Actions Markdown Lint

- ❌ 刪除 `.github/workflows/markdown-lint.yml`
- ✅ 保持原有的 `deploy.yml` 不變

**理由**：只在本地檢查，不在 CI/CD 增加額外的失敗點。

### 2. 新增本地檢查工具

#### 📝 部署前檢查腳本
**文件**: `scripts/pre-deploy-check.sh`

執行三項檢查：
1. ✅ Markdown 格式（markdownlint-cli2）
2. ✅ 必要的配置文件存在
3. ✅ hi.tree XML 格式正確（可選）

使用方式：
```bash
npm run pre-deploy
```

#### 🪝 Git Pre-Push Hook（可選）
**文件**: `scripts/git-hooks/pre-push`

自動在推送前執行檢查，安裝方式：
```bash
npm run install-hooks
```

### 3. 更新 Package.json

新增兩個實用命令：
- `npm run pre-deploy` - 執行完整的部署前檢查
- `npm run install-hooks` - 安裝 Git hook

### 4. 更新文檔

- ✅ 更新 `README.md` - 強調部署前檢查流程
- ✅ 新增 `docs/PRE_DEPLOY_CHECK.md` - 部署前檢查指南
- ✅ 更新 `docs/MARKDOWN_LINT.md` - 移除 CI/CD 相關內容

## 🚀 推薦使用方式

### 方案 A: 手動檢查（保守）

每次推送前手動執行：

```bash
# 1. 編輯文檔
vim Writerside/topics/my-doc.md

# 2. 檢查
npm run pre-deploy

# 3. 如有問題，修復
npm run lint:md:fix

# 4. 推送
git add .
git commit -m "docs: 更新文檔"
git push
```

### 方案 B: 自動檢查（推薦）

一次性安裝 Git hook：

```bash
npm run install-hooks
```

之後每次推送會自動檢查，失敗會阻止推送。

**跳過檢查**：
```bash
git push --no-verify
```

## 📊 現在的 CI/CD 流程

### GitHub Actions (deploy.yml)

```
push → build → test → deploy → publish-indexes
              ↑
         Writerside 
         官方檢查工具
```

**唯一的檢查點**：Writerside checker（官方工具）

### 本地檢查（新增）

```
編輯 → npm run pre-deploy → git push
      ↑
   可選的 Git hook
   自動執行
```

## ✨ 優點

1. **減少 CI/CD 失敗** - 本地先過濾掉格式問題
2. **不增加 CI/CD 複雜度** - 沒有新的 workflow
3. **靈活性** - 可以選擇手動或自動檢查
4. **快速反饋** - 本地幾秒內就知道問題

## 📝 新增/更新的文件

### 新增
- ✅ `scripts/pre-deploy-check.sh` - 部署前檢查腳本
- ✅ `scripts/git-hooks/pre-push` - Git pre-push hook
- ✅ `docs/PRE_DEPLOY_CHECK.md` - 使用指南

### 更新
- ✅ `package.json` - 新增 pre-deploy 和 install-hooks 命令
- ✅ `README.md` - 更新工作流程說明
- ✅ `docs/MARKDOWN_LINT.md` - 移除 CI/CD 相關內容

### 刪除
- ✅ `.github/workflows/markdown-lint.yml` - 移除獨立的 lint workflow

## 🎯 下一步

### 立即可用

```bash
# 1. 測試部署前檢查
npm run pre-deploy

# 2. 如果想要自動檢查，安裝 hook
npm run install-hooks

# 3. 正常使用
git add .
git commit -m "feat: 調整為純本地檢查方案"
git push
```

### 可選：安裝 xmllint

用於驗證 hi.tree 的 XML 格式：

```bash
brew install libxml2
```

## 💡 提示

- **本地檢查通過 ≠ deploy.yml 一定通過**
  - 本地只檢查格式和配置
  - Writerside 建構還會檢查更多（圖片、連結等）
  
- **如果 deploy.yml 仍然失敗**
  - 查看 GitHub Actions 的錯誤日誌
  - 通常是圖片路徑、連結錯誤等
  - 這些需要實際建構才能發現

- **可以跳過本地檢查**
  - `git push --no-verify`
  - 但建議只在緊急情況使用

## 📚 相關文檔

- [部署前檢查指南](docs/PRE_DEPLOY_CHECK.md)
- [Markdown Lint 使用指南](docs/MARKDOWN_LINT.md)
- [快速修復指南](docs/QUICK_FIX_GUIDE.md)

---

**總結**：現在你有一個純本地的檢查方案，可以在推送前發現大部分問題，而不會增加 CI/CD 的複雜度！🎉

