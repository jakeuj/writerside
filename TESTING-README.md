# Writerside 測試工具總覽

本專案提供多種 Writerside 文檔測試工具，適用於不同場景。

## 🎯 快速選擇指南

| 場景 | 推薦工具 | 執行時間 | 命令 |
|------|---------|---------|------|
| 日常開發 | GitHub Actions | 2-3 分鐘 | `./test-with-github.sh` |
| 快速驗證 | GitHub Actions | 2-3 分鐘 | `git push && gh run watch` |
| 離線工作 | 本地測試 | 10-30 分鐘 | `./check-writerside.sh` |
| 自動修復 | 修復腳本 | < 1 分鐘 | `./fix-writerside-errors.sh` |
| 完整流程 | 工作流程腳本 | 視情況 | `./writerside-workflow.sh` |

---

## 📚 工具說明

### 1. test-with-github.sh（推薦）

**用途**：使用 GitHub Actions 測試文檔（最快速）

**特點**：
- ✅ 自動提交並推送變更
- ✅ 開啟 GitHub Actions 頁面
- ✅ 支援 GitHub CLI 整合
- ✅ 自動下載錯誤報告（如果測試失敗）

**使用方式**：
```bash
./test-with-github.sh
```

**適用場景**：
- 日常開發測試
- 快速驗證修復
- 批次修改後的驗證

---

### 2. check-writerside.sh

**用途**：本地執行 Writerside 測試

**特點**：
- ⚠️ 在 ARM 架構上執行較慢（10-30 分鐘）
- ✅ 離線可用
- ✅ 自動顯示錯誤摘要

**使用方式**：
```bash
./check-writerside.sh
```

**適用場景**：
- 離線工作
- 緊急情況
- 測試腳本功能

---

### 3. fix-writerside-errors.sh

**用途**：自動修復常見的 Writerside 錯誤

**特點**：
- ✅ 自動修復 MRK002 錯誤（未閉合的 XML 標籤）
- ✅ 自動備份原始檔案
- ✅ 顯示修復統計

**使用方式**：
```bash
./fix-writerside-errors.sh
```

**適用場景**：
- 批次修復錯誤
- 快速處理常見問題

---

### 4. writerside-workflow.sh

**用途**：完整的測試、修復、提交工作流程

**特點**：
- ✅ 整合測試、修復、驗證、提交
- ✅ 互動式操作
- ✅ 顯示詳細進度

**使用方式**：
```bash
./writerside-workflow.sh
```

**適用場景**：
- 需要完整流程的情況
- 學習工作流程

---

## 🚀 推薦工作流程

### 方案一：GitHub Actions（推薦）

```bash
# 1. 修改文檔
vim Writerside/topics/some-topic.md

# 2. 使用輔助腳本測試
./test-with-github.sh

# 3. 等待 2-3 分鐘查看結果
# 腳本會自動開啟 GitHub Actions 頁面

# 4. 如果失敗，下載報告並修復
# 腳本會自動詢問是否下載錯誤報告

# 5. 修復後重複步驟 2-4
```

### 方案二：手動 GitHub Actions

```bash
# 1. 修改文檔
vim Writerside/topics/some-topic.md

# 2. 提交並推送
git add .
git commit -m "docs: 更新文檔"
git push origin master

# 3. 查看測試結果
open https://github.com/jakeuj/writerside/actions

# 或使用 GitHub CLI
gh run watch

# 4. 如果失敗，下載報告
gh run download --name report.json
cat report.json | jq '.errors'

# 5. 修復後重複步驟 2-4
```

### 方案三：本地測試（僅緊急情況）

```bash
# 1. 修改文檔
vim Writerside/topics/some-topic.md

# 2. 執行本地測試（需要 10-30 分鐘）
./check-writerside.sh

# 3. 查看錯誤
cat artifacts/report.json | jq '.errors'

# 4. 自動修復常見錯誤
./fix-writerside-errors.sh

# 5. 重新測試驗證
./check-writerside.sh

# 6. 提交變更
git add .
git commit -m "fix: 修正 Writerside 錯誤"
git push origin master
```

---

## 📖 詳細文檔

- **[WRITERSIDE-TEST-STRATEGY.md](WRITERSIDE-TEST-STRATEGY.md)** - 測試策略指南（必讀）
- **[WRITERSIDE-LOCAL-TEST.md](WRITERSIDE-LOCAL-TEST.md)** - 本地測試詳細說明
- **[.augment/rules/writerside-test-prompt.md](.augment/rules/writerside-test-prompt.md)** - AI 輔助測試 Prompt

---

## 🔧 常見錯誤快速修復

### MRK002: 未閉合的 XML 標籤

```bash
# 自動修復
./fix-writerside-errors.sh

# 或手動修復
# 將 <T> 改為 `<T>`
# 將 <int> 改為 `<int>`
```

### MRK003: 重複的 ID

```markdown
# 為重複的標題添加唯一描述
### GetAuthorListDto - 獲取作者列表
### CreateAuthorDto - 創建作者
```

### CTT004: URL 編碼問題

```markdown
# 使用 Markdown 連結語法
[連結文字](https://example.com/path#anchor)

# 或添加 ignore-vars 屬性
<https://example.com/path#anchor>
{ignore-vars="true"}
```

---

## 💡 最佳實踐

1. **優先使用 GitHub Actions**
   - 速度快（2-3 分鐘 vs 10-30 分鐘）
   - 環境一致（原生 linux/amd64）
   - 自動化程度高

2. **批次修改**
   - 累積多個修改後一次性推送
   - 減少 CI/CD 執行次數

3. **使用自動修復腳本**
   - 快速處理常見錯誤
   - 減少手動修改時間

4. **善用 GitHub CLI**
   - 安裝：`brew install gh`
   - 認證：`gh auth login`
   - 快速查看結果：`gh run watch`

---

## 🔗 相關連結

- [GitHub Actions 工作流程](.github/workflows/deploy.yml)
- [專案 GitHub Actions](https://github.com/jakeuj/writerside/actions)
- [專案 GitHub Pages](https://jakeuj.github.io/writerside/)
- [JetBrains Writerside 官方文檔](https://www.jetbrains.com/help/writerside/)

---

## ❓ 常見問題

### Q: 為什麼本地測試這麼慢？

A: JetBrains 的 Docker image 只支援 x86_64 架構，在 Mac M4 (ARM) 上需要模擬執行，因此速度很慢。建議使用 GitHub Actions。

### Q: 如何加速測試？

A: 使用 `./test-with-github.sh` 腳本，透過 GitHub Actions 測試只需 2-3 分鐘。

### Q: 可以跳過測試直接推送嗎？

A: 不建議。GitHub Actions 會自動測試，如果有錯誤會導致部署失敗。建議先測試再推送。

### Q: 如何查看歷史測試結果？

A: 使用 `gh run list` 或訪問 https://github.com/jakeuj/writerside/actions

### Q: 測試失敗了怎麼辦？

A: 
1. 下載錯誤報告：`gh run download --name report.json`
2. 查看錯誤：`cat report.json | jq '.errors'`
3. 修復錯誤（可使用 `./fix-writerside-errors.sh`）
4. 重新推送測試

---

## 📞 需要幫助？

- 查看 [WRITERSIDE-TEST-STRATEGY.md](WRITERSIDE-TEST-STRATEGY.md) 了解詳細策略
- 查看 [WRITERSIDE-LOCAL-TEST.md](WRITERSIDE-LOCAL-TEST.md) 了解本地測試
- 查看 GitHub Actions 日誌了解具體錯誤

