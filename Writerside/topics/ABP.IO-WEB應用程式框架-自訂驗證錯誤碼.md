# ABP.IO WEB應用程式框架 自訂驗證錯誤碼

> **原文發布日期:** 2023-04-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/04/25/ABP-CustomExceptionToErrorInfoConverter
> **標籤:** 無

---

Restful API 預設驗證錯誤回傳 HttpStatusCode 400

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/cca35751-832f-4c1c-b77c-1454629d143f/1682405338.png.png)

Code

## 結論

`src/TsetCode.Domain/ExceptionHandling/MyExceptionToErrorInfoConverter.cs`

```
using System;
using Microsoft.Extensions.Localization;
using Microsoft.Extensions.Options;
using Volo.Abp.AspNetCore.ExceptionHandling;
using Volo.Abp.DependencyInjection;
using Volo.Abp.ExceptionHandling.Localization;
using Volo.Abp.Http;
using Volo.Abp.Localization.ExceptionHandling;
using Volo.Abp.Validation;

namespace TsetCode.ExceptionHandling;

[Dependency(ReplaceServices = true)]
[ExposeServices(typeof(IExceptionToErrorInfoConverter))]
public class MyExceptionToErrorInfoConverter :
    DefaultExceptionToErrorInfoConverter,
    IExceptionToErrorInfoConverter
{
    public MyExceptionToErrorInfoConverter(
        IOptions<AbpExceptionLocalizationOptions> localizationOptions,
        IStringLocalizerFactory stringLocalizerFactory,
        IStringLocalizer<AbpExceptionHandlingResource> stringLocalizer,
        IServiceProvider serviceProvider) : base(localizationOptions,
        stringLocalizerFactory,
        stringLocalizer,
        serviceProvider)
    {
    }

    protected override RemoteServiceErrorInfo CreateErrorInfoWithoutCode(
        Exception exception,
        AbpExceptionHandlingOptions options)
    {
        var errorInfo = base.CreateErrorInfoWithoutCode(exception, options);

        if (exception is IHasValidationErrors)
        {
            // workaround for Ray
            errorInfo.Code = "test";
        }

        return errorInfo;
    }
}
```

### 備註

將驗證錯誤時的 Code 手動指定

`if (exception is IHasValidationErrors){errorInfo.Code = "test";}`

### 參照

[Dependency Injection | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Dependency-Injection#dependency-attribute)

[abp/DefaultExceptionToErrorInfoConverter.cs at dev · abpframework/abp (github.com)](https://github.com/abpframework/abp/blob/dev/framework/src/Volo.Abp.ExceptionHandling/Volo/Abp/AspNetCore/ExceptionHandling/DefaultExceptionToErrorInfoConverter.cs#L104)

[How should we customize exception message of Check.NotNull() class for specific cases ? #2092 | Support Center | ABP Commercial](https://support.abp.io/QA/Questions/2092/How-should-we-customize-exception-message-of-CheckNotNull--class-for-specific-cases)

### 延伸閱讀

自訂 HttpStatusCode

[Exception Handling | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Exception-Handling#http-status-code-mapping)

![]()
![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
