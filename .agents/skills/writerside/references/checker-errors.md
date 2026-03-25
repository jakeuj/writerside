# Writerside Checker Errors

在下列情況讀這份參考：

- GitHub Actions 或 Writerside checker 報錯，但 `markdownlint-cli2` 沒報錯
- 遇到 `MRK003: Element ID is not unique`
- 懷疑是 anchor、圖片、topic 路徑或 `hi.tree` 掛載問題

## 常見問題對照

| 症狀 | 常見原因 | 優先檢查 | 常見修法 |
|------|----------|----------|----------|
| `MRK003: Element ID is not unique` | 多個標題被 Writerside 轉成同一個 id | 相近標題、重複英文關鍵詞 | 直接補唯一 `{#...}` anchor |
| checker 找不到 topic | `hi.tree` 的檔名與實際檔名不一致 | `Writerside/hi.tree`、topic 檔名 | 修正 `topic="..."` 或檔名 |
| 圖片無法顯示或建構失敗 | 圖片不在 `Writerside/images/`、引用路徑錯誤 | 圖片檔名、Markdown 引用 | 把檔案放到 `Writerside/images/`，並用相對路徑引用 |
| TOC 看得到但點了失敗 | 文章改名後沒同步 `hi.tree` | `Writerside/hi.tree` | 同步更新 `topic` 屬性 |
| XML 標記區塊解析異常 | `<tabs>`、`<warning>` 等區塊格式不完整 | XML 區塊前後空行、成對標籤 | 補齊標籤並整理空行 |

## Anchor 命名慣例

- 優先用小寫英文加連字號，例如 `{#why-native-nvme-is-faster}`
- 讓 id 反映章節意圖，不要只用流水號
- 若兩個標題共用英文關鍵詞，主動補顯式 anchor，不要等 checker 報錯
- 如果標題之後可能改名，但希望外部連結穩定，保留既有 anchor

## Anchor 範例

```markdown
## 為什麼 Native NVMe 可能會比較快 {#why-native-nvme-is-faster}
## 如果你以前已經開過非官方 Native NVMe {#existing-native-nvme-users}
## 本地檢查與 CI 差異 {#local-vs-ci-validation}
```

## `MRK003` 修法流程

1. 找出錯誤行號對應的標題或元素。
2. 判斷是不是 Writerside 忽略中文，只留下英文片段產生 slug。
3. 直接為衝突的標題補唯一 `{#...}`。
4. 重新跑單檔 lint，再做 Writerside 層級檢查。

## 相關檔案

- `Writerside/hi.tree`
- `scripts/pre-deploy-check.sh`
- `.github/workflows/deploy.yml`
