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

**注意**：Docker 方式在 macOS ARM64 (Apple Silicon) 上可能遇到相容性問題，建議使用方法一或方法二。

如果您使用 Linux 或 Windows，可以嘗試以下方式：

```bash
# 在專案根目錄執行（與 .idea / Writerside 同層）
docker run --rm \
  -v "$PWD":/opt/sources \
  registry.jetbrains.team/p/writerside/builder/writerside-builder:2025.04.8412 \
  /opt/builder/bin/idea.sh helpbuilderinspect \
  --source-dir /opt/sources \
  --product Writerside/hi \
  --runner other \
  --output-dir /opt/sources/artifacts/
```

**已知問題**：
- macOS ARM64 需要使用 `--platform linux/amd64` 但可能很慢
- Docker image 的使用方式與 GitHub Action 封裝不同
- 需要正確的掛載路徑和參數配置

**建議**：如果 Docker 方式失敗，請使用方法一（Writerside IDE）或方法二（GitHub Actions）

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

**原因**: URL 中的 URL 編碼字符（如 `%E6%B7%BB%E5%8A%A0`）被誤認為變數引用。

**修復方式**:
```markdown
# 方法 1: 使用 Markdown 連結語法
[ABP 官方教學](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0)

# 方法 2: 使用 {ignore-vars="true"} 屬性
<https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0>
{ignore-vars="true"}
```

### MRK058: Large image in paragraph

**原因**: 大圖片被放在段落內，Writerside 預設會將大圖片渲染為區塊元素，可能導致排版問題。

**修復方式**:
```markdown
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
```

**參考文檔**: 詳細說明請參考 `Writerside/topics/MRK058-Large-image.md`

## 參考資源

- [JetBrains 官方指南 - 本地測試 Writerside](https://www.jetbrains.com/help/writerside/testing-your-docs-locally.html)
- [writerside-checker-action GitHub Repository](https://github.com/JetBrains/writerside-checker-action)