# 發布 Package 到自己的 Nuget Server

> **原文發布日期:** 2022-12-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/12/19/dotnet-nuget-push-Package-Nuget-Server
> **標籤:** 無

---

筆記下指令

Example

dotnet pack

dotnet nuget push YourLib.1.1.1.nupkg --api-key YourApiKey --source <https://your-nuget-server.azurewebsites.net/v3/index.json>

Ref

[連線到摘要併發布 NuGet 套件 - NuGet.exe - Azure Artifacts | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/devops/artifacts/nuget/publish?view=azure-devops#publish-packages-from-external-sources)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [NuGet](/jakeuj/Tags?qq=NuGet)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
