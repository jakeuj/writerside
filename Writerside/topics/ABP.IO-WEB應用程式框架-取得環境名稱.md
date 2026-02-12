# ABP.IO WEB應用程式框架 取得環境名稱

> **原文發布日期:** 2023-04-14
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/04/14/abp-IAbpHostEnvironment
> **標籤:** 無

---

簡介下 Domain 取得環境名稱

## 結論

```
public class TestManager : DomainService
{
    private readonly IAbpHostEnvironment _abpHostEnvironment;

    public TestManager(IAbpHostEnvironment abpHostEnvironment)
    {
        _abpHostEnvironment = abpHostEnvironment;
    }

    public string GetEnv()
    {
        return _abpHostEnvironment.EnvironmentName;
    }
}
```

## 簡介

有時，在創建一個應用程序時，我們需要獲得當前的主機環境，並根據該環境採取相應的行動。

在這種情況下，我們可以在最終的應用程序中使用一些服務，

如由.NET提供的 [IWebHostEnvironment](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.hosting.iwebhostenvironment?view=aspnetcore-7.0) 或 [IWebAssemblyHostEnvironment](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.components.webassembly.hosting.iwebassemblyhostenvironment)。

然而，我們不能在類庫中使用這些服務，而類庫是由最終的應用程序使用的。

ABP框架提供了`IAbpHostEnvironment`服務，它允許你隨時獲得當前的環境名稱。

`IAbpHostEnvironment`被ABP框架在幾個地方使用，以執行環境的特定動作。

例如，ABP框架在開發環境上減少一些服務的緩存時間。

`IAbpHostEnvironment`通過以下順序獲得當前環境名稱：

1. 獲取並設置環境名稱，如果它在`AbpApplicationCreationOptions`中被指定。
2. 如果環境名稱沒有在`AbpApplicationCreationOptions`中指定，
   則嘗試從`IWebHostEnvironment`或`IWebAssemblyHostEnvironment`服務
   為 ASP.NET Core & Blazor WASM 應用程序獲取環境名稱。
3. 如果環境名稱未被指定或無法從服務中獲得，則將環境名稱設置為生產(**Production**)。

## **What's New with ABP Framework 7.1?**

In this section, I will introduce some major features released in this version. In addition to these features, so many enhancements have been made in this version too.

Here is a brief list of the titles explained in the next sections:

- Blazor WASM option added to Application Single Layer Startup Template
- Introducing the `IHasEntityVersion` interface and `EntitySynchronizer` base class
- Introducing the `DeleteDirectAsync` method for the `IRepository` interface
- Introducing the `IAbpHostEnvironment` interface
- Improvements on the eShopOnAbp project
- Others

## 同場加映

取得 appsettings 設定值

```
public class TestManager : DomainService
{
    private readonly IConfiguration configuration;

    public TestManager(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public string? GetKey()
    {
        return _configuration.GetSection("Titles")["Name"];
    }
}
```

### 參照

[Application Startup | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Application-Startup#iabphostenvironment)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- 回首頁

---

*本文章從點部落遷移至 Writerside*
