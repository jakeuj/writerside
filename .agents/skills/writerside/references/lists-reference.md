# Writerside Lists Reference

在下列情況讀這份參考：

- 不確定該用一般 list、procedure、還是 definition list
- 想寫巢狀清單、ordered list、marker-less list 或 multiple columns
- 想把 FAQ、troubleshooting、參數說明、CLI option 說明整理成 `deflist`
- 想決定 `deflist` 的 `type` 該用 `full`、`wide`、`medium`、`narrow` 還是 `compact`

這份筆記依據 JetBrains 官方文件整理：

- `Lists`
- `Structural elements`

## 先判斷用哪一種列表

- 一般特性列舉、畫面註解、支持項目清單，用 `list`。
- 一連串操作步驟，用 `procedure`，不要用 list。
- 名詞與解釋、FAQ、troubleshooting、參數/方法/CLI option 參考，用 `deflist`。

快速判斷：

- 有順序的動作：`procedure`
- 單純列舉重點：`list`
- 標題 + 說明成對內容：`deflist`

## 一般 Lists

- XML 用 `<list>` 搭配 `<li>`。
- Markdown 的 ordered list 用 `1.`、`2.` 這種數字加句點。
- Markdown 的 unordered list 可用 `-`、`*`、`+`。
- 巢狀清單靠縮排建立。
- 若要加列表屬性，在 Markdown 中放在清單後的空行之後，用 `{...}`。

## `list` 常用屬性

### `type`

- `type="decimal"`：數字清單，順序或總數重要時用。
- `type="alpha-lower"`：小寫字母，適合 ordered nested list。
- `type="none"`：不顯示 marker。

### `start`

- 控制 ordered list 的起始編號。
- 適合接續前面段落已經開始的編號情境。

### `columns`

- 很多短項目時，用 `columns="3"` 之類的多欄顯示，減少垂直高度。
- 適合產品名、短命令、短關鍵字清單。
- 不適合長句或每項都很重的說明。

## List 的寫作準則

官方頁面提到的實務建議很值得直接沿用：

- 在 list 前先寫一小段引言，不要讓清單毫無上下文。
- 一份 list 盡量維持 2 到 8 個項目。
- 每個 item 盡量只承載一個核心概念。
- 如果每個 item 都很長，考慮改成 `deflist` 或拆成章節。
- 不要整篇文章都只剩清單；list 是用來補結構，不是拿來取代完整敘述。

這個 repo 的建議：

- 筆記型文章很容易不小心全部變成 bullet list，寫完要回頭看有沒有足夠的情境說明。
- 如果 list 前後沒有任何交代，通常代表還需要補一段導言或結論。

## Definition Lists

- XML 用 `<deflist>` 搭配 `<def title="...">`。
- Markdown 寫法是：

```markdown
First Term
: This is the definition of the first term.
```

- 多個 definition item 連續往下寫即可。
- `deflist` 很適合：
  - FAQ
  - troubleshooting guide
  - commands / options / methods / API endpoints reference
  - 參數或 UI control 說明

## `deflist` 的 type 怎麼選

### `type="full"`

- 預設值。
- title 與 description 上下分行。
- 適合 FAQ、troubleshooting、長標題項目。

### `type="wide"`

- 左右並排，約 1:1。
- 適合 REST API endpoint 參考。

### `type="medium"`

- 左右並排，約 1:2。
- 適合 methods / functions reference。

### `type="narrow"`

- 左右並排，約 2:7。
- 適合 CLI 長選項，例如 `--output`。

### `type="compact"`

- 左右並排，約 1:8。
- 適合縮寫、單字母選項，例如 `-o`、`-v`。

## FAQ 與 Troubleshooting 的建議寫法

- FAQ 或 troubleshooting 項目通常優先用 `deflist type="full"`。
- 問題或症狀當 `def` title，解法或說明放在內容。
- 如果每個問題還有很多步驟，再在 definition 內容內嵌 `procedure` 或補小章節。

## Topic Navigation 與 Definition Lists

- 如果想把 definition list 項目顯示到右側 topic navigation，加入：

```xml
<show-structure for="def"/>
```

- 只有在 definition item 本身很多、而且讀者真的需要右側快速跳轉時才開。

## 與其他元素的分工

- `list` vs `procedure`
  - 只要是做事步驟，就選 `procedure`
- `list` vs `table`
  - 真正欄列對照資料才用 `table`
- `list` vs `deflist`
  - item 若已經是「名詞 + 說明」，應改成 `deflist`

如果你已經確定要用表格，改讀 `tables-reference.md`。

## 在這個 repo 的採用建議

- 一般技術筆記的短重點清單維持 Markdown list 就好。
- 安裝步驟、排錯步驟不要偷懶寫成 ordered list，能改成 `procedure` 就改。
- 遇到「名詞/參數/選項/FAQ」這類格式，優先想到 `deflist`，不要先塞表格。
- 如果清單超過 8 項，先停一下，確認是不是該拆章節、改多欄、或改 definition list。
