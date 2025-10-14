# Azure App Service Web Job

> **原文發布日期:** 2022-03-03
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/03/03/Azure-App-Service-Web-Job-PowerShell-API
> **標籤:** 無

---

本文說明如何在 Azure App Service 使用 Web Job 定期執行 PowerShell 腳本來呼叫 API。

應注意而未注意的事情

結論

```
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12
Invoke-RestMethod -uri "https://test.azurewebsites.net/?a=1&b=2"
```

問題

1. 如果 uri 有 & 則需要使用雙引號包起來
2. 放上去執行出現錯誤：PowerShell –
   The underlying connection was closed: An unexpected error occurred on a send.
   需要加上第一行來使 PS 使用 TLS 1.2

參照

[The underlying connection was closed: An unexpected error occurred on a send](https://blog.darrenjrobinson.com/powershell-the-underlying-connection-was-closed-an-unexpected-error-occurred-on-a-send/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* App Service
{ignore-vars="true"}
* Azure
* PowerShell

* 回首頁

---

*本文章從點部落遷移至 Writerside*
