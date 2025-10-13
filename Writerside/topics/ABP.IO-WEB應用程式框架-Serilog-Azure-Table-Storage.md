# ABP.IO WEB應用程式框架 Serilog Azure Table Storage

> **原文發布日期:** 2023-03-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/03/23/ABP-Serilog-Azure-Table-Storage
> **標籤:** 無

---

紀錄一下 Serilog 的設定檔與存到 Azure Table Storage

## 結論

1. 切到 Host / Web 專案目錄
2. 安裝套件

```
dotnet add package Serilog.Sinks.AzureTableStorage
```

     3. Program.cs

```
Log.Logger = new LoggerConfiguration()
    .WriteTo.Async(c => c.File("Logs/logs.txt"))
    .WriteTo.Async(c => c.Console())
    .CreateBootstrapLogger();

try
{
    Log.Information("Starting YourProjectName.HttpApi.Host.");
    var builder = WebApplication.CreateBuilder(args);
    builder.Host.AddAppSettingsSecretsJson()
        .UseAutofac()
        .UseSerilog((context, service, configuration) => configuration
            .ReadFrom.Configuration(context.Configuration)
            .ReadFrom.Services(service)
            .WriteTo.Async(c => c.File("Logs/log.txt", rollingInterval: RollingInterval.Day))
            .WriteTo.Async(c => c.Console())
            .Enrich.FromLogContext()
        );
```

     4. appsettings.json

```
"Serilog": {
  "MinimumLevel": {
    "Default": "Information",
    "Override": {
      "Microsoft": "Information",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  }
}
```

     5. appsettings.Development.json

```
"Serilog": {
  "MinimumLevel": {
    "Default": "Debug",
    "Override": {
      "Hangfire": "Information",
      "OpenIddict": "Information"
    }
  }
}
```

這邊範例針對 `Hangfire` 與 `OpenIddict` 將記錄層級提高

實際上可自行調整想在開發階段到看的各組件紀錄詳細程度

     6. appsettings.Production.json

```
"Serilog": {
  "Using": [
    "Serilog.Sinks.AzureTableStorage"
  ],
  "WriteTo": [
    {
      "Name": "Async",
      "Args": {
        "configure": [
          {
            "Name": "AzureTableStorage",
            "Args": {
              "restrictedToMinimumLevel": "Warning",
              "storageTableName": "儲存體內資料表的名稱",
              "connectionString": "儲存體的連線字串"
            }
          }
        ]
      }
    }
  ]
}
```

連結字串格式

`DefaultEndpointsProtocol=https;AccountName=你的帳號;AccountKey=你的鑰匙;EndpointSuffix=core.windows.net`

### 備註

可以針對自己寫的類別的 FullName 作單獨設定

```
"Serilog": {
  "MinimumLevel": {
    "Default": "Warning",
    "Override": {
      "YourProjectName.Blogs.BlogAppService": "Information",
      "YourProjectName.Others.XxxxxxxWorker": "Information",
```

### 參照

[最詳細 ASP.NET Core 使用 Serilog 套件寫 log 教學](https://www.ruyut.com/2022/09/aspnet-core-serilog.html)

[serilog/serilog-sinks-async: An asynchronous wrapper for Serilog sinks that logs on a background thread (github.com)](https://github.com/serilog/serilog-sinks-async#xml-appsettings-and-json-configuration)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP
* Azure
* Serilog
* Storage

* 回首頁

---

*本文章從點部落遷移至 Writerside*
