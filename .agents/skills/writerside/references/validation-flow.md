# Validation Flow

在下列情況讀這份參考：

- 不確定該跑單檔檢查還是整體檢查
- 本地檢查通過，但 CI 的 Writerside checker 失敗
- 想理解 `markdownlint-cli2`、`pre-deploy`、CI checker 各自抓什麼

## 檢查層級

| 層級 | 指令或位置 | 主要用途 | 抓不到什麼 |
| ------ | ------------ | ---------- | ------------ |
| 單檔 Markdown | `npx markdownlint-cli2 --no-globs Writerside/topics/<topic-file>.md` | 快速確認單篇格式 | Writerside checker 錯誤 |
| 單檔 Markdown 修復 | `npx markdownlint-cli2 --fix --no-globs Writerside/topics/<topic-file>.md` | 修可自動修復的格式問題 | Writerside checker 錯誤 |
| 全站 Markdown | `./scripts/check-markdown.sh` | 掃整個 `Writerside/topics/**/*.md` | Writerside checker 錯誤 |
| 本地部署前檢查 | `npm run pre-deploy` | Markdown + 必要配置檔 + `hi.tree` XML | 真正的 Writerside build/checker 問題 |
| CI 權威檢查 | `.github/workflows/deploy.yml` | Writerside build + checker + GitHub Pages deploy + Algolia publish | 無，這是最接近正式結果的一層 |

## 為什麼單檔要加 `--no-globs`

這個 repo 的 `.markdownlint-cli2.jsonc` 內有：

```json
"globs": [
  "Writerside/topics/**/*.md"
]
```

如果不加 `--no-globs`，即使你命令列只指定一個檔案，`markdownlint-cli2` 還是可能把整個 `Writerside/topics/**/*.md` 一起掃進來。

## 推薦流程

### 只改一篇文章

1. 需要自動修復時先跑 `npx markdownlint-cli2 --fix --no-globs Writerside/topics/<topic-file>.md`。
2. 跑 `npx markdownlint-cli2 --no-globs Writerside/topics/<topic-file>.md`。
3. 依內容掃描常見 code language、識別資料與內部環境殘留：

    ```bash
    rg -n '^```(cmd|csharp)$' Writerside/topics/<topic-file>.md
    rg -n '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}' Writerside/topics/<topic-file>.md
    rg -n '/subscriptions/|resourceGroups/|privatelink|\.corp|\.local|@' Writerside/topics/<topic-file>.md
    ```

4. 若用了 Writerside XML，依 `checker-errors.md` 掃描未 escape 的字元。
5. 若更新 `hi.tree`，執行 `xmllint --noout Writerside/hi.tree`。
6. 修改 `hi.tree`、XML 或站台設定後跑 `npm run pre-deploy`。
7. 如果仍懷疑 checker 問題，回頭看 CI 或 IDE 預覽。

### 同時改多篇文章

1. 先跑 `./scripts/check-markdown.sh`。
2. 再跑 `npm run pre-deploy`。
3. 等 CI 的 Writerside checker 當最終判定。

### 遇到 CI 才出現的錯

優先懷疑這幾類：

- anchor / element id 衝突
- `hi.tree` 掛載錯誤
- 圖片或 topic 路徑錯誤
- `%...%` 被 Writerside 當成變數，例如 Windows PATH 或 URL percent-encoding
- Writerside XML 標記格式問題
- `<tabs>` / `<tab>` 混用複雜 HTML 結構造成的語法或上下文錯誤
- GitHub Pages 權限、artifact 或 `web-path` 路徑問題

這類問題通常不是 `markdownlint-cli2` 的責任範圍。

## 大型 section 的索引大小

大型表格、匯入矩陣或 generated reference page 要額外確認每個 H2 section 的 UTF-8 大小。以 8000 bytes 為保守上限；超過時回到 `topic-authoring-workflow.md` 分段。可用下列 Node.js 檢查：

```bash
node - Writerside/topics/<topic-file>.md <<'NODE'
const fs = require('fs');
const text = fs.readFileSync(process.argv[2], 'utf8');
const sections = text.split(/(?=^## )/m)
  .filter((section) => section.startsWith('## '))
  .map((section) => ({
    title: section.split('\n', 1)[0],
    bytes: Buffer.byteLength(section, 'utf8'),
  }))
  .sort((a, b) => b.bytes - a.bytes);
console.table(sections.slice(0, 10));
if (sections.some(({ bytes }) => bytes >= 8000)) process.exitCode = 1;
NODE
```

## 相關檔案

- `.markdownlint-cli2.jsonc`
- `scripts/check-markdown.sh`
- `scripts/pre-deploy-check.sh`
- `.github/workflows/deploy.yml`
- `references/build-deploy.md`
