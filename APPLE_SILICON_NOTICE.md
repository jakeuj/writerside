# ⚠️ Apple Silicon Mac 用戶重要提醒

## 🚫 Docker 建構不可用

Writerside Builder 的 Docker image 在 Apple Silicon (M1/M2/M3) Mac 上**無法運行**。

### 錯誤現象
```
Process finished with exit code 133 (interrupted by signal 5:SIGTRAP)
```

### 原因
- Writerside Builder Docker image 是 x86 架構
- 在 ARM64 Mac 上運行時會被系統終止
- 即使使用 `--platform linux/amd64` 也無法解決
- 這是 x86 模擬的已知限制

### 無法使用的腳本
- ❌ `local-test.sh` - 會失敗
- ❌ 任何包含 `writerside-builder` Docker image 的命令

---

## ✅ 推薦方案

### 方案 1：Writerside IDE（最推薦）⭐

**優點**：
- ✅ 原生 ARM64 支援
- ✅ 速度快（2-3 分鐘）
- ✅ 即時錯誤提示
- ✅ 可以預覽文檔

**步驟**：
1. 安裝 [Writerside IDE](https://www.jetbrains.com/writerside/)
2. 開啟專案
3. 執行：**Build → Build Documentation**
4. 查看 Build 面板的錯誤和警告

---

### 方案 2：IDE + 檢查腳本

**步驟 1**：使用 IDE 建構
```bash
# 在 Writerside IDE 中
Build → Build Documentation
```

**步驟 2**：執行檢查腳本
```bash
chmod +x local-test-checker-only.sh
./local-test-checker-only.sh
```

**優點**：
- ✅ 結合 IDE 速度和腳本自動化
- ✅ 與 GitHub Actions 使用相同的檢查邏輯

---

### 方案 3：GitHub Actions

**步驟**：
1. 推送代碼到 GitHub
2. 前往 Actions 頁面查看結果
3. （可選）下載 artifacts 進行本地檢查

**優點**：
- ✅ 無需本地安裝
- ✅ 與生產環境完全一致

---

## 📊 平台支援對照表

| 功能 | Apple Silicon | Linux/Windows |
|------|--------------|---------------|
| Writerside IDE | ✅ 原生支援 | ✅ 支援 |
| Docker 完整建構 | ❌ 不支援 | ✅ 支援 |
| Docker 僅檢查 | ✅ 支援 | ✅ 支援 |
| GitHub Actions | ✅ 支援 | ✅ 支援 |

## 🔧 可用的腳本

### ✅ `local-test-checker-only.sh`
- **功能**：僅執行檢查（不建構）
- **需求**：需要先有 `artifacts/report.json`
- **平台**：✅ 所有平台（包括 Apple Silicon）

### ❌ `local-test.sh`
- **功能**：完整建構 + 檢查
- **平台**：❌ Apple Silicon 不支援 / ✅ Linux/Windows 支援

---

## 💡 快速開始（Apple Silicon Mac）

```bash
# 1. 使用 Writerside IDE 建構文檔
#    Build → Build Documentation

# 2. 執行檢查腳本
chmod +x local-test-checker-only.sh
./local-test-checker-only.sh

# 3. 查看結果
# ✅ 沒有錯誤 → 可以推送
# ❌ 有錯誤 → 修復後重新建構
```

---

## 🆘 常見問題

### Q: 為什麼不能用 Docker？
**A**: Writerside Builder 是 x86 image，在 ARM64 Mac 上會被系統終止（SIGTRAP）。這是硬體架構限制，無法解決。

### Q: 有沒有 ARM64 版本的 Docker image？
**A**: 目前 JetBrains 沒有提供 ARM64 版本的 Writerside Builder。

### Q: 我一定要安裝 IDE 嗎？
**A**: 不一定。你可以：
- 使用 GitHub Actions（無需本地安裝）
- 或在 Linux/Windows 機器上使用 Docker

### Q: 檢查腳本可以在 Apple Silicon 上運行嗎？
**A**: 可以！`local-test-checker-only.sh` 使用的是標準的 OpenJDK image，支援 ARM64。

---

## 📚 相關文檔

- [完整測試指南](LOCAL_TEST_README.md)
- [詳細文檔](.augment/rules/test.md)
- [Docker 建構說明](DOCKER_BUILD_NOTES.md)

---

## 🎓 總結

**Apple Silicon Mac 用戶**：
1. ✅ **使用 Writerside IDE** - 最快、最穩定
2. ✅ **使用檢查腳本** - 配合 IDE 或 GitHub Actions
3. ❌ **不要使用 Docker 建構** - 會失敗

**記住**：這不是你的問題，是硬體架構的限制！

