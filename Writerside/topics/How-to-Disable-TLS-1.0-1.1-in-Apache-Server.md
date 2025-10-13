# How to Disable TLS 1.0 /1.1 in Apache Server

> **原文發布日期:** 2022-06-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/06/20/DisableTls1011
> **標籤:** 無

---

筆記一下禁用 TLS 1.0 與 1.1

結論

Apche

sudo vi /etc/apache2/httpd.conf

```
#   SSL Protocol support:
# List the enable protocol levels with which clients will be able to
# connect.  Disable SSLv2 access by default:
SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
```

Windows

[Nartac Software - IIS Crypto](https://www.nartac.com/Products/IISCrypto/)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/09b94ce6-dd1e-4590-865d-0d5a2b049cbd/1655716824.png.png)

參照

[How to Disable TLS 1.0 /1.1 in Apache Server - Fedingo](https://fedingo.com/how-to-disable-tls-1-0-1-1-in-apache/)

延伸閱讀

[Azure VPN Windows Server 2012 R2 Error 812 | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2022/06/15/AzureVpnWindowsServer2012R2Error812)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Apache](/jakeuj/Tags?qq=Apache)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
