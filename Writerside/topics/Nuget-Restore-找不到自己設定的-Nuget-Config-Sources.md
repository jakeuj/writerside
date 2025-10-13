# Nuget Restore 找不到自己設定的 Nuget Config Sources

> **原文發布日期:** 2024-03-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/03/04/CSharp-Nuget-Config
> **標籤:** 無

---

筆記一下還原找不到包的情形

## 結論

改用 SLN Level Nuget Config

`NuGet.Config` 從 `.proj` 改到 `.sln` 同一層目錄

```
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <!-- remove any machine-wide sources with <clear/> -->
    <clear />
    <!-- add an Azure Artifacts feed -->
    <add key="nuget.server" value="https://nuget-server.azurewebsites.net/v3/index.json" />
    <!-- also get packages from the NuGet Gallery -->
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" protocolVersion="3" />
  </packageSources>
</configuration>
```

最新版本的 NuGet 不正式支持專案級 NuGet.config 檔。

以下是文件中的[最新更新](fixing #1433 · NuGet/docs.microsoft.com-nuget@e3058f0 (github.com))

[fixing #1433 · NuGet/docs.microsoft.com-nuget@e3058f0 (github.com)](https://github.com/NuGet/docs.microsoft.com-nuget/commit/e3058f0061995ce8d5c5c71f6c9d9a865ce2384b)

[Rider 不會在“管理 Nuget 包”視窗中顯示存儲在專案級別的 NuGet.config 中的 NuGet 源：RIDER-19809 (jetbrains.com)](https://youtrack.jetbrains.com/issue/RIDER-19809/Rider-does-not-show-NuGet-feeds-from-NuGet.config-stored-at-project-level-in-Manage-Nuget-Packages-window)

[docs.microsoft.com-nuget/docs/consume-packages/configuring-nuget-behavior.md at main · NuGet/docs.microsoft.com-nuget (github.com)](https://github.com/NuGet/docs.microsoft.com-nuget/blob/main/docs/consume-packages/configuring-nuget-behavior.md#config-file-locations-and-uses)

## 情境

隔一段時間會遇到自定義 Nuget Server 沒有自動 Restore 的情況

可以按以下情況進行對應處理

* 無 Custom Nuget Server Url
  + 手動下載 .nuget 並於 nuget source 加入 local path
* 有 Custom Nuget Server Url
  + 有 NuGet.Config
    - 確認該檔路徑位於 .sln 目錄
  + 無 NuGet.Config
    - 於 .sln 目錄新建 NuGet.Config
    - 手動於 nuget source 加入 Url

## 延伸閱讀

[發布 Package 到自己的 Nuget Server | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2022/12/19/dotnet-nuget-push-Package-Nuget-Server)

[指定 NuGet packages 存放位置 - Yowko's Notes](https://blog.yowko.com/nuget-folder/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [C#](/jakeuj/Tags?qq=C%23)
{ignore-vars="true"}
* [NuGet](/jakeuj/Tags?qq=NuGet)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
