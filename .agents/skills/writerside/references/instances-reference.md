# Writerside Instances Reference

在下列情況讀這份參考：

- 想理解什麼是 help instance，以及什麼時候該拆成多個輸出
- 想看 tree file、`<instance-profile>`、instance ID、`name`、`start-page`、`status`
- 想做跨 instance 重用、`<include>`、`<snippet>`、`ref` / `in`、reusable TOC chunk
- 想理解 `wip`、redirect、`accepts-web-file-names` 或 tree file 層級條件過濾

這份筆記依據 JetBrains 官方文件整理：

- `Instances`

若你需要的是 help module 主設定、`writerside.cfg`、`<instance src="...">`、topics/images/vars 目錄配置，改讀 `writerside-cfg-reference.md`。  
若你需要的是 help module structure、多 module 專案、module root 或跨 module `origin` 重用，改讀 `help-modules-reference.md`。  
若你需要的是單純調整左側 TOC 階層、`toc-title`、hidden topic、外部 `href` 或首頁 topic，改讀 `toc-reference.md`。  
若你需要的是 project root / help module root / templates / existing project 導入，改讀 `projects-reference.md`。

## 先理解 instance 是什麼

- instance 是一組內容 topics，加上一份 tree file 定義出的階層結構。
- 一個 instance 會建成一套獨立的 help website、user guide 或其他輸出。
- 預設專案通常只有一個 instance。

只有在這些情境，才認真考慮多個 instances：

- 同一個 repo 要產出多套文件
- 同一份內容要面向不同產品、版本、方案或角色
- 需要不同 audience 或不同 output format

如果只是新增或修改單篇文章，在這個 repo 通常不需要動到 instance 層級。

## 這個 repo 目前的 instance 現況

目前 [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 只有一個 instance：

```xml
<instance src="hi.tree" web-path="writerside" version="master"/>
```

而 [hi.tree](/Users/jakeuj/WritersideProjects/writerside/Writerside/hi.tree) 的根元素是：

```xml
<instance-profile id="hi" name="Jakeuj's Notes" start-page="Default.md">
```

這代表目前 repo 是：

- 單一 instance
- tree file 是 `hi.tree`
- instance ID 是 `hi`
- header 顯示名稱是 `Jakeuj's Notes`
- 首頁 topic 是 `Default.md`
- `writerside.cfg` 上的 version 是 `master`

另外，這個 repo 的 [buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml) 也已經有：

```xml
<build-profile instance="hi">
```

所以 `hi` 這個 instance ID 目前已經和 tree file、build profile 互相對應。

## 什麼時候不要亂新增 instance

- 只是多一個分類，不需要新增 instance。
- 只是新增一篇 topic，不需要新增 instance。
- 只是想調整左側 TOC 階層，通常改 `hi.tree` 就夠。
- 只是某篇文章還沒寫完，通常先用 hidden topic、WIP 標記或一般草稿流程，不要急著切新 instance。

## tree file 是 instance 的核心

- 每個 instance 都對應一份 tree file。
- tree file 用來定義：
  - instance ID
  - 顯示名稱
  - 首頁 topic
  - TOC 階層
  - reusable TOC snippets
  - cross-instance references

官方也說，新增 instance 時 Writerside 會建立新的 `.tree` 檔並在 `writerside.cfg` 註冊。

## `<instance-profile>`

- tree file 的根元素。
- 常見屬性：
  - `id`
  - `name`
  - `start-page`
  - `status`
  - `is-library`

### `id`

- 每個 instance 都要有唯一 ID。
- 這個 ID 不只是 tree file 身分，也常會被其他地方引用。
- 改 ID 時要很保守，因為 publication scripts 或其他設定不一定會自動跟著更新。

在這個 repo，目前 ID 是 `hi`。

### `name`

- 會作為輸出文件的主標題。
- 這個 repo 目前是 `Jakeuj's Notes`。

### `start-page`

- 定義使用者打開 help root URL 時先看到哪篇 topic。
- 這個 repo 目前是 `Default.md`。
- 想改首頁入口時，通常先改這裡。

### `status`

- `release`
  - 預設狀態，正常輸出
- `deprecated`
  - 文件過時，頁面會顯示過期警告 banner
- `eap`
  - 文件仍在開發中，頁面會顯示可能變動的警告 banner

這個 repo 目前沒有設定 `status`，可視為一般 release 狀態。

### `is-library`

- 用來標示這份 tree file 是可重用 TOC snippets library，不是實際發布的 instance。
- 如果只是一般網站輸出，不需要加。

這個 repo 目前沒有使用 library tree file。

## `<toc-element>` 在 instance 文件裡的進階屬性

單純 TOC 階層、`toc-title`、`hidden`、`href` 的基本用途，改看 `toc-reference.md`。  
這裡只補 instance / reuse 相關的進階層面。

### `wip="true"`

- 會把 TOC 項目標成 work-in-progress。
- 讀者看到的 tooltip 會是 `Will be available soon`。
- 適合明確想讓讀者知道「即將提供」的節點。

### `accepts-web-file-names`

- 用來建立舊網址到新 TOC 節點的 redirect。
- 適合 topic 改名或 URL 更換後，保留舊連結可達性。

範例：

```xml
<toc-element topic="related.topic" accepts-web-file-names="some-topic.html"/>
```

### `target-for-accept-web-file-names`

- 把舊網址直接導向外部或其他 URL。
- 這個 TOC element 本身要 hidden，而且不應再綁 topic 或外部 href。

### `accepts-web-file-names-ref`

- 改用 `redirection-rules.xml` 裡的規則 ID，而不是直接寫檔名。

### `id`

- 給 TOC element 一個識別值。
- 常用在 `<include from="..." element-id="...">` 之類的重用場景。

### `instance`

- 可在 tree file 中加條件，控制某段內容只對特定 instances 生效。
- 可用 `!` 做排除。

### `ref` 與 `in`

- 建立對另一個 instance topic 的參照。
- 這種寫法通常出現在多 instance 專案，不是單一 instance 日常編輯會碰到的內容。

### `origin`

- 如果要從另一個 help module 重用內容，可指定來源 module。
- 但這已經不只是 instance 問題，也牽涉 module 邊界與 module 命名。
- 真正要規劃多 module 時，應一起看 `help-modules-reference.md`。

## `<include>` 與 `<snippet>`

### `<snippet>`

- 用來先定義一段可重用的 tree hierarchy。
- 適合把一組共同的 TOC 片段抽出來，在多個 instances 重複使用。

### `<include>`

- 把另一份 tree file 裡的片段引進來。
- 常見屬性：
  - `from`
  - `element-id`
  - `instance`
  - `origin`
  - `use-filter`

這類能力主要是為了 single sourcing 與多 instance 重用。

## `filter` 與 `use-filter`

- `filter` 可標記可重用片段或元素的適用條件。
- `use-filter` 可在 include 時只取指定條件的內容。

這對多 instance 專案很有用，但也代表複雜度會明顯上升。

對這個 repo 目前的建議：

- 因為現在只有一個 instance，先不要為了「未來可能會用到」而提早導入這套。

## rename instance 的風險

- 改 instance `name` 相對單純，主要影響顯示文字。
- 改 instance `id` 要非常小心。
- 官方明講 IDE 會協助更新 references 與 `.tree` 檔名，但 publication scripts 不一定會同步改。

在這個 repo，`id="hi"` 目前還會影響：

- [hi.tree](/Users/jakeuj/WritersideProjects/writerside/Writerside/hi.tree)
- [cfg/buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml) 裡的 `instance="hi"`

所以除非真的需要，不要主動改 ID。

## 和其他參考檔的分工

- help instance、tree file、instance ID、`status`、reusable TOC chunk、cross-instance reuse：這份檔案
- help module structure、多 module、跨 module `origin`：`help-modules-reference.md`
- `writerside.cfg` 主設定、`<instance src="...">`、module-level settings：`writerside-cfg-reference.md`
- 左側 TOC 階層、`toc-title`、hidden topic、外部 `href`、`start-page`：`toc-reference.md`
- project 結構、help module root、templates：`projects-reference.md`
- instance-specific build output、`<build-profile instance="...">`：`buildprofiles-reference.md`

## 在這個 repo 的採用建議

- 目前是單一 instance repo，預設不要把一般修文問題升級成多 instance 設計問題。
- 如果未來真的要拆多套輸出，先從命名清楚的 instance ID 和 tree file 開始，再談 snippets / include / filters。
- 對 `status`、instance ID、redirect、cross-instance references 這類設定要保守，因為它們會影響整套輸出與既有連結，而不是單篇文章而已。
