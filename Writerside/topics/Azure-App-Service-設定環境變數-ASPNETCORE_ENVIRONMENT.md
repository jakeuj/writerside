# Azure App Service 設定環境變數 ASPNETCORE_ENVIRONMENT

> **原文發布日期:** 2022-04-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/04/20/AzureAppServiceASPNETCORE_ENVIRONMENT
> **標籤:** 無

---

ASPNETCORE\_ENVIRONMENT=staging

## 結論

ASPNETCORE\_ENVIRONMENT=staging

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/41e83032-0b77-427c-9343-72ddff238994/1650450041.png.png)

ASPNETCORE\_ENVIRONMENT=staging

## 補充

如果要複寫appsetting.json的設定，則需要在階層處加上"雙"底線 **\_\_**

例如

```
{
  app:{
    url:"localhost"
  }
}
```

則設定如下

`app__url=staging.domain.com`

## 參照

[使用 Azure 應用服務和 ASP.NET 核心|進行配置elmah.io](https://blog.elmah.io/configuration-with-azure-app-services-and-aspnetcore/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [.Net Core](/jakeuj/Tags?qq=.Net%20Core)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
