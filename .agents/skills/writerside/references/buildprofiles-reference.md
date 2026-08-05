# Writerside buildprofiles.xml Reference

在下列情況讀這份參考：

- 想調整 Writerside 網站輸出的 header / footer
- 想加入或調整自訂 HTML、CSS、JavaScript、留言系統、贊助按鈕或第三方 widget
- 想設定 Algolia 搜尋、shortcut switcher、OG metadata、sitemap、Search Console 或 SEO URL 前綴
- 想理解 `buildprofiles.xml` 的 global 設定和 instance-specific 設定差別
- 想判斷 `cfg/`、`writerside.cfg`、`buildprofiles.xml` 三者怎麼配合

這份筆記依據 JetBrains 官方文件整理：

- `buildprofiles.xml`

若你需要專門處理 `llms.txt`、`<llms-txt>`、single-file / per-topic 輸出或 LLM agent 匯出用途，改讀 `llms-reference.md`。

## 內容索引

- [`buildprofiles.xml` 的用途與位置](#buildprofilesxml-是做什麼的)
- [結構與目前設定](#結構怎麼看)
- [常見設定分類](#常見設定分類)
- [第三方 script / widget](#第三方-script--widget-的放置與定位)
- [問題忽略與其他設定](#ignore-problems)
- [採用建議](#在這個-repo-的採用建議)

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
  - `generate-sitemap-url-prefix`
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

#### 第三方 script / widget 的放置與定位

加入留言、分析、贊助按鈕或浮動 widget 時，先依用途選注入點：

- 需要出現在 `<head>` 的 metadata、預載或官方明確要求的 script 才用 `include-in-head`。
- 需要 DOM 已建立後再初始化的互動 widget，優先放在 `include-after-body` 指向的 HTML 檔。
- `analytics-head-script-file` 與 `analytics-body-html-file` 留給 analytics；不要把一般 UI widget 混進去。
- 不要把全站第三方 script 直接貼進 topic Markdown。這會讓內容與站台行為耦合，也可能被 Writerside 過濾或只影響單頁。

`include-after-body` 只決定 script 的注入階段，不會自動讓產生的元素浮動。若第三方 API 在 script 所在位置插入一般 flow element，元件仍可能被排到 header 前方。要做浮動按鈕時：

1. 優先選供應商提供的 overlay / floating 版本。
2. 檢查實際輸出的 DOM 與 computed CSS，不要只看 script 名稱。
3. 若要換邊，按鈕 wrapper、桌面 popup、行動版 wrapper 與行動版 popup 要一起移動。
4. 第三方 CSS 可能在初始化後才載入；必要時用範圍精確的 `!important` override，並避免覆寫整站通用 selector。
5. Writerside 是 SPA；全站 widget 通常只初始化一次。切換 topic 時確認沒有重複建立按鈕或 popup。

Ko-fi 的舊 `Widget_2.js` 搭配 `kofiwidget2.draw()` 會在目前文件位置畫出按鈕，放進 Writerside 的全站注入檔時可能佔用正常排版。需要浮動贊助面板時，改用 `overlay-widget.js`：

```html
<!-- Ko-fi floating widget -->
<style>
  .floatingchat-container-wrap,
  .floatingchat-container-wrap-mobi,
  .floating-chat-kofi-popup-iframe,
  .floating-chat-kofi-popup-iframe-mobi {
    right: 16px !important;
    left: auto !important;
  }
</style>
<script src="https://storage.ko-fi.com/cdn/scripts/overlay-widget.js"></script>
<script>
  kofiWidgetOverlay.draw('<ko-fi-handle>', {
    'type': 'floating-chat',
    'floating-chat.donateButton.text': 'Support me',
    'floating-chat.donateButton.background-color': '#00b9fe',
    'floating-chat.donateButton.text-color': '#fff'
  });
</script>
```

Ko-fi overlay 的供應商 CSS 目前預設靠左；上例同時把 desktop / mobile 的按鈕與 popup 改到右側。這些 class 屬於第三方實作細節，日後修改前要重新檢查官方 snippet、CDN 回應與實際 DOM，不要假設 selector 永遠不變。

第三方 widget 的驗證至少包含：

- 確認 script 使用 HTTPS、CDN 可回應，公開 handle 可以提交，但不要把 token、secret 或私密 ID 寫進 repo。
- 執行 `git diff --check` 與 `npm run pre-deploy`；這只能驗證 repo 結構，不能執行瀏覽器 JavaScript。
- 部署後以桌面與行動版 viewport 檢查按鈕位置、popup 展開方向、header/footer 遮擋、console error 與 SPA 換頁後是否重複初始化。
- 若只有線上環境能完整載入 widget，先明確說明本地檢查的限制，再用 CI 與部署後瀏覽器驗收完成閉環。

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
- `generate-sitemap-url-prefix`
- `images-prefix-override`

如果某些設定只應影響特定 instance，不要放在 root `<variables>`。

### Sitemap 與 SEO URL

這個 repo 的 canonical 公開 URL 策略是根目錄短網址：

- `https://jakeuj.com/<topic-web-file-name>.html`
- 不使用 `/writerside/master/` 作為公開文章 URL 前綴

目前相關設定是：

- root `<web-root>`：`https://jakeuj.com/`
- root `<generate-sitemap-url-prefix>`：`https://jakeuj.com/`
- `<build-profile instance="hi">` 內保留 `<sitemap priority="1" change-frequency="weekly" />`
- `<product-web-url>`：`https://jakeuj.com/`
- `<noindex-content>`：`false`

調整 sitemap / Search Console / SEO 時先驗證：

- `https://jakeuj.com/sitemap.xml` 應是 `200 application/xml`
- sitemap 的 `<loc>` 不應包含 `/writerside/master/`
- 抽測 sitemap 裡的頁面 URL 應回傳 200
- `robots.txt` 由 deploy workflow 複製到 Pages artifact 根目錄，內容應指向 `https://jakeuj.com/sitemap.xml`

### `sitemap.xml` 與 `sitemap-index.xml`

這個 repo 目前使用單一 sitemap：

- Search Console 提交 `https://jakeuj.com/sitemap.xml`
- `https://jakeuj.com/sitemap-index.xml` 目前 404 是預期狀態，不是錯誤
- 不要為了 Search Console 另外建立空的 `sitemap-index.xml`

只有在符合下列任一條件時才考慮 sitemap index：

- 單一 sitemap 超過 50,000 URLs
- 單一 sitemap 未壓縮超過 50MB
- 明確要拆成多個 sitemap，並用 index 統一提交

如果未來要改用 sitemap index，`robots.txt` 和 Search Console 都應改指向 index；否則維持指向 `sitemap.xml`。

不要為了修 sitemap 先開 `<generate-canonicals>`；若使用不當，可能把多頁 canonical 指到同一個 URL。需要 canonical 時先用建置產物抽測 `og:url`、Schema `url` 與 `<link rel="canonical">`。

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
- 只有在使用者明確提到站台 header、footer、自訂 HTML/CSS/JavaScript、第三方 widget、搜尋、社群連結、OG、sitemap、robots.txt、Search Console、SEO URL 或 checker 忽略規則時，才進到這層。
- 修改前先判斷設定是全域還是只屬於 `instance="hi"`。
- 若變更牽涉 `algolia-*`、analytics 或 HTML injection，優先視為高影響設定，做法要比一般 topic 編修更保守。
