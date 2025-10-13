# ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.7 建立WebApi

> **原文發布日期:** 2016-07-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/07/28/abp7
> **標籤:** 無

---

ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.7 建立WebApi

​[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.0 索引](https://dotblogs.com.tw/jakeuj/2016/07/28/abp0)

---

ABP可以自動以應用服務產生WebApi

關於WebApi設定的部分ABP預設已經會自動將public的service做成WebApi

預設是用Post呼叫，這邊一方面方便測試，另一方面稍微示範一下怎樣改成Get呼叫

WebApi設定位於 MyCompany.MyProject.WebApi\Api\MyProjectWebApiModule.cs

```

using System.Reflection;
using System.Web.Http;
using Abp.Application.Services;
using Abp.Configuration.Startup;
using Abp.Modules;
using Abp.WebApi;
using Abp.WebApi.Controllers.Dynamic.Builders;
using Abp.Web;

namespace MyCompany.MyProject.Api
{
    [DependsOn(typeof(AbpWebApiModule), typeof(MyProjectApplicationModule))]
    public class MyProjectWebApiModule : AbpModule
    {
        public override void Initialize()
        {
            IocManager.RegisterAssemblyByConvention(Assembly.GetExecutingAssembly());

            //http://localhost/api/services/app/player/getPlayers
            DynamicApiControllerBuilder
                .ForAll<IApplicationService>(typeof(MyProjectApplicationModule).Assembly, "app")
                .ForMethods(builder =>
                {
                    builder.Verb = HttpVerb.Get;
                })
                .Build();

            Configuration.Modules.AbpWebApi().HttpConfiguration.Filters.Add(new HostAuthenticationFilter("Bearer"));
        }
    }
}
```

這邊我在DynamicApiControllerBuilder的.ForAll與.Build();之間加上了.ForMethods片段程式碼

```

.ForMethods(builder =>
{
    builder.Verb = HttpVerb.Get;
})
```

用HttpVerb.Get指定以Get方式呼叫，如此一來我們就可以直接在執行程式在瀏覽器上以網址方式測試WebApi

http://localhost/api/services/app/player/getPlayers

執行後開啟以上網址即可呼叫我們先前完成的Service (有port請自行加上)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/897bd0d4-bf8d-4568-89c6-a0850d226e51/1469680650_66273.png)

---

下一篇

[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.8 單元測試](https://dotblogs.com.tw/jakeuj/2016/07/28/abp6)

參照

[一步一步使用ABP框架搭建正式項目系列教程](http://www.cnblogs.com/farb/p/4849791.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [C#](/jakeuj/Tags?qq=C%23)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
