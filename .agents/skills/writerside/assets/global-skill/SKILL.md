---
name: writerside
description: 從任何專案蒐集技術資訊，整理成可公開發布的 Writerside 技術筆記，並回寫固定 repo `/Users/jakeuj/WritersideProjects/writerside`。涵蓋 topics/hi.tree、web-summary/SEO、去識別化、Markdown 與 semantic markup、anchor/TOC/checker（含 MRK002）、GitHub Pages、sitemap/robots、Search Console、站內搜尋與 Algolia；在使用者明確要求時也可 commit/push。用於跨 repo 整理筆記、修 Writerside 錯誤、調整發布或搜尋設定。
---

# 從任何專案回寫 Writerside 發布 repo

以「從來源萃取可公開知識，產出可通過檢查的文章」為主；除非任務明確涉及部署、發布或整站設定，不要擴大範圍。

## 讀取策略

- 先完整讀完本檔，再依「參考檔路由」只選本次任務需要的 reference。
- 選中的 reference 必須完整讀到 EOF；若工具輸出被截斷，改用分段讀取續讀，不得依截斷內容開始修改。
- 不要一次載入全部 reference。先用本檔完成分類，再讀最少且足夠的檔案。
- 新增或大幅改寫 topic 時，必讀 `references/topic-authoring-workflow.md`；其他任務依路由選讀。

## 工作位置

- `SOURCE_WORKSPACE` 是目前蒐集資訊的專案；預設為當前工作目錄。
- `WRITERSIDE_REPO` 固定為 `/Users/jakeuj/WritersideProjects/writerside`。
- 先在來源專案理解問題與蒐集證據，再到 `WRITERSIDE_REPO` 寫檔、調整 TOC、驗證與發布。
- 進入發布 repo 後，共用 reference 內的 `Writerside/...`、`scripts/...`、`.github/...` 都相對於 repo root。
- 不要把來源專案的內部路徑、識別資料或私有實作原封不動搬進公開文件。

## 核心流程

1. 分清來源與發布 repo，判斷任務是新增/修改 topic、調整 `hi.tree`、修 checker、改站台設定，還是處理部署/搜尋。
2. 在發布 repo 的 `Writerside/topics/` 與 `Writerside/hi.tree` 搜尋同主題內容；寫作時再讀 1 到 2 篇同類文章。
3. 從來源萃取可公開的問題、原因、解法與驗證方式；盤點並替換真實 ID、資源名稱、IP、網域、email、帳號、secret、token、connection string 與客戶/專案資訊。
4. 只讀本次需要的 reference，完成內容或設定修改；避免順手修改來源專案或無關文章。
5. 在發布 repo 驗證 touched files；只有使用者明確要求發布、commit 或 push 時才執行 Git 寫入與遠端操作。

## 不可省略的內容規則

- 以繁體中文敘述；技術術語、CLI、程式碼與設定鍵保留英文。
- 新 topic 預設使用短而穩定的 ASCII kebab-case 檔名；已發布文章改名等同改 URL，先處理 redirect 與外部連結影響。
- 開頭先給解法或判斷。公開 topic 預設在 H1 後放一行 `<web-summary>`；有 1 到 3 個 quick facts 時才補 `<tldr>`。
- 一般標題、段落、清單、連結與 code fence 優先用 Markdown；只有語意、結構或重用需求明確時才用 semantic markup。不要使用 `<caution>`。
- 在 `hi.tree` 把 topic 放到最接近的既有分類；`toc-title` 與 H1 相同時省略，避免 `TOC007`。
- 內部 topic 連結只用 `[標題](topic-filename.md)`：保留 `.md`，不要加 `./` 或 `../`。
- XML/semantic markup 與 `hi.tree` 中的 `&`、`<`、`>` 必須正確 escape；Markdown 一般文字的 `&` 通常可保留。
- 超過約 40 列或單一 section 接近 8000 bytes 的表格/清單要拆成穩定、唯一 anchor 的同層 sections。

## 驗證與發布

- 只改單篇時先跑單檔 markdownlint；改多篇時跑 `./scripts/check-markdown.sh`。
- 修改 `hi.tree`、XML、部署或站台設定時，再跑 `npm run pre-deploy`；CI Writerside checker 才是正式建置的最終判定。
- 送出前檢查 topic 與 `hi.tree` 檔名一致，並重做去識別化掃描。
- 具體命令與檢查層級讀 `references/validation-flow.md`；MRK/CTT/CDE/TOC/REF 錯誤讀 `references/checker-errors.md`。
- 發布前在 `WRITERSIDE_REPO` 檢查 `git status` 與 diff，只 stage 預期檔案；未獲明確要求時不要 commit/push。

## 參考檔路由

以下路徑都位於已安裝的 writerside skill；內容中的 repo 相對路徑則以 `WRITERSIDE_REPO` 為根目錄。

- **文章工作流**：新增/改寫 topic、檔名、文章骨架、公開內容安全、TOC、內部連結或大型 section 時讀 `references/topic-authoring-workflow.md`。
- **摘要與入口頁**：`web-summary`、link/card summary 或 Search Console 摘要讀 `references/summary-reference.md`；quick facts 讀 `references/tldr-reference.md`；首頁/章節入口頁讀 `references/starting-pages-reference.md`。
- **一般 markup**：Markdown/XML 選擇、tabs/procedure/include 等讀 `references/markup-reference.md`；長文結構讀 `references/structural-elements.md`；清單、表格與提醒分別讀 `references/lists-reference.md`、`references/tables-reference.md`、`references/admonitions-reference.md`。
- **程式碼與媒體**：code block、CDATA、`ignore-vars` 讀 `references/code-reference.md`；圖片/GIF/thumbnail/MRK058 讀 `references/images-reference.md`；附件讀 `references/downloadable-resources-reference.md`。
- **圖表與公式**：依格式讀 `references/mermaid-reference.md`、`references/plantuml-reference.md`、`references/d2-reference.md` 或 `references/math-reference.md`。
- **專案與 instance**：專案根目錄讀 `references/projects-reference.md`；module 結構讀 `references/help-modules-reference.md`；主設定讀 `references/writerside-cfg-reference.md`；instance/reuse 讀 `references/instances-reference.md`。
- **TOC、標籤與變數**：`hi.tree`/home page/hidden topic 讀 `references/toc-reference.md`；labels 讀 `references/labels-reference.md`；`v.list`、`%var%`、`ignore-vars` 讀 `references/variables-reference.md`。
- **建置、SEO 與搜尋**：GitHub Actions/Pages/Algolia request 讀 `references/build-deploy.md`；`buildprofiles.xml`、header/footer、sitemap、Search Console 讀 `references/buildprofiles-reference.md`；`llms.txt` 輸出讀 `references/llms-reference.md`。
- **錯誤與驗證**：checker code、anchor、XML escape、topic/image path 讀 `references/checker-errors.md`；lint/pre-deploy/CI 分層讀 `references/validation-flow.md`。

## 維護與同步

- repo-local `.agents/skills/writerside/` 是共用 reference 的 source of truth；這個檔案只處理跨專案差異。
- 把核心決策與路由留在入口；長例子、完整命令與領域細節只放一份 reference。
- 在發布 repo 更新模板後，只有需要重建已安裝的全域版時才執行 `./scripts/sync-writerside-skill.sh`。
