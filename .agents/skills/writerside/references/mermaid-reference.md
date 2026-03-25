# Writerside Mermaid Reference

在下列情況讀這份參考：

- 想在 Writerside topic 裡畫流程圖、sequence diagram、state diagram 或 git graph
- 想使用 ` ```mermaid ` 或 `<code-block lang="mermaid">`
- 想從 `.mermaid` 檔引用圖表，而不是把圖表內容直接寫進 topic
- 想確認 Writerside 目前支援和不支援哪些 Mermaid 功能

這份筆記依據 JetBrains 官方文件整理：

- `Mermaid diagrams`
- `Code`

## 先判斷該不該用 Mermaid

- 要表達流程、狀態轉換、互動順序、分支流向時，Mermaid 很適合。
- 如果只是放一小段指令、設定或資料範例，還是用一般 code block。
- 如果圖已經是現成 UI 截圖或高度視覺化示意圖，可能圖片更直接。

這個 repo 的預設判斷：

- 講邏輯流程、設定判斷路徑、Git flow 時，可以優先考慮 Mermaid。
- 不要為了「看起來很厲害」把簡單兩步驟也硬畫成圖。

## 基本寫法

- 最直接的方式是使用 language 為 `mermaid` 的 code block。
- Markdown 和 XML 都可以。

Markdown 範例：

````markdown
```mermaid
graph LR
    A[Do you write docs?] --> B[Use Writerside]
```
````

XML 範例：

```xml
<code-block lang="mermaid">
graph LR
    A[Do you write docs?] --> B[Use Writerside]
</code-block>
```

## 支援的常見圖表類型

官方頁面特別示範並點出這些很適合 Writerside：

- flowcharts
- sequence diagrams
- state diagrams
- Git graphs
- Gantt charts
- pie charts

這個 repo 比較常見、也較實用的情境通常是：

- flowchart：操作流程、判斷分支
- sequence diagram：系統互動順序
- state diagram：狀態流轉
- git graph：分支策略或協作流程

## 從檔案引用 Mermaid

- 如果 Mermaid 程式碼已經放在獨立檔案，可以用 `src` 引用，不必把內容整段貼進 topic。
- 這和一般 `code-block src="..."` 的概念相同。

範例：

```xml
<code-block lang="Mermaid" src="graph.mermaid"/>
```

Markdown 也可以：

````markdown
```Mermaid
```
{ src="graph.mermaid" }
````

- 也可以用相對路徑，例如 `../codeSnippets/graph.mermaid`。
- 如果只是單篇文章使用一次，通常直接內嵌 Mermaid 內容就夠了。
- 如果同一張圖要跨篇重複用，或圖表很長，才考慮抽成獨立 `.mermaid` 檔。

## IDE 輔助

- Writerside 內建支援 Mermaid 輸出。
- 如果想在編輯器裡拿到更完整的 completion、highlighting 和 validation，官方建議安裝並啟用 JetBrains 的 Mermaid plugin。
- 這是編輯體驗增強，不是網站輸出的必要條件。

## 目前不支援的 Mermaid 功能

官方頁面明確提到，目前 Writerside 的 Mermaid 實作不支援：

- Font Awesome icons
- 用 `%%{ }%%` directive 切換 diagram theme
- class diagrams 的 namespace groups
- class diagrams 的 cardinality options
- sequence diagrams 中的 creating actors / destroying actors

所以實務上：

- 不要先假設 Mermaid 官網所有語法都能在 Writerside 正常輸出。
- 如果圖表用了這些功能，優先簡化圖，或改用圖片。

## 寫作建議

- 圖表前先有一句話交代它要說明什麼，不要直接丟圖。
- 節點文字保持短而清楚，避免整句段落都塞進框裡。
- 若圖表只是正文的補充，避免畫得比正文還難讀。
- 太大的圖可以考慮拆成兩張，或改回條列與小節。

## 和其他機制的分工

- Mermaid vs 一般 code block
  - 要表達圖形關係：Mermaid
  - 要表達可複製的程式碼或指令：code block
- Mermaid vs 圖片
  - 需要可維護、可版本化的圖：Mermaid
  - 需要真實畫面、UI 細節或高度自訂視覺：圖片
- Mermaid vs `<compare>`
  - before / after 程式碼對照：`<compare>`
  - 流程或狀態轉換：Mermaid

## 在這個 repo 的採用建議

- 目前 repo 內已經有 [SettingUi.md](/Users/jakeuj/WritersideProjects/writerside/Writerside/topics/SettingUi.md) 和 [指定-dotnet-SDK-版本.md](/Users/jakeuj/WritersideProjects/writerside/Writerside/topics/指定-dotnet-SDK-版本.md) 使用 ` ```mermaid `。
- 代表這個專案本身已接受 Mermaid topic 寫法，不需要另外開創新慣例。
- 一般情況下，先用 Markdown fenced Mermaid block 就好。
- 只有在圖表很長、要跨篇共用或想抽離維護時，再改成 `src="graph.mermaid"`。
- 如果某張圖需要 Mermaid 不支援的進階語法，優先簡化，不要在單篇筆記裡硬拗 workaround。
