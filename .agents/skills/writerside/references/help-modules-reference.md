# Writerside Help Modules Reference

在下列情況讀這份參考：

- 想理解什麼是 help module、module root，以及它和 project root 的關係
- 想確認 help module 應有哪些目錄與設定檔
- 想規劃多個 Writerside modules，而不是只增加新的 instance
- 想做跨 module 重用，使用 `origin` 參照另一個 module 的內容

這份筆記依據 JetBrains 官方文件整理：

- `Modules`

若你需要的是 project templates、新建專案或把文件加進既有開發專案，改讀 `projects-reference.md`。  
若你需要的是 `writerside.cfg` 欄位、`<topics>`、`<images>`、`<instance>` 或 `build-config`，改讀 `writerside-cfg-reference.md`。  
若你需要的是 help instances、tree file、`<instance-profile>`、多套輸出或跨 instance reuse，改讀 `instances-reference.md`。

## 先理解 help module 是什麼

- 每個 Writerside documentation project 至少會有一個 help module。
- help module 就是放 Writerside 設定檔與內容檔的那個目錄。
- `writerside.cfg` 的存在，會讓 Writerside 知道哪裡是這個 help module 的根目錄。

官方也提到：

- 如果整個專案就是純文件專案，可以直接把內容放在 project root。
- 但實務上通常仍建議用獨立目錄裝文件來源，尤其是和 source code 共用同一個 repo 時。

## 這個 repo 目前的 module 現況

- [Writerside](/Users/jakeuj/WritersideProjects/writerside/Writerside) 就是目前唯一的 help module root。
- [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 在這個目錄底下。
- 目前是單一 help module，不是 multi-module 專案。

也就是說，這個 repo 目前沒有：

- 第二個 module 目錄
- 跨 module `origin` 重用
- 每個 module 各自獨立的一套內容樹

## help module 的基本結構

官方列出的核心結構包括：

- `writerside.cfg`
- `topics/`
- `images/`
- `*.tree`

### `writerside.cfg`

- help module 的主設定檔。
- 定義基礎設定與 instances。
- 也是 Writerside 用來辨識 module root 的入口。

### `topics/`

- 放 `.md` 和 `.topic` 文章檔。
- 預設目錄是 `topics/`，也可在 `writerside.cfg` 改。

### `images/`

- 放圖片、GIF、影片等媒體資產。
- 預設目錄是 `images/`，也可在 `writerside.cfg` 改。

### `*.tree`

- tree file。
- 定義某個 instance 的 TOC、階層、instance 名稱與 ID。
- 每個 instance 都必須在 `writerside.cfg` 透過 `<instance>` 註冊。

官方還特別提醒：

- tree file 的檔名應和 instance ID 對上。
- 例如 `aa.tree` 通常對應 `id="aa"`。

這個 repo 目前就是：

- [hi.tree](/Users/jakeuj/WritersideProjects/writerside/Writerside/hi.tree)
- `id="hi"`

## 可選檔案與目錄

官方列出的 optional files / directories 包括：

- `v.list`
- `c.list`
- `redirection-rules.xml`
- `resources/`
- `code-snippets/`
- `cfg/`

### `v.list`

- 全域變數清單。
- 需在 `writerside.cfg` 用 `<vars>` 註冊。
- 這個 repo 目前有使用 `v.list`。

### `c.list`

- `seealso` 分類清單。
- 需在 `writerside.cfg` 用 `<categories>` 註冊。
- 這個 repo 目前有使用 `c.list`。

### `redirection-rules.xml`

- redirect 規則設定檔。
- 適合集中管理舊網址到新網址的對應。
- 這個 repo 目前沒有既定 `redirection-rules.xml` 配置。

### `resources/`

- 給讀者下載的檔案目錄。
- 常搭配 `<resource src="..."/>`。
- 這個 repo 目前還沒有宣告 `<resources .../>`，也沒有既定 resources 目錄慣例。

### `code-snippets/`

- 程式碼 sample 檔案目錄。
- 常搭配 `<snippets src="..."/>` 與 `code-block src="..."`。
- 這個 repo 目前沒有既定 snippets 目錄配置。

### `cfg/`

- build configuration 目錄。
- 可包含：
  - `buildprofiles.xml`
  - `build-script.xml`
  - `glossary.xml`

這個 repo 目前已有：

- [cfg/buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml)

而且 [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 沒有改 `<build-config>`，表示仍使用預設 `cfg/`。

## 一個 module 多個 instances，和多個 modules 的差別

- 一個 module 多個 instances：
  - 共用同一組 module-level 目錄與設定
  - 適合同一套文件基底產出多個版本或多個 audience
- 多個 modules：
  - 每個 module 都有自己的 `writerside.cfg`、instances、topics、images
  - 適合管理多套相對獨立的文件集合

判斷方式：

- 只是多套輸出、但仍共享大部分結構：先想 instance。
- 需要各自獨立的內容根目錄、媒體、設定與 build 邊界：再想多 module。

## 多 module 專案

官方明講，一個專案可以有多個 Writerside modules，而且它們可以放在不同目錄。

這代表：

- 不一定只能有一個 `Writerside/`
- 也可以是 `main-docs/`、`supplementary/` 這類並列結構

官方示例流程是：

1. 在 project root 建新目錄
2. 建立新的 `writerside.cfg`
3. 補上基本 XML boilerplate
4. 重啟專案後，讓 Writerside 識別新 module

## rename module

- module rename 本質上是目錄改名。
- 官方建議從 Project tool window 做 refactor rename。
- 這類變更會影響路徑感知與跨 module 參照，應保守處理。

## 跨 module 重用與 `origin`

- 即使 instances 分散在不同 modules，仍可共享內容。
- 這時會用 `origin` 指向來源 module。

官方示例：

```xml
<include origin="main-docs" from="lib.topic" element-id="important_note"/>
```

實務上可用於：

- 從另一個 module 重用 topic 片段
- 重用 snippets
- 重用 images 或其他可被 `origin` 參照的內容

但這也代表：

- module 名稱要穩定
- 跨 module 路徑與責任邊界要更清楚
- 變更 module 名稱時，風險會比單一 module 更高

## 這個 repo 目前的採用狀態

目前這個 repo 是：

- 單一 help module
- 單一 instance
- 已使用：
  - `writerside.cfg`
  - `topics/`
  - `images/`
  - `hi.tree`
  - `v.list`
  - `c.list`
  - `cfg/buildprofiles.xml`
- 尚未形成既定配置：
  - `resources/`
  - `code-snippets/`
  - `redirection-rules.xml`
  - 多 module `origin`

## 和其他參考檔的分工

- help module、module root、module structure、多 module、跨 module `origin`：這份檔案
- project / help module root / templates / existing project 導入：`projects-reference.md`
- `writerside.cfg` 欄位、目錄註冊、`<topics>`、`<images>`、`<instance>`：`writerside-cfg-reference.md`
- instances、tree file、instance ID、multi-output：`instances-reference.md`
- `cfg/buildprofiles.xml` 的站台輸出設定：`buildprofiles-reference.md`
- resources directory 與 `<resource>`：`downloadable-resources-reference.md`
- code snippets 目錄與 `code-block src="..."`：`code-reference.md`

## 在這個 repo 的採用建議

- 日常寫文章或掛 `hi.tree` 時，先不要把問題升級成 module 設計問題。
- 只有在真的需要第二套相對獨立的文件根目錄時，才考慮新增 module。
- 目前 repo 還沒有跨 module reuse 慣例，所以如果未來要引入 `origin`，先用最小範圍驗證，不要一次大規模重構。
