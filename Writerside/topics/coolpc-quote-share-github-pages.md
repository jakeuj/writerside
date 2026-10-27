# 用 GitHub Actions 抓原價屋報價，做成可分享估價單的靜態網站

<web-summary>用 Python 標準函式庫每小時抓原價屋含稅報價、GitHub Actions 只在價格變動時 commit，再以純靜態 GitHub Pages 做可換零件的估價網站；整張估價單壓縮進網址 hash 分享，附 Big5 解碼、品名對照、價格歷史與帶單回原價屋的做法與坑。</web-summary>

想做一個「免登入、不用伺服器、連結就是估價單」的配電腦網站，最省事的組合是：GitHub Actions 定時抓原價屋估價頁並解析成 JSON，GitHub Pages 放純靜態網頁，分享時把整張單（分類、品名、當時價格、日期）壓縮後寫進網址 `#` 後面。以下以 [原價屋估價單分享](https://pc.jakeuj.com/)（[原始碼](https://github.com/jakeuj/architect-pc-builder)）為例，整理做法與實際踩到的坑。

<tldr>
<p>抓價：每小時 <code>fetch_coolpc.py</code> 抓 Big5 頁面解析成 JSON，<code>git diff --cached --quiet</code> 有變才 commit</p>
<p>分享：估價單快照用 deflate-raw 壓縮後 base64url 放進 <code>#v=1&amp;q=</code>，字首代表編碼版本，舊連結永遠能開</p>
<p>對照：原價屋的選項 id 會變，一律用「分類 + 品名」對照，品名消失時再退回同型號</p>
</tldr>

以下內容整理於 2026 年 10 月；原價屋頁面結構隨時可能改版，實作細節以 repo 現況為準。這是個人工具，不是原價屋官方網站。

## 整體架構 {#architecture}

整個網站沒有後端，資料流只有三段：

1. **抓價**：`fetch_coolpc.py` 下載 `https://www.coolpc.com.tw/evaluate.php`，交給 `parse_coolpc.py` 解析成 `data/coolpc_prices.json`（30 個分類 → 群組 → 商品）。
2. **產生網頁資料**：`build_site.py` 依 `site.json` 與 `builds/*.json`（預設配置）輸出三個檔：
   - `docs/data.json`：主機相關 11 個分類與預設配置，首頁一定載入。
   - `docs/data-more.json`：其他分類（螢幕、鍵鼠、作業系統…），切到「全部分類」才載入。
   - `docs/history.json`：主機零件的價格變動紀錄。
3. **前端**：`docs/index.html` 加 `builder-ui.js`、`builder.css`，原生 HTML／CSS／JavaScript，不需要 build 工具。

所有腳本只用 Python 3 標準函式庫，CI 不必 `pip install`。

## 抓價與解析 {#fetch-and-parse}

### Big5 解碼要有 fallback {#big5-decode}

原價屋估價頁回傳 Big5。用 `cp950` 解大部分沒問題，但頁面偶爾混進香港增補字（例如 `0xFB40`），整頁 `decode()` 直接丟例外，排程就會連續失敗。

解法是逐字退回 `big5hkscs`（行為與瀏覽器的 `TextDecoder('big5')` 一致），真的解不出來才換成 `�`，並把字數印到 stderr，排程不中斷。

另外送 `Accept-Encoding: gzip` 可以把每次傳輸從約 1.06MB 降到約 220KB；`urllib` 不會自動解壓，要自己看 `Content-Encoding` 再 `gzip.decompress()`。

### 估價頁的資料結構 {#evaluate-page-structure}

每個分類是一個 `<SELECT name=nN>`，商品是 `<OPTION value=N>品名, $價格[↘$下殺價] 符號</OPTION>`。解析時要注意：

- `disabled` 的 OPTION 是說明列（活動、續行），不是商品。
- 活動說明或運送提醒偶爾被寫成一般 OPTION、標價 `$1`，解析時略過標價 ≤ $1 的列。
- 驗證方式：各分類解析出的商品數，應等於該分類第一列「共有商品 N 樣」減去略過的 `$1` 說明列。
- 品名裡的「搭板專案」、「組裝價」、「任搭折N」等是條件價，解析成 `flags`，前端再提示使用條件。

## GitHub Actions 只在價格變動時 commit {#scheduled-workflow}

workflow 每小時 `:30` 抓一次，重新產出資料後，**只有內容真的變了才 commit**（以下為節錄，省略產生估價單 Markdown 的步驟）：

```yaml
on:
  schedule:
    - cron: "30 * * * *"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 .claude/skills/coolpc/scripts/fetch_coolpc.py --out .
      - run: python3 .claude/skills/coolpc/scripts/build_site.py
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add -A -- data docs quote.md
          if git diff --cached --quiet; then
            echo "報價無變化"
          else
            git commit -m "更新原價屋報價"
            git push
          fi
```

幾個要點：

- **先 `git add -A` 再比 staged**。不要寫成 `git diff --quiet -- <檔案>`，它看不到第一次產生、還沒追蹤的新檔。
- **輸出要 deterministic**。內容沒變時 `build_site.py` 沿用上次的 `generated` 時間戳，`history.json` 的 key 排序且不放時間戳，才不會每小時產生空 commit。
- **時區**：runner 是 UTC，時間戳在 Python 裡用 `ZoneInfo("Asia/Taipei")` 產生。
- **測試 workflow 要排除資料 commit**：`test.yml` 的 `paths-ignore` 加上 `data/**`、`docs/data.json`、`docs/history.json` 等，機器人的報價 commit 才不會觸發測試。

### 排程不準時 {#schedule-delay}

GitHub 的 `schedule` 只是排進佇列。實測 2026 年 9 月每天 03:30 UTC 的排程，實際在 08:11 到 10:01 UTC 才開跑，晚了 4.7 到 6.5 小時，還有一天整次被跳過。

所以「每小時更新」實際上可能是一天幾次。網頁上方要標出報價日期，快照超過 24 小時沒更新另外提示，不要對使用者承諾準時。

public repo 使用標準 runner 不計 Actions 分鐘數，每次約 10 到 25 秒；private repo 每小時跑一次約 720 分鐘／月，會吃掉免費方案大半額度。

## 分享連結就是估價單 {#share-link}

分享時把估價單快照（每列分類、品名、當時價格，加上報價日期）序列化成 JSON，壓縮後放在網址 hash：

| 連結 | 打開後 |
| --- | --- |
| `#v=1&q=<資料>` | 唯讀估價單（可列印、存 PDF、帶 QR Code） |
| `#q=<資料>` | 直接進編輯畫面 |

hash 不會送到伺服器，所以估價單完全不經過任何後端；GitHub Pages 換網域做 301 時，瀏覽器也會帶著 `#` 後面的內容，舊分享連結不會壞。

### 用字首標記編碼版本 {#share-link-versioning}

`q` 的第一個字元是**編碼方式**，不是資料格式版本：

- `1`：`base64url(JSON)`
- `2`：`base64url(deflate-raw(JSON))`，用瀏覽器內建的 `CompressionStream`

規則是解碼端永遠同時支援 `1` 與 `2`，新欄位直接加在 JSON 裡（舊版網頁會忽略不認得的鍵），不為新欄位升版。實測 8 列主機單從 1,243 字元壓到 1,028 字元；中文品名不太好壓，加購的其他商品越多省得越多。

實作時要注意：

- **不能只檢查 `CompressionStream` 存不存在**。部分舊版 Chromium 有這個類別但不支援 `deflate-raw`，要實際試建一次，失敗就退回 `1`。
- **解壓後限制大小**（例如 256KB），避免壓縮炸彈。
- **編碼變成 async 之後，剪貼簿要改寫法**。Safari 在離開使用者手勢後不讓寫剪貼簿，先把壓縮結果快取起來；拿不到時把 promise 交給 `ClipboardItem`，不要 `await` 完再呼叫 `writeText()`。
- Node 端要用到 `deflate-raw` 需 Node 20.12 以上。

### 打開舊連結時跟現價比 {#compare-with-current-price}

打開分享連結時一定先還原當初的內容，再跟目前的報價逐列對照，列出「分享時 → 現在」的漲跌、合計差與已下架品項。改過的列改用現價，沒改的列保留原報價，並另外列出「跟分享時比換了哪幾格」。

## 用品名對照，不用選項 id {#match-by-name}

原價屋選項的 `value` 只是清單位置，每次更新都可能變。估價單、預設配置與分享連結一律用「分類 + 品名」當鍵；原價屋自己的手機查價清單與帶單功能也是用品名當商品鍵。

品名對不到時還要再判斷一次：

- 品名開頭的「搭板專案」、「裝機價」等條件價結束後，品名會變，但 `｛…｝` 裡的型號不變。這種情況標「優惠已結束」，跟同型號現價比，不算下架。
- 同型號也找不到，才標「已下架」，並保留最後的品名與價格讓使用者改選。
- 預設配置的零件下架時，排程不能失敗：估價單標「已下架」不計價，網頁沿用上一版資料，再由人工找替代品。

## 價格歷史 {#price-history}

每個零件旁的「30 天最低／最高」與迷你折線，來自 `docs/history.json`。設計重點：

- key 是「分類 id + 型號」，型號取品名 `｛…｝` 內的文字；搭板、組裝價這類條件價另外加一段條件碼分開記，一般件的「30 天最低」才不會是搭板價。
- 同型號有多款（代理、平輸）時取最低價，網頁標「同型號最低款」。
- 只在價格變動時追加，同一天只留最新一筆，保留 90 天。
- 上一版檔案壞掉或格式不對就從頭記，並在 stderr 提示，不讓排程失敗。
- 既有網站第一次啟用時，從 `git log -- data/coolpc_prices.json` 依序回填（淺 clone 要先 `git fetch --unshallow`）。實際回填 42 次快照，得到 2,761 個 key（其中 162 個是條件價件）、約 158KB。

前端與 Python 的型號與條件 regex 必須完全一致，否則前端查不到 key；這類「兩邊各寫一份」的規則要用測試釘住。

## 帶單回原價屋估價頁 {#send-to-coolpc}

配好後可以在新分頁開啟原價屋官方估價頁，品項與數量已預先選好。原價屋接受 POST：

- `iname` = `<>品名1<>品名2…`，`icnt` = `<>數量1<>數量2…`
- 表單要用 **Big5 編碼**送出：前端臨時建立 `<form method="post" accept-charset="big5" target="_blank">` 再 `submit()`。
- 不需要 cookie 或 session；對不到的品名會被直接略過、不報錯，所以送出前先提醒已下架的列。

這只是開啟估價頁，不會下單。原價屋另有會送出 Email、手機或地址的頁面，網站一律不串。

驗收時要注意：部分 App 內建的瀏覽器面板會把 `target="_blank"` 改成同分頁 GET，POST 內容會遺失，看起來像功能壞掉；請用一般瀏覽器確認。

## 店家模式：用原價屋報價開自家估價單 {#store-mode}

電腦店老闆或業務可以開[店家模式](https://pc.jakeuj.com/#store)幫客人報價：估價單抬頭換成店名與聯絡方式，以原價屋合計為基準填一個本店價、加組裝費等服務，也能隱藏原價屋單價，再複製一段含本店合計與連結的訊息傳給客人。整套仍然沒有後端，店家資料存在自己的瀏覽器，報價跟著分享連結走。

### 資料放在哪 {#store-mode-data}

| 資料 | 存放位置 | 內容 |
| --- | --- | --- |
| 店家資訊 | 這台裝置的 `localStorage` | 店名、業務、電話、LINE ID、地址、標語 |
| 店家報價 | 每個分頁各一份，分享時寫進連結 | 本店價、服務列（最多 8 列）、客戶稱呼、有效期限、備註、是否隱藏原價屋單價 |

分享連結不升版，只在 JSON 加選用欄位：`s`（店家資訊）、`p`（`[本店價, 填價時的原價屋合計]`）、`x`（服務列）、`c`（客戶）、`u`（有效期限）、`m`（備註）、`h`（隱藏）。店家資訊存成固定順序的陣列，尾端空字串省略，連結短一點。

重點是**沒有店家資料時，編碼結果跟改版前逐字相同**，用測試釘住；舊版網頁打開店家連結，只會當成一般分享單顯示，不會報錯。

### 連結內容一律當成不可信 {#store-mode-validation}

分享連結任何人都能捏造，店家欄位又會顯示在估價單抬頭、變成撥號與 LINE 連結，所以解碼時逐欄清理與驗證，不合格只丟該欄：

- 先移除控制字元、零寬字元與 bidi 控制字元，再檢查長度（例如店名 30 字、地址 60 字、備註 200 字）；超長整欄丟棄，不截斷。
- 電話只收數字、`+-()#` 與空白，且至少 6 碼；LINE ID 限 `@?[a-z0-9._-]{3,20}`。
- 店名含「原價屋」或 `coolpc` 一律不收，避免冒用；沒有店名就不算店家單。
- 金額必須是範圍內的整數，服務列可以是負數（折抵），$0 顯示「免費」；有效期限必須是真實存在的 `YYYY-MM-DD`。
- `tel:` 與 `https://line.me/...` 的網址只由同一個函式產生，值不合格就不出連結。

驗收時把 `<svg onload>`、`<img onerror>` 放進店名、品名、服務名稱、客戶、備註等每個欄位，確認都只顯示成文字（包含分頁標題），沒有執行。

### 本店價要能察覺過期 {#store-mode-stale-price}

本店價是整單一個價，不逐項填。填價時同時記下當下的原價屋合計，之後只要合計對不上，就代表零件或價格變了（以下為省略欄位驗證的簡化版）：

```javascript
// quoted = 目前的原價屋合計；biz.ref = 填本店價時的原價屋合計
function bizTotals(quoted, biz) {
  const extras = (biz.extras || []).reduce((sum, e) => sum + e[1], 0);
  const has = biz.price != null;
  return {
    stale: has && biz.ref !== quoted,            // 需重新確認
    final: (has ? biz.price : quoted) + extras,  // 本店合計
    save: has ? quoted - biz.price : 0,          // 比原價屋合計省多少
  };
}
```

改零件、改數量或全部改用現價後標「需重新確認」，店家按「保留本店價」可以解除，改回原本的配置會自動解除。客人改過零件再分享回來，估價單上顯示「本店價（需向店家確認）」。

### 誰能改這張單 {#store-mode-ownership}

「同一家店」用正規化後的店名判斷，不分大小寫、全半形與空白。

- **自己的單**：店家模式開著，而且這張單沒有店家或就是本店，可以編輯。店家打開客人自己配的一般分享單再轉傳，會帶上自己的店家資訊。
- **別家店的單**：唯讀；店家模式開著時可以按「改用本店報價」，改成自己的單。
- **客人**（本機沒有店家資料）：唯讀，沒有「帶到原價屋估價頁」按鈕，改提供「複製零件清單」。

### 唯讀估價單的店家版 {#store-mode-readonly}

- 抬頭是店家區塊：手機點電話直接撥號、點 LINE 加好友；另列客戶稱呼與有效期限，過期會標示。
- 合計依序列出原價屋合計、本店價、服務列、本店合計。
- 拿掉原價屋專屬的漲跌 ▲▼、下架、條件標籤、任搭折與帶單按鈕。
- 隱藏模式只剩項目、品名、數量欄，整頁不出現任何原價屋金額。
- 保留「由網站產生」的小字與店家版聲明，不假裝是店家自己的系統。

### 店家設定連結 {#store-mode-settings-link}

老闆設定一次，用「店家設定連結」把店家資訊傳給同事，格式是 `?openExternalBrowser=1#s=1<base64url(JSON)>`：

- 連結**不含業務姓名**。打開時先跳出設定對話框、標出會被取代的欄位，保留這台裝置原本的業務姓名，按「儲存」才套用，取消不改任何資料。
- `openExternalBrowser=1` 是給在 LINE 裡點開的情況，讓 LINE 內建瀏覽器改用外部瀏覽器開啟；這點還沒在實機驗證。
- 估價單的分享網址只帶 `#`，不帶 `?` 後面的參數，設定連結的參數不會跟著估價單傳出去。

### 驗收重點 {#store-mode-verification}

- 店家模式關閉時，估價單、摘要與分享連結都跟改版前相同。
- 輸入本店價與備註時，畫面重畫後輸入框要保留值與游標。網址同步（`history.replaceState`）加上 400ms 延遲與 `try/catch`，避免 Safari 限制呼叫頻率時報錯；Safari 注音輸入尚未實測。
- 1440、1024、768、390px 都沒有水平溢出，手機上的撥號、LINE 與勾選框至少 44px；列印或存 PDF 是白底、沒有按鈕，合計區不跨頁。

## 想要即時報價得加 CORS 代理 {#live-price-proxy}

原價屋沒有開 CORS，網頁不能直接 `fetch()` 估價頁。repo 裡準備了 Cloudflare Worker 代理（原樣轉送 Big5 頁面、加 CORS header、邊緣快取 5 分鐘），再用 `parse_coolpc.py` 的 JavaScript 版在瀏覽器解析。

目前網站沒有啟用，價格只靠 workflow 快照。若要啟用，兩份解析器要一起改，並用同一份頁面驗證兩邊輸出的 JSON 完全相同。

## 其他自動化與測試 {#automation-and-tests}

- **追蹤配單來源**：預設配置照公開的每月組裝建議文章配。另一個每日 workflow 抓文章的菜單段落，跟上次存檔比對；菜單有變就開 Issue 附差異，同標題 Issue 還開著就改成留言，人工收到後再重配。整套不用 AI。
- **測試**：push／PR 時跑 Node 與 Python 測試，並比對網站與模板的介面檔是否一致。
- **Node 22 的 `node --test` 不接受目錄參數**，CI 要用 glob：

```bash
node --test '.claude/skills/coolpc/tests/*.test.js'
python3 -m unittest discover -s .claude/skills/coolpc/tests
```

## 本機試跑 {#run-locally}

```bash
git clone https://github.com/jakeuj/architect-pc-builder.git
cd architect-pc-builder
python3 .claude/skills/coolpc/scripts/fetch_coolpc.py --out .
python3 .claude/skills/coolpc/scripts/search_coolpc.py 12 'RTX5060'
python3 .claude/skills/coolpc/scripts/build_site.py
python3 -m http.server 8765 --directory docs
```

瀏覽 `http://localhost:8765/` 即可預覽。要另做一個網站（例如某款遊戲專用的配單站），在新目錄跑 `build_site.py --init` 會複製腳本與網頁骨架，再改 `site.json` 與 `builds/*.json`。

## 參考資料 {#references}

- [原價屋估價單分享](https://pc.jakeuj.com/)
- [jakeuj/architect-pc-builder](https://github.com/jakeuj/architect-pc-builder)
- [原價屋線上估價](https://www.coolpc.com.tw/evaluate.php)
- [Compression Streams API（MDN）](https://developer.mozilla.org/en-US/docs/Web/API/Compression_Streams_API)
- [Events that trigger workflows: schedule（GitHub Docs）](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [用 graphify 把 repo 做成知識圖，發布到 GitHub Pages](graphify-knowledge-graph-github-pages.md)
- [Side Projects](Side-Projects.md)
