---
type: "agent_requested"
description: "當需要本地測試 Writerside 文檔、執行文檔檢查、或修復 Writerside 建構錯誤和警告時，參考此規則"
---

# 本地測試 Writerside 文檔

在推送到 GitHub 之前，可以在本地執行與 GitHub Actions 相同的檢查，避免 CI/CD 失敗。

## 方法一：使用 IntelliJ IDEA / Writerside IDE（推薦）

1. 安裝 [Writerside IDE](https://www.jetbrains.com/writerside/) 或在 IntelliJ IDEA 中安裝 Writerside Plugin
2. 開啟專案（開啟包含 `Writerside` 目錄的根目錄）
3. 執行：**Build → Build Documentation**
4. IDE 會在下方的 **Build** 面板顯示具體的錯誤行數與問題
5. 點擊錯誤訊息可直接跳轉到對應的文件位置

**優點**：
- 即時語法檢查和錯誤提示
- 可直接點擊錯誤跳轉到問題位置
- 支援預覽功能，可即時查看文檔效果
- 與 GitHub Actions 使用相同的檢查引擎

## 方法二：推送到 GitHub 讓 CI/CD 驗證

如果沒有安裝 Writerside IDE，最簡單的方式是直接推送到 GitHub：

1. 提交並推送變更到 `main` 或 `master` 分支
2. 前往 GitHub Actions 頁面查看建構結果
3. 在 **Test documentation** 步驟中查看詳細的錯誤和警告

**查看方式**：
- 前往 `https://github.com/jakeuj/writerside/actions`
- 點擊最新的 workflow run
- 展開 **Test documentation** 步驟查看檢查結果

**優點**：
- 無需本地安裝任何工具
- 與生產環境完全一致的檢查
- 可以在 GitHub 上直接查看建構產物

## 方法三：使用 Docker 執行 Writerside 檢查（進階）

**⚠️ Apple Silicon Mac 重要提醒**：
Writerside Builder 的 Docker image 是 x86 架構，在 Apple Silicon (M1/M2/M3) Mac 上**無法穩定運行**。容器會在初始化階段被系統終止（SIGTRAP signal 5，退出碼 133）。

**Apple Silicon 用戶請使用**：
- ✅ 方法一：Writerside IDE（最推薦）
- ✅ 方法二：GitHub Actions
- ✅ 本節的「僅檢查」腳本（配合 IDE 或 GitHub Actions）

**適用平台**：
- ✅ Linux (x86_64)
- ✅ Windows (x86_64)
- ❌ macOS Apple Silicon（不支援完整建構，僅支援檢查）

### 步驟 1：建構文檔並生成 report.json（僅限 Linux/Windows）

首先需要使用 Writerside Builder 建構文檔並生成檢查報告：

```bash
# 在專案根目錄執行（與 Writerside 目錄同層）
# ⚠️ 此命令在 Apple Silicon Mac 上會失敗
docker run --rm \
  -v "$PWD":/opt/sources \
  registry.jetbrains.team/p/writerside/builder/writerside-builder:2025.04.8412 \
  /opt/builder/bin/idea.sh helpbuilderinspect \
  --source-dir /opt/sources \
  --product Writerside/hi \
  --runner other \
  --output-dir /opt/sources/artifacts/
```

**說明**：
- 這個步驟會建構文檔並在 `artifacts/` 目錄下生成 `report.json`
- `--product Writerside/hi` 中的 `hi` 是你的 instance ID，需要與 `writerside.cfg` 中的設定一致
- 建構完成後會在 `artifacts/` 目錄看到 `webHelpHI2-all.zip` 和 `report.json`
- **預期時間**：Linux/Windows 約 2-5 分鐘

### 步驟 2：執行文檔檢查器

建構完成後，使用 writerside-checker 檢查 report.json：

```bash
# 方法 A：使用 writerside-checker-action 的 Docker image
docker run --rm \
  -v "$PWD":/github/workspace \
  -w /github/workspace \
  ghcr.io/jetbrains/writerside-checker-action:latest \
  artifacts/report.json \
  Writerside/hi \
  false

# 方法 B：手動執行 checker JAR（與 GitHub Action 完全相同）
docker run --rm \
  -v "$PWD":/opt/sources \
  -w /opt/sources \
  openjdk:18-jdk-slim \
  bash -c "apt-get update && apt-get install -y curl && \
    curl -o wrs-doc-app.jar -L https://packages.jetbrains.team/maven/p/writerside/maven/com/jetbrains/writerside/writerside-ci-checker/1.0/writerside-ci-checker-1.0.jar && \
    java -jar wrs-doc-app.jar artifacts/report.json Writerside/hi false"
```

**參數說明**：
- 第一個參數：`artifacts/report.json` - 報告檔案路徑
- 第二個參數：`Writerside/hi` - instance 或 group ID
- 第三個參數：`false` - 是否為 group（true/false）

### 完整的本地測試腳本（僅限 Linux/Windows）

專案根目錄提供了 `local-test.sh` 腳本來自動化整個流程：

```bash
#!/bin/bash
set -e

echo "🔨 步驟 1: 建構 Writerside 文檔..."
docker run --rm \
  -v "$PWD":/opt/sources \
  registry.jetbrains.team/p/writerside/builder/writerside-builder:2025.04.8412 \
  /opt/builder/bin/idea.sh helpbuilderinspect \
  --source-dir /opt/sources \
  --product Writerside/hi \
  --runner other \
  --output-dir /opt/sources/artifacts/

echo ""
echo "✅ 建構完成!"
echo ""
echo "🔍 步驟 2: 執行文檔檢查..."

docker run --rm \
  -v "$PWD":/opt/sources \
  -w /opt/sources \
  openjdk:18-jdk-slim \
  bash -c "..."  # 執行檢查邏輯

echo ""
echo "✅ 檢查完成!"
```

**使用方式（僅限 Linux/Windows）**：
```bash
chmod +x local-test.sh
./local-test.sh
```

**Apple Silicon Mac 用戶**：
此腳本會自動檢測 Apple Silicon 並顯示警告，但**仍會失敗**。請改用：
```bash
# 1. 使用 Writerside IDE 建構文檔
# 2. 然後執行僅檢查腳本
chmod +x local-test-checker-only.sh
./local-test-checker-only.sh
```

### macOS Apple Silicon 專用方案

**❌ 已確認問題**：Writerside Builder Docker image 在 Apple Silicon Mac 上**無法運行**。

**錯誤現象**：
- 容器在初始化階段就被終止
- 退出碼：133 (SIGTRAP signal 5)
- 錯誤訊息：`interrupted by signal 5:SIGTRAP`
- 原因：x86 模擬的相容性問題

**即使加上 `--platform linux/amd64` 也無法解決此問題。**

---

**✅ Apple Silicon Mac 推薦方案**：

#### 方案 A：使用 Writerside IDE（最推薦）⭐

**步驟**：
1. 安裝 [Writerside IDE](https://www.jetbrains.com/writerside/)
2. 開啟專案
3. 執行：**Build → Build Documentation**
4. 查看 Build 面板的錯誤和警告

**優點**：
- ✅ 原生 ARM64 支援，速度快
- ✅ 即時錯誤提示和跳轉
- ✅ 支援預覽功能
- ✅ 與 GitHub Actions 使用相同的檢查引擎

---

#### 方案 B：IDE 建構 + 本地檢查腳本

**步驟 1**：使用 Writerside IDE 建構文檔
- 在 IDE 中執行 **Build → Build Documentation**
- 這會在 `artifacts/` 目錄生成 `report.json`

**步驟 2**：執行本地檢查腳本
```bash
chmod +x local-test-checker-only.sh
./local-test-checker-only.sh
```

**優點**：
- ✅ 結合 IDE 的建構速度和命令列的自動化
- ✅ 可以在 CI/CD 流程中使用相同的檢查邏輯
- ✅ 適合需要腳本化測試的場景

---

#### 方案 C：使用 GitHub Actions

**步驟**：
1. 推送代碼到 GitHub
2. 前往 `https://github.com/jakeuj/writerside/actions`
3. 查看最新的 workflow run
4. 在 **Test documentation** 步驟查看檢查結果

**下載 artifacts 進行本地檢查**：
1. 從 Actions 頁面下載 `docs` artifact
2. 解壓到專案根目錄的 `artifacts/` 資料夾
3. 執行 `./local-test-checker-only.sh`

**優點**：
- ✅ 無需本地安裝任何工具
- ✅ 與生產環境完全一致
- ✅ 可以查看完整的建構日誌

---

#### ❌ 不推薦：強制使用 Docker

```bash
# ⚠️ 此命令在 Apple Silicon Mac 上會失敗
docker run --rm \
  --platform linux/amd64 \
  -v "$PWD":/opt/sources \
  registry.jetbrains.team/p/writerside/builder/writerside-builder:2025.04.8412 \
  /opt/builder/bin/idea.sh helpbuilderinspect \
  --source-dir /opt/sources \
  --product Writerside/hi \
  --runner other \
  --output-dir /opt/sources/artifacts/
```

**已知問題**：
- ❌ 容器會被系統終止（SIGTRAP）
- ❌ 無法完成建構
- ❌ 沒有可行的解決方案

**結論**：在 Apple Silicon Mac 上，請使用方案 A、B 或 C。

### 查看檢查結果

檢查完成後：
- ✅ 如果沒有錯誤，會顯示 "No errors found"
- ❌ 如果有錯誤，會列出所有錯誤和警告，並返回非零退出碼

你也可以直接查看 `artifacts/report.json` 檔案來了解詳細的檢查結果。

### 關於建構過程中的警告訊息

在執行 Docker 建構時，你會看到許多 `SEVERE` 和 `WARN` 級別的訊息，例如：

```
2025-10-13 09:52:37,179 [   3414] SEVERE - #c.i.s.ComponentManagerImpl -
com.jetbrains.rdserver.unattendedHost.portForwarding.ui.data.ForwardedPortUiData <clinit>
requests com.intellij.l10n.LocalizationStateService instance...

2025-10-13 09:52:38,303 [   4538]   WARN - #c.i.i.s.p.i.BundledSharedIndexProvider -
Bundled shared index is not found at: /opt/builder/jdk-shared-indexes
```

**這些訊息可以安全忽略**：
- 這些是 JetBrains IDE 內部框架的警告
- 與文檔建構功能無關
- 不會影響最終的建構結果

**關鍵訊息**：
當你看到以下訊息時，表示建構正在正常進行：
```
Preparing "/opt/sources" for build.
```

**重要**：不要在看到警告訊息時就按 `Ctrl+C` 中斷建構！建構過程可能需要 5-10 分鐘（在 Apple Silicon 上可能更久），請耐心等待直到看到：
```
✅ 建構完成!
```

## 常見錯誤修復

### MRK002: Source file syntax is corrupted

**原因**: 未閉合的 XML/HTML 標籤，例如 `<T>`、`<int>` 被 Writerside 認為是 XML 而非 Markdown code。

**修復方式**:
```markdown
# 錯誤寫法
返回 IQueryable<T>

# 正確寫法
返回 `IQueryable<T>`
```

或使用程式碼區塊：
````markdown
```csharp
Func<T>
```
````

### MRK003: Element ID is not unique

**原因**: 多個標題產生了相同的 ID。

**修復方式**:
```markdown
# 錯誤寫法
### DTO
### DTO

# 正確寫法
### GetAuthorListDto - 獲取作者列表
### CreateAuthorDto - 創建作者
```

### CTT004: Undefined variable

**原因**:
- URL 中的 URL 編碼字符（如 `%E6%B7%BB%E5%8A%A0`）被誤認為變數引用
- 行內程式碼中的 `%variable%` 語法（如 Windows 環境變數 `%windir%`）被誤認為 Writerside 變數

**修復方式**:

#### 情況 1: URL 中的百分號編碼

```markdown
# 方法 1: 使用 Markdown 連結語法（推薦）
[ABP 官方教學](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0)

# 方法 2: 在連結後添加 {ignore-vars="true"}
- [msdn](http://social.msdn.microsoft.com/Forums/en/netfx64bit/thread/8b0ed9bb){ignore-vars="true"}
- [google](http://www.google.com.tw/search?q=%E5%9C%A8){ignore-vars="true"}
```

#### 情況 2: 行內程式碼中的變數語法

**重要**: `{ignore-vars="true"}` 必須**緊接在行內程式碼後面**，不能放在段落前面。

```markdown
# ❌ 錯誤寫法 - 放在段落前面無效
{ignore-vars="true"}

1. 複製檔案到 `%windir%\system32`
2. 執行命令 `%windir%\system32\cmd.exe`

# ✅ 正確寫法 - 緊接在每個行內程式碼後面
1. 複製檔案到 `%windir%\system32`{ignore-vars="true"}
2. 執行命令 `%windir%\system32\cmd.exe`{ignore-vars="true"}
```

**實際範例**:
```markdown
1. 複製 capicom.dll 到 `%windir%\syswow64`{ignore-vars="true"}
2. 執行 CMD 命令 `%windir%\syswow64\regsvr32.exe %windir%\syswow64\capicom.dll`{ignore-vars="true"}
```

### MRK058: Large image in paragraph

**原因**: 大圖片被放在段落內，Writerside 預設會將大圖片渲染為區塊元素，可能導致排版問題。

**修復方式**:
````markdown
# 方法 1: 將圖片放在段落外（推薦）
# 在圖片前後加空行，使其成為獨立的區塊

這是一段文字。

![flutter-project.png](flutter-project.png)

這是另一段文字。

# 方法 2: 使用 style 屬性明確指定為行內元素
這是一段文字 ![flutter-project.png](flutter-project.png){ style="inline" } 繼續文字。

# 方法 3: 在列表中使用圖片時，添加適當縮排
1. 列表項目標題

   ![圖片說明](image.png)

   圖片說明文字
````

**參考文檔**: 詳細說明請參考 `Writerside/topics/MRK058-Large-image.md`

## 參考資源

- [JetBrains 官方指南 - 本地測試 Writerside](https://www.jetbrains.com/help/writerside/testing-your-docs-locally.html)
- [writerside-checker-action GitHub Repository](https://github.com/JetBrains/writerside-checker-action)