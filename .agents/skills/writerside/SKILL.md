---
name: writerside
description: 在目前的 JetBrains Writerside repo `/Users/jakeuj/WritersideProjects/writerside` 中撰寫、修改與驗證公開技術筆記及站台設定。涵蓋 `Writerside/topics/*.md`、`Writerside/hi.tree`、web-summary/SEO、去識別化、Markdown 與 semantic markup、anchor/TOC/checker（含 MRK002）、GitHub Pages、header/footer、自訂 HTML/CSS/JavaScript、第三方 widget、sitemap/robots、Search Console、站內搜尋與 Algolia。用於新增或改寫文章、修 Writerside/Markdown 錯誤、調整網站外觀、站台注入、發布或搜尋設定；若從其他專案蒐集內容並回寫固定發布 repo，改用全域版 writerside skill。
---

# 在這個 repo 中處理 Writerside

以「產出可公開、可通過檢查的內容」為主；除非任務明確涉及部署或整站設定，不要擴大範圍。

## 讀取策略

- 先完整讀完本檔，再依「參考檔路由」只選本次任務需要的 reference。
- 選中的 reference 必須完整讀到 EOF；若工具輸出被截斷，改用分段讀取續讀，不得依截斷內容開始修改。
- 不要一次載入全部 reference。先用本檔完成分類，再讀最少且足夠的檔案。
- 新增或大幅改寫 topic 時，必讀 [topic-authoring-workflow.md](references/topic-authoring-workflow.md)；其他任務依路由選讀。

## Repo-local 與全域版分工

- 當前工作目錄是本 repo 時，使用這份 repo-local skill，所有 `Writerside/...`、`scripts/...` 路徑都相對於 repo root。
- 從其他專案整理資訊並回寫本 repo 時，使用全域版；不要把來源專案的硬編碼路徑寫進共用規則。
- 本目錄是共用 reference 的 source of truth。全域入口模板位於 `assets/global-skill/`。
- 需要重建已安裝的全域版時才執行 `./scripts/sync-writerside-skill.sh`；不要因一般寫作任務自行同步。

## 核心流程

1. 判斷任務是新增/修改 topic、調整 `hi.tree`、修 checker、改站台設定或第三方 widget，還是處理部署/搜尋。
2. 在 `Writerside/topics/` 與 `Writerside/hi.tree` 搜尋同主題內容；寫作時再讀 1 到 2 篇同類文章以沿用語氣與結構。
3. 把內容視為會公開上網，先盤點並替換真實 ID、資源名稱、IP、網域、email、帳號、secret、token、connection string 與客戶/專案資訊。
4. 只讀本次需要的 reference，完成內容或設定修改；避免順手重構無關文章或整站。
5. 先驗證 touched files，再依變更範圍執行 Writerside 層級或專案層級檢查。

## 不可省略的內容規則

- 以繁體中文敘述；技術術語、CLI、程式碼與設定鍵保留英文。
- 新 topic 預設使用短而穩定的 ASCII kebab-case 檔名；已發布文章改名等同改 URL，先處理 redirect 與外部連結影響。
- 開頭先給解法或判斷。公開 topic 預設在 H1 後放一行 `<web-summary>`；有 1 到 3 個 quick facts 時才補 `<tldr>`。
- 一般標題、段落、清單、連結與 code fence 優先用 Markdown；只有語意、結構或重用需求明確時才用 semantic markup。不要使用 `<caution>`。
- 在 `hi.tree` 把 topic 放到最接近的既有分類；`toc-title` 與 H1 相同時省略，避免 `TOC007`。
- 內部 topic 連結只用 `[標題](topic-filename.md)`：保留 `.md`，不要加 `./` 或 `../`。
- XML/semantic markup 與 `hi.tree` 中的 `&`、`<`、`>` 必須正確 escape；Markdown 一般文字的 `&` 通常可保留。
- 超過約 40 列或單一 section 接近 8000 bytes 的表格/清單要拆成穩定、唯一 anchor 的同層 sections。

## 驗證原則

- 只改單篇時先跑單檔 markdownlint；改多篇時跑 `./scripts/check-markdown.sh`。
- 修改 `hi.tree`、XML、部署或站台設定時，再跑 `npm run pre-deploy`；CI Writerside checker 才是正式建置的最終判定。
- 送出前檢查 topic 與 `hi.tree` 檔名一致，並重做去識別化掃描。
- 具體命令與檢查層級讀 [validation-flow.md](references/validation-flow.md)；MRK/CTT/CDE/TOC/REF 錯誤讀 [checker-errors.md](references/checker-errors.md)。

## 參考檔路由

- **文章工作流**：新增/改寫 topic、檔名、文章骨架、公開內容安全、TOC、內部連結或大型 section 時讀 [topic-authoring-workflow.md](references/topic-authoring-workflow.md)。
- **摘要與入口頁**：`web-summary`、link/card summary 或 Search Console 摘要讀 [summary-reference.md](references/summary-reference.md)；quick facts 讀 [tldr-reference.md](references/tldr-reference.md)；首頁/章節入口頁讀 [starting-pages-reference.md](references/starting-pages-reference.md)。
- **一般 markup**：Markdown/XML 選擇、tabs/procedure/include 等讀 [markup-reference.md](references/markup-reference.md)；長文結構讀 [structural-elements.md](references/structural-elements.md)；清單、表格與提醒分別讀 [lists-reference.md](references/lists-reference.md)、[tables-reference.md](references/tables-reference.md)、[admonitions-reference.md](references/admonitions-reference.md)。
- **程式碼與媒體**：code block、CDATA、`ignore-vars` 讀 [code-reference.md](references/code-reference.md)；圖片/GIF/thumbnail/MRK058 讀 [images-reference.md](references/images-reference.md)；附件讀 [downloadable-resources-reference.md](references/downloadable-resources-reference.md)。
- **圖表與公式**：依格式讀 [mermaid-reference.md](references/mermaid-reference.md)、[plantuml-reference.md](references/plantuml-reference.md)、[d2-reference.md](references/d2-reference.md) 或 [math-reference.md](references/math-reference.md)。
- **專案與 instance**：專案根目錄讀 [projects-reference.md](references/projects-reference.md)；module 結構讀 [help-modules-reference.md](references/help-modules-reference.md)；主設定讀 [writerside-cfg-reference.md](references/writerside-cfg-reference.md)；instance/reuse 讀 [instances-reference.md](references/instances-reference.md)。
- **TOC、標籤與變數**：`hi.tree`/home page/hidden topic 讀 [toc-reference.md](references/toc-reference.md)；labels 讀 [labels-reference.md](references/labels-reference.md)；`v.list`、`%var%`、`ignore-vars` 讀 [variables-reference.md](references/variables-reference.md)。
- **建置、SEO 與搜尋**：GitHub Actions/Pages/Algolia request 讀 [build-deploy.md](references/build-deploy.md)；`buildprofiles.xml`、header/footer、自訂 HTML/CSS/JavaScript、第三方 widget、sitemap、Search Console 讀 [buildprofiles-reference.md](references/buildprofiles-reference.md)；`llms.txt` 輸出讀 [llms-reference.md](references/llms-reference.md)。
- **錯誤與驗證**：checker code、anchor、XML escape、topic/image path 讀 [checker-errors.md](references/checker-errors.md)；lint/pre-deploy/CI 分層讀 [validation-flow.md](references/validation-flow.md)。

## 維護這個 skill

- 把核心決策與路由留在 `SKILL.md`；長例子、完整命令與領域細節只放一份 reference，避免重複。
- 新增 reference 時，從本檔直接連結並寫清楚讀取條件；不要建立多層 reference 鏈。
- 修改共用規則時，同步檢查 `assets/global-skill/SKILL.md` 的跨專案入口是否仍一致，並驗證兩個 skill folder。
