---
name: writerside
description: 在這個 JetBrains Writerside 專案中撰寫新技術筆記、建立新的 `Writerside/topics/*.md` 文件、補一篇新教學、為新文章選檔名與標題、把新 topic 掛進 `Writerside/hi.tree`、加入 Writerside 語義標記與圖片時使用。遇到「幫我新增一篇筆記」、「寫一篇某技術的教學」、「建立新 topic」、「替某個問題補一篇新文章」這類需求時優先使用。
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
- 避免使用 `note.md`、`temp.md`、`test.md` 這類沒有辨識度的名稱。

可參考這類現有命名：

- `macOS-WiFi-DNS-設定筆記.md`
- `Jetbrains-Writerside-CICD-自動化部署-Markdown-到-GIthub-Pages.md`
- `Azure-App-Service-Deploy.md`

## 決定文章放在哪個分類

- 打開 `Writerside/hi.tree`，先找最接近主題的既有分類，再把新 topic 掛進去。
- 優先放在現有群組底下，不要沒有必要就新增新的頂層分類。
- 把新 topic 放在相近主題旁邊，不要只是機械式地加在檔案最後面。
- 只有在側欄標題需要更短、或想跟 H1 顯示名稱不同時，才加 `toc-title`。

常用格式：

```xml
<toc-element topic="my-topic.md"/>
<toc-element topic="my-topic.md" toc-title="較短的側欄名稱"/>
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

只在真的能改善閱讀體驗時才加入 Writerside XML 標記，不要為了用而用。

- 用 `<tabs>` 表示不同平台或不同工具版本的做法。
- 用 `<procedure>` 表示必須照順序執行的步驟。
- 用 `<note>`、`<tip>`、`<warning>`、`<caution>` 表示提醒與風險。
- 用 `<control>`、`<path>`、`<shortcut>` 標示 UI 名稱、路徑與快捷鍵。

範例：

````xml
<tabs>
    <tab title="macOS">

```bash
brew install example
```

    </tab>
    <tab title="Windows">

```powershell
winget install Example.Tool
```

    </tab>
</tabs>
````

注意事項：

- 在 XML 區塊和 Markdown 內容之間保留空行。
- 不要把 `<tab>` 內的 Markdown 內容縮排成巢狀列表。

## 處理圖片

- 把圖片放到 `Writerside/images/`。
- 在文章中用相對路徑引用，不要加 `images/` 前綴。
- 使用有意義的檔名，例如 `writerside-new-topic-dialog.png`。

範例：

```markdown
![新增 topic 對話框](writerside-new-topic-dialog.png)
```

## 避免搬用舊文遷移格式

- 只有真的從舊部落格搬文時，才保留「原文發布日期」、「原文連結」或「本文章從點部落遷移至 Writerside」這類區塊。
- 如果是全新筆記，不要憑空補這些欄位。

## 收尾驗證

- 先確認 `Writerside/hi.tree` 中的 `topic` 檔名和實際檔名完全一致。
- 先修新增那篇文章的 Markdown 格式，再做整體檢查。
- 如果只有單篇變更，優先跑單檔檢查；如果同時改了多篇，再跑專案腳本。

單檔修復與驗證：

```bash
npx markdownlint-cli2 --fix Writerside/topics/<topic-file>.md
npx markdownlint-cli2 Writerside/topics/<topic-file>.md
```

整體檢查：

```bash
./scripts/check-markdown.sh
```

## 需要更多上下文時再讀這些檔案

- `Writerside/hi.tree`: 查分類與 TOC 寫法。
- `.markdownlint.json`: 查 Markdown 規則。
- `scripts/check-markdown.sh`: 查專案實際使用的 lint 流程。
- `Writerside/topics/*.md`: 查相近主題的標題、段落與寫作習慣。
