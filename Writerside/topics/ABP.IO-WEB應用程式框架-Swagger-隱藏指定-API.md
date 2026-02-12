# ABP.IO Swagger 隱藏指定 API

> **原文發布日期:** 2021-09-08
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/08/Abp-Swagger-Hide-Endpoint
> **標籤:** 無

---

筆記一下 Swagger DocumentFilter 用法

首先新增一個 Filter 繼承 `IDocumentFilter`

```
public class HideIdentityUserFilter : IDocumentFilter
{
    private const string pathToHide = "/api/identity/users";

    public void Apply(OpenApiDocument swaggerDoc, DocumentFilterContext context)
    {
        var identityUserPaths = swaggerDoc
            .Paths
            .Where(pathItem => pathItem.Key.Contains(pathToHide, StringComparison.OrdinalIgnoreCase))
            .ToList();

        foreach (var item in identityUserPaths)
        {
            swaggerDoc.Paths.Remove(item.Key);
        }
    }
}
```

然後加到 ConfigureServices

```
services.AddAbpSwaggerGen(
    options =>
    {
        options.SwaggerDoc("v1", new OpenApiInfo {Title = "PlmAPI API", Version = "v1"});
        options.DocInclusionPredicate((docName, description) => true);
        options.CustomSchemaIds(type => type.FullName);
        // add filter
        options.DocumentFilter<HideIdentityUserFilter>();
    }
);
```

當然 Filter 裡頭的 path 需要改成自己要隱藏的 api 路徑 (就 swagger 畫面顯示的網址)

參照：[How to hide an endpoint from Swagger? #264 | Support Center | ABP Commercial](https://support.abp.io/QA/Questions/264/How-to-hide-an-endpoint-from-Swagger)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- Swagger

- 回首頁

---

*本文章從點部落遷移至 Writerside*
