# Writerside Structural Elements

在下列情況讀這份參考：

- 不確定該用普通 Markdown 標題，還是改成 Writerside `chapter`
- 想控制右側 topic navigation，而不是只依靠預設章節顯示
- 想做可折疊章節、可折疊 procedure、可折疊 definition list 或 code block
- 想判斷 `list`、`deflist`、`table`、`seealso` 各自適合什麼內容
- 文章開始變長，想把內容切成較清楚的章節與子章節

這份筆記依據 JetBrains 官方文件整理：

- `Structural elements`
- `Collapsible elements`
- `Semantic markup reference` 中的 `chapter`、`show-structure`、`deflist`、`list`、`table`、`seealso`

若你需要的是 list 細節、巢狀清單、definition list type 或 FAQ 寫法，改讀 `lists-reference.md`。
若你需要的是 Markdown table 限制、XML table、merge cells 或欄寬控制，改讀 `tables-reference.md`。
若你需要的是首頁或章節入口 landing page、spotlight cards 或 `<section-starting-page>`，改讀 `starting-pages-reference.md`。
若你需要的是 topic / chapter labels、`labels.list` 或 primary/secondary label，改讀 `labels-reference.md`。
若你需要的是左側 TOC、`hi.tree`、`<toc-element>`、`start-page`、`toc-title` 或 hidden topic，改讀 `toc-reference.md`。

## 先決定需不需要結構元素

- 短篇、偏速記、單一路徑的筆記，通常只要 Markdown 標題就夠了。
- 長文、導覽需求明顯、章節內還有子章節或多段流程時，再考慮 structural elements。
- 在 Markdown topic 裡，`##` 會變成第一層 chapter，`###` 會變成 subchapter；不一定非得改成 XML `chapter`。
- 只有在需要顯式 `id`、條件化 `title`、巢狀 chapter、或搭配 XML 結構時，再改用 `<chapter>`。
- 如果你要做的是整個 section 的入口頁，而不是一般正文 topic，先停一下，因為那通常不是 `chapter` 問題，而是 `starting page` 類型。

## Chapters 與標題層級

- `# Title` 是 topic title，也就是整篇文章的 H1。
- `## Title` 是第一層 chapter。
- `### Title` 是 subchapter，以此類推。
- Markdown 標題已經能提供大多數章節語意；對這個 repo 的一般技術筆記來說，這通常是預設首選。
- `<chapter title="...">` 適合用在：
  - 需要顯式 `id`
  - 要在 chapter 內再包 chapter
  - 要用 `<title instance="...">` 依 instance 改標題
  - 要整段內容都待在 semantic markup 結構中
- 如果需求是幫 topic 或 chapter 補版本、方案、WIP 之類的視覺標記，那通常不是 chapter 階層問題，而是 label 問題。

範例：

```xml
<chapter title="Example chapter" id="example-chapter-id">
    <p>Some text.</p>
    <chapter title="Subchapter" id="subchapter">
        <p>Some more text.</p>
    </chapter>
</chapter>
```

## Topic navigation 與 `<show-structure>`

- Writerside 預設會在右側顯示第一層 chapters 的連結。
- 如果想把 procedures 也放進右側導覽，或限制深度，使用 `<show-structure>`。
- 在 XML topic 中，`<show-structure>` 要當 `<topic>` 的 direct child。
- 在 Markdown topic 中，把它放在第一個 H1 下面。

常見寫法：

```xml
<show-structure for="chapter,procedure" depth="2"/>
```

判斷準則：

- `<show-structure/>`
  - 顯示所有有 title 的結構元素
- `<show-structure for="none"/>`
  - 關閉右側 topic navigation
- `<show-structure for="chapter,procedure"/>`
  - 顯示 chapters 與 procedures
- `<show-structure depth="2"/>`
  - 只顯示到第二層
- `for` 還可以包含 `tab` 與 `def`
  - 適合右側也想導到 tabs 或 definition list 項目時

這個 repo 的建議：

- 一般短文先用預設行為。
- 只有在文章很長、procedure 很多、或右側導覽真的不夠用時才加 `<show-structure>`。

## Procedures 還是 lists

- 描述操作步驟時，用 `<procedure>`，不要用有序清單。
- Writerside 官方也提供從 list 轉 procedure 的動作，代表這是預期的寫法。
- 如果是列舉觀察點、功能點、畫面標號、選項集合，而不是「照順序執行的任務」，才留在 `list`。

## Lists、Definition Lists、Tables 的分工

### `<list>`

- 一般清單或列舉項目用 `list`。
- `type="decimal"` 可做數字清單。
- `columns="3"` 適合很多短項目。
- `sorted` 可讓內容自動排序。
- 但只要是 task steps，仍應回到 `<procedure>`。

### `<deflist>` / `<def>`

- 名詞與解釋、設定鍵與說明、術語對照時，優先用 `deflist`。
- 官方明確說明：term + description 這類內容，比兩欄 table 或一般 unordered list 更適合 definition list。
- `def` 必須有 `title`。
- 適合：
  - 參數解釋
  - 名詞表
  - option 與說明

### `<table>`

- 真正的矩陣資料、需要欄列對照時再用 table。
- `style` 可指定 `header-row`、`header-column`、`both`、`none`。
- `column-width="fixed"` 可固定欄寬。
- 不要用 table 硬裝 glossary 或 key/value 說明；那通常應該改成 `deflist`。
- 更完整的 table 寫法、Markdown table 限制與 merge cell 規則，改讀 `tables-reference.md`。

## Related links 與 `<seealso>`

- `<seealso>` 用來放與目前主題有關的內部 topic 或外部資源。
- link 會依 `c.list` 定義的 category 分類。
- 適合文章尾端的延伸閱讀，不適合拿來代替正文內容。
- 可用 `style` 控制渲染方式，也可自訂 section title。

範例：

```xml
<seealso>
    <category ref="external">
        <a href="https://example.com">外部參考</a>
    </category>
</seealso>
```

## Collapsible elements

- 可折疊元素包含：
  - chapters
  - procedures
  - code blocks
  - definition list items
- 用 `collapsible="true"` 讓內容預設收合。
- 用 `default-state="expanded"` 讓內容預設展開，但仍可手動收合。
- 重要資訊不要折疊，因為讀者在網頁上用 `Ctrl+F` 找不到收合區塊裡的內容。

Markdown 章節範例：

```markdown
## Supplementary info {collapsible="true"}
```

code block 範例：

````markdown
```kotlin
class Person(val name: String)
```
{collapsible="true" collapsed-title="Person.kt"}
````

使用準則：

- 補充資訊、延伸說明、長程式碼範例才折疊。
- 主要結論、必要前提、關鍵風險不要折疊。

## 在這個 repo 的採用建議

- `Starter.md` 已示範 Markdown 標題的 `collapsible="true"` 屬性。
- `Chapters.md` 已示範 procedure 與 collapsible chapter 的基本概念。
- 多數技術筆記先用 Markdown 標題就好，不要因為 Writerside 支援 `chapter` 就全面改成 XML。
- 當文章很長、右側導覽不夠、或你需要定義更明確的結構語意時，再導入這份 reference 裡的 structural elements。
- 如果你要調整的是左側網站目錄結構，而不是文章內章節，改去看 `toc-reference.md`，不要把 TOC 階層問題誤判成 chapter 問題。
