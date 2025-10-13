# 🎯 Writerside 測試快速指南

> 為 Mac M4 (Apple Silicon) 使用者優化的測試解決方案

## ⚡ 快速開始（推薦）

```bash
# 最快速的測試方式（2-3 分鐘）
./test-with-github.sh
```

這個腳本會：
1. ✅ 自動提交並推送變更
2. ✅ 開啟 GitHub Actions 頁面
3. ✅ 等待測試完成（可選）
4. ✅ 自動下載錯誤報告（如果失敗）

---

## 📊 測試方式對比

| 方式 | 時間 | 推薦度 | 適用場景 |
|------|------|--------|---------|
| **GitHub Actions** | 2-3 分鐘 | ⭐⭐⭐⭐⭐ | 日常開發（推薦） |
| **本地測試** | 10-30 分鐘 | ⭐⭐ | 離線工作、緊急情況 |

### 為什麼 GitHub Actions 更快？

- ✅ 原生 linux/amd64 環境（無需模擬）
- ✅ 高效能 CI/CD 伺服器
- ✅ 自動化程度高
- ✅ 免費（公開專案）

### 為什麼本地測試慢？

- ⚠️ Mac M4 是 ARM 架構
- ⚠️ Docker image 只支援 x86_64
- ⚠️ 需要 Rosetta 2 模擬執行
- ⚠️ 效能損失 5-10 倍

---

## 🛠️ 可用工具

### 1. test-with-github.sh（推薦）
使用 GitHub Actions 測試，最快速可靠

```bash
./test-with-github.sh
```

### 2. check-writerside.sh
本地 Docker 測試（慢，僅緊急情況）

```bash
./check-writerside.sh
```

### 3. fix-writerside-errors.sh
自動修復常見錯誤

```bash
./fix-writerside-errors.sh
```

### 4. writerside-workflow.sh
完整工作流程（測試 → 修復 → 驗證 → 提交）

```bash
./writerside-workflow.sh
```

---

## 📖 詳細文檔

- **[TESTING-README.md](TESTING-README.md)** - 完整工具說明
- **[WRITERSIDE-TEST-STRATEGY.md](WRITERSIDE-TEST-STRATEGY.md)** - 測試策略（必讀）
- **[WRITERSIDE-LOCAL-TEST.md](WRITERSIDE-LOCAL-TEST.md)** - 本地測試指南

---

## 🔗 快速連結

- [GitHub Actions](https://github.com/jakeuj/writerside/actions) - 查看測試結果
- [GitHub Pages](https://jakeuj.github.io/writerside/) - 查看發布的文檔
- [JetBrains 官方文檔](https://www.jetbrains.com/help/writerside/) - Writerside 使用指南

---

## 💡 最佳實踐

1. **優先使用 GitHub Actions**（快 5-10 倍）
2. **批次修改後一次性推送**（減少 CI 次數）
3. **使用自動修復腳本**（快速處理常見錯誤）
4. **安裝 GitHub CLI**（更好的整合體驗）

```bash
# 安裝 GitHub CLI
brew install gh
gh auth login
```

---

## ❓ 常見問題

**Q: 為什麼本地測試這麼慢？**  
A: Mac M4 是 ARM 架構，Docker image 只支援 x86_64，需要模擬執行。建議使用 GitHub Actions。

**Q: 如何加速測試？**  
A: 使用 `./test-with-github.sh`，透過 GitHub Actions 測試只需 2-3 分鐘。

**Q: 測試失敗了怎麼辦？**  
A: 腳本會自動下載錯誤報告，或手動執行：
```bash
gh run download --name report.json
cat report.json | jq '.errors'
./fix-writerside-errors.sh  # 自動修復
```

---

## 🎉 開始使用

```bash
# 1. 修改文檔
vim Writerside/topics/your-topic.md

# 2. 測試（推薦方式）
./test-with-github.sh

# 3. 完成！
```

就是這麼簡單！🚀

