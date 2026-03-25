# Writerside Tables Reference

在下列情況讀這份參考：

- 不確定該用 Markdown table、XML `table`、還是改成 `deflist`
- 想調整 header row / header column
- 想控制欄寬、border、cell padding / spacing
- 想合併儲存格，或把 Markdown table 轉成 XML table
- 想判斷表格是不是太複雜，應該拆成其他結構

這份筆記依據 JetBrains 官方文件整理：

- `Tables`
- `Semantic markup reference` 中的 `table`、`tr`、`td`

## 先判斷該不該用表格

- 真正需要 rows / columns 對照時才用 table。
- 適合：
  - 版本功能比較
  - 角色責任對照
  - 固定欄位的資料矩陣
- 不適合：
  - 純步驟流程
  - glossary / key-value 解釋
  - FAQ / troubleshooting

分工原則：

- 流程：`procedure`
- 名詞與說明：`deflist`
- 真正欄列對照：`table`

## Markdown table 還是 XML `table`

- 簡單表格先用 Markdown table。
- 只要遇到 Markdown table 做不到的需求，就改成 XML `table`。

Markdown table 適合：

- 結構簡單
- 固定 header row
- 沒有合併儲存格
- 不需要換行複雜內容

XML `table` 適合：

- 想控制 header row / column
- 想指定欄寬
- 想合併儲存格
- cell 內要放比較複雜的內容

## Markdown table 的限制

官方頁面明確提到 Markdown table 有這些限制：

- 一定要有 header row
- cell 內不能換行
- 不能跨列或跨欄 merge cells

所以只要你需要：

- `style="header-column"` 或 `style="both"`
- `colspan` / `rowspan`
- 固定欄寬
- 複雜 cell 內容

就直接改成 XML `table`。

## Markdown table 基本寫法

```markdown
| Foo | Bar | Baz |
|-----|-----|-----|
| One | Two | Three |
| Higher | Faster | Stronger |
```

在 Writerside 裡，也可以用 `Alt+Insert` 產生 Markdown table。

## XML `table` 基本寫法

```xml
<table>
    <tr>
        <td>Column A</td>
        <td>Column B</td>
    </tr>
    <tr>
        <td>Value 1</td>
        <td>Value 2</td>
    </tr>
</table>
```

## Header rows / columns

- `style="header-row"`：預設值，第一列是 header
- `style="header-column"`：第一欄是 header
- `style="both"`：第一列與第一欄都當 header
- `style="none"`：沒有 header 強調

判斷準則：

- 一般比較表：`header-row`
- 左欄是名稱、右欄是屬性值：`header-column`
- 矩陣比較：`both`
- 純資料格、不想強調標頭：`none`

## 欄寬控制

- 預設下 Writerside 會依內容自動調整欄寬。
- 如果要指定某欄寬度，在第一列對應的 `<td>` 上加 `width="300"` 這類像素值。
- 如果要整張表不要自動調整，改用：

```xml
<table column-width="fixed">
```

- `column-width="fixed"` 會讓所有欄位等寬。
- 即使 fixed，也仍可在特定欄的第一列 cell 上指定 `width`；其他欄會平分剩餘空間。

## 合併儲存格

- XML `td` 支援：
  - `colspan`
  - `rowspan`
- 這是 Markdown table 做不到的，所以需要 merge cells 時直接轉 XML。

範例：

```xml
<table>
    <tr>
        <td colspan="2">Merged header</td>
    </tr>
    <tr>
        <td rowspan="2">Shared label</td>
        <td>Value A</td>
    </tr>
    <tr>
        <td>Value B</td>
    </tr>
</table>
```

## 其他常用 table 屬性

### `border`

- `border="true"`：顯示一般邊框
- `border="false"`：不顯示邊框

### `cellpadding`

- 控制 cell 邊框和內容之間的空間。

### `cellspacing`

- 控制各個 cell 之間的空間。

這些屬性只有在你真的需要微調版面時再用；大多數筆記維持預設就好。

## 表格轉換

- Markdown table 要轉 XML：
  - 把游標放在表格內
  - 按 `Alt+Enter`
  - 選 `Convert Markdown table to XML format`

- 這在需要 merge cells 或擴充 table 屬性時特別有用。
- `Starter.md` 也已經示範過這個操作概念。

## 寫表格的實務建議

- 不要把整篇文章塞滿 table；表格是用來做對照，不是拿來代替敘述。
- 如果只有兩三個 key-value 項目，先想想是不是 `deflist` 更自然。
- 如果 cell 內容越寫越長，先停一下，確認是不是應該拆成小章節、list 或 definition list。
- 表格前最好先有一句說明，讓讀者知道這張表在比較什麼。

## 在這個 repo 的採用建議

- 簡單比較表先用 Markdown table。
- 需要 merge cells、header-column、fixed width 時改 XML `table`。
- glossary、參數說明、FAQ 先想 `deflist`，不要慣性上 table。
- 真的要改 XML table 時，優先利用 Writerside 的 Convert Markdown table to XML，而不是手打整張表。
