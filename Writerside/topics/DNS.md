# Domain

使用自己的網域來設定 Github Page

## Doc

[官方文件](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

## Custom Domain

![page.png](page.png)

## DNS Configuration

[cloudflare](https://www.cloudflare.com/zh-tw/products/registrar/)

![dns.png](dns.png)

### ERR_TOO_MANY_REDIRECTS

如果設定 DNS 的時候啟用 Proxy 功能，會遇到`重新導向太多次`的問題。

即使已更新 DNS 設定來禁用 Proxy，EDGE 仍然可能會連到舊的 IP 位置，

最後需要關閉並清空 Socket 才會恢復正常。

- edge://net-internals/#sockets

- edge://net-internals/#dns

- edge://settings/siteData

#### 參考

[Edge: DNS Flush](https://techcommunity.microsoft.com/t5/discussions/edge-dns-flush/m-p/1131012)

![301.png](301.png)

![sockets.png](sockets.png)