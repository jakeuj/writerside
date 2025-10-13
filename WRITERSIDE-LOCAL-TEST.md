# Writerside 本地測試指南 (Mac M4 / ARM 版本)

> ⚠️ **重要提示**：在 Mac M4 (ARM) 上本地測試非常慢（10-30 分鐘）
> ✅ **強烈建議**：使用 GitHub Actions 測試（2-3 分鐘）
> 📖 **詳細說明**：請參閱 [WRITERSIDE-TEST-STRATEGY.md](WRITERSIDE-TEST-STRATEGY.md)

## 🚀 推薦方式：使用 GitHub Actions

最快速的測試方式：

```bash
# 使用輔助腳本（推薦）
./test-with-github.sh

# 或手動推送
git add .
git commit -m "docs: 更新文檔"
git push origin master

# 查看結果
open https://github.com/jakeuj/writerside/actions
```

---

## 📋 本地測試前置需求

**⚠️ 僅在緊急情況使用本地測試**

### 1. Docker Desktop
確保已安裝並啟動 Docker Desktop for Mac (Apple Silicon 版本)

```bash
# 檢查 Docker 是否運行
docker info | grep "Architecture"
# 應該顯示: Architecture: aarch64
```

### 2. jq (JSON 處理工具)
用於解析錯誤報告

```bash
# 安裝 jq
brew install jq
```

## 🚀 快速開始

### 方法一：完整工作流程（推薦）

執行完整的測試、修復、提交流程：

```bash
./writerside-workflow.sh
```

這個腳本會：
1. ✅ 執行 Writerside 檢查
2. 📊 分析錯誤類型
3. 🔧 詢問是否自動修復
4. 🔄 重新檢查驗證
5. 💾 詢問是否提交變更

### 方法二：只檢查不修復

```bash
./check-writerside.sh
```

查看詳細錯誤報告：

```bash
cat artifacts/report.json | jq
```

### 方法三：只執行自動修復

```bash
./fix-writerside-errors.sh
```

## 📁 檔案說明

| 檔案 | 用途 |
|------|------|
| `writerside-workflow.sh` | 完整工作流程（測試→修復→驗證→提交） |
| `check-writerside.sh` | 只執行 Writerside 檢查 |
| `fix-writerside-errors.sh` | 只執行自動修復 |
| `artifacts/report.json` | 錯誤報告（由 Docker 生成） |

## 🔧 自動修復功能

目前支援自動修復的錯誤類型：

### MRK002: Source file syntax is corrupted

**問題**: 程式碼區塊中錯誤的反引號包裹泛型標記

**範例**:
```markdown
# ❌ 錯誤寫法（會被自動修正）
`IOptions<IdentityOptions>`
`List<T>`
`Func<int>`

# ✅ 正確寫法
IOptions<IdentityOptions>
List<T>
Func<int>
```

**自動修復**: 移除程式碼區塊中多餘的反引號

## 🛡️ 安全機制

### 自動備份
執行 `fix-writerside-errors.sh` 時會自動建立備份：

```bash
.writerside-backup-20250113-143025/
└── topics/
    └── (所有原始檔案)
```

### 還原備份
如果修復結果不理想，可以還原：

```bash
# 找到最新的備份目錄
ls -la | grep writerside-backup

# 還原（替換 YYYYMMDD-HHMMSS 為實際時間戳）
rm -rf Writerside/topics
cp -r .writerside-backup-YYYYMMDD-HHMMSS/topics Writerside/
```

## 🐛 常見錯誤類型

### MRK002: Source file syntax is corrupted
- **原因**: 未閉合的 XML/HTML 標籤，如 `<T>`、`<int>`
- **修復**: 用反引號包裹或放入程式碼區塊
- **自動修復**: ✅ 支援

### MRK003: Element ID is not unique
- **原因**: 重複的標題產生相同 ID
- **修復**: 為標題添加唯一描述
- **自動修復**: ❌ 需手動處理

### CTT004: Undefined variable
- **原因**: URL 編碼字符被誤認為變數
- **修復**: 使用 Markdown 連結語法或添加 `{ignore-vars="true"}`
- **自動修復**: ❌ 需手動處理

## 📊 工作流程範例

### 完整流程

```bash
# 1. 執行完整工作流程
./writerside-workflow.sh

# 輸出範例:
# 🚀 Writerside Complete Workflow
# ================================
# 
# 【Step 1/5】Running Writerside checker...
# 🔍 Checking Writerside docs...
# ✅ Writerside check finished!
# 📊 Error Summary:
#    Errors: 15
#    Warnings: 0
# 
# 【Step 2/5】Analyzing errors...
# Error breakdown:
#   MRK002 (Syntax errors): 12
#   MRK003 (Duplicate IDs): 3
#   CTT004 (Undefined vars): 0
# 
# 【Step 3/5】Auto-fix available for MRK002 errors
# Do you want to apply automatic fixes? (y/n) y
# 
# 🔧 Writerside Auto-Fix Tool
# ==========================
# 📦 Creating backup...
# ✅ Backup created
# 🔍 Scanning and fixing Markdown files...
# Processing: Writerside/topics/ABP.md
#   ✅ Fixed 2 issue(s)
# ...
# 📊 Summary:
#    Files fixed: 8
#    Total fixes: 12
# 
# 【Step 4/5】Re-running checker to verify fixes...
# 📊 Results:
#   Errors before: 15
#   Errors after: 3
#   Fixed: 12
# ✅ Some errors fixed, but 3 remain
# 
# 【Step 5/5】Commit changes?
# Do you want to commit and push the fixes? (y/n) y
# ✅ Changes pushed to GitHub
```

## 🔗 相關資源

- [JetBrains Writerside 官方文檔](https://www.jetbrains.com/help/writerside/)
- [本地測試指南](https://www.jetbrains.com/help/writerside/testing-your-docs-locally.html)
- [writerside-checker-action](https://github.com/JetBrains/writerside-checker-action)
- [專案 GitHub Actions](https://github.com/jakeuj/writerside/actions)
- [專案 GitHub Pages](https://jakeuj.github.io/writerside/)

## 💡 提示

1. **定期測試**: 在推送前執行 `./writerside-workflow.sh`
2. **查看備份**: 自動修復會建立備份，可隨時還原
3. **手動檢查**: 自動修復後建議檢查變更內容
4. **CI/CD 驗證**: 推送後檢查 GitHub Actions 確認通過

## 🆘 疑難排解

### Docker 架構錯誤

```bash
# 錯誤: exec format error
# 解決: 強制拉取 ARM64 版本
docker pull --platform linux/arm64 jetbrains/writerside-checker:latest
```

### jq 未安裝

```bash
# 安裝 jq
brew install jq
```

### 權限問題

```bash
# 重新設定執行權限
chmod +x *.sh
```

## 📝 注意事項

1. **備份重要**: 自動修復前會建立備份，但建議先提交現有變更
2. **檢查變更**: 自動修復後請檢查 `git diff` 確認變更合理
3. **手動處理**: 某些錯誤類型需要手動修復（如 MRK003、CTT004）
4. **測試頻率**: 建議每次修改文檔後都執行本地測試

---

**最後更新**: 2025-01-13  
**適用版本**: Mac M4 (Apple Silicon / ARM)  
**Docker 版本**: jetbrains/writerside-checker:latest (multi-arch)

