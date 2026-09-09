# 最新文章、首頁與 RSS

用於文章登錄、發布日期、精選、重大更新、生成入口及 RSS 維護。以下為本 repo 的自訂發布流程，不是 Writerside 原生 RSS 生成功能；`social type="rss"` 只提供連結圖示。

## 資料與日期

`data/posts.json` 是文章登錄來源，`scripts/publication.py` 是實作依據。不要另外建立一份 RSS 或首頁文章清單。

- `posts` 每筆含 `topic`（不含目錄的 topic 檔名）、`url`（本站正式絕對 URL）、`published`（YYYY-MM-DD）、`date_basis`（可核對的來源日期或新增 commit 與說明）。topic 必須存在且掛入 `hi.tree`。
- H1 與 `web-summary` 優先提供標題與摘要；舊文缺少 `web-summary` 才用清單中的 `summary`。新增文章仍依正常寫作規則提供 `web-summary`。
- 發布日期優先採原文日期；採 Git 首次新增紀錄前，排除搬站、改名、批次匯入造成的假日期。不以檔案修改時間或部署時間替代。無法確認時暫緩登錄，不偽造日期。
- `featured` 依陣列順序列出目前 3 篇已登錄文章；這是現行程式約束，若使用者要調整數量需一併改驗證與測試。
- `updated` 與 `update_summary` 成對填寫，僅用於作者明確標記的重大更新；日期不能早於發布日，也不能在未來。修字不改發布日期。
- `excluded` 以 topic 檔名對應排除理由，適用分類、索引、維護或其他不收錄文章。不要為了通過 CI 而任意排除正式新文。
- `registration_baseline` 固定為首次導入前的 commit。`check` 比對此後新增與未追蹤的 Markdown topics，要求登錄或排除；導入前舊文可逐步補齊，不可向前移動 baseline 跳過檢查。

正式 URL 必須核對，不能只將檔名換成 `.html`：Writerside 可能正規化大小寫與底線。已發布文章用線上 sitemap／頁面 `og:url` 核對；尚未發布的新文用建置產物核對。既有 URL 也是 RSS GUID，改名需處理轉址與訂閱身分影響。

## 生成內容與日常命令

- `Default.md` 保留人工維護的介紹與作者連結，只重建 `<!-- publications:start -->` 至 `<!-- publications:end -->` 區塊。
- `recent-posts.md` 全檔由程式生成，按年份分組、每 10 篇拆段，避免搜尋索引單段過大；保留尚未涵蓋所有歷史文章的說明。
- 首頁列最新 10 篇、精選與主題入口；重大更新依更新日期列最多 5 篇，空資料時隱藏。
- 新文依發布日降冪，同日依 topic 檔名固定排序。

```bash
npm run publications:generate
npm run publications:check
```

先更新來源 topic／JSON，再生成；把清單、來源文章、首頁與近期索引的必要差異一起納入此次變更。改 H1 或摘要也要重建，即使日期沒變。

`check` 需要包含 baseline 的 Git 歷史；CI build 使用完整 checkout。若 shallow checkout 缺歷史，補齊歷史，不修改 baseline。

## RSS 與部署

- 公開端點為 `https://jakeuj.com/feed.xml`，RSS 2.0，取最近 20 篇的標題、摘要、連結、GUID 與 pubDate；不是全文 feed。
- 日期以 Asia/Taipei 解讀，只有日期時輸出當日 00:00 +08:00。GUID 為已確認公開 URL；不為重大更新新增項目或重設發布日。
- 第一次訂閱包含清單中的歷史文章，保留原始日期；舊文修字仍可能改變摘要文字，但不改排序或 GUID。
- 建置前檢查生成同步與功能測試；Writerside build／checker 通過後，deploy 在解壓與既有 SEO 處理完成後執行：

```bash
python3 scripts/publication.py publish --site <解壓網站目錄>
```

這個命令只修改本地產物，不自行上傳網站。它驗證清單對應 HTML 的 `og:url`；已有 canonical 必須吻合，缺少則補上。通過後生成 feed，並為帶有 head 的 HTML 加入單一 RSS 自動探索標籤。正式發布仍走既有 Pages 與 Algolia 流程，依當前任務授權執行。

## 驗證重點

- 一般文章更新跑 generate、check 及受影響 Markdown 檢查；改產生器或發布流程時，再跑 `npm run publications:test`、`npm run pre-deploy` 與實際 Writerside build／checker。
- 測試發布日期、同日排序、重複 URL、缺少文章／摘要、失效連結、XML 特殊字元、20 篇上限、固定 GUID、重大更新不重新推送、生成結果同步與新文漏登錄。
- 網址不符或生成不同步時修資料來源，不移除檢查或直接手改產物掩蓋錯誤。
- 發布後檢查首頁、recent-posts.html、feed.xml、抽樣文章與站內搜尋；RSS 要用閱讀器實際抓取，確認日期和文章數，不只檢查 HTTP 200。
- 首頁或排版變更時檢視桌面與手機，確認入口連結、RSS 探索標籤與橫向溢出。閱讀器驗證可用已有工具或暫存環境，不固定要求某套軟體。
