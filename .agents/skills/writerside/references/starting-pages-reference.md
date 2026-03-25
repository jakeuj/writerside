# Writerside Starting Pages Reference

在下列情況讀這份參考：

- 想做文件首頁或某個 section 的 landing page
- 想用 `<section-starting-page>` 做 overview、learning path 或熱門主題入口
- 想整理 spotlight cards、primary/secondary groups、misc links
- 不確定 starting page 和一般 Markdown / XML topic 有什麼差別

這份筆記依據 JetBrains 官方文件整理：

- `Starting pages`

## 先判斷需不需要 starting page

- starting page 適合首頁，或一組相關 TOC 內容的入口頁。
- 它的目的不是取代一般文章，而是先給讀者 overview、熱門入口與閱讀路徑。
- 官方也特別提到，這類頁面對讀者導覽和 SEO 都有幫助。
- 如果你只是要寫一篇普通技術筆記，不要硬轉成 starting page。

這個 repo 的預設判斷：

- 一般 `Writerside/topics/*.md` 技術筆記，還是以 Markdown topic 為主。
- 只有在明確要做首頁或 section overview 時，才考慮 starting page。

## 格式限制

- starting page 只能用 XML topic。
- 不能在 Markdown topic 中使用 `<section-starting-page>`。
- 如果 topic 裡有 `<section-starting-page>`，Writerside 會把它視為 starting page topic。
- 所有寫在 `<section-starting-page>` 外面的其他內容，都會被忽略。

所以實務上：

- 不要把 starting page 當成「Markdown 文章裡插一小段 XML」。
- 要做 starting page，就直接建立專用的 XML topic。

## 什麼時候不要用

- 文件是要發布到 JetBrains Marketplace 時，不要依賴 starting pages，因為官方明講不支援。
- 如果你只需要在 TOC 裡多一層分類名稱，用 `toc-title` 或一般 topic 結構就好。
- 如果你需要的是正文章節、步驟、FAQ 或表格，也不是 starting page 的場景。
- 如果你要改的是首頁 topic 指向、tree file 階層、hidden topic 或外部 TOC 連結，先改讀 `toc-reference.md`。

## 基本結構

官方給的 starting page 結構大致是：

```xml
<topic>
    <section-starting-page>
        <title>Section starting page title</title>
        <description>Short overview text.</description>
        <spotlight>
            <card href="Topic1.topic" badge="start" summary="..."/>
            <card href="Topic2.topic" badge="search" summary="..."/>
        </spotlight>
        <primary>
            <title>Main group</title>
            <card href="Topic.topic" summary="..."/>
        </primary>
        <secondary>
            <title>Highlighted group</title>
            <card href="Topic.topic" summary="..."/>
        </secondary>
        <misc>
            <cards>
                <title>Custom cards</title>
                <card href="Topic.topic" summary="..."/>
            </cards>
            <links narrow="true">
                <group>
                    <title>Custom links</title>
                    <a href="Topic.topic" summary="..."/>
                </group>
            </links>
        </misc>
    </section-starting-page>
</topic>
```

## 各區塊怎麼分工

### `<title>` 與 `<description>`

- `title` 是入口頁主標題。
- `description` 是最上方的簡短說明，負責交代這個 section 在講什麼。
- 文字應該偏導覽與定位，不要寫成過長的正文段落。

### `<spotlight>`

- 放兩個最重要的 topics。
- 適合「從哪裡開始」、「最常被點的功能」、「新手先看這兩篇」這種入口。
- 如果你放了很多 card，就失去 spotlight 的作用。

### `<primary>` 與 `<secondary>`

- 放其他重要內容。
- `primary` 比 `secondary` 更核心。
- 可把內容理解成「主要路徑」和「次要但仍值得注意的路徑」。

### `<misc>`

- 放額外但仍相關的入口。
- 可以混用 `<cards>` 和 `<links>`。
- `<links>` 裡可再用 `<group>` 分群。

## Cards 與 links

- `<card>` 和 `<a>` 都可以加 `summary`。
- summary 應該短而可掃描，讓讀者在入口頁快速判斷值不值得點。
- 如果目標 topic 已經有 `card-summary` 或 link summary 規劃，也要一起考慮，避免文案互相打架。

若你想細分：

- topic 預設摘要、`card-summary`、`web-summary` 的分工，改讀 `summary-reference.md`。

## `narrow="true"`

- 官方指出，misc 裡的額外 groups 預設會是兩欄。
- 如果你想把 links groups 顯示成三個較窄的欄位，可加 `narrow="true"`。
- 只在每個 link label 都夠短時才用，避免欄位過窄難讀。

## Card 的 icon、image、badge

- `icon`：小圖示，適合輕量提示。
- `image`：卡片上半部的大圖，適合視覺導向入口。
- `badge`：使用 Writerside 內建 badge 名稱，例如 `start`、`search`。

選擇原則：

- 想低干擾地補充語意，用 `icon` 或 `badge`。
- 想做比較強的視覺導引，再考慮 `image`。
- 如果沒有明確幫助，就不要為了好看把每張卡片都塞圖。

## 在這個 repo 的採用建議

- 目前這個 repo 大多是一般技術筆記，不要把 starting page 當成預設格式。
- 若未來要重做首頁、某個大分類總覽頁，starting page 會比一般 Markdown topic 更合適。
- 真要導入時，先確認會不會影響現有 `Writerside/hi.tree` 的入口安排，再建立專用 XML topic。
- 入口頁要優先幫讀者找到下一步，不要把它寫成另一篇長文章。
- 如果只是要把某篇既有文章設成首頁，通常先調 `hi.tree` 的 `start-page`，不是直接引入 starting page。
