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
- 在這個 repo，公開 topic 預設要明確補 `<web-summary>`，不要只依賴第一段自動推導。
- 放在 H1 下一個區塊、正文第一段之前，讓維護者一眼看出這篇有 SEO description。

範例：

```xml
<web-summary>This text is used only in the meta web description.</web-summary>
```

- 同樣可以用 `rel` 指向既有 paragraph：

```xml
<web-summary rel="intro"/>
<p id="intro">Use this paragraph as a web summary.</p>
```

## `<web-summary>` 寫法原則

- 用 1 句純文字說清楚「主題 + 讀者能得到的解法/判斷」。
- 優先寫給搜尋結果與分享預覽看，不要寫成正文前言。
- 避免空泛句，例如「本文記錄...」、「這篇介紹...」；直接說「在 X 情境下，用 Y 做 Z」。
- 技術關鍵詞可以保留英文，例如 `Azure App Service`、`Dockerfile`、`Swagger UI`。
- 避免 Markdown link、粗體、清單、code fence；它最後會進 HTML attribute / meta description。
- 如果文字含 XML 特殊字元，要 escape：
  - `<` → `&lt;`
  - `>` → `&gt;`
  - `&` → `&amp;`
- 若摘要需要提到 XML tag，寫成 `&lt;web-summary&gt;`、`&lt;example&gt;`。
- 以 50 到 160 個中文字元左右作為保守範圍；太短通常缺乏辨識度，太長容易在搜尋結果被截斷。

建議格式：

```markdown
# Azure App Service 部署 FastAPI 的 Startup Command 設定

<web-summary>在 Azure App Service 部署 FastAPI 時，設定 Startup Command 使用 gunicorn 搭配 uvicorn worker，並用 --chdir 指到正確 src 目錄。</web-summary>
```

## `rel` 的使用原則

- 如果正文第一段本來就寫得很好，仍優先在 SEO 任務中寫明確 `<web-summary>`；只有一般內部連結/卡片摘要才考慮完全依賴第一段。
- 如果你只是想重用已存在的某段 intro、又不想複製文字，使用 `rel` 最乾淨。
- 如果你想讓 preview 文案和正文完全分離，再寫獨立的 `link-summary` / `card-summary` / `web-summary` 內容。

## 和 `<tldr>` 的差異

- `<tldr>` 是正文內、標題下方的 quick facts。
- summary elements 不會直接出現在正文裡。
- `<tldr>` 是給已經打開文章的人快速上手。
- summary elements 是給還沒點開文章的人做判斷或預覽。

## 在這個 repo 的採用建議

- 一般技術筆記先把第一段 intro paragraph 寫好，但公開發佈的 topic 預設仍補 `<web-summary>`。
- 只要需求涉及 SEO、Search Console、CTR、OG/Twitter preview、Schema description 或社群分享預覽，就在 H1 下方明確加 `<web-summary>`；不要只依賴 Writerside 從第一段自動推導。
- 修改既有文章時，如果同時改 H1/title、Search Console 高曝光頁、sitemap/OG/Schema 或任何 SEO metadata，也要順手檢查並補上 `<web-summary>`。
- 目前 artifact 驗證過：`<web-summary>` 會產生 `meta name="description"`，但 Writerside 仍可能讓 `og:description`、`twitter:description` 與 Schema `description` 保持空字串。
- 這個 repo 的 deploy workflow 會把非空 `meta name="description"` 後處理同步到 OG / Twitter / Schema description；新增要公開發佈的 topic 時仍預設先補 `<web-summary>`。
- 只有在第一段不適合當 preview，或你真的要優化卡片/搜尋摘要時，再加 `link-summary` / `card-summary`。
- 若使用 `seealso style="cards"` 或未來有 starting page cards，優先考慮 `card-summary`。
- 如果需求已經變成 section landing page 或首頁卡片編排，改讀 `starting-pages-reference.md`。

## Search Console 匯出資料的優先順序

使用者提供 Search Console CSV 或要求「看線上 SEO」時，先找最有槓桿的頁面，不要一口氣改全站舊文：

- 優先處理 impressions 高、average position 約 1 到 15、CTR 偏低的頁面。
- 若頁面 title/H1 太泛，例如只有 `Docker`、`Swagger`、`Studio`，先改 H1 成可辨識的搜尋結果標題，但不要改檔名或 URL。
- 同一批頁面都要補 `<web-summary>`，並讓 summary 對齊新的 H1。
- 不把 Search Console 小樣本解讀成大規模內容重構依據；先做 title/summary/metadata 基礎修正，再觀察 2 週以上。
