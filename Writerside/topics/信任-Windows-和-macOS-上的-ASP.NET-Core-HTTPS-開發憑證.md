# 信任 Windows 和 macOS 上的 ASP.NET Core HTTPS 開發憑證

> **原文發布日期:** 2021-01-05
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/01/05/certificate-not-trusted
> **標籤:** 無

---

dotnet 執行後發現 https 有問題

你的連線不是私人連線

NET::ERR\_CERT\_AUTHORITY\_INVALID

解決方法筆記

關閉瀏覽器(可能要停止原本執行的網站)

dotnet dev-certs https --clean

dotnet dev-certs https --trust

Done.

參考：[所有平臺-憑證不受信任](https://docs.microsoft.com/zh-tw/aspnet/core/security/enforcing-ssl?view=aspnetcore-3.1&tabs=visual-studio#all-platforms---certificate-not-trusted)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* .Net Core
{ignore-vars="true"}
* HTTPS
* SSL

* 回首頁

---

*本文章從點部落遷移至 Writerside*
