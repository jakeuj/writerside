# Docker 建構重要說明

## 🎯 關鍵發現

### ❌ Apple Silicon Mac 無法運行 Writerside Builder

**已確認**：Writerside Builder Docker image 在 Apple Silicon (M1/M2/M3) Mac 上**無法運行**。

**錯誤現象**：
- 容器在初始化階段就被終止
- 退出碼：133
- 錯誤訊息：`interrupted by signal 5:SIGTRAP`
- 即使使用 `--platform linux/amd64` 也無法解決

**結論**：Apple Silicon Mac 用戶必須使用 Writerside IDE 或 GitHub Actions。

---

### Docker 建構過程中的「錯誤」訊息實際上是正常的

在執行 Writerside Docker 建構時（Linux/Windows），你會看到大量的 `SEVERE` 和 `WARN` 級別訊息。**這些不是真正的錯誤**！

## 📊 訊息類型分析

### 1. 平台警告（可忽略）
```
WARNING: The requested image's platform (linux/amd64) does not match 
the detected host platform (linux/arm64/v8)
```
- **原因**：在 Apple Silicon Mac 上運行 x86 Docker image
- **影響**：會比較慢，但可以正常運行
- **處理**：忽略，這是預期的行為

### 2. JVM 警告（可忽略）
```
[0.044s][warning][cds] Archived non-system classes are disabled because 
the java.system.class.loader property is specified
```
- **原因**：JVM 的類加載器配置
- **影響**：無，不影響建構
- **處理**：忽略

### 3. IDE 內部警告（可忽略）
```
2025-10-13 09:52:37,179 [   3414] SEVERE - #c.i.s.ComponentManagerImpl - 
com.jetbrains.rdserver.unattendedHost.portForwarding.ui.data.ForwardedPortUiData 
<clinit> requests com.intellij.l10n.LocalizationStateService instance...
```
- **原因**：JetBrains IDE 內部服務初始化順序問題
- **影響**：無，這是 IDE 框架的內部警告
- **處理**：完全忽略，與文檔建構無關

### 4. 其他常見警告（可忽略）
```
WARN - #c.i.i.s.p.i.BundledSharedIndexProvider - 
Bundled shared index is not found at: /opt/builder/jdk-shared-indexes

WARN - #c.i.u.Alarm - 
Do not create alarm without coroutineScope

WARN - #c.i.s.ComponentManagerImpl - 
`preload=TRUE` must be used only for core services
```
- **原因**：IDE 內部組件的配置警告
- **影響**：無
- **處理**：忽略

## ✅ 真正重要的訊息

### 建構開始
```
Preparing "/opt/sources" for build.
```
**這才是關鍵！** 看到這個訊息表示建構正在正常進行。

### 建構成功
```
✅ 建構完成!
```
或者檢查 `artifacts/` 目錄是否包含：
- `report.json` - 檢查報告
- `webHelpHI2-all.zip` - 建構的網站檔案

## ⏱️ 預期建構時間

### Linux / Windows (x86)
- **正常時間**：2-5 分鐘
- **首次建構**：可能需要 5-10 分鐘（下載依賴）

### macOS Apple Silicon (ARM64)
- ❌ **無法完成建構**
- **錯誤**：容器會在初始化階段被終止（SIGTRAP）
- **替代方案**：使用 Writerside IDE（原生 ARM64，建構時間 2-3 分鐘）

## 🚫 常見錯誤：過早中斷建構

### 錯誤行為
```bash
# 看到 SEVERE/WARN 訊息就按 Ctrl+C
^C
```

### 正確行為
```bash
# 看到警告訊息 → 繼續等待
# 看到 "Preparing for build" → 繼續等待
# 等待 5-10 分鐘 → 看到 "✅ 建構完成!"
```

## 🔍 如何判斷建構是否真的失敗

### 真正的失敗會顯示：
1. **明確的錯誤訊息**（不是 SEVERE/WARN）
2. **非零退出碼**（通常是 1 或 2，不是 133）
3. **artifacts/ 目錄為空**或沒有 `report.json`

### 退出碼說明
- `0` - 成功
- `1-2` - 建構錯誤（真正的問題）
- `133` - 被中斷（通常是手動 Ctrl+C 或超時）
- `137` - 記憶體不足（OOM killed）

## 💡 最佳實踐

### 1. 使用正確的工具

**Apple Silicon Mac**：
```bash
# ✅ 使用 Writerside IDE 建構（原生 ARM64，最快、最穩定）
# 然後執行檢查腳本
./local-test-checker-only.sh

# ❌ 不要使用 Docker 建構（會失敗）
```

**Linux/Windows**：
```bash
# ✅ 可以使用 Docker 完整建構
./local-test.sh
```

### 2. 給予足夠的時間
```bash
# 不要在看到警告時就中斷
# 等待至少 10 分鐘（Apple Silicon）
# 等待至少 5 分鐘（x86）
```

### 3. 檢查結果
```bash
# 建構完成後檢查
ls -la artifacts/
# 應該看到：
# - report.json
# - webHelpHI2-all.zip
```

### 4. 如果真的失敗
```bash
# 檢查 Docker 記憶體配置
# Docker Desktop → Settings → Resources → Memory
# 建議：8GB 或更多

# 或者使用替代方案
./local-test-checker-only.sh  # 只檢查，不建構
```

## 📝 總結

| 訊息類型 | 級別 | 是否需要處理 | 說明 |
|---------|------|------------|------|
| Platform warning | WARNING | ❌ 否 | Apple Silicon 正常現象 |
| CDS warning | WARNING | ❌ 否 | JVM 內部警告 |
| ComponentManager | SEVERE | ❌ 否 | IDE 框架警告 |
| SharedIndex | WARN | ❌ 否 | IDE 內部警告 |
| Preparing for build | INFO | ✅ 是 | 建構正在進行 |
| 建構完成 | INFO | ✅ 是 | 成功完成 |
| 退出碼 133 | ERROR | ✅ 是 | 被中斷，需重試 |
| 退出碼 1-2 | ERROR | ✅ 是 | 真正的錯誤 |

## 🎓 學到的教訓

1. **不要被 SEVERE/WARN 嚇到** - 這些是 IDE 內部的日誌，不影響建構
2. **耐心等待** - 建構需要時間，特別是在 Apple Silicon 上
3. **使用正確的工具** - IDE 比 Docker 更適合本地開發
4. **檢查實際結果** - 看 `artifacts/` 目錄，不要只看日誌

## 🔗 相關資源

- [完整測試指南](LOCAL_TEST_README.md)
- [詳細文檔](.augment/rules/test.md)
- [JetBrains 官方文檔](https://www.jetbrains.com/help/writerside/)

