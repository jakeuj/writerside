# Azure App Service timeout 設定：ASP.NET Framework、ASP.NET Core 與 230 秒限制

<web-summary>釐清 Azure App Service 的平台 timeout、IIS connectionTimeout、ASP.NET Framework executionTimeout 與 ASP.NET Core requestTimeout，並提供各層的設定範例。</web-summary>

Azure App Service 的 timeout 不能只靠一個設定值解決。Windows App Service 的同步 HTTP request 約在 230 秒後 timeout，Linux App Service 約為 240 秒；這是 App Service 前端的限制，無法透過 `web.config`、`applicationHost.xdt` 或 .NET 程式碼調高。

如果工作可能超過這個時間，應改成背景工作，由 API 先回傳工作 ID，再讓前端輪詢或由後端通知完成結果。只有在 request 會於平台上限內完成時，才需要繼續檢查 IIS、ASP.NET Framework 或 ASP.NET Core 的 timeout。

> **原文發布日期：** 2021-08-23
>
> **原文連結：** https://www.dotblogs.com.tw/jakeuj/2021/08/23/AzureAppServiceTimeOut
>
> **更新日期：** 2026-08-27

## 先判斷是哪一層 timeout {#timeout-layers}

| 層級 | 設定 | 適用情境 | 重點 |
| --- | --- | --- | --- |
| Azure App Service 前端 | 無法自行調高 | 對外 HTTP request | Windows 約 230 秒；Linux 約 240 秒 |
| IIS 閒置連線 | `webLimits connectionTimeout` | Windows App Service | 斷開被視為 inactive 的 connection，不是應用程式執行時間 |
| ASP.NET Framework | `httpRuntime executionTimeout` | .NET Framework | request 可執行的秒數 |
| ASP.NET Core Module | `aspNetCore requestTimeout` | ASP.NET Core out-of-process hosting | ANCM 等待 Kestrel 回應的時間；in-process 不適用 |
| ASP.NET Core 8 以上 | Request Timeouts middleware | 應用程式內的全域或 endpoint policy | 可主動取消 request，但不能延長 App Service 平台上限 |
| IIS request filtering | `maxAllowedContentLength` | 上傳 request body | 單位是 bytes，這是大小限制，不是 timeout |
| ASP.NET Framework request body | `maxRequestLength` | .NET Framework 上傳 | 單位是 KB，這是大小限制，不是 timeout |

若 request 大約固定在 110、120 或 230 秒附近失敗，通常可以依序檢查 `executionTimeout`、ANCM `requestTimeout` 與 App Service 前端限制。若更早失敗，還要檢查 client、CDN、API gateway、reverse proxy 與下游 `HttpClient.Timeout`。

## Azure App Service 前端約 230 或 240 秒的限制

Azure App Service 透過 Azure Load Balancer 對外提供服務。應用程式若沒有在約 230 秒（Windows）或 240 秒（Linux）內回傳 response，client 會收到 timeout。

把下列值設成 15 分鐘，也不代表外部 client 能等待 15 分鐘：

- `connectionTimeout="00:15:00"`
- `executionTimeout="900"`
- `requestTimeout="00:15:00"`
- `HttpClient.Timeout = TimeSpan.FromMinutes(15)`

它們分別控制不同元件，而且都無法覆寫 App Service 前端限制。長時間工作可改用 WebJobs、queue consumer 或其他背景工作，HTTP endpoint 只負責建立工作並快速回應。

## Windows App Service 的 applicationHost.xdt

Windows App Service 沒有直接開放完整的 IIS `applicationHost.config`，需要調整 machine-level IIS 設定時，可在 Kudu 的 `site` 目錄建立 `applicationHost.xdt`。舊環境通常會顯示為：

```text
D:\home\site\applicationHost.xdt
```

以下設定把 IIS 的 inactive connection timeout 改成 15 分鐘：

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration xmlns:xdt="http://schemas.microsoft.com/XML-Document-Transform">
  <system.applicationHost>
    <webLimits
      connectionTimeout="00:15:00"
      xdt:Transform="SetAttributes(connectionTimeout)" />
  </system.applicationHost>
</configuration>
```

重新啟動 App Service 後，可在 Kudu 的 `LogFiles\Transform` 查看 XDT transform log。

`connectionTimeout` 是 IIS 判定 connection inactive 後等待多久才中斷，不能拿來取代 ASP.NET request execution timeout，也不能延長 App Service 的 230／240 秒前端限制。這個做法只適用於 Windows App Service。

## ASP.NET Framework 的 executionTimeout

ASP.NET Framework 使用 `<system.web>` 下的 `httpRuntime executionTimeout`，單位是秒。以下設定允許 request 執行 180 秒：

```xml
<configuration>
  <system.web>
    <httpRuntime executionTimeout="180" />
  </system.web>
</configuration>
```

`executionTimeout` 只在 `<compilation debug="false">` 時生效，預設值是 110 秒。這是 ASP.NET Framework 設定，不適用於 ASP.NET Core。

## ASP.NET Core 的 requestTimeout

ASP.NET Core 部署到 Windows IIS 或 Windows App Service 時，會由 ASP.NET Core Module（ANCM）處理 IIS 與應用程式之間的轉送。

### Out-of-process hosting

若既有 `web.config` 的 `<aspNetCore>` 使用 `hostingModel="outofprocess"`，可以加入 `requestTimeout`。下例讓 ANCM 最多等待 Kestrel 180 秒：

```xml
<configuration>
  <system.webServer>
    <aspNetCore
      processPath="dotnet"
      arguments=".\MyApp.dll"
      hostingModel="outofprocess"
      requestTimeout="00:03:00" />
  </system.webServer>
</configuration>
```

`requestTimeout` 格式為 `hh:mm:ss`，ANCM 的預設值是 2 分鐘。實際使用時應修改 `dotnet publish` 產生的既有 `<aspNetCore>` element，不要直接用上面的片段覆蓋整份 `web.config`。

### In-process hosting

若設定為 `hostingModel="inprocess"`，ANCM 的 `requestTimeout` 不生效。不要只為了使用這個屬性而把 hosting model 改成 out-of-process；in-process request 仍受 App Service 約 230 秒的前端限制。

## ASP.NET Core 8 以上的 Request Timeouts middleware

ASP.NET Core 本身不會預設限制每個 request 的處理時間。ASP.NET Core 8 以上可使用 Request Timeouts middleware，為全域或個別 endpoint 設定應用程式層的 timeout。

以下範例把全域 timeout 設為 180 秒，讓應用程式在 App Service 前端 timeout 前先取消 request：

```C#
using Microsoft.AspNetCore.Http.Timeouts;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRequestTimeouts(options =>
{
    options.DefaultPolicy = new RequestTimeoutPolicy
    {
        Timeout = TimeSpan.FromSeconds(180)
    };
});

var app = builder.Build();

app.UseRouting();
app.UseRequestTimeouts();

app.Run();
```

若應用程式明確呼叫 `UseRouting`，`UseRequestTimeouts` 要放在它之後。Timeout 發生時，middleware 會取消 `HttpContext.RequestAborted`；後續的 database、HTTP 或其他 async operation 也要傳入這個 `CancellationToken`，才能停止實際工作。

這個 middleware 用來建立可控的應用程式 timeout policy，不是用來延長 Azure App Service 的 request 時間。

## 上傳大小限制不是 timeout {#request-body-size-limits}

原本筆記中的 `maxRequestLength` 與 `maxAllowedContentLength` 是 request body 大小限制。以 100 MiB 為例：

```xml
<configuration>
  <system.web>
    <httpRuntime
      executionTimeout="180"
      maxRequestLength="102400" />
  </system.web>
  <system.webServer>
    <security>
      <requestFiltering>
        <requestLimits maxAllowedContentLength="104857600" />
      </requestFiltering>
    </security>
  </system.webServer>
</configuration>
```

- `maxRequestLength` 的單位是 KB，ASP.NET Framework 預設為 4096 KB（4 MB）。
- `maxAllowedContentLength` 的單位是 bytes，IIS 預設為 30,000,000 bytes，約 28.6 MB。

不要直接把上限放到 2 GB；應依實際檔案需求設定最小可用值，降低記憶體、磁碟與 denial-of-service 風險。

## 參考資料

- [Web request times out in App Service](https://learn.microsoft.com/en-us/troubleshoot/azure/app-service/web-request-times-out-app-service)
- [ASP.NET Core Module for IIS](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/aspnet-core-module?view=aspnetcore-10.0)
- [Request timeouts middleware in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/performance/timeouts?view=aspnetcore-10.0)
- [IIS Web Limits](https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/weblimits)
- [HttpRuntimeSection.ExecutionTimeout](https://learn.microsoft.com/en-us/dotnet/api/system.web.configuration.httpruntimesection.executiontimeout?view=netframework-4.8.1)
- [IIS Request Limits](https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/requestfiltering/requestlimits/)
- [Kudu XDT transform samples](https://github.com/projectkudu/kudu/wiki/Xdt-transform-samples)

---

*本文章從點部落遷移至 Writerside，並於 2026-08-27 依目前官方文件更新。*
