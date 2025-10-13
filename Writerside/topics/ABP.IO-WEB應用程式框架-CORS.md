# ABP.IO WEB應用程式框架 CORS

> **原文發布日期:** 2023-05-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/05/09/ABP-CORS
> **標籤:** 無

---

筆記下寫完 API 卻無法被成功呼叫的可能問題

## 徵狀

開發測試 Swagger API 正常，開放給前端(或其他站台)呼叫 API 時，出現 Option http method CORS 錯誤

## 結論

原因有兩個

1. 忘記加上新網址
2. 建立專案時是 MVC 架構
   本身不需要被其他前端網站(React, Angular, Vue)呼叫，因此沒有 CORS 的問題，也就沒有相對應的設定。
   此時只能自己呼叫自己，如果要讓其他網站(不同 Domain)呼叫，則需要補上 CORS 設定相關程式碼。

P.S. 雖說 CORS 其實是 .NET 原生的東西，但這邊就以 ABP 官方做法為例

### appsettings

首先檢查 appsettings 中是否有 `CorsOrigins` 字段，

如果有則加上目前要被呼叫的網址，

例如：https://projectname.azurewebsites.net

appsettings.json

```
"App": {
  "SelfUrl": "https://localhost:44305",
  "CorsOrigins": "https://*.ProjectName.com,https://localhost:44305,https://projectname.azurewebsites.net",
  "RedirectAllowedUrls": ""
}
```

### WebModule

如果沒有，則需要手動加上 .Net 內建的 Cors 設定

HttpApi.Web > ProjectNameHttpApiWebModule.cs

1. 新增服務 `services.AddCors();`
2. 使用管道 `app.UseCors();`

```
public override void ConfigureServices(ServiceConfigurationContext context)
{
    var configuration = context.Services.GetConfiguration();
    var hostingEnvironment = context.Services.GetHostingEnvironment();

    // ...

    ConfigureVirtualFileSystem(context);

    // 新增 Cors 服務
    ConfigureCors(context, configuration);

    ConfigureSwaggerServices(context, configuration);
}

private void ConfigureCors(ServiceConfigurationContext context, IConfiguration configuration)
{
    context.Services.AddCors(options =>
    {
        options.AddDefaultPolicy(builder =>
        {
            builder
                .WithOrigins(configuration["App:CorsOrigins"]?
                    .Split(",", StringSplitOptions.RemoveEmptyEntries)
                    .Select(o => o.RemovePostFix("/"))
                    .ToArray() ?? Array.Empty<string>())
                .WithAbpExposedHeaders()
                .SetIsOriginAllowedToAllowWildcardSubdomains()
                .AllowAnyHeader()
                .AllowAnyMethod()
                .AllowCredentials();
        });
    });
}

public override void OnApplicationInitialization(ApplicationInitializationContext context)
{
    // ...

    app.UseCorrelationId();
    app.UseStaticFiles();
    app.UseRouting();

    // 使用 Cors 管道
    app.UseCors();

    app.UseAuthentication();
    app.UseAbpOpenIddictValidation();

    // ...
}
```

#### 注意

這邊 `UseCors` 是有順序性的

### 參照

[在 ASP.NET Core 中啟用 CORS (跨原始來源要求) | Microsoft Learn](https://learn.microsoft.com/zh-tw/aspnet/core/security/cors?view=aspnetcore-7.0)

### 延伸

[Azure Storage Blob 403 CORS | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2022/10/14/Azure-Storage-CORS-Blob-403)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* .Net 7
{ignore-vars="true"}
* C#
{ignore-vars="true"}
* CORS

* 回首頁

---

*本文章從點部落遷移至 Writerside*
