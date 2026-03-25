---
name: writerside
description: 在這個 JetBrains Writerside 專案中撰寫或修改技術筆記、建立或更新 `Writerside/topics/*.md`、把 topic 掛進 `Writerside/hi.tree`、處理 Writerside 語義標記、圖片、Markdown 格式與 Writerside 特有的 anchor/TOC/checker 問題時使用。遇到「幫我新增一篇筆記」、「修改既有文章」、「補 topic 到 hi.tree」、「修 Writerside/Markdown 錯誤」、「處理 element id/anchor/TOC 問題」這類需求時優先使用。
---

# 撰寫新筆記

先把重點放在「產出一篇可發布的新文章」，不要先把注意力擴散到部署、站台設定或整站重構。

## 先確認新增目標

- 先到 `Writerside/topics/` 和 `Writerside/hi.tree` 搜尋是否已經有同主題文章，避免重複寫一篇只差措辭的新筆記。
- 先讀 1 到 2 篇同類型文章，模仿這個專案慣用的語氣與結構。
- 優先沿用繁體中文敘述，技術術語、CLI 指令、程式碼與設定鍵值保留英文。

## 決定檔名

- 在 `Writerside/topics/` 建立新檔案。
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

## 使用 Writerside 語義標記

- 用 `<tabs>` 表示不同平台或不同工具版本的做法。
- 用 `<procedure>` 表示必須照順序執行的步驟。
- 用 `<note>`、`<tip>`、`<warning>`、`<caution>` 表示提醒與風險。
- 用 `<control>`、`<path>`、`<shortcut>` 標示 UI 名稱、路徑與快捷鍵。
- 只在真的能改善閱讀體驗時才加入，不要為了用而用。
- 在 XML 區塊和 Markdown 內容之間保留空行。
- 不要把 `<tab>` 內的 Markdown 內容縮排成巢狀列表。

## 處理圖片

- 把圖片放到 `Writerside/images/`。
- 在文章中用相對路徑引用，不要加 `images/` 前綴。
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

- `Writerside/hi.tree`: 查分類與 TOC 寫法。
- `.markdownlint-cli2.jsonc`: 查 Markdown 規則。
- `scripts/check-markdown.sh`: 查專案實際使用的 lint 流程。
- `scripts/pre-deploy-check.sh`: 查本地部署前檢查流程。
- `.github/workflows/deploy.yml`: 查 CI 端的 Writerside build 與 checker 流程。
- `Writerside/topics/*.md`: 查相近主題的標題、段落與寫作習慣。
- `references/checker-errors.md`: 遇到 `MRK003`、anchor 衝突、圖片或 topic 路徑問題時讀。
- `references/validation-flow.md`: 要判斷單檔 lint、整體 lint、`pre-deploy` 與 CI checker 差異時讀。
- `references/build-deploy.md`: 使用者問 Writerside build、GitHub Actions、部署或 Algolia 時讀。
