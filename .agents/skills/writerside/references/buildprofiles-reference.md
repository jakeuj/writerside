# Writerside buildprofiles.xml Reference

在下列情況讀這份參考：

- 想調整 Writerside 網站輸出的 header / footer
- 想設定 Algolia 搜尋、shortcut switcher、OG metadata、sitemap
- 想理解 `buildprofiles.xml` 的 global 設定和 instance-specific 設定差別
- 想判斷 `cfg/`、`writerside.cfg`、`buildprofiles.xml` 三者怎麼配合

這份筆記依據 JetBrains 官方文件整理：

- `buildprofiles.xml`

若你需要專門處理 `llms.txt`、`<llms-txt>`、single-file / per-topic 輸出或 LLM agent 匯出用途，改讀 `llms-reference.md`。

## `buildprofiles.xml` 是做什麼的

- 用來設定文件建置流程與輸出網站外觀。
- 官方頁面特別點到它會影響：
  - header
  - footer
  - search settings
  - shortcut switcher
  - version / instance 相關輸出

對這個 repo 來說，它也是站台層級設定的主要入口，不是單篇 topic 的設定檔。

## 檔案位置

- 預設情況下，`buildprofiles.xml` 應放在 help module 底下的 `cfg/` 目錄。
- 官方也提到：如果在 `writerside.cfg` 用 `<build-config>` 指到別的位置，才會改變這個預設。
- `build-config` 本身屬於 `writerside.cfg` 設定；如果你需要看那一層的完整脈絡，改讀 `writerside-cfg-reference.md`。

在這個 repo：

- 檔案位置是 [cfg/buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml)
- [writerside.cfg](/Users/jakeuj/WritersideProjects/writerside/Writerside/writerside.cfg) 目前沒有另外指定 `<build-config>`
- 所以這個 repo 正在使用官方預設的 `cfg/` 位置

## 結構怎麼看

根元素是 `<buildprofiles>`。

常見分成兩層：

- 全域設定：
  - `<variables>`
  - `<shortcuts>`
  - `<footer>`
  - 其他 root-level 設定
- instance 專屬設定：
  - `<build-profile instance="...">`

簡單判斷：

- 所有 instance 都共用的東西，放在 root level
- 只針對某個 instance 的 sitemap、OG、noindex 或特殊變數，放在 `<build-profile instance="...">`

## 這個 repo 目前怎麼用

目前 [buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml) 已經在用這幾塊：

- root `<variables>`
  - `web-root`
  - `download-page`
  - `download-title`
  - `showDownloadButton`
  - `primary-color`
  - `header-logo`
  - `custom-favicons`
  - `algolia-index`
  - `algolia-id`
  - `algolia-api-key`
  - `analytics-head-script-file`
  - `include-after-body`
- `<shortcuts>`
  - `src`
  - `layout`
- `<footer>`
  - 多個 `social`
  - `copyright`
- `<build-profile instance="hi">`
  - `sitemap`
  - instance-specific `<variables>`
  - `noindex-content`
  - `product-web-url`
  - `og-twitter`
  - `og-image`
  - `webmaster`
  - `ignore-problems`

## 常見設定分類

### 1. 網站與品牌外觀

常見元素：

- `primary-color`
- `header-logo`
- `custom-favicons`
- `color-preset`
- `content-max-width`
- `custom-banner`

適合在你真的要調整整站視覺與品牌時修改。

### 2. Header / download button

常見元素：

- `download-page`
- `download-title`
- `showDownloadButton`

如果需求是修改 header 上方的 CTA 或下載按鈕，優先看這一層。

### 3. Search / Algolia

常見元素：

- `algolia-index`
- `algolia-id`
- `algolia-api-key`
- `algolia-show-logo`

如果使用者問搜尋不能用、索引沒更新或 Algolia 設定，這層最直接。

### 4. Analytics / custom injection

常見元素：

- `analytics-head-script-file`
- `analytics-body-html-file`
- `custom-css`
- `include-in-head`
- `include-before-body`
- `include-after-body`

這些都偏站台層級注入，不應該因為單篇文章需求就隨便動。

### 5. Footer / social links

常見元素：

- `footer`
- `social`
- `link`
- `copyright`
- `notice`
- `icp`

如果使用者問網站底部社群連結、聯絡方式或版權文字，優先看這裡。

### 6. Shortcuts

常見元素：

- `shortcuts`
- `src`
- `layout`

這和 [keymap.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/keymap.xml) 配合，讓 `<shortcut key="$..."/>` 能根據 layout 顯示不同快捷鍵。

### 7. Instance-specific 輸出

常見元素：

- `<build-profile instance="...">`
- `sitemap`
- `noindex-content`
- `product-web-url`
- `og-twitter`
- `og-image`
- `images-prefix-override`

如果某些設定只應影響特定 instance，不要放在 root `<variables>`。

### 8. LLM export

常見元素：

- `llms-txt`

這層是把文件輸出成給 LLM 使用的 Markdown 近似格式。  
如果要判斷 `single-file`、`_llms/` 目錄或 artifact 內會長什麼樣子，改讀 `llms-reference.md`。

## `ignore-problems`

- 官方 `buildprofiles.xml` 可承載很多輸出層級設定；這個 repo 也用它來放 `ignore-problems`。
- 目前 [buildprofiles.xml](/Users/jakeuj/WritersideProjects/writerside/Writerside/cfg/buildprofiles.xml) 已在 `instance="hi"` 下忽略：
  - `VIS011`
  - `SCT001`

這表示：

- 不要把 `ignore-problems` 當成修文的第一選項
- 只有在確認是可接受、且有意識地要忽略時才加
- 單篇文件錯誤應優先修內容，不是先擴大忽略清單

## `code-soft-wrap`

- 官方頁面也把 `code-soft-wrap` 放在 `buildprofiles.xml` 中。
- 這是整站 code block 閱讀體驗設定，不是單篇 topic 的屬性。
- 如果你只是處理某篇文章的 code block，不要先動這個。
- 更早前 skill 已在 `code-reference.md` 提過它；這裡要記得它屬於站台層級設定。

## 和其他參考檔的分工

- `buildprofiles.xml` 欄位與站台輸出設定：這份檔案
- help instance、instance ID、tree file 與 multiple outputs：`instances-reference.md`
- help module structure 與 `cfg/` 所在層級：`help-modules-reference.md`
- 專案 / help module / `cfg/` 位置：`projects-reference.md`
- `writerside.cfg` 與 `build-config` / module root 主設定：`writerside-cfg-reference.md`
- `llms.txt` 輸出與 `<llms-txt>`：`llms-reference.md`
- build / deploy / GitHub Actions / Algolia 發布流程：`build-deploy.md`
- 本地檢查和 CI 檢查差異：`validation-flow.md`

## 在這個 repo 的採用建議

- 這個 repo 已有明確的 `buildprofiles.xml`，不要把它當成空白模板重寫。
- 如果需求只是新增或修改文章，通常不需要動 `cfg/buildprofiles.xml`。
- 只有在使用者明確提到站台 header、footer、搜尋、社群連結、OG、sitemap 或 checker 忽略規則時，才進到這層。
- 修改前先判斷設定是全域還是只屬於 `instance="hi"`。
- 若變更牽涉 `algolia-*`、analytics 或 HTML injection，優先視為高影響設定，做法要比一般 topic 編修更保守。
