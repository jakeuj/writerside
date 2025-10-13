# C# 具名選項模式

> **原文發布日期:** 2023-04-11
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/04/11/CSharp-Named-IOptions-appsettings
> **標籤:** 無

---

打半天 400 Bad Request… 大家快逃阿！

結論

```
{
  "ApiSettings": {
    "A廠商": {
      "ClientId": "Green Widget",
      "Secret": "GW46"
    },
    "B廠商": {
      "ClientId": "Orange Gadget",
      "Secret": "OG35"
    }
  }
}
```

```
public class ApiSettings
{
    public const string A = "A廠商";
    public const string B = "B廠商";

    public string ClientId { get; set; } = string.Empty;
    public string Secret { get; set; } = string.Empty;
}
```

```
builder.Services.Configure<ApiSettings>(TopItemSettings.A,
    builder.Configuration.GetSection("ApiSettings:A廠商"));

builder.Services.Configure<ApiSettings>(TopItemSettings.B,
    builder.Configuration.GetSection("ApiSettings:B廠商"));
```

```
public class TestNOModel : PageModel
{
    private readonly ApiSettings _aApiSettings;
    private readonly ApiSettings _bApiSettings;

    public TestNOModel(IOptionsSnapshot<ApiSettings> namedOptionsAccessor)
    {
        _aApiSettings = namedOptionsAccessor.Get(ApiSettings.A);
        _bApiSettings = namedOptionsAccessor.Get(ApiSettings.B);
    }

    public ContentResult OnGet()
    {
        return Content($"A廠商:ClientId {_aApiSettings.ClientId} \n" +
                       $"A廠商:Secret {_aApiSettings.Secret} \n\n" +
                       $"B廠商:ClientId {_bApiSettings.ClientId} \n" +
                       $"B廠商:Secret {_bApiSettings.Secret} \n"   );
    }
}
```

參照

[C# 選項模式 | 御用小本本 - 點部落 (dotblogs.azurewebsites.net)](https://dotblogs.azurewebsites.net/jakeuj/2022/10/21/CSharp-IOptions-appsettings)

[ASP.NET Core 中的選項模式 | Microsoft Learn](https://learn.microsoft.com/zh-tw/aspnet/core/fundamentals/configuration/options?view=aspnetcore-7.0#named)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [.Net 7](/jakeuj/Tags?qq=.Net%207)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
