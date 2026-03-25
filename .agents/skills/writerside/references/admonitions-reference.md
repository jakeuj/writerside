# Writerside Admonitions Reference

在下列情況讀這份參考：

- 不確定該用 `tip`、`note`、還是 `warning`
- 想在 Markdown topic 裡用 blockquote 做提醒區塊
- 想判斷某段提醒是可選建議、重要限制，還是高風險警告
- 想修正文檔裡既有的 `>` blockquote，確認它在 Writerside 的實際渲染

這份筆記依據 JetBrains 官方文件整理：

- `Admonitions`
- `Semantic markup reference` 中的 `tip`、`note`、`warning`

## 三種 admonition 的分工

### `<tip>`

- 放可選資訊、實用建議、替代作法。
- 不是必讀，但能幫讀者更順利完成任務。

### `<note>`

- 放讀者應該知道的重要資訊，例如限制、已知問題、前置條件。
- 重要，但不一定有立即性的破壞風險。

### `<warning>`

- 放高風險或有害後果，例如資料遺失、系統破壞、金錢風險、設備損害。
- 只要讀者做錯會有明顯代價，就優先升級成 warning。

## Markdown blockquote 的 Writerside 行為

- 在 Markdown topic 裡，一般 blockquote 預設會被渲染成 `tip`。

範例：

```markdown
> 這段在 Writerside 會預設視為 tip。
```

- 如果你要讓 blockquote 呈現成 `note` 或 `warning`，可以在 blockquote 後補 `style` 屬性。

### Blockquote 轉成 note

```markdown
> 這是重要限制或已知問題。
{style="note"}
```

### Blockquote 轉成 warning

```markdown
> 這裡有資料遺失或破壞性風險。
{style="warning"}
```

## 什麼時候用 XML，什麼時候用 Markdown blockquote

- 單純短提醒、且你在 Markdown topic 裡工作時，可直接用 blockquote。
- 如果你想更明確表達結構、要放進 `<step>`、`<tab>` 等 XML 容器，或內容比較複雜，優先用 `<tip>`、`<note>`、`<warning>`。
- 若團隊未來可能大量維護同類內容，直接用 semantic markup 通常比 blockquote 更清楚。

## 提醒層級的實務判斷

- 可以不看也沒差，只是有幫助：`tip`
- 不看可能會踩限制、忽略重要前提：`note`
- 不看可能造成資料遺失或明顯傷害：`warning`

不要把所有提醒都升級成 `warning`，否則真正高風險訊息會失去辨識度。

## 在這個 repo 的採用建議

- 已有 XML 結構的文章，優先維持 `<tip>`、`<note>`、`<warning>` 寫法。
- 純 Markdown 筆記若只有一句短提醒，可以接受用 blockquote，但要有意識地補 `style`。
- 遇到資料刪除、磁碟格式化、覆寫設定、破壞性指令，一律優先考慮 `warning`。
- 既有舊文若只是普通引用或心得，不要因為看到 `>` 就自動當成 admonition；先判斷那段內容在 Writerside 的實際用途。
