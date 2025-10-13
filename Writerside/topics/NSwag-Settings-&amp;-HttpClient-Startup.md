# NSwag Settings &amp; HttpClient Startup

> **原文發布日期:** 2022-09-27
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/09/27/NSwag-Settings-HttpClient-Startup
> **標籤:** 無

---

筆記下用 NSwag 產生 HttpClient 的設定注意事項

## 結論

1. 按照微軟官方文件下載並安裝 NSwag 桌面應用程式
   [NSwag 與 ASP.NET Core 使用者入門 | Microsoft Learn](https://learn.microsoft.com/zh-tw/aspnet/core/tutorials/getting-started-with-nswag?view=aspnetcore-6.0&tabs=visual-studio)
2. 設定 NSwag 產生 Client 的細節，改命名空間跟類別名稱
   這邊因為我打算從 Startup 用 Typed Client 的方式設定 baseUrl
   所以需要特別取消勾選 Use the base URL for the request

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/8dc743da-3174-4606-81be-8d3c2038a1b8/1664251597.png.png)

      3. 在專案內建立一個程式碼檔案，並將產生的 Outputs 程式碼複製貼上，例如 TestProxy.cs

      4. 在 Startup 註冊該 TypedClient，並由 appsettings 設定 baseUrl

```
private void ConfigureHttpClient(
    ServiceConfigurationContext context,
    IConfiguration configuration)
{
    context.Services.AddHttpClient<ITestProxy,TestProxy>(opt =>
    {
        if(Uri.TryCreate(configuration["TestProxy:URL"], UriKind.Absolute,out var uri))
        {
            opt.BaseAddress = uri;
        }
    });
}
```

      5. 最後在需要使用的地方直接注入該 TypedClient，範例是 `ITestProxy`

```
private readonly ITestProxy _service;

public TestManager(ITestProxy service)
{
    _service = service;
}
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* HttpClinet
* NSwag
* Swagger

* 回首頁

---

*本文章從點部落遷移至 Writerside*
