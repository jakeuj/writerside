# Writerside 測試策略指南（Mac M4 / ARM 架構）

## 🚨 重要：ARM 架構限制

經過實際測試，JetBrains 的 `writerside-builder` Docker image 目前只支援 **linux/amd64** 架構。

### 在 Mac M4 (ARM64) 上的問題

當在 Apple Silicon (M1/M2/M3/M4) 上執行時：

- ⚠️ Docker 會使用 Rosetta 2 模擬 x86_64 架構
- 🐌 **執行速度極慢**（測試顯示可能需要 10-30 分鐘以上）
- 💻 消耗大量 CPU 和記憶體資源
- ⏱️ 可能會出現超時或記憶體不足的問題
- ❌ 不適合日常開發使用

### 實測結果

```
測試環境：Mac M4, 16GB RAM
Docker Image: jetbrains/writerside-builder:2025.04.8412
測試時間：超過 10 分鐘仍在運行（最終被中止）
```

---

## ✅ 推薦測試策略

### 方案一：使用 GitHub Actions（強烈推薦）

這是**最快速、最可靠**的測試方式：

#### 優點
- ⚡ **速度快**：約 2-3 分鐘完成
- 🎯 **準確**：原生 linux/amd64 環境，無需模擬
- 🔄 **自動化**：推送即測試
- 📊 **完整報告**：自動生成 report.json
- 💰 **免費**：GitHub Actions 對公開專案免費

#### 使用步驟

1. **推送程式碼到 GitHub**：
   ```bash
   git add .
   git commit -m "docs: 更新文檔"
   git push origin master
   ```

2. **查看測試結果**：
   ```bash
   # 在瀏覽器中開啟 Actions 頁面
   open https://github.com/jakeuj/writerside/actions
   
   # 或使用 GitHub CLI
   gh run list --limit 5
   gh run view --web
   ```

3. **如果測試失敗，下載錯誤報告**：
   ```bash
   # 使用 GitHub CLI 下載 artifacts
   gh run download --name report.json
   
   # 查看錯誤
   cat report.json | jq '.errors'
   ```

4. **修復錯誤後再次推送**：
   ```bash
   # 修復錯誤...
   git add .
   git commit -m "fix: 修正 Writerside 錯誤"
   git push origin master
   ```

#### 工作流程範例

```bash
# 1. 修改文檔
vim Writerside/topics/some-topic.md

# 2. 提交並推送
git add .
git commit -m "docs: 更新某主題"
git push origin master

# 3. 等待 2-3 分鐘，查看結果
gh run view --web

# 4. 如果失敗，下載報告並修復
gh run download --name report.json
cat report.json | jq '.errors[] | "[\(.code)] \(.file):\(.line) - \(.message)"'

# 5. 修復後再次推送
# ... 重複步驟 1-3
```

---

### 方案二：本地測試（僅緊急情況）

**⚠️ 警告**：本地測試在 ARM 架構上非常慢，僅在以下情況使用：

- 🔌 離線工作，無法連接 GitHub
- 🚨 緊急情況，需要立即驗證單一修復
- 🧪 測試腳本本身的功能

#### 使用方式

```bash
# 執行測試（需要 10-30 分鐘）
./check-writerside.sh

# 查看結果
cat artifacts/report.json | jq
```

#### 注意事項

1. **預留充足時間**：至少 30 分鐘
2. **避免同時執行其他任務**：會消耗大量資源
3. **確保電源充足**：避免筆電進入省電模式
4. **監控進度**：可以查看 Docker Desktop 的 CPU 使用率

---

## 🔧 常見錯誤修復指南

### MRK002: Source file syntax is corrupted

**原因**：未閉合的 XML/HTML 標籤，例如 `<T>`、`<int>` 被誤認為 XML。

**修復方式**：

```markdown
# ❌ 錯誤寫法
返回 IQueryable<T>

# ✅ 正確寫法（在文字中）
返回 `IQueryable<T>`

# ✅ 正確寫法（在程式碼區塊中）
```csharp
IQueryable<T> GetAll()
```
```

**自動修復**：
```bash
./fix-writerside-errors.sh
```

### MRK003: Element ID is not unique

**原因**：多個標題產生了相同的 ID。

**修復方式**：

```markdown
# ❌ 錯誤寫法
### DTO
### DTO

# ✅ 正確寫法
### GetAuthorListDto - 獲取作者列表
### CreateAuthorDto - 創建作者
```

### CTT004: Undefined variable

**原因**：URL 中的 URL 編碼字符（如 `%E6%B7%BB%E5%8A%A0`）被誤認為變數。

**修復方式**：

```markdown
# ❌ 錯誤寫法
<https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0>

# ✅ 方法 1: 使用 Markdown 連結語法
[ABP 官方教學](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0)

# ✅ 方法 2: 使用 ignore-vars 屬性
<https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0>
{ignore-vars="true"}
```

---

## 📊 測試結果對比

| 測試方式 | 執行時間 | CPU 使用率 | 可靠性 | 推薦度 |
|---------|---------|-----------|--------|--------|
| GitHub Actions | 2-3 分鐘 | N/A (遠端) | ⭐⭐⭐⭐⭐ | ✅ 強烈推薦 |
| 本地測試 (ARM) | 10-30+ 分鐘 | 80-100% | ⭐⭐⭐ | ⚠️ 僅緊急情況 |

---

## 🎯 最佳實踐

### 日常開發流程

1. **批次修改**：累積多個文檔修改後一次性推送
2. **使用 GitHub Actions**：讓 CI/CD 自動測試
3. **快速迭代**：根據測試結果快速修復並再次推送
4. **本地預覽**：使用 Writerside IDE 預覽文檔外觀（不需要完整測試）

### 緊急修復流程

如果必須使用本地測試：

1. **確認問題範圍**：只測試修改的檔案
2. **使用自動修復腳本**：`./fix-writerside-errors.sh`
3. **驗證修復**：執行 `./check-writerside.sh`（預留 30 分鐘）
4. **推送到 GitHub**：最終還是要通過 GitHub Actions 驗證

---

## 🔗 相關資源

- [GitHub Actions 工作流程](.github/workflows/deploy.yml)
- [本地測試腳本](./check-writerside.sh)
- [自動修復腳本](./fix-writerside-errors.sh)
- [完整工作流程腳本](./writerside-workflow.sh)
- [JetBrains 官方文檔](https://www.jetbrains.com/help/writerside/build-with-docker.html)
- [專案 GitHub Actions](https://github.com/jakeuj/writerside/actions)
- [專案 GitHub Pages](https://jakeuj.github.io/writerside/)

---

## 💡 總結

**對於 Mac M4 使用者**：

1. ✅ **優先使用 GitHub Actions** - 快速、可靠、免費
2. ⚠️ **避免本地測試** - 除非絕對必要
3. 🔄 **擁抱快速迭代** - 推送 → 測試 → 修復 → 再推送
4. 📝 **使用 IDE 預覽** - Writerside IDE 可以即時預覽文檔外觀

**記住**：在 ARM 架構上，GitHub Actions 比本地測試快 **5-10 倍**！

