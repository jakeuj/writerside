# ABP.IO 6.0.0 Publish Azure App Service 503 OpenIddict Exception

> **原文發布日期:** 2022-10-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/13/OpenIddict-WindowsCryptographicException-Access-is-denied
> **標籤:** 無

---

CryptographicException: Access is denied

## 結論

組態中新增以下設定

`WEBSITE_LOAD_USER_PROFILE=1`

[在程式碼中使用 TLS/SSL 憑證 - Azure App Service | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/app-service/configure-ssl-certificate-in-code#load-certificate-from-file)

### 症狀

發布後網站開不起來顯示 503

查看 Log 後程式死在 OpenIddict

堆疊顯示以下錯誤訊息

```
WindowsCryptographicException: Access is denied.
```

### 參照

[c# - Windows 加密異常：在 Azure 中發佈應用時拒絕存取 - 堆疊溢出 (stackoverflow.com)](https://stackoverflow.com/questions/67629592/windowscryptographicexception-access-is-denied-when-publishing-app-in-azure)

[OpenIddict WindowsCryptographicException: Access is denied #3537 | Support Center | ABP Commercial](https://support.abp.io/QA/Questions/3537/OpenIddict-WindowsCryptographicException-Access-is-denied)

[ABP.IO WEB應用程式框架 Azure App Service CI/CD deployment | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2022/10/21/abp-Azure-App-Service-Github-CICD)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)
* [App Service](/jakeuj/Tags?qq=App%20Service)
* [Azure](/jakeuj/Tags?qq=Azure)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
