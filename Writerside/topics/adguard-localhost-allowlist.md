# AdGuard for Mac 不過濾 localhost：在 User rules 加入 $document 例外規則

<web-summary>在 AdGuard for Mac 的 User rules 加入 @@||localhost^$document 與 @@||127.0.0.1^$document，讓本機開發網站在任何 port 與路徑都不會被 AdGuard 封鎖請求、隱藏元素或注入腳本。</web-summary>

要讓 `localhost:port/xxxx` 這類本機開發網站不被 AdGuard 過濾，到「AdGuard 設定 → 過濾器 → User rules」加入下面兩條例外規則，確認規則與 User rules 都已勾選，再回瀏覽器強制重新整理即可。這兩條會涵蓋所有 port 與路徑，不需要每換一個 dev server port 就加一條。

```text
@@||localhost^$document
@@||127.0.0.1^$document
```

<tldr>
<ul>
<li>規則結尾一定要加 `$document`，才會讓整個頁面停用過濾。</li>
<li>`||localhost^` 已涵蓋任何 port、路徑與 `*.localhost` 子網域。</li>
<li>加完規則後在瀏覽器按 `⌘⇧R` 強制重新整理。</li>
</ul>
</tldr>

## 加入例外規則 {#add-user-rules}

1. 開啟 AdGuard 設定，切換到「過濾器」分頁。
2. 在左側清單選取「User rules」，確認前方核取方塊已勾選；沒勾選時，裡面的規則都不會生效。
3. 在右側規則清單下方按「＋」，新增一列並輸入 `@@||localhost^$document`。
4. 再按一次「＋」，輸入 `@@||127.0.0.1^$document`。
5. 確認兩條規則前方都已勾選。清單最下方若多出未勾選的空白列，可以忽略，或選取後按「−」刪除。
6. 回到瀏覽器按 `⌘⇧R` 強制重新整理本機網站。

## 依範圍選擇規則 {#choose-rule-scope}

只想放行特定 dev server 時，可以把 port 或路徑寫進規則；`3000`、`/admin` 換成實際值：

- 所有 port 與路徑：`@@||localhost^$document`
- 用 IP 開啟的所有 port 與路徑：`@@||127.0.0.1^$document`
- 只放行一個 port：`@@||localhost:3000^$document`
- 只放行某個路徑底下的頁面：`@@||localhost:3000/admin^$document`

本機開發通常會頻繁更換 port，直接用不含 port 的前兩條最省事。

## 規則語法說明 {#rule-syntax}

- `@@`：例外規則的標記，表示放行而不是封鎖。
- `||`：從網域開頭比對，同時套用到子網域，所以 `app.localhost` 也會被涵蓋。
- `^`：分隔字元。字母、數字與 `_`、`-`、`.`、`%` 以外的字元都算分隔字元，包含 `:`、`/`、`?`，網址結尾也算；因此 `localhost^` 後面接任何 port 都能比對。
- `$document`：用在例外規則時，等同同時套用 `$elemhide`、`$content`、`$urlblock`、`$jsinject`、`$extension`，也就是整頁不封鎖請求、不套用元素隱藏與內容過濾，也不注入 JavaScript 與 userscript。

如果只寫 `@@||localhost^` 而沒有 `$document`，只會放行送往 localhost 的請求；頁面載入的第三方資源仍可能被封鎖，元素隱藏規則也仍會作用，畫面看起來還是像被過濾。

## 驗證方式 {#verify}

1. 在瀏覽器按 `⌘⇧R` 強制重新整理本機網站，確認原本被擋的資源或區塊已恢復。
2. 若仍異常，從選單列的 AdGuard 圖示開啟過濾記錄（Filtering log），重新整理頁面後查看哪些請求被封鎖、套用了哪條規則。
3. 回頭檢查規則是否打錯字、規則與 User rules 是否都已勾選。

## 其他做法 {#alternatives}

- **AdGuard 瀏覽器助理**：在本機網站開啟 AdGuard 助理，關閉這個網站的過濾開關，AdGuard 會自動在 User rules 新增對應的 `$document` 例外規則。這種做法只會加入當下的網域，不會同時處理 `127.0.0.1`。
- **HTTPS 本機站台**：若 dev server 使用自簽憑證的 HTTPS，加了例外規則後仍出現憑證或連線錯誤，可到 AdGuard 設定的「網路」分頁，在 HTTPS 過濾的排除清單加入 `localhost`，讓 AdGuard 不解密這個網站的流量。

## 參考資料

- [AdGuard Knowledge Base：How to create your own ad filters](https://adguard.com/kb/general/ad-filtering/create-own-filters/)
