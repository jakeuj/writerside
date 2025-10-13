# Azure App Service 組態 Connection String 吃不到設定

> **原文發布日期:** 2021-02-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/02/23/AzureAppServiceConnectionString
> **標籤:** 無

---

日前新增了一個 App Service 然後把一個 .Net 3.5 的專案搬上去。
想說把連接字串移出 web.config 改由 Azure 組態裡面來設定，結果吃不到。
今天因緣際會把 3.5 升級到 4.8 忽然連不到資料庫，原來是終於吃到 Azure 的設定了。

![file](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6bf23d11-9482-4778-a5b5-9ea06e7779e3/1614050835.png)

# 結論

Azure App Service 連接字串 override 不支援 .Net 3.5，
需要升級專案到 .Net 4.x Runtime 才能由外部複寫連接字串設定值。

![file](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6bf23d11-9482-4778-a5b5-9ea06e7779e3/1614050817.png)

# Note

this magic is not available if you choose .NET 3.5 since it relies on functionality that only exists in .NET 4.5

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* .Net 3.5
{ignore-vars="true"}
* .Net 4.8
{ignore-vars="true"}
* App Service
{ignore-vars="true"}
* Azure
* Cloud

* 回首頁

---

*本文章從點部落遷移至 Writerside*
