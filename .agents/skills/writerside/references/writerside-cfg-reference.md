# Writerside writerside.cfg Reference

在下列情況讀這份參考：

- 想理解 `writerside.cfg` 在 Writerside 專案中的角色
- 想調整 `topics/`、`images/`、`vars`、`categories`、`snippets` 或 build config 目錄
- 想理解 `<instance>`、`<settings>`、`smart-ignore-vars`、`disable-web-name-preprocessing`
- 看到舊檔名 `project.ihp`，不確定和 `writerside.cfg` 的關係

這份筆記依據 JetBrains 官方文件整理：

- `writerside.cfg`

若你需要深入理解 help instance 本身、tree file 結構、`<instance-profile>`、`status`、多 instance 輸出或跨 instance 重用，改讀 `instances-reference.md`。
若你需要深入理解 help module structure、module root、可選目錄或多 module 專案，改讀 `help-modules-reference.md`。

## `writerside.cfg` 是做什麼的

- `writerside.cfg` 是 Writerside 專案的主設定檔。
- 它放在 help module root。
- 主要負責定義：
  - help instances
  - 各種設定與內容檔所在位置

官方也提到，舊版檔名叫 `project.ihp`。

重點是：

- 如果專案裡還在用 `project.ihp`，不一定要改名，因為官方視為等價。
- 但在這個 repo 裡，我們用的是 `writerside.cfg`。

## 在這個 repo 的位置

- 檔案位置是 [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg)
- 它位在 [Writerside](/Users/jakeuj/WritersideProjects/writerside/Writerside) 這個 help module root

目前內容是：

```xml
<ihp version="2.0">
    <topics dir="topics" web-path="topics"/>
    <images dir="images" web-path="images"/>
    <categories src="c.list"/>
    <vars src="v.list"/>
    <instance src="hi.tree" web-path="writerside" version="master"/>
</ihp>
```

這表示這個 repo 目前採用的是偏精簡的 `writerside.cfg`。

## 根元素 `<ihp>`

- `<ihp>` 是根元素。
- 可定義整個 help module 的全域設定。
- `version` 屬性可以設定所有 help instances 的全域版本。

## 常見子元素怎麼分工

### `<topics>`

- 定義 topic 檔案所在目錄。
- 預設是 `topics/`。
- 也可以用 `web-path` 控制建置後的路徑。

這個 repo 目前是：

- `dir="topics"`
- `web-path="topics"`

### `<images>`

- 定義媒體檔案所在目錄。
- 預設是 `images/`。
- `web-path` 控制建置後圖片所在路徑。
- 還可用 `version` 指定 image set version。
- 如果部署到 GitHub Pages，官方特別提醒要確認 `web-path` 是否和實際發佈路徑一致。

這個 repo 目前是：

- `dir="images"`
- `web-path="images"`

判斷補充：

- 如果網站掛在 repo 子路徑下，`web-path` 很可能不能只照字面寫成 `images`
- 如果有 custom domain 或既定站台路徑，則要以實際部署 URL 結構為準
- 真要處理 GitHub Pages 圖片路徑問題，改讀 `build-deploy.md`

### `<categories>`

- 指向 `seealso` 分類用的 category 檔。
- 預設通常是 `c.list`。

這個 repo 目前是：

- `src="c.list"`

### `<vars>`

- 指向變數檔。
- 預設通常是 `v.list`。

這個 repo 目前是：

- `src="v.list"`

### `<instance>`

- 定義 help instance。
- 常見屬性：
  - `src`
  - `web-path`
  - `version`
  - `keymaps-mode`

這個 repo 目前只有一個 instance：

- `src="hi.tree"`
- `web-path="writerside"`
- `version="master"`

如果你要處理的是：

- 一個 repo 產出多套文件
- tree file 的 `id` / `name` / `start-page` / `status`
- `ref` / `in` / `<include>` / `<snippet>` 這類跨 instance 或重用策略

那已經超過 `writerside.cfg` 的入口設定範圍，應改讀 `instances-reference.md`。

## `<build-config>`

- 用來指定 build configuration 目錄。
- 像 `buildprofiles.xml`、`build-script.xml` 這類檔案就受它影響。
- 預設是 `cfg/`。

這個 repo 目前沒有另外設 `<build-config>`。

所以代表：

- [cfg/buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml) 使用的是官方預設位置。

如果要深入看 `buildprofiles.xml` 本身的欄位，改讀 `buildprofiles-reference.md`。

### `<snippets>`

- 指定 code snippets 目錄。
- 適合從檔案引用程式碼 sample。
- 這個 repo 目前沒有設定 `<snippets>`。

### `<api-specifications>`

- 指定 API specification 檔案目錄。
- 預設是 `specifications/`。
- 這個 repo 目前沒有設定。

### `<instance-groups>`

- 指向 instance groups 宣告檔，例如 `instance-groups.xml`。
- 這個 repo 目前沒有設定。

### `<module>`

- 用來設定 help module 本身，例如名稱。
- 這個 repo 目前沒有設定。

## `<settings>`

- `<settings>` 裡放的是 help module 額外設定。
- 官方頁面列出常見子元素：
  - `<caps>`
  - `<default-property>`
  - `<disable-web-name-preprocessing>`
  - `<smart-ignore-vars>`
  - `<wrs-supernova>`

這個 repo 目前沒有 `<settings>`，代表仍採用預設行為。

## 幾個特別值得記的設定

### `<caps>`

- 控制標題大小寫呈現方式。
- 可對 `toc-element`、`topic`、`chapter` 指定 `sentence`、`title`、`aswritten`。

### `<default-property>`

- 可替某些 markup element 設預設屬性。
- 例如替所有 `img` 預設加 `border-effect="line"`。

### `<disable-web-name-preprocessing>`

- 控制 web file names 是否做預設正規化。
- 預設會把特殊字元轉成 `-`，並把英文字母轉小寫。
- 如果要盡量保留和 topic 檔名接近的 web file name，才考慮改這個。

這層會影響 URL，屬於高影響設定，不能輕易調。

### `<smart-ignore-vars>`

- 預設情況下，Writerside 會在 code blocks、URLs、外部圖片引用中解析 `%var%`。
- 如果設成 `<smart-ignore-vars>true</smart-ignore-vars>`，就改成預設不展開，除非元素上顯式 `ignore-vars="false"`。

這和前面 skill 裡整理過的 `ignore-vars` 規則直接相關。

### `<wrs-supernova>`

- 可指定 Docker help builder 版本。
- 官方提到 CI/CD 可用這個值決定 builder version。
- 這層比較偏進階建置，不是一般修文時會主動碰的設定。

## 和其他參考檔的分工

- `writerside.cfg` 主設定、help module 目錄、instances、settings：這份檔案
- help module structure、optional files、多 module / `origin`：`help-modules-reference.md`
- help instance 概念、tree file、multiple outputs、instance reuse：`instances-reference.md`
- 專案 / help module root / templates：`projects-reference.md`
- `buildprofiles.xml` 與 `cfg/` 內建置輸出設定：`buildprofiles-reference.md`
- 實際 build / deploy / CI 流程：`build-deploy.md`
- code sample / snippets / `src` 引用：`code-reference.md`

## 在這個 repo 的採用建議

- 這個 repo 的 `writerside.cfg` 目前很精簡，先不要為了「用滿功能」而擴充它。
- 如果需求只是新增或修改文章，通常不需要動 `writerside.cfg`。
- 只有在內容目錄、圖片目錄、instance 結構、變數檔、categories、build config 位置真的要變時，才進到這層。
- 對 URL、instance、`smart-ignore-vars`、`disable-web-name-preprocessing` 這類全域設定要特別保守，因為它們可能影響整站輸出，不只是單篇文章。
