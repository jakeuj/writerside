# ABP.IO ICachedServiceProvider

> **原文發布日期:** 2023-05-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/05/23/Dependency-Injection-Cached-Service-Providers
> **標籤:** 無

---

筆記下 ICachedServiceProvider 與 HttpClient 的坑

## 結論

```
var httpClientFactory = _cachedServiceProvider.GetRequiredService<IHttpClientFactory>();
var httpClient = httpClientFactory.CreateClient(nameof(ITestService));
// ...
var response = await httpClient.PostAsJsonAsync("oauth/token", testRequest);
```

總之直接用 `ICachedServiceProvider` 取得 `HttpClient` 會吃不到 `TypedHttpClient` 的設定

這邊改用 `ICachedServiceProvider`取得 `IHttpClientFactory`再用 介面名稱 透過工廠模式取得

### 問題

```
var httpClient = _cachedServiceProvider.GetRequiredService<HttpClient>();
// ...
var response = await httpClient.PostAsJsonAsync("oauth/token", testRequest);
```

會報錯誤訊息

> System.InvalidOperationException An invalid request URI was provided.
>
> Either the request URI must be an absolute URI or BaseAddress must be set.
>
> at System.Net.Http.HttpClient.PrepareRequestMessage(HttpRequestMessage request)

### 備註

`ConfigureServices`

```
private void ConfigureHttpClient(ServiceConfigurationContext context)
{
    var options = context.Services.ExecutePreConfiguredActions<TestOptions>();
    context.Services.AddHttpClient<ITestService, TestService>(httpClient =>
    {
        httpClient.BaseAddress = options.BaseAddress;
    });
}
```

### 參照

[Dependency Injection | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Dependency-Injection#cached-service-providers)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* DI
* HttpClinet

* 回首頁

---

*本文章從點部落遷移至 Writerside*
