# ABP.IO WEB應用程式框架 SendGrid 整合

> **原文發布日期:** 2023-02-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/02/13/ABP-SendGrid-IEmailSender-Attachments
> **標籤:** 無

---

使用 SendGrid 實作 IEmailSender 替換服務

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b138c20f-61ac-4c98-b4cf-928761b6730d/1676273155.png.png)

## 結論

### 1. Domain 專案安裝套件

安裝 SendGrid.Extensions.DependencyInjection

### Host (Web) 專案

設定 API KEY

appsetting.json

```
"SendGrid": {
    "ApiKey": "SG.xxxxxxxxxxx"
  }
```

設定 SendGrid 服務

SendGridTestWebModule

```
public override void ConfigureServices(ServiceConfigurationContext context)
{
    var hostingEnvironment = context.Services.GetHostingEnvironment();
    var configuration = context.Services.GetConfiguration();

    ConfigureAuthentication(context);
    ConfigureUrls(configuration);
    ConfigureBundles();
    ConfigureAutoMapper();
    ConfigureVirtualFileSystem(hostingEnvironment);
    ConfigureNavigationServices();
    ConfigureAutoApiControllers();
    ConfigureSwaggerServices(context.Services);

    // 設定 key
    context.Services.AddSendGrid(options =>
    {
        options.ApiKey = configuration["SendGrid:ApiKey"];
    });
}
```

到這邊是原本 SendGrid 初始化的部分

此時可以直接用 SendGrid 寄信了

接著是透過 ABP 的 `IEmailSender` 寄信的部分

好處是可以隨時替換寄信方式

例如內建 SMTP 或是 MailKit … ETC.

### 2. Domain 專案實作介面

ISendGridEmailSender

```
public interface ISendGridEmailSender : IEmailSender
{
}
```

SendGridEmailSender

```
using System;
using System.IO;
using System.Linq;
using System.Net.Mail;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using SendGrid;
using SendGrid.Helpers.Mail;
using Volo.Abp.BackgroundJobs;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Emailing;
using Attachment = SendGrid.Helpers.Mail.Attachment;

namespace SendGridTest.SendGrid;

[Dependency(ServiceLifetime.Transient, ReplaceServices = true)]
public class SendGridEmailSender : EmailSenderBase, ISendGridEmailSender
{
    private readonly ISendGridClient _sendGridClient;

    public SendGridEmailSender(
        IEmailSenderConfiguration configuration,
        IBackgroundJobManager backgroundJobManager,
        ISendGridClient sendGridClient)
        : base(configuration, backgroundJobManager)
    {
        _sendGridClient = sendGridClient;
    }

    protected override async Task SendEmailAsync(MailMessage mail)
    {
        var msg = new SendGridMessage()
        {
            From = new EmailAddress(mail.From?.Address, mail.From?.DisplayName),
            Subject = mail.Subject
        };

        if (mail.IsBodyHtml)
        {
            msg.HtmlContent = mail.Body;
        }
        else
        {
            msg.PlainTextContent = mail.Body;
        }

        mail.To.ToList().ForEach(t => msg.AddTo(new EmailAddress(t.Address, t.DisplayName)));
        mail.CC.ToList().ForEach(t => msg.AddCc(new EmailAddress(t.Address, t.DisplayName)));
        mail.Bcc.ToList().ForEach(t => msg.AddBcc(new EmailAddress(t.Address, t.DisplayName)));

        if (mail.Attachments.Any())
        {
            msg.Attachments = mail.Attachments.Select(t => new Attachment
            {
                Content = Convert.ToBase64String(t.ContentStream.GetAllBytes()),
                Filename = t.Name,
                Type = t.ContentType.MediaType,
                Disposition = "attachment"
            }).ToList();
        }

        var response = await _sendGridClient.SendEmailAsync(msg);

        if (response.StatusCode != System.Net.HttpStatusCode.Accepted)
        {
            var result = await response.Body.ReadAsStringAsync();
            throw new Exception(result);
        }
    }
}
```

至此就可以用 `IEmailSender` 寄信了

```
using System.Threading;
using System.Threading.Tasks;
using Volo.Abp.Emailing;

namespace SendGridTest.SendGrid;

public class SendGridAppService : SendGridTestAppService
{
    private readonly IEmailSender _emailSender;

    public SendGridAppService(IEmailSender emailSender)
    {
        _emailSender = emailSender;
    }

    public async Task GetAsync(CancellationToken cancellationToken)
    {
        await _emailSender.SendAsync("jakeuj@hotmail.com", "test", "test");
    }
}
```

但如果要在本機開發測試需要注意一下

SendGridTestDomainModule

```
#if DEBUG
    context.Services.Replace(ServiceDescriptor.Singleton<IEmailSender, NullEmailSender>());
#endif
```

需要把這行註解掉，不然會寄不出去

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b138c20f-61ac-4c98-b4cf-928761b6730d/1676273719.png.png)

## 測試

同上需要註解掉 NullEmailSender

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/b138c20f-61ac-4c98-b4cf-928761b6730d/1676273429.png.png)

SendGridTest.Domain.Tests > SampleDomainTests

```
[Fact]
public async Task Should_Get_Email_Of_A_User()
{
    var emailSender = GetRequiredService<IEmailSender>();

    using var stream = new MemoryStream();
    await stream.WriteAsync(Encoding.Default.GetBytes("Test"));
    stream.Position = 0;

    var mailMessage = new MailMessage("jakeuj@hotmail.com", "jakeuj@hotmail.com","test", "test")
    {
        //Stream contentStream, string? name, string? mediaType
        Attachments = { new Attachment(stream,"test.txt") }
    };

    await WithUnitOfWorkAsync(async () =>
    {
        await emailSender.SendAsync(mailMessage);
    });

    emailSender.ShouldNotBeNull();
}
```

SendGridTest.TestBase > SendGridTestTestBaseModule

```
public override void ConfigureServices(ServiceConfigurationContext context)
{
    Configure<AbpBackgroundJobOptions>(options =>
    {
        options.IsJobExecutionEnabled = false;
    });

    context.Services.AddAlwaysAllowAuthorization();

    context.Services.AddSendGrid(options =>
    {
        options.ApiKey = "SG.xxxxxxxxxxxxxxxxxx";
    });
}
```

這樣就可以發信，並且收到帶有附件的測試信，打開裡面應該是 `Test`

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- SendGrid

- 回首頁

---

*本文章從點部落遷移至 Writerside*
