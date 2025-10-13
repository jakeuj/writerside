# ABP.IO WEB應用程式框架 Mail Razor 樣板

> **原文發布日期:** 2022-11-08
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/11/08/ABP-Mail-Razor
> **標籤:** 無

---

筆記下怎麼讓 Mail 支援 Razor 語法

## 前置

[ABP.IO WEB應用程式框架 Mail 樣板 | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2022/11/07/abp-mail-template)

### 結論

於 Domain 層開始進行以下操作

### Volo.Abp.TextTemplating.Razor

```
dotnet add package Volo.Abp.TextTemplating.Razor
```

### DomainModule.cs

```
[DependsOn(
    //...other dependencies
    //Add the new module dependency
    typeof(AbpTextTemplatingRazorModule)
)]
public class MyProjectNameDomainModule : AbpModule
{
    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        //...other configuration
        //Add this configuration
        Configure<AbpRazorTemplateCSharpCompilerOptions>(options =>
        {
            options.References.Add(MetadataReference.CreateFromFile(
                typeof(MyProjectDomainModule).Assembly.Location));
        });

        context.Services.Configure<AbpCompiledViewProviderOptions>(options =>
        {
            // MyMessage is template name.
            options.TemplateReferences.Add("MyMessage", new List<Assembly>()
                {
                    Assembly.Load("Microsoft.Extensions.Logging.Abstractions"),
                    Assembly.Load("Microsoft.Extensions.Logging")
                }
                .Select(x => MetadataReference.CreateFromFile(x.Location))
                .ToList());
        });

        Configure<AbpVirtualFileSystemOptions>(options =>
        {
            options.FileSets.AddEmbedded<MyProjectNameDomainModule>(nameof(MyProjectName));
        });
    }
}
```

### Layout.cshtml

```
@inherits Volo.Abp.TextTemplating.Razor.RazorTemplatePageBase
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
</head>
<body>
    @Body
</body>
</html>
```

### MyDataModel.cs

```
using System.Collections.Generic;

namespace MyProjectName.Emailing;

public class MyDataModel
{
    public List<string> Items { get; set; }
}
```

### Message.cshtml

```
@inherits Volo.Abp.TextTemplating.Razor
    .RazorTemplatePageBase<MyProjectName.Emailing.MyDataModel>

<div class="table">
    @foreach (var item in Model.Items)
    {
        <div class="row">
            <div class="cell">
                @item
            </div>
        </div>
    }
</div>
```

### Embedded Resource

![](https://raw.githubusercontent.com/abpframework/abp/rel-6.0/docs/en/images/hello-template-razor.png)

### TemplateDefinitionProvider

```
public class DemoTemplateDefinitionProvider : TemplateDefinitionProvider
{
    public override void Define(ITemplateDefinitionContext context)
    {
        context.Add(
            new TemplateDefinition(
                    "MyLayout",
                    isLayout: true //SET isLayout!
                )
                .WithRazorEngine()
                .WithVirtualFilePath(
                    "/Emailing/Templates/Layout.cshtml",
                    isInlineLocalized: true
                )
        );

        context.Add(
            new TemplateDefinition(
                    "MyMessage",
                    layout: "MyLayout"
                )
                .WithRazorEngine()
                .WithVirtualFilePath(
                    "/Emailing/Templates/Message.cshtml",
                    isInlineLocalized: true
                )
        );
    }
}
```

### ITemplateRenderer

```
public class MailManager : DomainService
{
    private readonly IEmailSender _emailSender;
    private readonly ITemplateRenderer _templateRenderer;

    public MailManager(IEmailSender emailSender,
        ITemplateRenderer templateRenderer)
    {
        _emailSender = emailSender;
        _templateRenderer = templateRenderer;
    }

    public async Task SendAsync(
        string to,
        string subject,
        List<string> items)
    {
        var body = await _templateRenderer.RenderAsync(
            "MyMessage",
            new MyModel
            {
                Items = items
            }
        );
        await _emailSender.SendAsync(
            to,
            subject,
            body
        );
    }
}
```

### 參照

[Text Templating Razor | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Text-Templating-Razor)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Razor

* 回首頁

---

*本文章從點部落遷移至 Writerside*
