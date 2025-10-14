# Writerside 本地測試指南

本專案提供兩個腳本來協助在本地測試 Writerside 文檔。

## 📋 腳本說明

### 1. `local-test.sh` - 完整建構與檢查
執行完整的文檔建構和檢查流程（與 GitHub Actions 相同）。

**適用平台**：
- ✅ Linux (x86_64)
- ✅ Windows (x86_64)
- ❌ macOS Apple Silicon（**無法運行**）

**⚠️ Apple Silicon Mac 重要提醒**：
- Writerside Builder Docker image 在 M1/M2/M3 Mac 上**無法運行**
- 容器會被系統終止（SIGTRAP signal 5，退出碼 133）
- **請使用方法一（Writerside IDE）或方法三（僅檢查）**

### 2. `local-test-checker-only.sh` - 僅執行檢查 ⭐
只執行文檔檢查，不進行建構。需要先有 `artifacts/report.json` 檔案。

**適用平台**：
- ✅ 所有平台（包括 Apple Silicon Mac）

**適用情境**：
- 已經使用 Writerside IDE 建構過文檔
- 從 GitHub Actions 下載了 artifacts
- **Apple Silicon Mac 用戶必須使用此方案**

## 🚀 使用方法

### 方法一：使用 Writerside IDE（最推薦）

1. 安裝 [Writerside IDE](https://www.jetbrains.com/writerside/)
2. 開啟專案
3. 執行：**Build → Build Documentation**
4. 查看 Build 面板的錯誤和警告

**優點**：
- ✅ 最快速、最穩定
- ✅ 即時錯誤提示和跳轉
- ✅ 支援預覽功能
- ✅ 適用於所有平台（包括 Apple Silicon）

### 方法二：完整 Docker 測試（僅限 Linux/Windows）

**⚠️ 此方法不適用於 Apple Silicon Mac**

```bash
# 給予執行權限
chmod +x local-test.sh

# 執行完整測試
./local-test.sh
```

這會：
1. 建構 Writerside 文檔
2. 生成 `artifacts/report.json`
3. 執行文檔檢查
4. 顯示所有錯誤和警告

**Apple Silicon Mac 用戶**：
- ❌ 此腳本會失敗（SIGTRAP 錯誤）
- ✅ 請使用方法一或方法三

### 方法三：僅檢查（Apple Silicon Mac 必須使用）⭐

**步驟 1：使用 IDE 建構文檔**
1. 在 Writerside IDE 中執行 **Build → Build Documentation**
2. 這會在 `artifacts/` 目錄生成 `report.json`

**步驟 2：執行檢查腳本**
```bash
# 給予執行權限
chmod +x local-test-checker-only.sh

# 執行檢查
./local-test-checker-only.sh
```

**為什麼 Apple Silicon Mac 必須使用此方法？**
- Writerside Builder Docker image 是 x86 架構
- 在 ARM64 Mac 上會被系統終止（SIGTRAP）
- 無法通過 `--platform linux/amd64` 解決
- Writerside IDE 有原生 ARM64 支援，速度快且穩定

### 方法四：使用 GitHub Actions artifacts

**步驟 1：從 GitHub 下載 artifacts**
1. 推送代碼到 GitHub
2. 前往 `https://github.com/jakeuj/writerside/actions`
3. 點擊最新的 workflow run
4. 下載 `docs` artifact
5. 解壓到專案根目錄的 `artifacts/` 資料夾

**步驟 2：執行檢查**
```bash
./local-test-checker-only.sh
```

## 📊 檢查結果說明

### 成功
```
✅ 檢查完成! 沒有發現錯誤。
```

### 發現錯誤
腳本會顯示所有錯誤和警告，例如：
```
❌ 檢查發現錯誤或警告，請查看上方輸出。
```

常見錯誤類型：
- **MRK002**: 未閉合的 XML/HTML 標籤
- **MRK003**: 重複的元素 ID
- **CTT004**: 未定義的變數
- **MRK058**: 段落中的大圖片

詳細的錯誤修復方法請參考：`.augment/rules/test.md`

## 🔧 故障排除

### 問題：看到很多 SEVERE 和 WARN 訊息
**這是正常的！**

在 Docker 建構過程中，你會看到許多類似這樣的訊息：
```
2025-10-13 09:52:37,179 [   3414] SEVERE - #c.i.s.ComponentManagerImpl -
com.jetbrains.rdserver.unattendedHost.portForwarding.ui.data.ForwardedPortUiData...

2025-10-13 09:52:38,303 [   4538]   WARN - #c.i.i.s.p.i.BundledSharedIndexProvider -
Bundled shared index is not found...
```

**解決方案**：
- ✅ **這些可以安全忽略**，它們是 JetBrains IDE 內部框架的警告
- ✅ 只要看到 `Preparing "/opt/sources" for build.` 就表示建構正在進行
- ⚠️ **不要按 Ctrl+C 中斷**！建構需要 5-10 分鐘（Apple Silicon 可能更久）
- ✅ 等待直到看到 `✅ 建構完成!` 訊息

### 問題：`artifacts/report.json` 不存在
**解決方案**：
1. 使用 Writerside IDE 建構文檔
2. 或從 GitHub Actions 下載 artifacts
3. 確保 `artifacts/` 目錄存在且包含 `report.json`
4. 如果使用 Docker 建構，確保沒有提前中斷建構過程

### 問題：Docker 容器在 Apple Silicon Mac 上失敗或很慢
**解決方案**：
- 使用方法一（Writerside IDE）- **最推薦**
- 或使用方法三（僅檢查）
- 如果堅持使用 Docker：
  - 確保有足夠的耐心等待（可能需要 10-15 分鐘）
  - 不要在看到警告訊息時就中斷
  - 確保 Docker Desktop 有足夠的記憶體配置（建議 8GB+）

### 問題：建構過程被中斷（退出碼 133）
**可能原因**：
- 手動按了 Ctrl+C
- Docker 記憶體不足
- Apple Silicon 的 x86 模擬超時

**解決方案**：
- 增加 Docker Desktop 的記憶體限制
- 使用 Writerside IDE 代替
- 或使用 GitHub Actions 建構

### 問題：檢查通過但 GitHub Actions 失敗
**可能原因**：
- 本地和遠端的 Docker 版本不同
- 檔案編碼問題
- Git 換行符設定不同

**解決方案**：
- 確保使用相同的 `DOCKER_VERSION`（目前是 `2025.04.8412`）
- 檢查 `.gitattributes` 設定

## 📚 相關資源

- [JetBrains 官方指南 - 本地測試 Writerside](https://www.jetbrains.com/help/writerside/testing-your-docs-locally.html)
- [writerside-checker-action GitHub Repository](https://github.com/JetBrains/writerside-checker-action)
- [專案 GitHub Actions 配置](.github/workflows/deploy.yml)
- [詳細測試文檔](.augment/rules/test.md)

## 💡 最佳實踐

1. **開發時**：使用 Writerside IDE 的即時檢查
2. **提交前**：執行本地檢查腳本確認無誤
3. **推送後**：檢查 GitHub Actions 的建構結果
4. **Apple Silicon 用戶**：優先使用 IDE，避免 Docker 建構

## 🆘 需要幫助？

如果遇到問題：
1. 查看 `.augment/rules/test.md` 的常見錯誤修復
2. 檢查 GitHub Actions 的詳細日誌
3. 確認 Docker 和相關工具已正確安裝

