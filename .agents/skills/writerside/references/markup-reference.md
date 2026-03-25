# Writerside Markup Reference

在下列情況讀這份參考：

- 不確定該維持純 Markdown，還是改成 Writerside semantic markup
- 想判斷 `<tabs>`、`<procedure>`、`<note>`、`<warning>`、`<img>`、`<video>`、`<tldr>`、`<compare>`、`<snippet>`、`<include>`、`<if>` 何時該用
- 要在 Markdown topic 內混用 XML，怕格式被 Markdown 或 checker 誤判
- 想補 anchor、`id`、快捷鍵 keymap、媒體尺寸或 reusable content

這份筆記依據 JetBrains Writerside 官方文件整理：

- `Markup`: Markdown 與 semantic markup 的搭配方式
- `Semantic markup reference`: XML 標記、屬性與用法

若問題偏向章節切分、右側導覽、可折疊元素或 definition list，改讀 `structural-elements.md`。
若問題偏向提醒區塊、Markdown blockquote admonition 或 `tip/note/warning` 的選擇，改讀 `admonitions-reference.md`。
若問題偏向 `<tldr>` 的 quick facts 設計、條目數量或和正文/提醒區塊的區別，改讀 `tldr-reference.md`。
若問題偏向 inline code、code block、CDATA、code sample 引用或 code compare，改讀 `code-reference.md`。
若問題偏向數學公式、`<math>`、Markdown `$...$` 或 `lang="tex"` block math，改讀 `math-reference.md`。
若問題偏向 `labels.list`、`<primary-label>`、`<secondary-label>` 或 topic/chapter header labels，改讀 `labels-reference.md`。
若問題偏向可下載附件、`<resource>`、resources directory 或 `writerside.cfg` 的 resources 設定，改讀 `downloadable-resources-reference.md`。
若問題偏向圖片路徑、thumbnail、GIF、dark theme image 或 inline/block image，改讀 `images-reference.md`。

## 先判斷用 Markdown 還是 semantic markup

- 小型、單篇、偏筆記型內容，先用 Markdown。
- 需要表達元素意義而不是外觀時，改用 semantic markup。
- 官方特別點名這幾類 semantic markup 比 Markdown 更適合：
  - `<control>`：按鈕、核取方塊、對話框名稱
  - `<procedure>`：有順序的操作步驟
  - `<tabs>`：切換式內容
  - `<if>`：條件輸出
- 這個 repo 大多是單篇技術筆記，所以原則是：
  - 一般段落、標題、清單、單純程式碼區塊：Markdown 優先
  - 切平台、切工具、切版本、做步驟卡、做摘要卡、做媒體控制、做 reusable content：再引入 XML

## 在 Markdown topic 內混用 XML

- XML 區塊要保持連續；Markdown 會把空白行當成段落邊界。
- 可以在 XML 元素內穿插 Markdown 段落，但要刻意控制空行。
- 不要用 tab 縮排 XML 內容；Markdown 可能把它當成 block quote 或 code block。
- 在 `<step>`、`<tab>`、`<li>` 裡如果有多段文字，或文字和圖片/程式碼混排，優先包成 `<p>`。
- 如果 IDE 裡不確定當前位置允許哪些標記，直接在編輯器輸入 `<` 看可用 tag 清單。

## 常用 block elements

### `<tabs>` / `<tab>`

- 用在平台差異、工具差異、語言版本差異。
- 這是 Markdown 自己做不到的互動元件，符合情境就直接用。
- `<tab>` 內可放 `<p>`、Markdown code fence、`<code-block>`、`<note>` 等內容。
- 若只是兩三個很短的比較，不一定要上 tabs；讀者若需要來回切換時才值得用。

範例：

```xml
<tabs>
    <tab title="Windows">
        <p>使用安裝程式完成設定。</p>
    </tab>
    <tab title="macOS">
        <p>改用對應的 shell 指令。</p>
    </tab>
</tabs>
```

### `<procedure>` / `<step>`

- 只要內容是在描述「怎麼完成某件事」，優先用 `<procedure>`，不要用單純有序清單。
- `title` 可省略，但有 `title` 的 procedure 才會產生 anchor，也比較容易出現在文內 TOC。
- `type="choices"` 可把步驟渲染成選項而不是編號步驟。
- `default-state="collapsed"` 或 `expanded` 可做可折疊流程。
- 如果只有一個 step，畫面會改成 bullet 而不是編號。

範例：

```xml
<procedure title="部署流程" id="deploy-flow">
    <step>
        <p>先更新設定檔。</p>
    </step>
    <step>
        <p>再執行部署命令。</p>
    </step>
</procedure>
```

### `<note>` / `<tip>` / `<warning>`

- `<note>`：前置條件、限制、一般提醒。
- `<tip>`：提高效率的小技巧、替代作法、建議。
- `<warning>`：資料遺失、破壞性操作、金錢或設備風險。
- 官方 reference 有 `<note>`、`<tip>`、`<warning>`，沒有 `<caution>`；不要再新增 `<caution>` 用法。
- Markdown blockquote 在 Writerside 會預設渲染成 `tip`；若要改成 `note` 或 `warning`，讀 `admonitions-reference.md`。

### `<tldr>`

- 用來放這篇文章最重要的快速事實。
- 會顯示在 topic 或 chapter 標題正下方。
- 只放短句，不要把它寫成摘要版正文。
- 更完整的條目數量、只能有一個 block、每條都用 `<p>` 包住，以及和 admonition 的差別，改讀 `tldr-reference.md`。

範例：

```xml
<tldr>
    <p><ui-path>File | New Project</ui-path></p>
    <p><shortcut key="$Copy"/></p>
</tldr>
```

### `<compare>`

- 用來並排比較兩段程式碼，比手寫表格或兩段相鄰 code fence 更清楚。
- 適合「before / after」、「Java / Kotlin」、「Windows / Linux 指令」這類對照。

### `<img>` / `<video>`

- 純截圖、沒有特殊需求時，可先用 Markdown 圖片。
- 需要 `width`、`height`、`border-effect`、縮圖、主題控制等屬性時，改用 `<img>`。
- 小於等於 16px 的圖片會被視為 inline icon；若要獨立成區塊，記得加 `type="block"`。
- `<video>` 適合示範流程；本地影片要放在 `Writerside/images/`，並準備同名預覽圖。
- `border-effect="line"` 或 `border-effect="rounded"` 很適合 UI 截圖避免貼到背景。
- 實際圖片路徑、thumbnail、GIF、dark theme 規則改讀 `images-reference.md`。

## 常用 inline elements

### `<control>`

- 用在按鈕、對話框、欄位名稱、GUI 標籤。
- 比單純粗體更有語意，也更符合官方建議。

### `<ui-path>`

- 用在選單路徑或一連串 UI 點擊路徑。
- 遇到 `File | New | Project` 這種內容，優先用 `<ui-path>`，不要只當普通文字。

### `<path>`

- 用在檔名、目錄、實體路徑。
- 像 `Writerside/hi.tree`、`~/Library/Application Support/...` 這類內容都適合。

### `<shortcut>`

- 可直接硬寫：`<shortcut>Ctrl+C</shortcut>`
- 也可用 keymap identifier：`<shortcut key="$Copy"/>`
- 這個 repo 已有 `Writerside/keymap.xml`，如果快捷鍵對應得到既有 action，優先用 `key="$..."`
- 如果只是示意、或 keymap 裡沒有對應 action，再硬寫快捷鍵內容。

### `<resource>`

- 用來插入可下載檔案連結，例如 ZIP、CSV、TXT、範例設定檔。
- 它不是一般外部連結，也不是圖片或 code sample 引用。
- 需要先有 Writerside 的 resources directory 設定，才能正確打包與輸出下載網址。
- 更完整的 resources 目錄、`writerside.cfg` 設定與 repo 採用建議，改讀 `downloadable-resources-reference.md`。

### `<math>`

- 用來把數學公式放在段落內，而不是獨立成 block。
- 在 Markdown topic 也可以直接用 `$...$`。
- 更完整的 Tex block、inline math 與 repo 採用建議，改讀 `math-reference.md`。

## 重複內容與條件輸出

### `<snippet>` / `<include>`

- 只在內容要重複被多篇文章共用時使用。
- `element-id` 可指定重用某個元素，`use-filter` 可只取特定 filter 的內容。
- 如果只是單篇筆記裡偶爾重複一句話，不值得為它抽 snippet。

### `<if>`

- 用來依 instance、platform 或自訂 filter 決定輸出哪些內容。
- 這對多產品、多平台官方文件很有用，但這個 repo 以單站個人筆記為主，除非真的有條件輸出需求，不要主動引入。

## Anchor、ID 與 include target

- Markdown 標題若怕自動 slug 不穩定，直接補 `{#custom-id}`。
- XML 元素若要提供可重用片段或連結目標，補 `id="custom-id"`。
- `id` 除了可拿來連結，也能讓 `<include from="..." element-id="..."/>` 指向具體元素。
- 若文章標題含中文但夾英文關鍵詞，為了避開 `MRK003` 類型衝突，主動補顯式 anchor 比較穩。

## 程式碼相關屬性

- `lang="bash"`、`lang="c#"` 這類語言標記照實填。
- `prompt="$"`：顯示命令提示字元，但不會跟著被複製。
- `noinject="true"`：範例程式碼不完整、會造成 IDE 語法報錯時使用。
- `ignore-vars="true"`：內容含 `%foo%` 這類字串，避免被 Writerside 誤認成變數。
- `src="..."`：直接從檔案帶入程式碼時使用；只有在真的需要同步外部檔案內容時才用。
- 更完整的 inline code、CDATA、`src`、`include-lines`、`include-symbol`、soft wrap 與 code compare 規則，改讀 `code-reference.md`。

## 在這個 repo 的實際採用建議

- `Windows-重灌-UUP-dump-Ventoy-安裝USB.md` 已示範 `<note>`、`<tip>`、`<warning>`、`<procedure>`、`<tabs>`。
- `Starter.md` 已示範 Markdown 與 semantic markup 混用、`<img>`、可折疊標題與 `<procedure>`。
- `shortcut.md` 與 `Rider.md` 已示範 `<shortcut>` 和 `keymap.xml` 的用法。
- 如果只是修單篇筆記，優先保持簡單；先讓文章清楚、穩定、能過 checker，再追求語義化。
