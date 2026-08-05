# Writerside Topic Authoring Workflow

新增 topic、大幅改寫既有文章、調整檔名/TOC，或把內部資料整理成公開文章時讀這份參考。

## 目錄

- [先盤點內容與風險](#先盤點內容與風險)
- [決定檔名與 URL](#決定檔名與-url)
- [安排 TOC](#安排-toc)
- [撰寫文章](#撰寫文章)
- [處理大型 section](#處理大型-section)
- [處理內部連結與舊文](#處理內部連結與舊文)

## 先盤點內容與風險

1. 先判斷是新增 topic、修改既有文章、補 `hi.tree`，還是將既有 Markdown 改成 semantic markup。
2. 在 `Writerside/topics/` 與 `Writerside/hi.tree` 搜尋同主題內容，避免建立只差措辭的重複文章。
3. 讀 1 到 2 篇同類文章，沿用繁體中文語氣、段落結構與術語選擇。
4. 把文章視為會公開上網；除非使用者明確說是私人草稿，否則先去識別化再寫入。

盤點 subscription/tenant ID、GUID、完整 resource ID、resource group、App Service/Function App/VM/database、VNet/subnet、IP、FQDN、email、帳號、客戶名、專案代號、secret、token 與 connection string。用一致的中性值替換，例如 `<subscription-id>`、`<resource-group>`、`<app-name>`、`<private-ip>`。

- 指令、JSON、表格與終端輸出要整段一起去識別化，不能只改輸入而保留真實輸出。
- 去識別化後仍可能暴露內部環境時，改寫成抽象步驟、參數化指令與示意名稱。
- 若文章來自真實案例，可在前言或範例前註明名稱、ID 與路徑已去識別化。

## 決定檔名與 URL

- topic 放在 `Writerside/topics/`，保留 `.md` 副檔名。
- 新文預設用能直接看出「主要技術 + 核心問題/動作」的 ASCII kebab-case，例如：
  - `azure-app-service-vnet-tcpping-timeout.md`
  - `nswag-settings-httpclient-startup.md`
  - `windows-11-native-nvme-enable.md`
- 檔名會直接影響 URL；H1 與 `toc-title` 只改顯示文字。次要環境、傳輸路徑或診斷工具放在 H1/前言，不要把檔名寫成整句搜尋 query。
- 避免 `note.md`、`temp.md`、`test.md` 等無辨識度名稱。
- 已發布文章改名會改 URL；先確認 `Writerside/redirection-rules.xml`、`accepts-web-file-names` 與外部連結是否要同步。歷史中文檔名不代表新文也要使用中文 slug。

## 安排 TOC

- 在 `Writerside/hi.tree` 找最接近的既有分類，把 topic 放在相關文章旁；沒有必要不要新增頂層分類。
- H1 太長或側欄需要不同文字時才加 `toc-title`。若它與 H1 完全相同，移除以避免 `TOC007`。
- `toc-title` 不改 URL。語意不變時避免 `&`、`<`、`>`；若必須使用，依 XML 規則 escape。
- 修改後確認 `topic="..."` 與實際檔名完全一致，並執行 `xmllint --noout Writerside/hi.tree`。

## 撰寫文章

- H1 可以比檔名自然完整。第一段先回答「現在該怎麼做」，不要只說本文要記錄什麼，也不要把答案藏到後面的「先講結論」。
- 公開 topic 預設在 H1 下一個區塊放一行 `<web-summary>`，用純文字說明「主題 + 可得到的解法/判斷」；避免「本文記錄……」。其中的 `<`、`>`、`&` 要 XML escape。
- 只有 1 到 3 個可立即執行的關鍵動作或判斷時才補 `<tldr>`。
- 預設用 Markdown；只有 semantic markup 能清楚表達步驟、提醒、UI 路徑、切換內容、重用或結構時才導入 XML。

通用骨架如下，依任務刪減，不必硬湊所有章節：

````markdown
# 標題

<web-summary>用一句話說明情境，以及讀者能得到的解法或判斷。</web-summary>

先用 1 到 3 句給答案、最短解法或判斷。

## 問題描述

## 解決方案

## 操作步驟

## 指令與設定範例

```bash
example command
```

## 驗證方式

## 補充說明

## 參考資料
````

錯誤排除文依「解法/最短判斷 → 症狀 → 根本原因 → 驗證」排序；安裝教學依「建議做法 → 前置條件 → 步驟 → 驗證 → 常見問題」排序。

## 處理大型 section

- 超過約 40 列的表格、全站索引、完成矩陣、API/DB/item 全量表，先做短總覽，再依類型、狀態、模組、等級、字母或來源頁拆成同層 H2。
- 每段使用穩定且唯一的 `{#custom-id}`；總覽只放摘要與分段連結，不重複完整資料。
- 以 8000 bytes 作為單一 section 的保守上限，不要等到搜尋服務的 10000 bytes hard limit。
- 產生器要直接 deterministic 地輸出分段，避免重跑後 anchor、列順序或分組漂移。
- 正文只需說明「避免搜尋索引單段內容過大」；除非正在排除部署錯誤，不要公開供應商錯誤訊息或 internal record ID。

## 處理內部連結與舊文

- 跨 topic 使用 `[標題](topic-filename.md)`；必須保留 `.md`，且不要加 `./` 或 `../`。目標檔也必須存在並掛入 `hi.tree`，否則 checker 會報 `REF002`。
- 只有真的從舊部落格搬文時才保留原文日期、原文連結或遷移聲明；全新筆記不要憑空加入。
- 圖片與影片、code block、anchor、semantic markup 的完整規則依 `SKILL.md` 的路由讀對應 reference，不在這份工作流重複。
