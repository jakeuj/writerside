# Writerside 本地測試與修復 Prompt

## 快速開始 Prompt

```
請幫我執行 Writerside 本地測試並修復所有錯誤：

1. 使用 Docker 執行 Writerside 檢查
2. 解析 artifacts/report.json 中的錯誤
3. 逐一修復所有錯誤
4. 再次執行測試確認修復成功
5. 提交並推送所有修改

專案資訊：
- 專案根目錄：/Users/jakeuj/WritersideProjects/writerside
- Writerside instance：Writerside/hi
- Docker 版本：jetbrains/writerside-checker:2025.04.8412
```

---

## 詳細步驟 Prompt

### 步驟 1: 執行本地測試

```
請幫我執行 Writerside 本地測試：

1. 在專案根目錄執行以下 Docker 命令：
   docker run --rm \
     -v "$PWD":/docs \
     jetbrains/writerside-checker:2025.04.8412 \
     "artifacts/report.json" "Writerside/hi"

2. 使用 jq 格式化並顯示錯誤：
   cat artifacts/report.json | jq '.errors'

3. 統計錯誤數量並分類顯示
```

### 步驟 2: 分析錯誤

```
請分析 artifacts/report.json 中的錯誤，並按照以下格式整理：

1. 錯誤類型統計（MRK002, MRK003, CTT004 等）
2. 每個錯誤的具體位置（檔案名稱和行號）
3. 錯誤原因分析
4. 建議的修復方案
```

### 步驟 3: 修復錯誤

```
請根據錯誤報告逐一修復所有問題：

常見錯誤類型：

1. MRK002 (Source file syntax is corrupted)
   - 未閉合的 XML/HTML 標籤（如 <T>, <int>）
   - 修復：用反引號包裹或放入程式碼區塊

2. MRK003 (Element ID is not unique)
   - 重複的標題產生相同 ID
   - 修復：為標題添加唯一的描述或前綴

3. CTT004 (Undefined variable)
   - URL 編碼字符被誤認為變數
   - 修復：使用 Markdown 連結語法或添加 {ignore-vars="true"}

請修復所有錯誤後，再次執行測試確認。
```

### 步驟 4: 驗證與提交

```
請完成以下驗證與提交步驟：

1. 再次執行 Docker 測試確認所有錯誤已修復
2. 檢查 artifacts/report.json 確認錯誤數為 0
3. 使用 git status 查看修改的檔案
4. 提交修改並推送到 GitHub：
   - 使用有意義的 commit message
   - 包含修復的錯誤類型和數量
5. 提供 GitHub Actions 連結讓我確認 CI/CD 狀態
```

---

## 一鍵執行 Prompt（推薦）

```
請幫我完整執行 Writerside 測試與修復流程：

【步驟 1】執行本地測試
- 使用 Docker 執行 Writerside 檢查
- 命令：docker run --rm -v "$PWD":/docs jetbrains/writerside-checker:2025.04.8412 "artifacts/report.json" "Writerside/hi"

【步驟 2】分析錯誤
- 解析 artifacts/report.json
- 按錯誤類型分類統計
- 列出所有錯誤的檔案和行號

【步驟 3】修復錯誤
- 根據錯誤類型逐一修復：
  * MRK002: 將 <T>, <int> 等用反引號包裹
  * MRK003: 為重複標題添加唯一描述
  * CTT004: 處理 URL 編碼問題
- 修復過程中顯示進度

【步驟 4】驗證修復
- 再次執行 Docker 測試
- 確認錯誤數為 0

【步驟 5】提交推送
- git add -A
- git commit -m "🐛 修復(docs): 修正 Writerside 檢查器錯誤"
- git push origin master
- 提供 GitHub Actions 連結

專案資訊：
- 根目錄：/Users/jakeuj/WritersideProjects/writerside
- Instance：Writerside/hi
- Docker 版本：2025.04.8412
```

---

## 進階選項

### 只測試不修復

```
請幫我執行 Writerside 本地測試，但不要修復錯誤：

1. 執行 Docker 檢查
2. 顯示所有錯誤的詳細資訊
3. 提供修復建議但不實際修改檔案
```

### 只修復特定類型錯誤

```
請只修復 MRK002 類型的錯誤：

1. 執行 Docker 檢查
2. 過濾出 MRK002 錯誤
3. 只修復這些錯誤
4. 驗證並提交
```

### 批次處理多個檔案

```
請批次修復以下檔案中的所有 Writerside 錯誤：

檔案列表：
- Writerside/topics/ABP.md
- Writerside/topics/Flutter.md
- Writerside/topics/Docker.md

修復後統一提交。
```

---

## 常見問題處理

### 如果 Docker 測試失敗

```
Docker 測試執行失敗，請幫我：

1. 檢查 Docker 是否正在運行
2. 確認 Docker 映像版本是否正確
3. 檢查專案路徑是否正確
4. 提供替代的測試方法（如使用 GitHub Actions 日誌）
```

### 如果錯誤太多

```
錯誤數量超過 50 個，請幫我：

1. 先統計各類型錯誤的數量
2. 優先修復數量最多的錯誤類型
3. 分批次提交修復（每次不超過 20 個檔案）
4. 每次修復後執行測試確認
```

### 如果出現新的錯誤類型

```
出現了不在常見錯誤列表中的新錯誤類型，請：

1. 查看錯誤的詳細描述
2. 搜尋 Writerside 官方文檔
3. 提供可能的修復方案
4. 如果無法確定，建議我手動檢查
```

---

## 使用範例

### 範例 1: 完整流程

```
我剛修改了 10 個 Markdown 檔案，請幫我執行完整的 Writerside 測試與修復流程。
```

### 範例 2: 快速檢查

```
我想快速檢查目前的文檔是否有錯誤，不需要修復，只要告訴我有哪些問題。
```

### 範例 3: 針對性修復

```
GitHub Actions 報告有 5 個 MRK003 錯誤，請幫我只修復這些重複 ID 的問題。
```

---

## 注意事項

1. **執行前確認**：確保在專案根目錄（與 `.idea` / `Writerside` 同層）
2. **Docker 版本**：使用與 GitHub Actions 相同的版本 `2025.04.8412`
3. **備份建議**：大量修改前建議先建立 Git 分支
4. **測試頻率**：每次修復後都應該重新測試
5. **提交訊息**：使用清晰的 commit message 說明修復內容

---

## 相關資源

- [JetBrains 官方指南](https://www.jetbrains.com/help/writerside/testing-your-docs-locally.html)
- [writerside-checker-action](https://github.com/JetBrains/writerside-checker-action)
- [專案 GitHub Actions](https://github.com/jakeuj/writerside/actions)
- [專案 GitHub Pages](https://jakeuj.github.io/writerside/)

