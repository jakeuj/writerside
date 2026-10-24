# AdGuard 不過濾 localhost：User rules 的 $document 例外規則（Mac／Windows）

<web-summary>在 AdGuard 的 User rules 加入 @@||localhost^$document、@@||127.0.0.1^$document，Windows 再補 @@|http://127.0.0.1:$document，讓本機開發網站在任何 port 都不被封鎖、隱藏元素或改寫 HTML。</web-summary>

要讓 `localhost:port/xxxx` 這類本機開發網站不被 AdGuard 過濾，到 AdGuard 的 User rules（Windows 版介面為「使用者規則」）加入下面的例外規則，確認規則與 User rules 都已勾選，再回瀏覽器強制重新整理。AdGuard for Windows 實測時，只有 `||127.0.0.1^` 的規則擋不住 HTML 改寫，要再加第三條 `|http://` 前綴規則才涵蓋所有 port。

```text
@@||localhost^$document
@@||127.0.0.1^$document
@@|http://127.0.0.1:$document
```

<tldr>
<ul>
<li>規則結尾一定要加 `$document`，才會讓整個頁面停用過濾。</li>
<li>Windows 用 IP 開本機站台時，補上 `@@|http://127.0.0.1:$document`，涵蓋任何 port。</li>
<li>確認有沒有被改寫：檢視原始碼搜尋 `local.adguard.org`。</li>
</ul>
</tldr>

## 加入例外規則 {#add-user-rules}

AdGuard for Mac：

1. 開啟 AdGuard 設定，切換到「過濾器」分頁。
2. 在左側清單選取「User rules」，確認前方核取方塊已勾選；沒勾選時，裡面的規則都不會生效。
3. 在右側規則清單下方按「＋」，新增一列並輸入 `@@||localhost^$document`。
4. 依同樣方式加入 `@@||127.0.0.1^$document` 與 `@@|http://127.0.0.1:$document`。
5. 確認每條規則前方都已勾選。清單最下方若多出未勾選的空白列，可以忽略，或選取後按「−」刪除。
6. 回到瀏覽器按 `⌘⇧R` 強制重新整理本機網站。

AdGuard for Windows 的位置在「過濾器編輯器」左側的「自訂的過濾器 → 使用者規則」，同樣在右側按「＋」逐條加入並勾選，回瀏覽器按 `Ctrl+Shift+R` 重新整理。

## Windows 實測：||127.0.0.1^ 擋不住 HTML 改寫 {#windows-ip-rule-gap}

在 AdGuard for Windows 上，User rules 已有 `@@||127.0.0.1^$document` 與 `@@||localhost^$document`，本機用 Node 在隨機 port 啟動 HTTP 伺服器提供 `index.html`，抓回來的內容和原檔仍然不同：

- 頁面原本的 `Content-Security-Policy` meta 被換成 AdGuard 的版本，裡面多了 `local.adguard.org` 的來源。
- 瀏覽器導覽頁面、頁面內 `fetch()`、Node 的 `fetch()` 抓到的內容都被改寫，不只頁面導覽。
- 每次抓回來的大小都不太一樣，代表注入內容會變動。

同時期只放行單一 port 的 `@@|http://127.0.0.1:8942/$document` 是有效的：那個 port 上每一種請求都回傳原檔。把這條改成不含 port 的前綴 `@@|http://127.0.0.1:$document` 之後，隨機 port 也不再被改寫。這個差異的原因沒有在官方文件找到說明；`@@||localhost^$document` 在 Windows 上是否同樣失效，這次沒有測試。

HTML 被改寫時最明顯的副作用是 PWA：Service Worker 安裝時會比對資產雜湊，`index.html` 的雜湊對不上，離線快取就裝不起來，頁面顯示類似「離線準備失敗」的訊息。用 Subresource Integrity 或自行比對檔案雜湊的流程，也會出現同樣的不一致。

## 依範圍選擇規則 {#choose-rule-scope}

只想放行特定 dev server 時，可以把 port 或路徑寫進規則；`3000`、`/admin` 換成實際值：

- 所有 port 與路徑：`@@||localhost^$document`
- 用 IP 開啟的所有 port 與路徑：`@@||127.0.0.1^$document`
- 用 IP 開啟的所有 port（Windows 實測有效的寫法）：`@@|http://127.0.0.1:$document`
- 只放行一個 port：`@@||localhost:3000^$document`，或 `@@|http://127.0.0.1:3000/$document`
- 只放行某個路徑底下的頁面：`@@||localhost:3000/admin^$document`

本機開發通常會頻繁更換 port，用不含 port 的規則最省事。

## 規則語法說明 {#rule-syntax}

- `@@`：例外規則的標記，表示放行而不是封鎖。
- `||`：從網域開頭比對，同時套用到子網域，所以 `app.localhost` 也會被涵蓋。
- `|`：放在規則開頭時，表示網址必須從這段文字開始。`|http://127.0.0.1:` 會比對所有以這段開頭的網址，也就是任何 port。
- `^`：分隔字元。字母、數字與 `_`、`-`、`.`、`%` 以外的字元都算分隔字元，包含 `:`、`/`、`?`，網址結尾也算；因此 `localhost^` 後面接任何 port 都能比對。
- `$document`：用在例外規則時，等同同時套用 `$elemhide`、`$content`、`$urlblock`、`$jsinject`、`$extension`，也就是整頁不封鎖請求、不套用元素隱藏與內容過濾，也不注入 JavaScript 與 userscript。

如果只寫 `@@||localhost^` 而沒有 `$document`，只會放行送往 localhost 的請求；頁面載入的第三方資源仍可能被封鎖，元素隱藏規則也仍會作用，畫面看起來還是像被過濾。

## 驗證方式 {#verify}

1. 強制重新整理本機網站，確認原本被擋的資源或區塊已恢復。
2. 檢視頁面原始碼（Windows 按 `Ctrl+U`），搜尋 `local.adguard.org`。找得到就代表 HTML 仍被 AdGuard 改寫，例外規則沒有套用到這個網址。
3. 需要精確判斷時，把伺服器回傳的內容和磁碟上的原檔比對位元組或 SHA-256；兩者相同才算完全沒被改寫。
4. 若仍異常，開啟 AdGuard 的過濾記錄（Filtering log），重新整理頁面後查看哪些請求被處理、套用了哪條規則。
5. 回頭檢查規則是否打錯字、規則與 User rules 是否都已勾選。

## 其他做法 {#alternatives}

- **AdGuard 瀏覽器助理**：在本機網站開啟 AdGuard 助理，關閉這個網站的過濾開關，AdGuard 會自動在 User rules 新增對應的 `$document` 例外規則。這種做法只會加入當下的網域，不會同時處理 `127.0.0.1`。
- **測試固定 port**：自動化測試若無法調整過濾器，可以讓測試伺服器用固定 port，並只放行那個 port，例如 `@@|http://127.0.0.1:8942/$document`。缺點是 port 被占用時測試會直接失敗。
- **測試開跑前先檢查**：在測試啟動前，用同一個 port 提供一次 HTML 並和原檔比對，不一致就停下並提示改 port 或加例外，避免整批測試跑完才看到一堆不明原因的失敗。
- **HTTPS 本機站台**：若 dev server 使用自簽憑證的 HTTPS，加了例外規則後仍出現憑證或連線錯誤，可到 AdGuard 設定的「網路」分頁，在 HTTPS 過濾的排除清單加入 `localhost`，讓 AdGuard 不解密這個網站的流量。

## 參考資料

- [AdGuard Knowledge Base：How to create your own ad filters](https://adguard.com/kb/general/ad-filtering/create-own-filters/)
