# Writerside Code Reference

在下列情況讀這份參考：

- 不確定該用 inline code、fenced code block，還是 XML `code-block`
- 想設定 `prompt`、`noinject`、`ignore-vars`、`src`、`include-lines`、`include-symbol`
- 想放 XML / HTML 範例，怕被 Writerside 當成真正標記解析
- 想做程式碼比較、在 code block 中放連結，或啟用 soft wraps
- 想把重複出現的程式碼 sample 抽成檔案，不直接寫死在文章裡

這份筆記依據 JetBrains 官方文件整理：

- `Code`
- `Semantic markup reference` 中的 `code-block`、`compare`

若問題偏向 Mermaid 圖表語法、diagram 類型、Mermaid plugin 或 Writerside 目前不支援的 Mermaid 功能，改讀 `mermaid-reference.md`。
若問題偏向 PlantUML 語法、Graphviz、`@startuml`、`ignore-vars="false"` 或 `.puml` 檔引用，改讀 `plantuml-reference.md`。
若問題偏向 D2 語法、`.d2` 檔引用或建置前安裝 D2，改讀 `d2-reference.md`。
若問題偏向 `lang="tex"` 的 block math、`<math>` 或 Markdown `$...$` inline math，改讀 `math-reference.md`。
若問題偏向 `v.list`、`<var>`、`%var%` 插值、built-in variables、`smart-ignore-vars` 或 snippet 變數傳值，改讀 `variables-reference.md`。
若問題偏向 `code-snippets/` 在 help module 的位置、多 module 專案或 module-level snippets 目錄分工，改讀 `help-modules-reference.md`。

## 先判斷用哪種 code 表達

- 變數、方法名、指令、option、檔名片段這類短文字，用 inline code。
- 一整段 source code、設定檔、CLI interaction、REST API call，用 code block。
- 只是一般文章中的短語，避免濫用 code 格式，免得可讀性變差。

## Inline code

- Markdown 用單反引號：

```markdown
Call the `getAllItems()` method.
```

- XML 可用 `<code>`。
- 適合：
  - 函式名
  - option 名稱
  - CLI 子命令
  - 設定鍵

## Code blocks

- Markdown 用 fenced code block，開頭標明語言：

````markdown
```bash
npm run pre-deploy
```
````

- XML 用：

```xml
<code-block lang="bash">npm run pre-deploy</code-block>
```

- 有明確語言就盡量標上，因為 Writerside 會做 syntax highlighting。
- 官方輸出高亮使用 Prism；IDE 內的高亮與輔助功能則仰賴對應語言 plugin。

這個 repo 優先使用的語言標籤：

- Shell script 或 macOS/Linux CLI：`bash` 或 `shell`
- PowerShell：`powershell`
- Windows Command Prompt / batch file：`batch`，不要用 `cmd`
- C#：`C#`，不要用 `csharp`
- SQL Server / T-SQL：`sql`
- JSON、XML、YAML：分別用 `json`、`xml`、`yaml`
- 純輸出、log、錯誤訊息或不確定語言：`text`

## 什麼時候用 Markdown fenced code，什麼時候改 `<code-block>`

- 一般單篇筆記，先用 Markdown fenced code 就好。
- 需要更多屬性控制時，改用 `<code-block>`，或在 Markdown fenced block 後加屬性。
- 常見需要切到 `code-block` 的情境：
  - `prompt`
  - `noinject`
  - `ignore-vars`
  - `src`
  - `include-lines`
  - `include-symbol`
  - `disable-links`
  - collapsible code block

## 常用 `code-block` 屬性

### `prompt`

- 顯示不可複製的提示字元，例如 `$`、`>>>`。
- 適合 CLI、REPL、shell session。
- 提示字元不會跟著 copy。

範例：

```xml
<code-block lang="bash" prompt="$">npm run build</code-block>
```

### `noinject="true"`

- Writerside 預設會在編輯器裡注入對應語言，做高亮、檢查與輔助。
- 如果 sample 不完整、故意省略上下文、會一直報 syntax error，就加 `noinject="true"`。

### `ignore-vars="true"`

- 如果程式碼裡出現 `%foo%` 這類字串，避免被 Writerside 當成變數。
- 如果多行 code block 內有多個 `%...%`，例如 SQL `LIKE '%READTEXT%'`，優先用 XML `<code-block ignore-vars="true">` 搭配 `CDATA`，不要只在 fenced code 後加 `{ignore-vars="true"}`。
- 如果你要判斷的不是程式碼，而是整個 Writerside 變數系統、built-in variables 或 `<smart-ignore-vars>` 全域行為，改讀 `variables-reference.md`。

範例：

```xml
<code-block lang="sql" ignore-vars="true"><![CDATA[
SELECT *
FROM sys.sql_modules
WHERE definition LIKE '%READTEXT%';
]]></code-block>
```

### `src`

- 從外部檔案載入 code sample。
- 適合多篇文件重複用同一段 sample，或想把 sample 維持在單一來源。
- Mermaid 圖表也可以沿用同一套 `src` 機制；若重點是 Mermaid 本身，改讀 `mermaid-reference.md`。
- PlantUML 圖表也可以沿用同一套 `src` 機制；若重點是 PlantUML 本身，改讀 `plantuml-reference.md`。
- D2 圖表也可以沿用同一套 `src` 機制；若重點是 D2 本身，改讀 `d2-reference.md`。
- 數學公式若重點在 Tex/LaTeX 表示法或 inline math，而不是一般 code sample，改讀 `math-reference.md`。

### `include-lines`

- 只引入檔案中的指定行數。

### `include-symbol`

- 只引入某個 class、method、function 或其他 symbol。

## 從檔案引用程式碼

有兩種常見方式：

### 1. 專用 snippets 目錄

- 在 `writerside.cfg` 設定：

```xml
<snippets src="codeSnippets"/>
```

- 再用：

```xml
<code-block lang="kotlin" src="newTest.kt"/>
```

### 2. 相對路徑

- 不一定要先設定 snippets 目錄，也可以直接用相對 topic 的路徑：

```xml
<code-block lang="kotlin" src="../code-samples/newTest.kt"/>
```

這個 repo 目前沒有既定的 snippets 目錄規範，所以：

- 單篇筆記、單次使用：先直接寫 fenced code
- 真正跨篇重複引用：再考慮設 snippets 目錄或用相對路徑 sample

## Markdown 也能加 code-block 屬性

- 在 Writerside Markdown 中，可以對 fenced code block 補屬性，例如：

````markdown
```kotlin
```
{ src="newTest.kt" include-symbol="testMultiply" }
````

- 這對維持 Markdown topic 可讀性很有幫助，不一定每次都要改成 XML。
- Mermaid 也能用同樣模式寫成 fenced code block 再補 `src`。
- PlantUML 也能用同樣模式寫成 fenced code block 再補 `src`。
- D2 也能用同樣模式寫成 fenced code block 再補 `src`。

## XML / HTML 範例

- 如果 code sample 內有 XML / HTML tag，優先用 `CDATA` 包起來，避免被當成真正標記。

範例：

```xml
<code-block lang="xml"><![CDATA[
<some-tag>text in tag</some-tag>
]]></code-block>
```

- 另一種方式是把 `<`、`>` escape 成 `&lt;`、`&gt;`。
- 對這個 repo 來說，只要是在示範 Writerside XML，本能上就先想到 `CDATA`。

## Code block 內的連結

- 在 code block 裡要做連結，用 `[[[text|URL]]]`。
- 如果你要原樣顯示這段語法，不讓 Writerside 把它變成 link，設 `disable-links="true"`。

## Compare code blocks

- 要對照 before / after、語言差異、重構前後，優先用 `<compare>`。
- 預設是左右並排，標題是 `Before` / `After`。
- 可以用 `type="top-bottom"` 改成上下排列。
- 可用 `first-title`、`second-title` 自訂標題。

範例：

```xml
<compare type="top-bottom" first-title="Before" second-title="After">
    <code-block lang="kotlin">if (true) { doThis() }</code-block>
    <code-block lang="kotlin">if (true) doThis()</code-block>
</compare>
```

## Collapsible code blocks

- code block 也可以折疊。
- 常用屬性：
  - `collapsible="true"`
  - `collapsed-title`
  - `collapsed-title-line-number`

- 適合很長的 sample、補充範例、不是主流程必讀的程式碼。
- 主要解法或讀者一定要看的核心指令，不要預設折疊。

## Soft wraps

- Writerside 預設不會對 code block 自動換行，長行會出現水平捲軸。
- 若要在輸出網站提供 soft wrap 開關，在 `buildprofiles.xml` 設：

```xml
<code-soft-wrap>true</code-soft-wrap>
```

- 這是站台層級設定，不是單篇 topic 層級設定。
- 如果使用者只是寫一篇筆記，通常不用主動動這層；只有在整站閱讀體驗被長 code block 影響時再考慮。

## Copy 行為

- Writerside 輸出頁的 code block 預設有 copy 按鈕。
- `prompt` 顯示的提示字元不會被複製，適合可執行命令。

## 在這個 repo 的採用建議

- 一般筆記預設先用 fenced code block。
- CLI 範例需要提示字元時，再補 `prompt`。
- 不完整 sample 或 Writerside XML 範例，優先想到 `noinject="true"` 或 `CDATA`。
- 若同一段 sample 在多篇文章重複出現，再考慮 `src`、`include-lines`、`include-symbol`。
- 要比較兩段程式碼時，優先用 `<compare>`，不要自己拼表格。
- 要描述流程、狀態流轉或 Git branching 時，可考慮 Mermaid，而不是硬用截圖或純文字縮排。
- 要描述 UML 關係、JSON/YAML 結構、Gantt 或 mind map 時，可考慮 PlantUML。
- 要描述較自由的宣告式節點關係圖，並且建置環境可控時，也可考慮 D2。
