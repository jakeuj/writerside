# Domain

使用自己的網域來設定 Github Page

## Doc

[官方文件](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

## Verify

[verifying-a-domain-for-your-user-site](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages#verifying-a-domain-for-your-user-site)

如果您沒有看到下述選項，請確保您位於 Profile settings （配置檔設置） 中，而不是 repository settings （倉庫設置） 中。

1. 在 GitHub 上任何頁面的右上角，按兩下您的個人資料照片，然後按兩下設置.
2. 在邊欄的“Code， planning， and automation（代碼、規劃和自動化）”部分中，按兩下頁面.
3. 在右側，按兩下 Add a domain（新增域）。
4. 在“What domain would you want to add？”下，輸入您要驗證的域，然後選擇 Add domain（添加域）。
用於為 GitHub Pages 網站添加已驗證域的欄位的螢幕截圖。該欄位下方會顯示一個綠色的 「Add domain」 按鈕。
5. 按照「添加 DNS TXT 記錄」 下的說明，使用您的域託管服務創建 TXT 記錄。
GitHub Pages 將 TXT 記錄添加到 example.com 的 DNS 配置的說明的螢幕截圖。
6. 等待您的 DNS 設定更改，這可能是立即更改，也可能最多需要 24 小時。您可以通過在命令列上運行命令來確認對 DNS 設定的變更。在下面的命令中，替換為您的使用者名和您正在驗證的域。如果您的 DNS 設定已更新，您應該會在輸出中看到新的 TXT 記錄。

`dig _github-pages-challenge-USERNAME.example.com +nostats +nocomments +nocmd TXT`

1. 確認 DNS 設定已更新後，您可以驗證域。如果更改未立即生效，並且您已離開上一頁，請按照前幾個步驟返回到 Pages 設置，然後在域右側按下 Continue verifying（繼續驗證）。
2. 要驗證您的域，請按兩下 Verify （驗證）。
3. 要確保您的自定義域保持驗證狀態，請將 TXT 記錄保留在域的 DNS 配置中。

## Custom Domain

![page.png](page.png){style="block"}

## DNS Configuration

[cloudflare](https://www.cloudflare.com/zh-tw/products/registrar/)

![dns.png](dns.png){style="block"}

### ERR_TOO_MANY_REDIRECTS

如果設定 DNS 的時候啟用 Proxy 功能，會遇到`重新導向太多次`的問題。

即使已更新 DNS 設定來禁用 Proxy，EDGE 仍然可能會連到舊的 IP 位置，

最後需要關閉並清空 Socket 才會恢復正常。

- edge://net-internals/#sockets

- edge://net-internals/#dns

- edge://settings/siteData

#### 參考

[Edge: DNS Flush](https://techcommunity.microsoft.com/t5/discussions/edge-dns-flush/m-p/1131012)

![301.png](301.png){style="block"}

![sockets.png](sockets.png){style="block"}
