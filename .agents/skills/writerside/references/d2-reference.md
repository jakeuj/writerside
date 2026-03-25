# Writerside D2 Reference

在下列情況讀這份參考：

- 想在 Writerside topic 裡加入 D2 圖表
- 想使用 ` ```d2 ` 或 `<code-block lang="d2">`
- 想從 `.d2` 檔引用圖表，而不是把內容直接寫進 topic
- 想確認 D2 的前置需求，以及它和 Mermaid / PlantUML 的分工

這份筆記依據 JetBrains 官方文件整理：

- `D2 diagrams`
- `Code`

## 先判斷該不該用 D2

- D2 是宣告式 diagram language，適合用簡潔文字描述節點、關係與版面方向。
- 如果需求是一般流程圖或簡單分支，Mermaid 通常更常見。
- 如果需求偏 UML、JSON、Gantt 或 mind map，PlantUML 通常更對位。

這個 repo 的預設判斷：

- 只有在你明確想用 D2 語法，或它比 Mermaid / PlantUML 更貼近你要的圖表風格時，再選 D2。
- 不要為了嘗鮮，把原本已經能用 Mermaid 解決的圖硬換成 D2。

## 前置需求

- 官方頁面明確提醒：要先安裝 D2。
- 這表示不只作者本機，真正負責建置文件的環境也要具備 D2，圖表才有機會正常輸出。

實務上：

- 如果只是更新 skill 或寫草稿，可以先記住這個前提。
- 如果要真的在 repo 導入 D2 topic，最好先確認 build 環境能不能使用 D2。

## 基本寫法

- 最直接的方式是使用 language 為 `d2` 的 code block。
- Markdown 和 XML 都可以。

Markdown 範例：

````markdown
```d2
direction: right
question: Do you write docs?
yes: Use Writerside
no: You should
question -> yes: Yes
question -> no: No
```
````

XML 範例：

```xml
<code-block lang="d2">
direction: right
question: Do you write docs?
yes: Use Writerside
no: You should
question -> yes: Yes
question -> no: No
</code-block>
```

## 從檔案引用 D2

- 如果 D2 程式碼已經放在獨立檔案，可以用 `src` 引用。
- 這和其他 `code-block src="..."` 的概念相同。

範例：

```xml
<code-block lang="D2" src="graph.d2"/>
```

Markdown 也可以：

````markdown
```D2
```
{ src="graph.d2" }
````

- 也可以用相對路徑，例如 `../codeSnippets/graph.d2`。
- 單篇、單次使用時，直接內嵌通常就夠了。
- 要跨篇共用或圖表很長時，再抽成 `.d2` 檔。

## 和其他圖表機制的分工

- D2 vs Mermaid
  - 一般流程圖、sequence、state、git graph：Mermaid
  - 想用 D2 的宣告式語法與版面描述：D2
- D2 vs PlantUML
  - UML / JSON / Gantt / mind map：PlantUML
  - 一般關係圖與宣告式 diagram：D2
- D2 vs 圖片
  - 要可版本化、可文字維護的圖：D2
  - 要真實畫面或高度客製視覺：圖片

## 寫作建議

- 圖表前先說明它要表達什麼，不要只丟一塊 D2 code。
- 如果圖很長，優先抽成 `.d2` 檔，讓 topic 本身保持可讀。
- 若團隊或 repo 內其他文章都用 Mermaid，新增 D2 前先確認不是只是語法偏好不同而已。
- 只要 build 環境不明，導入 D2 前要先把「D2 已安裝」當成必要檢查項。

## 在這個 repo 的採用建議

- 目前 repo 內還沒有既定的 D2 topic 範例。
- 這表示可以導入，但最好先用最小可行範例驗證建置環境是否支援。
- 如果只是一般流程圖，優先考慮 repo 已經有實例的 Mermaid。
- 若未來真的採用 D2，建議先從單篇、短圖、fenced `d2` code block 開始，不要一開始就把多篇圖表全面改寫。
