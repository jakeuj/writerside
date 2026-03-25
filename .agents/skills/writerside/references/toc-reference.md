# Writerside Table Of Contents Reference

在下列情況讀這份參考：

- 想理解 `hi.tree` 這類 tree file 怎麼控制左側 TOC
- 想調整 `start-page`、home page、topic order 或 hierarchy
- 想用 `toc-title`、empty group、`hidden="true"` 或外部連結型 TOC 項目
- 想分清楚左側網站 TOC 和右側 in-page TOC / `<show-structure>` 的差別

這份筆記依據 JetBrains 官方文件整理：

- `Table of contents`

若你需要的是右側 article 內導覽、`<show-structure>`、`chapter`、`procedure` 或文章內結構元素，改讀 `structural-elements.md`。  
若你需要的是首頁或 section landing page、`<section-starting-page>`、spotlight cards 或 overview entry page，改讀 `starting-pages-reference.md`。  
若你需要的是 help module 主設定、`writerside.cfg`、instances 或 `project.ihp`，改讀 `writerside-cfg-reference.md`。
若你需要的是多個 help instances、tree file `status`、`<include>`、`<snippet>`、`ref`/`in`、reusable TOC chunk 或 multi-output strategy，改讀 `instances-reference.md`。

## 先分清楚兩種 TOC

- 左側網站 TOC：
  - 代表某個 instance 的整體內容結構。
  - 由 tree file 控制，在這個 repo 就是 [hi.tree](/Users/jakeuj/WritersideProjects/writerside/Writerside/hi.tree)。
- 右側 in-page TOC：
  - 是單篇 topic 頁面內的章節導覽。
  - 預設顯示第一層 chapter。
  - 需要調整時通常用 `<show-structure>`。

實務判斷：

- 要調整「文章在網站左側放哪裡」時，改 `hi.tree`。
- 要調整「文章內章節怎麼出現在右側」時，改 `chapter` / `<show-structure>`。

## tree file 在這個 repo 的位置

- 目前 help instance 定義在 [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg)
- 這個 repo 的 instance 指向：

```xml
<instance src="hi.tree" web-path="writerside" version="master"/>
```

- 所以目前左側網站 TOC 是由 [hi.tree](/Users/jakeuj/WritersideProjects/writerside/Writerside/hi.tree) 控制。

## `instance-profile` 與 home page

- tree file 的根元素通常是 `<instance-profile>`。
- `start-page` 屬性定義這個 instance 的 home page，也就是使用者打開 help root URL 時最先看到的 topic。

這個 repo 目前是：

```xml
<instance-profile id="hi" name="Jakeuj's Notes" start-page="Default.md">
```

代表：

- instance id 是 `hi`
- 站台顯示名稱是 `Jakeuj's Notes`
- 首頁 topic 是 `Default.md`

如果只是想改首頁 topic，通常優先改 `start-page`，不是改 Markdown 文章內容本身。

## `toc-element` 是左側 TOC 的基本單位

- 每個 `<toc-element>` 可以：
  - 直接指向一篇 topic
  - 只當分組容器，不綁 topic
  - 指向外部 URL
- 可以彼此巢狀，形成 section hierarchy。

最常見的寫法：

```xml
<toc-element topic="getting-started.md"/>
```

## 直接指向 topic

- `topic="file.md"` 代表這個 TOC 項目對應到一篇 topic。
- Writerside 左側預設顯示的是 topic title，不是檔名。
- 如果 H1 太長，才考慮在 tree file 補 `toc-title`。

範例：

```xml
<toc-element topic="windows-11-native-nvme-enable.md" toc-title="啟用 Native NVMe"/>
```

採用原則：

- 沒必要時不要濫用 `toc-title`。
- 只有在側欄需要更短、更穩定，或要和 H1 明確區分時才加。

## 空的 TOC 群組

- 如果你只想在左側 TOC 多一層分組，但不想建立額外 overview topic，可以用沒有 `topic` 的 `<toc-element>`。
- 這種 empty group 只負責分群，不會產生對應頁面或 URL。

範例：

```xml
<toc-element toc-title="Getting started">
    <toc-element topic="Installation.md"/>
    <toc-element topic="Configuration.md"/>
</toc-element>
```

注意：

- empty group 很適合純分類。
- 但如果這組內容需要一篇真正的 overview，通常更適合用一篇 topic 當父節點，或進一步評估 `starting page`。

## 用 topic 當 section 父節點

- 你也可以讓某篇 topic 自己當 section 入口，再把子 topics 掛在底下。
- 這樣讀者點父節點時，會先看到那篇 overview topic。

例如這個 repo 目前就有：

```xml
<toc-element topic="links.md">
    <toc-element topic="Side-Projects.md"/>
    <toc-element topic="贊助.md"/>
</toc-element>
```

判斷方式：

- 需要說明這個 section 在講什麼：用 topic 當父節點。
- 只想做純分類、不需要任何正文：用 empty group。

## 隱藏 topic 但仍納入 instance

- 想讓文章能被搜尋或直接連結到，但不出現在左側 TOC，可加 `hidden="true"`。

範例：

```xml
<toc-element topic="legal-info.md" hidden="true"/>
```

適用情境：

- 法務頁
- 參考頁
- 尚未準備好曝光的內容
- 不適合放在一般導覽層級，但仍要保留可搜尋性

## 外部連結型 TOC 項目

- `<toc-element>` 也可以不指向 topic，改用 `href` 指向外部 URL。
- 沒補 `toc-title` 時，Writerside 會直接拿 URL 當顯示名稱，所以通常應補上。

範例：

```xml
<toc-element href="https://www.jetbrains.com/writerside" toc-title="JetBrains Writerside"/>
```

這個 repo 目前也有相同型態：

```xml
<toc-element href="https://www.dotblogs.com.tw/jakeuj/" toc-title="原筆記(點部落)"/>
```

## topic order 與 hierarchy

- 左側 TOC 順序就是 tree file 中 `<toc-element>` 的順序。
- 巢狀關係則決定 section hierarchy。
- 所以如果你只是想調整顯示順序，不需要動文章內容，只要調整 `hi.tree`。

官方建議也可以在 IDE 的 Writerside 工具窗拖拉，但在這個 repo 內實作時：

- 可以直接編輯 [hi.tree](/Users/jakeuj/WritersideProjects/writerside/Writerside/hi.tree)
- 把新 topic 放在最接近主題的現有群組下
- 盡量靠近相似內容，不要只是加到檔尾

## 這個 repo 目前的 TOC 結構特徵

- root home page 是 `Default.md`
- 第一層大量混用兩種型態：
  - 有正文的 section parent，例如 `links.md`、`LLM.md`、`Python.md`
  - 純分組節點，例如 `Mac`、`AI`、`Games`
- 已經有實際使用：
  - `toc-title`
  - 巢狀 `<toc-element>`
  - 外部 `href`

因此後續修改建議：

- 先沿用既有群組，而不是任意重整整棵 tree
- 新增文章時優先掛到現有最接近的節點下
- 只有在真的缺少分類時，才新增新的 empty group 或 section parent

## 和其他參考檔的分工

- 左側網站 TOC、tree file、`start-page`、`toc-title`、`hidden`、`href`：這份檔案
- help instance、tree file status、cross-instance reuse、reusable TOC snippets：`instances-reference.md`
- help module、`writerside.cfg`、instance 宣告：`writerside-cfg-reference.md`
- 文章內章節、右側導覽、`chapter`、`show-structure`：`structural-elements.md`
- 首頁 / section landing page / XML starting page：`starting-pages-reference.md`
- `hi.tree` 掛載錯誤、topic 路徑不一致、TOC 點了失敗：`checker-errors.md`

## 在這個 repo 的採用建議

- 多數日常修改只是新增 topic 或調整歸類，通常只需要小改 `hi.tree`。
- 若 H1 很長，再考慮補 `toc-title`，不要一開始就替所有節點手動命名。
- 想做純分類時，用 empty group 就好；想做真正入口頁時，再評估用父 topic 或 starting page。
- 對 `start-page` 要保守，因為它會直接改掉整個 instance 首頁入口。
