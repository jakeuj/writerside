# ABP.IO WEB應用程式框架 UnitTest 讀取 appsettings.json

> **原文發布日期:** 2022-09-22
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/09/22/abp-test-appsettings
> **標籤:** 無

---

筆記 Module IConfiguration 讀不到 appsettings.json 的處理方式

以 Configure AddHttpClient<IClient,TImplementation> 為例

## 結論

1. MyProject.TestBase 專案內新增 `appsettings.test.json` 並將屬性改成 內容/永遠複製
2. MyProjectTestBaseModule.cs 加上 `BuildConfiguration` 方法來取得 `configuration`
3. HttpClient 介面註冊 `AddHttpClient<TClient,TImplementation>(Action<HttpClient>)`
4. 統一將需要 appsettings 的服務註冊在 HttpApiHostModule，因為測試時不會用到該模組，所以不會發生例外
   然後統一於 TestBaseModule 來註冊測試方法所需的服務 (使用第一點與第二點進行 appsettings 讀取)

```
private static IConfigurationRoot BuildConfiguration()
{
    var builder = new ConfigurationBuilder()
        .SetBasePath(Directory.GetCurrentDirectory())
        .AddJsonFile("appsettings.test.json", optional: false);

    return builder.Build();
}

public override void ConfigureServices(ServiceConfigurationContext context)
{
    ConfigureBackgroundJob();
    context.Services.AddAlwaysAllowAuthorization();
    // Add
    var configuration = BuildConfiguration();
    ConfigureHttpClient(context, configuration);
    ConfigureMyOptions(configuration);
}

private void ConfigureHttpClient(ServiceConfigurationContext context,
    IConfiguration configuration)
{
    context.Services.AddHttpClient<IMyServiceProxy,MyServiceProxy>(opt =>
    {
        if (Uri.TryCreate(configuration["MyService:URL"],
            UriKind.Absolute, out var uri))
        {
            opt.BaseAddress = uri;
        }
    });
}

private void ConfigureMyOptions(IConfiguration configuration)
{
    Configure<MyOptions>(options =>
    {
        options.Path = configuration["MyOptions:Path"];
    });
}
```

## 問題

1. 單元測試裡面並沒有 appsetting.json 相關機制
   導致有些用到該設定檔的地方測試會取不到值
2. Typed HttpClient 官方教學不是用介面
   所以要用 Interface 需要在註冊服務的時候指定
   `AddHttpClient<TClient,TImplementation>(Action<HttpClient>)`
3. DomainModule, EntityFrameworkCoreModule, ApplicationModule
   src 內的上述模組內只要用到 appsettings 都會取不到值
   因此有可能會在需要該值進行設定時發生 null 例外

## 參考

[[ .NET Core ] - 使用 Typed client 打造具有 IntelliSense 的 HttpClient | 工程良田的小球場 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/armycoding/2021/03/21/net-core-typed-http-client)

[abp/TodoDbContextFactory.cs at dev · abpframework/abp (github.com)](https://github.com/abpframework/abp/blob/dev/test/DistEvents/DistDemoApp.EfCoreRabbitMq/TodoDbContextFactory.cs)

[Accessing Configuration in .NET Core Test Projects - Rick Strahl's Web Log (west-wind.com)](https://weblog.west-wind.com/posts/2018/Feb/18/Accessing-Configuration-in-NET-Core-Test-Projects)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* HttpClinet
* UnitTest

* 回首頁

---

*本文章從點部落遷移至 Writerside*
