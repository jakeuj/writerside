# ABP.IO WEB應用程式框架 選項模式

> **原文發布日期:** 2023-01-12
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/01/12/ABP-Options-Pre-Configure
> **標籤:** 無

---

簡介一下 ABP 增強的預配置 (Pre Configure)

## 簡介

ConfigureServices 註冊服務階段無法使用 IOptions 來進行設定

比如 AddHttpClient 時想要用 GithubOptions.BaseAddress 來設定 HttpClient.BaseAddress

會發現因為 IOptions<GithubOptions> 在此時還在做 DI

所以無法直接使用該設定值來進行 HttpClient 設定

為此 ABP 提供了預配置功能來解決此問題

### HttpApiHostModule

```
public override void PreConfigureServices(ServiceConfigurationContext context)
{
    var configuration = context.Services.GetConfiguration();
    PreConfigure<GithubOptions>(builder =>
        configuration.GetSection(GithubOptions.Position).Bind(builder));
}

public override void ConfigureServices(ServiceConfigurationContext context)
{
    var options = context.Services.ExecutePreConfiguredActions<GithubOptions>();

    context.Services.AddHttpClient<IGithubService, GithubService>(opt =>
    {
        opt.BaseAddress = options.ApiUrl;
    });
}
```

參照

[Options | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Options#pre-configure)

[C# 選項模式 | Jakeuj - 點部落 (dotblogs.azurewebsites.net)](https://dotblogs.azurewebsites.net/jakeuj/2022/10/21/CSharp-IOptions-appsettings)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [C#](/jakeuj/Tags?qq=C%23)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
