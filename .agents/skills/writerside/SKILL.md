---
name: writerside
description: 在這個 JetBrains Writerside 專案中撰寫或修改技術筆記、建立或更新 `Writerside/topics/*.md`、把 topic 掛進 `Writerside/hi.tree`、選擇 Markdown 或 semantic markup、處理 tabs、procedure、chapter、show-structure、deflist、table、seealso、note、warning、img、video、snippet、include、if 等 Writerside 標記，以及修正 anchor/TOC/checker 問題時使用。遇到「幫我新增一篇筆記」、「修改既有文章」、「補 topic 到 hi.tree」、「修 Writerside/Markdown 錯誤」、「處理 element id/anchor/TOC 問題」、「把內容改成合適的 Writerside 語義標記」這類需求時優先使用。
---

# 在這個 repo 中處理 Writerside 內容

先把重點放在「產出一篇可發布、可通過檢查的文章」，不要先把注意力擴散到部署、站台設定或整站重構。

## 先確認任務型態

- 先判斷這次是新增 topic、修改既有文章、補 `hi.tree`、修 checker 錯誤，還是把既有 Markdown 改寫成較合適的 semantic markup。
- 先到 `Writerside/topics/` 和 `Writerside/hi.tree` 搜尋是否已經有同主題文章，避免重複寫一篇只差措辭的新筆記。
- 先讀 1 到 2 篇同類型文章，模仿這個專案慣用的語氣與結構。
- 優先沿用繁體中文敘述，技術術語、CLI 指令、程式碼與設定鍵值保留英文。

## 決定檔名

- 在 `Writerside/topics/` 建立或修改檔案。
- 使用能直接看出主題的檔名，保留 `.md` 副檔名。
- 優先採用這個專案常見的命名方式：技術名稱 + 問題/動作 + 補充描述，用連字號串接，允許中英混用。
- 檔名也會影響預設的 web page name / URL，優先短、穩定、可讀，不要把所有關鍵詞都塞進檔名。
- 如果 H1 需要寫得比較完整，檔名仍可相對精簡，再用標題與 `toc-title` 補語意。
- 如果是已發布的既有文章，改檔名代表改 URL；除非只是未發布草稿，否則要先確認是否需要 redirect 或同步更新外部連結。
- 避免使用 `note.md`、`temp.md`、`test.md` 這類沒有辨識度的名稱。

可參考這類現有命名：

- `macOS-WiFi-DNS-設定筆記.md`
- `Jetbrains-Writerside-CICD-自動化部署-Markdown-到-GIthub-Pages.md`
- `Azure-App-Service-Deploy.md`

## 決定文章放在哪個分類

- 打開 `Writerside/hi.tree`，先找最接近主題的既有分類，再把新 topic 掛進去。
- 優先放在現有群組底下，不要沒有必要就新增新的頂層分類。
- 把新 topic 放在相近主題旁邊，不要只是機械式地加在檔案最後面。
- Writerside 預設會把 topic title 當成 TOC 項目；如果 H1 偏長，優先在 `hi.tree` 補較短的 `toc-title`。
- 只有在側欄標題需要更短、或想跟 H1 顯示名稱不同時，才加 `toc-title`。

範例：

```xml
<toc-element topic="windows-11-native-nvme-enable.md" toc-title="啟用 Native NVMe"/>
```

## 撰寫文章骨架

- 先寫清楚 H1 標題，標題可以比檔名更自然、更像人會看的文章名稱。
- 開頭先交代情境、問題或結論，不要一開始就丟一大段沒有上下文的指令。
- 優先使用問題導向、實作導向的寫法；讓讀者能快速知道「遇到什麼情境、怎麼做、做完怎麼驗證」。
- 沒有必要時，不要硬塞過多背景理論。

優先使用這種骨架，再依內容增減章節：

````markdown
# 標題

一句話說明這篇筆記在解決什麼問題。

## 問題描述

描述症狀、情境、限制條件。

## 解決方案

說明核心作法、設定方向或判斷方式。

## 操作步驟

1. 第一步
2. 第二步
3. 第三步

## 指令與設定範例

```bash
example command
```

## 補充說明

- 放常見坑、例外情況、替代方案。

## 參考資料
````

如果是錯誤排除型文章，優先寫成：

1. 問題症狀
2. 根本原因
3. 解法
4. 驗證方式

如果是安裝或教學型文章，優先寫成：

1. 前置條件
2. 安裝/設定步驟
3. 驗證結果
4. 常見問題

## 選擇 Markdown 或 semantic markup

- 預設先用 Markdown 寫標題、段落、清單、連結與一般程式碼區塊；只有在 semantic markup 能更清楚表達「意義」或改善重用性時再注入 XML。
- 依官方 Writerside markup 參考，遇到這些情境優先用 semantic markup：
  - 長文結構與右側導覽：`<chapter>`、`<show-structure>`
  - 可切換內容：`<tabs>`、`<tab>`
  - 明確步驟：`<procedure>`、`<step>`
  - 名詞解釋或結構化整理：`<deflist>`、`<def>`、`<table>`、`<seealso>`
  - 提醒與風險：`<note>`、`<tip>`、`<warning>`
  - UI 與路徑語意：`<control>`、`<ui-path>`、`<path>`、`<shortcut>`
  - 快速摘要：`<tldr>`
  - 並排比較：`<compare>`
  - 重複或條件內容：`<snippet>`、`<include>`、`<if>`
  - 需要尺寸或樣式控制的媒體：`<img>`、`<video>`
- 不要再用 `<caution>`；目前官方 semantic markup reference 找不到這個標記。
- 如果 `<tabs>` / `<tab>` 內會混多層 HTML list、`<note>`、`<warning>`、`<code-block>` 等較複雜內容，先評估是否真的值得保留 tabs；若 checker 已經出現 `MRK002`、`MRK009` 這類結構錯誤，優先簡化成較單純的 XML，必要時直接改回一般 Markdown 小節。
- 若不確定該用哪個標記，優先讀 `references/markup-reference.md`，再回頭決定是否真的需要 XML。
- 若問題偏向長文切章節、右側 topic navigation、可折疊章節、definition list 或 related links，直接讀 `references/structural-elements.md`。
- 若問題偏向一般清單、巢狀 list、multiple columns、definition list 寫法、FAQ/troubleshooting 排版，直接讀 `references/lists-reference.md`。
- 若問題偏向 Markdown table、XML table、merge cells、header row/column、欄寬控制或 table 轉換，直接讀 `references/tables-reference.md`。
- 若問題偏向 inline code、code block、`src` 引入程式碼、CDATA、soft wrap、code compare 或 code block link，直接讀 `references/code-reference.md`。
- 若問題偏向 Mermaid flowchart、sequence diagram、state diagram、git graph、`lang="mermaid"` 或 Mermaid 從檔案引用，直接讀 `references/mermaid-reference.md`。
- 若問題偏向 PlantUML、`@startuml`、class/use case/JSON/Gantt/mind map 圖、Graphviz、`ignore-vars="false"` 或 `.puml` 檔引用，直接讀 `references/plantuml-reference.md`。
- 若問題偏向 D2、`lang="d2"`、`.d2` 檔引用、宣告式圖表語法或建置環境安裝 D2，直接讀 `references/d2-reference.md`。
- 若問題偏向數學公式、`lang="tex"`、`<math>`、Markdown `$...$` inline math 或 Tex/LaTeX 數學語法，直接讀 `references/math-reference.md`。
- 若問題偏向 topic / chapter labels、`labels.list`、`<primary-label>`、`<secondary-label>`、版本/方案/內部功能標記或 label tooltip/href，直接讀 `references/labels-reference.md`。
- 若問題偏向 Writerside 專案結構、help module root、`writerside.cfg`、新建專案、把文件加進既有開發專案或 project templates，直接讀 `references/projects-reference.md`。
- 若問題偏向 help module、module root、module structure、`topics/` / `images/` / `*.tree` / `cfg/` 目錄分工、多 module 專案或跨 module `origin` 重用，直接讀 `references/help-modules-reference.md`。
- 若問題偏向 Writerside build、GitHub Actions、GitHub Pages、deployment workflow、`writerside-github-action`、checker action、Pages artifact 或 Algolia 發布，直接讀 `references/build-deploy.md`。
- 若問題偏向 `buildprofiles.xml`、header/footer、Algolia、shortcut switcher、OG metadata、sitemap、`ignore-problems` 或 `cfg/` 建置設定，直接讀 `references/buildprofiles-reference.md`。
- 若問題偏向 `llms.txt`、`<llms-txt>`、single-file vs per-topic LLM export、`_llms/` 產物目錄或把文件輸出給 LLM agent 使用，直接讀 `references/llms-reference.md`。
- 若問題偏向 `v.list`、`<var>`、`%product%` 這類變數插值、built-in variables、`ignore-vars`、`smart-ignore-vars`、snippet 變數傳值或 instance-conditioned variables，直接讀 `references/variables-reference.md`。
- 若問題偏向 `writerside.cfg`、`project.ihp`、`<topics>`、`<images>`、`<instance>`、`<settings>`、`<build-config>`、`smart-ignore-vars` 或 help module 目錄配置，直接讀 `references/writerside-cfg-reference.md`。
- 若問題偏向 help instance、multiple outputs、tree file、`<instance-profile>`、instance ID、`status="deprecated|eap"`、跨 instance 重用、`<include>`、`<snippet>`、`ref`/`in` 或 reusable TOC chunk，直接讀 `references/instances-reference.md`。
- 若問題偏向 `hi.tree`、tree file、`<toc-element>`、`start-page`、`toc-title`、hidden topic、外部 TOC 連結、home page 或 TOC 階層調整，直接讀 `references/toc-reference.md`。
- 若問題偏向 `tip`、`note`、`warning`、blockquote admonition 或提醒層級判斷，直接讀 `references/admonitions-reference.md`。
- 若問題偏向 `<tldr>`、quick facts、標題下方摘要區塊或 TLDR 長度拿捏，直接讀 `references/tldr-reference.md`。
- 若問題偏向 link summary、card summary、web summary、第一段摘要策略或搜尋預覽文字，直接讀 `references/summary-reference.md`。
- 若問題偏向首頁、section landing page、spotlight cards、`<section-starting-page>`、overview topic 或 learning path 入口頁，直接讀 `references/starting-pages-reference.md`。
- 若問題偏向可下載範例檔、ZIP/CSV/TXT 附件、`<resource>`、resources directory 或 `writerside.cfg` 的 resources 設定，直接讀 `references/downloadable-resources-reference.md`。
- 若問題偏向截圖、GIF、thumbnail、inline/block image、dark theme 圖、外部圖片或 `MRK058`，直接讀 `references/images-reference.md`。

## 在 Markdown 內注入 XML 的原則

- XML 區塊在 Markdown 中要維持連續，不要被不必要的空行切斷。
- 允許在 XML 元素內保留空行來插入 Markdown 段落，但不要用 tab 縮排，避免被 Markdown 當成 block quote 或 code block。
- 在 `<step>`、`<tab>`、`<li>` 這類容器內，如果有多段文字或文字混圖片/程式碼，優先用 `<p>` 包起來，不要留下難解析的 dangling text。
- 如果 `<tab>` 內已經混到多層 HTML list、提醒框和多段 code block，代表這段內容可能過於脆弱；先嘗試簡化結構，不要為了保留 tabs 而硬撐。
- 如果只是單純的有序清單，不必硬轉成 XML；但只要內容是在描述「如何完成任務」，優先改用 `<procedure>`。

## 程式碼、anchor 與重用

- CLI 指令或可執行命令，優先標清楚語言；需要提示字元時可用 `<code-block prompt="$">`，提示字元不會被複製。
- 如果 `<code-block>` 內容是不完整範例，或 IDE 語法注入會一直報錯，可加 `noinject="true"`。
- 如果程式碼、文字或連結 URL 內出現 `%foo%`、`%E5...`、`%20`、`%25` 這類可能被當成 Writerside 變數或 percent-encoding 的內容，可加 `ignore-vars="true"`。
- 需要穩定 anchor 時，Markdown 標題優先補 `{#custom-id}`；XML 元素則用 `id="custom-id"`。
- 只有在真的有重複內容或條件輸出需求時，才引入 `<snippet>`、`<include>`、`<if>`；一般單篇筆記不要過度工程化。

## 處理圖片與影片

- 把本地圖片放到 `Writerside/images/`。
- 在文章中用相對路徑引用，不要加 `images/` 前綴。
- 簡單截圖可直接用 Markdown 圖片；如果需要 `width`、`height`、`border-effect`、縮圖或其他顯示控制，改用 `<img>`。
- 圖片與影片都要補能看懂內容的 `alt` 或說明，不要只留空白替代文字。
- 如果使用 `<video>` 放本地影片，檔案也放在 `Writerside/images/`，並準備同名預覽圖。
- 使用有意義的檔名，例如 `writerside-new-topic-dialog.png`。

## 避免搬用舊文遷移格式

- 只有真的從舊部落格搬文時，才保留「原文發布日期」、「原文連結」或「本文章從點部落遷移至 Writerside」這類區塊。
- 如果是全新筆記，不要憑空補這些欄位。

## 收尾驗證

- 先確認 `Writerside/hi.tree` 中的 `topic` 檔名和實際檔名完全一致。
- 先修新增那篇文章的 Markdown 格式，再做整體檢查。
- 如果只有單篇變更，優先跑單檔檢查；如果同時改了多篇，再跑專案腳本。

單檔修復與驗證：

```bash
npx markdownlint-cli2 --fix --no-globs Writerside/topics/<topic-file>.md
npx markdownlint-cli2 --no-globs Writerside/topics/<topic-file>.md
```

整體檢查：

```bash
./scripts/check-markdown.sh
npm run pre-deploy
```

## 需要更多上下文時再讀這些檔案

- `references/markup-reference.md`: 判斷該用 Markdown、semantic markup、`id`、`tabs`、`procedure`、`compare`、`img`、`video` 時讀。
- `references/structural-elements.md`: 判斷 `chapter`、Markdown 標題層級、`show-structure`、collapsible blocks、`deflist`、`list`、`table`、`seealso` 時讀。
- `references/lists-reference.md`: 判斷 `list`、巢狀清單、multiple columns、`deflist`、definition list type、FAQ/troubleshooting list 寫法時讀。
- `references/tables-reference.md`: 判斷 Markdown table、XML `table`、merge cells、header row/column、欄寬、border 與 table 轉換時讀。
- `references/code-reference.md`: 判斷 inline code、fenced code、`code-block`、`src`、`include-lines`、`include-symbol`、CDATA、soft wrap、compare block 與 code links 時讀。
- `references/mermaid-reference.md`: 判斷 Mermaid code block、flowchart/sequence/state/git graph、從 `.mermaid` 檔引用、IDE plugin 與目前不支援功能時讀。
- `references/plantuml-reference.md`: 判斷 PlantUML code block、`@startuml`/`@startjson`/`@startgantt`、`.puml` 檔引用、Graphviz、CDATA 與 `ignore-vars="false"` 時讀。
- `references/d2-reference.md`: 判斷 D2 code block、從 `.d2` 檔引用、建置前安裝 D2 與 D2/Mermaid/PlantUML 的選擇時讀。
- `references/math-reference.md`: 判斷 `tex` block math、`<math>`、Markdown `$...$` inline math、Tex/LaTeX 數學表示法時讀。
- `references/labels-reference.md`: 判斷 `labels.list`、`<primary-label>`、`<secondary-label>`、short-name、label href/color/tooltip 與 topic/chapter label 採用時讀。
- `references/projects-reference.md`: 判斷 Writerside project / help module root、`writerside.cfg`、instances、project templates、existing project 加入文件與專案結構時讀。
- `references/help-modules-reference.md`: 判斷 help module、module root、module structure、`topics/`、`images/`、`*.tree`、`cfg/`、optional files、多 module 專案與跨 module `origin` 重用時讀。
- `references/build-deploy.md`: 判斷 Writerside build、GitHub Actions、GitHub Pages、deploy workflow、checker action、Pages artifact、Algolia 發布與 CI deploy 問題時讀。
- `references/buildprofiles-reference.md`: 判斷 `buildprofiles.xml`、`cfg/` 預設位置、global vs instance-specific build settings、header/footer、Algolia、social/footer、shortcut layouts、OG/sitemap 與 `ignore-problems` 時讀。
- `references/llms-reference.md`: 判斷 `llms.txt`、`<llms-txt>`、single-file / per-topic LLM 輸出、`_llms/` 產物目錄與 llms export 採用方式時讀。
- `references/variables-reference.md`: 判斷 `v.list`、`<var>`、`%var%` 插值、built-in variables、`ignore-vars`、`smart-ignore-vars`、snippet 變數傳值與 instance-conditioned variables 時讀。
- `Writerside/topics/variables.md`: 查 repo 內最小可用的變數、跳脫 `%` 與 `ignore-vars` 範例時讀。
- `references/writerside-cfg-reference.md`: 判斷 `writerside.cfg` / `project.ihp`、help module 主設定、topics/images/vars/categories/snippets/build-config、instances 與 module-level settings 時讀。
- `references/instances-reference.md`: 判斷 help instances、multiple outputs、instance ID、tree file、`<instance-profile>`、`status`、跨 instance reuse、`<include>`、`<snippet>`、`ref`/`in`、`wip`、redirect 與 reusable TOC chunk 時讀。
- `references/toc-reference.md`: 判斷 `hi.tree`、tree file、`<instance-profile>`、`<toc-element>`、`start-page`、`toc-title`、`hidden="true"`、外部連結 TOC 與 TOC 階層時讀。
- `references/admonitions-reference.md`: 判斷 `tip`、`note`、`warning`、Markdown blockquote admonition 與提醒層級時讀。
- `references/tldr-reference.md`: 判斷 `<tldr>`、quick facts、標題下方摘要、事實條目長度與數量時讀。
- `references/summary-reference.md`: 判斷 `link-summary`、`card-summary`、`web-summary`、第一段摘要與連結/卡片/搜尋預覽摘要時讀。
- `references/starting-pages-reference.md`: 判斷 `<section-starting-page>`、首頁/章節入口頁、spotlight/primary/secondary/misc 區塊、cards/links 群組與 XML-only starting page 規則時讀。
- `references/downloadable-resources-reference.md`: 判斷 `<resource>`、可下載檔案、resources directory、附件連結與 `writerside.cfg` resources 設定時讀。
- `references/images-reference.md`: 判斷圖片路徑、Markdown 圖片屬性、`img`、thumbnail、GIF、dark theme image、inline/block image 與 `MRK058` 時讀。
- `Writerside/hi.tree`: 查分類與 TOC 寫法。
- `.markdownlint-cli2.jsonc`: 查 Markdown 規則。
- `scripts/check-markdown.sh`: 查專案實際使用的 lint 流程。
- `scripts/pre-deploy-check.sh`: 查本地部署前檢查流程。
- `.github/workflows/deploy.yml`: 查 CI 端的 Writerside build 與 checker 流程。
- `Writerside/topics/*.md`: 查相近主題的標題、段落與寫作習慣。
- `references/checker-errors.md`: 遇到 `MRK003`、anchor 衝突、圖片或 topic 路徑問題時讀。
- `references/validation-flow.md`: 要判斷單檔 lint、整體 lint、`pre-deploy` 與 CI checker 差異時讀。
- `references/build-deploy.md`: 使用者問 Writerside build、GitHub Actions、部署或 Algolia 時讀。
