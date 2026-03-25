# Writerside Summary Reference

在下列情況讀這份參考：

- 想控制 link hover popup 的摘要
- 想控制 cards 的摘要文字
- 想控制搜尋引擎、分享預覽或 meta description 用的摘要
- 想判斷第一段 intro paragraph 要不要兼任 summary，還是改用獨立 summary element

這份筆記依據 JetBrains 官方文件整理：

- `Summary elements`
- `Semantic markup reference` 中的 `link-summary`、`card-summary`、`web-summary`

## 預設摘要行為

- Writerside 預設會把 topic 的第一段 paragraph 當成摘要來源。
- 這個摘要會被拿去做：
  - link popup summary
  - card popup / card summary
  - web description / meta description

所以一般情況下，把第一段寫好就很重要。

## 什麼時候需要 summary elements

- 第一段同時也是正文的一部分，但你想讓 preview 更短、更聚焦
- 你不想讓摘要文字直接出現在正文內容
- 同一篇文章需要：
  - 比較適合 hover popup 的摘要
  - 比較適合卡片的摘要
  - 比較適合搜尋結果的摘要

## `<link-summary>`

- 控制滑鼠 hover 在連結上時的 popup 摘要。
- 內容不會出現在 topic 正文裡。
- popup 只顯示純文字，因此不要期待裡面保留格式。

範例：

```xml
<link-summary>Use link summaries to provide context for links.</link-summary>
```

- 也可以用 `rel` 指向既有 paragraph 的 `id`：

```xml
<link-summary rel="intro"/>
<p id="intro">Use this paragraph as a link summary.</p>
```

- 如果某個 `<a>` 自己已經有 `summary="..."`，那個連結的 `summary` 會覆蓋 topic 的 link summary。

## `<card-summary>`

- 控制 cards 顯示的摘要，例如 starting pages 或 `seealso style="cards"`。
- 內容也不會出現在正文裡。

範例：

```xml
<card-summary>Use card summaries to provide context for cards.</card-summary>
```

- 也可用 `rel` 指向既有 paragraph。
- 若 `<a>` 上直接寫 `summary="..."`，該連結的 card summary 也會被覆蓋。

## `<web-summary>`

- 控制 HTML 頁面的 `meta description`。
- 搜尋引擎、社群平台或通訊軟體分享預覽可能會用這段文字。
- 但官方也提醒：搜尋引擎不保證一定採用這段，仍可能選別的內容。

範例：

```xml
<web-summary>This text is used only in the meta web description.</web-summary>
```

- 同樣可以用 `rel` 指向既有 paragraph：

```xml
<web-summary rel="intro"/>
<p id="intro">Use this paragraph as a web summary.</p>
```

## `rel` 的使用原則

- 如果正文第一段本來就寫得很好，優先考慮直接讓它兼任 summary。
- 如果你只是想重用已存在的某段 intro、又不想複製文字，使用 `rel` 最乾淨。
- 如果你想讓 preview 文案和正文完全分離，再寫獨立的 `link-summary` / `card-summary` / `web-summary` 內容。

## 和 `<tldr>` 的差異

- `<tldr>` 是正文內、標題下方的 quick facts。
- summary elements 不會直接出現在正文裡。
- `<tldr>` 是給已經打開文章的人快速上手。
- summary elements 是給還沒點開文章的人做判斷或預覽。

## 在這個 repo 的採用建議

- 一般技術筆記先把第一段 intro paragraph 寫好，通常就夠用。
- 只有在第一段不適合當 preview，或你真的要優化卡片/搜尋摘要時，再加 summary elements。
- 若使用 `seealso style="cards"` 或未來有 starting page cards，優先考慮 `card-summary`。
- 若特別在意搜尋與分享預覽，再補 `web-summary`。
- 如果需求已經變成 section landing page 或首頁卡片編排，改讀 `starting-pages-reference.md`。
