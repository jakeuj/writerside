# Writerside TLDR Reference

在下列情況讀這份參考：

- 不確定該不該用 `<tldr>`
- 想在 topic 或 chapter 標題下方放 quick facts
- 想判斷 TLDR 應該放哪些資訊、寫多短、放幾條
- 想分辨 TLDR 和 intro paragraph、admonition、一般摘要段落的差異

這份筆記依據 JetBrains 官方文件整理：

- `TLDR blocks`
- `Semantic markup reference` 中的 `<tldr>`

## `<tldr>` 是做什麼的

- 用來放一組 quick facts，讓讀者不用先看完整篇正文，也能立刻開始操作或探索功能。
- 適合放在 topic 或 chapter 標題下方，做成「先給我最重要資訊」的入口。
- 它不是拿來重寫文章摘要，也不是拿來塞一整段說明。

## 適合放什麼內容

官方特別提到可放這類資訊：

- 主要快捷鍵
- 指令語法
- action 名稱
- 相關設定位置

延伸到這個 repo，常見適合項目是：

- 主要 CLI 指令
- 關鍵設定路徑
- 必要快捷鍵
- 最短驗證方式

## 結構規則

- `<tldr>` 內每一條 fact 都用 `<p>` 包住。
- 一個 topic 或 chapter 只能有一個 TLDR block。
- 如果你已經放過一個 TLDR，就不要在同一層再加第二個。

範例：

```xml
<tldr>
    <p>Shortcut: <shortcut>Ctrl+Space</shortcut></p>
    <p>Configure: <ui-path>Settings / Preferences | Editor | Code Completion</ui-path></p>
</tldr>
```

## 長度與數量

- 事實要短，但要可操作。
- 盡量不要超過 3 條。
- TLDR 越長，價值越低；因為它本來就是給不想先讀正文、想直接動手的人。

實務判斷：

- 1 到 3 條：通常最剛好
- 每條一句：最佳
- 如果你開始寫成段落、背景說明、限制分析，代表這些內容應該回正文或 admonition

## 什麼時候不要用 TLDR

- 文章本身很短，開頭兩三句就已經足夠說清楚
- 沒有明確的 quick facts，只剩背景脈絡或長篇說明
- 你其實是想放風險、限制、警告
- 你其實是想做「本文摘要」而不是「立即可用的事實」

## 和其他元素的差異

### TLDR vs intro paragraph

- intro paragraph 是交代情境、問題、背景。
- TLDR 是直接給讀者可以拿來用的 facts。

### TLDR vs admonition

- admonition 是提醒、建議、限制、風險。
- TLDR 是快速可操作資訊，不強調提醒語氣。

### TLDR vs summary elements

- TLDR 會出現在 topic 或 chapter 標題下方，屬於正文體驗的一部分。
- `link-summary`、`card-summary`、`web-summary` 不會出現在正文裡，主要給連結 hover、卡片與搜尋/分享預覽使用。
- TLDR 是給「現在就在看這篇的人」快速上手。
- summary elements 是給「還沒點進來的人」先判斷這篇值不值得看。

### TLDR vs list

- list 可以是一般列舉。
- TLDR 是有特定位置與用途的 quick facts block，不是普通 bullet list。

## 在這個 repo 的採用建議

- 如果文章是 how-to、設定教學、工具使用筆記，而且真的有「最少資訊就能開始動手」的需求，再用 TLDR。
- 一般短篇技術筆記先不要為了用而用。
- 如果讀者最需要先知道的是風險或限制，優先用 `note` / `warning`，不要拿 TLDR 硬裝警告。
- 若 TLDR 超過 3 條，先刪到只剩最關鍵資訊，其餘移回正文。
