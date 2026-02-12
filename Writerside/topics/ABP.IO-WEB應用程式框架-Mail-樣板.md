# ABP.IO WEB應用程式框架 Mail 樣板

> **原文發布日期:** 2022-11-07
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/11/07/abp-mail-template
> **標籤:** 無

---

筆記下使用信件內容樣板來生成 email 內容

## 信件 html 樣板 產生器

![](https://raw.githubusercontent.com/abpframework/abp/dev/docs/en/Community-Articles/2020-09-09-Replacing-Email-Template-and-Sending-Emails/bee.gif)

[Free Email Templates | Responsive Email Templates – BEE Free](https://beefree.io/templates/free/)

## 結論

這個系統主要由兩部分組成

1. Layout
   - 定義整體布局，內含一個準備放內容的區塊
   - `{{content}}` 內容預備區塊，來放下面的 Message
2. Message
   - 定義訊息內容，內含一個準備放訊息的區塊
   - `{{model.message}}` 訊息預備區塊，呼叫時可以輸入 `message`

```
_templateRenderer.RenderAsync(StandardEmailTemplates.Message, new { message })
```

最後會將 Message 放到 Layout 中的 `{{content}}` 輸出

`new { message }` > `{{model.message}}` > MyMessage > `{{content}}` > MyLayout > Mail

### MyLayout.tpl

```
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
</head>
<body>

    <div>
        {{content}}
    </div>
</body>
</html>
```

### MyMessage.tpl

```
<p>
    {{model.message}}
</p>
```

### 呼叫

```
var body = await _templateRenderer.RenderAsync(
    StandardEmailTemplates.Message,
    new
    {
        message = "<b>Jake</b>"
    }
);
await _emailSender.QueueAsync(
    to,
    subject,
    body
);
```

### 輸出 Mail

```
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
</head>
<body>

    <div>
        <p>
            <b>Jake</b>
        </p>
    </div>
</body>
</html>
```

## 前置

[ABP.IO WEB應用程式框架 SendGrid](https://www.dotblogs.com.tw/jakeuj/2022/11/04/abp-SendGrid-STMP-587)

## EmbeddedResource

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/cc12a115-f58c-4c6e-a2e5-661d97d98931/1667807514.png.png)

### EmailTemplate.tpl

```
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
</head>
<body>
    {{content}}
</body>
</html>
```

### EmailTemplateDefinitionProvider.cs

```
using Volo.Abp.DependencyInjection;
using Volo.Abp.Emailing.Templates;
using Volo.Abp.TextTemplating;

namespace MyProject.Emailing;

public class EmailTemplateDefinitionProvider : TemplateDefinitionProvider
    , ITransientDependency
{
    public override void Define(ITemplateDefinitionContext context)
    {
        var emailLayoutTemplate = context.GetOrNull(
            StandardEmailTemplates.Message);

        emailLayoutTemplate
            .WithVirtualFilePath(
                "/Emailing/Templates/EmailTemplate.tpl",
                isInlineLocalized: true
            );
    }
}
```

### 註冊

```
public class MyProjectDomainModule : AbpModule
{
    public override void ConfigureServices(
        ServiceConfigurationContext context)
    {
        // ...

        //Add this configuration
        Configure<AbpVirtualFileSystemOptions>(options=>{
            options.FileSets.AddEmbedded<MyProjectDomainModule>();});
    }
}
```

### 發信

```
using System.Threading.Tasks;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Emailing;
using Volo.Abp.Emailing.Templates;
using Volo.Abp.TextTemplating;

namespace TemplateReplace.Emailing
{
    public class EmailService : ITransientDependency
    {
        private readonly IEmailSender _emailSender;
        private readonly ITemplateRenderer _templateRenderer;

        public EmailService(IEmailSender emailSender,
            ITemplateRenderer templateRenderer)
        {
            _emailSender = emailSender;
            _templateRenderer = templateRenderer;
        }

        public async Task SendAsync(string targetEmail)
        {
            var emailBody = await _templateRenderer.RenderAsync(
                StandardEmailTemplates.Message,
                new
                {
                    message = "ABP Framework provides
                        IEmailSender service that is used to send emails."
                }
            );

            await _emailSender.SendAsync(
                targetEmail,
                "Subject",
                emailBody
            );
        }
    }
}
```

### 參照

[Replacing Email Templates and Sending Emails | ABP Community](https://community.abp.io/posts/replacing-email-templates-and-sending-emails-jkeb8zzh)

[Text Templating | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Text-Templating)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- MAIL

- 回首頁

---

*本文章從點部落遷移至 Writerside*
