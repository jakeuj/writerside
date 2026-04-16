# Writerside Checker Errors

在下列情況讀這份參考：

- GitHub Actions 或 Writerside checker 報錯，但 `markdownlint-cli2` 沒報錯
- 遇到 `MRK003: Element ID is not unique`
- 遇到 `CTT004`、`MRK002`、`MRK009` 這類 Writerside 專屬錯誤
- 懷疑是 anchor、圖片、topic 路徑、變數展開或 `hi.tree` 掛載問題

## 常見問題對照

| 症狀 | 常見原因 | 優先檢查 | 常見修法 |
| --- | --- | --- | --- |
| `MRK003: Element ID is not unique` | 多個標題被 Writerside 轉成同一個 id | 相近標題、標題內的 inline code、重複英文關鍵詞，例如 `RDS`、`API` | 直接補唯一 `{#...}` anchor |
| `CDE016: Unknown language is specified for a code block` | fenced code block 或 `<code-block lang="...">` 使用 Writerside 不認得的語言名稱 | `cmd`、`csharp`、拼錯或自訂語言名稱 | 改成 checker 支援的語言，例如 `batch`、`C#`，不確定時用 `text` |
| `CTT004: Undefined variable` | 文字、URL、圖片引用或 code block 中的 `%...%` 被當成 Writerside 變數 | `%foo%`、SQL `LIKE '%KEYWORD%'`、Windows PATH、URL percent-encoding（例如 `%E5...`、`%20`、`%25`） | 短內容補 `ignore-vars="true"`；多行 code block 改用 `<code-block ignore-vars="true"><![CDATA[...]]></code-block>` |
| `TOC007: The 'toc-title' attribute is redundant as it matches the topic title` | `hi.tree` 的 `toc-title` 和 topic H1 完全相同 | 該 topic 的 H1 與 `<toc-element toc-title="...">` | 移除 redundant `toc-title`，保留 `topic` 即可 |
| checker 找不到 topic | `hi.tree` 的檔名與實際檔名不一致 | `Writerside/hi.tree`、topic 檔名 | 修正 `topic="..."` 或檔名 |
| 圖片無法顯示或建構失敗 | 圖片不在 `Writerside/images/`、引用路徑錯誤 | 圖片檔名、Markdown 引用 | 把檔案放到 `Writerside/images/`，並用相對路徑引用 |
| TOC 看得到但點了失敗 | 文章改名後沒同步 `hi.tree` | `Writerside/hi.tree` | 同步更新 `topic` 屬性 |
| XML 標記區塊解析異常 | `<tabs>`、`<warning>` 等區塊格式不完整 | XML 區塊前後空行、成對標籤 | 補齊標籤並整理空行 |
| `MRK002` / `MRK009` 出現在 `<tabs>` 附近 | `<tab>` 內混太多 HTML list、提醒框、code block，或 `tab` 結構被 Markdown 解析打斷 | 報錯行附近的 `<tabs>`、`<tab>`、空行、巢狀 HTML 結構 | 先簡化成較單純的 `<p> + code-block` 結構，必要時改回一般 Markdown 小節 |

## Anchor 命名慣例

- 優先用小寫英文加連字號，例如 `{#why-native-nvme-is-faster}`
- 讓 id 反映章節意圖，不要只用流水號
- 若兩個標題共用英文關鍵詞，主動補顯式 anchor，不要等 checker 報錯
- 標題含 inline code 時特別容易留下相同英文片段；只要看起來會重複 `RDS`、`API`、`skill`、`plugin` 這類詞，就先補唯一 anchor
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

## `CDE016` 修法流程

1. 找出 checker 指出的 code block 語言。
2. 若是 Windows Command Prompt，改用 `batch`，不要用 `cmd`。
3. 若是 C#，改用 `C#`，不要用 `csharp`。
4. 若只是命令輸出、錯誤訊息或不需要高亮的內容，改用 `text`。
5. 用 `rg -n '^```(cmd|csharp)$' Writerside/topics/<topic-file>.md` 確認沒有留下常見錯誤標籤。

## `CTT004` 修法流程

1. 找出錯誤行附近是否有 `%...%`。SQL `LIKE '%FASTFIRSTROW%'`、`'%READTEXT%'` 這類 pattern 也算。
2. 若是 Markdown link、image、inline code 或短句，先在該元素補 `{ignore-vars="true"}` 或 `ignore-vars="true"`。
3. 若是多行 fenced code block，尤其有多個 `%...%`，優先改成 XML code block 並用 `CDATA` 包住內容：

    ```xml
    <code-block lang="sql" ignore-vars="true"><![CDATA[
    SELECT *
    FROM sys.sql_modules
    WHERE definition LIKE '%READTEXT%';
    ]]></code-block>
    ```

4. 修改後跑 `npx markdownlint-cli2 --no-globs Writerside/topics/<topic-file>.md`，確認沒有因為 fenced code 後的屬性位置再觸發 `MD031`。

## `TOC007` 修法流程

1. 找出 `hi.tree` 報錯行。
2. 打開對應 topic，確認 H1。
3. 如果 `toc-title` 和 H1 完全相同，移除 `toc-title`；只有需要更短或不同側欄文字時才保留。
4. 修改後跑 `xmllint --noout Writerside/hi.tree`。

## `MRK002` / `MRK009` 快速排查

1. 如果行號落在 `<tabs>` / `<tab>` 區塊附近，先檢查是否有未關閉標記、過多 HTML list，或被空行切斷的 XML 結構。
2. 若 `<tabs>` 內容已經很長、混很多元素，先以「能穩定通過 checker」為優先，必要時退回一般 Markdown 小節，不必硬保留 tabs。

## 相關檔案

- `Writerside/hi.tree`
- `scripts/pre-deploy-check.sh`
- `.github/workflows/deploy.yml`
