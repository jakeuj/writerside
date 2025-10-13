# ABP.IO WEB應用程式框架 SendGrid

> **原文發布日期:** 2022-11-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/11/04/abp-SendGrid-STMP-587
> **標籤:** 無

---

筆記下使用 abp 內建 mail sender 發送到 sendgrid smtp 的方式

## 結論

### IEmailSender.SendAsync

```
using System.Threading.Tasks;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Emailing;

namespace MyProject
{
    public class MyService : ITransientDependency
    {
        private readonly IEmailSender _emailSender;

        public MyService(IEmailSender emailSender)
        {
            _emailSender = emailSender;
        }

        public async Task DoItAsync()
        {
            await _emailSender.SendAsync(
                "target@domain.com",     // target email address
                "Email subject",         // subject
                "This is email body..."  // email body
            );
        }
    }
}

```

P.S. IEmailSender 也有提供 QueueAsync 功能

### appsetings.json

```
"Settings": {
  "Abp.Mailing.DefaultFromAddress": "noreply@mydomain.com",
  "Abp.Mailing.DefaultFromDisplayName": "測試信件服務",
  "Abp.Mailing.Smtp.Host": "smtp.sendgrid.net",
  "Abp.Mailing.Smtp.Port": "587",
  "Abp.Mailing.Smtp.UserName": "apikey",
  "Abp.Mailing.Smtp.Password": "StringEncryption/DefaultPassPhrase/ApikKey=",
  "Abp.Mailing.Smtp.EnableSsl": "true",
  "Abp.Mailing.Smtp.UseDefaultCredentials": "false"
}
```

### 使用 ISettingEncryptionService 加密

```
public class EmailSettingProvider : SettingDefinitionProvider
{
    private readonly ISettingEncryptionService encryptionService;

    public EmailSettingProvider(ISettingEncryptionService encryptionService)
    {
        this.encryptionService = encryptionService;
    }

    public override void Define(ISettingDefinitionContext context)
    {
        var passSetting = context.GetOrNull("Abp.Mailing.Smtp.Password");
        if(passSetting!=null)
        {
            string debug = encryptionService.Encrypt(passSetting,"1q2w3e$R");
        }
    }
}
```

1. 將 SendGrid API KEY 取代 `"1q2w3e$R"`
2. 中斷點下在 debug 取得加密後的 string
3. 回填 `"Abp.Mailing.Smtp.Password"`
4. 刪除此類別 (只是為了取得加密後的 api key)

### 使用 SettingManager 加密

```

public class TemplateReplaceDomainModule : AbpModule
{
    public override void OnApplicationInitialization(
        ApplicationInitializationContext context)
    {
        var settingManager =
            context.ServiceProvider.GetService<SettingManager>();
        //encrypts the password on set and decrypts on get
        settingManager.SetGlobalAsync(
            EmailSettingNames.Smtp.Password, "your_password");
    }
}

```

1. 輸入密碼到 `your_password`
2. 到 DB 就可以到 AbpSetting 看到加密後的密碼
3. 刪除上面代碼 (只是為了取得加密後的 api key)

### 重點

* `"Abp.Mailing.Smtp.UserName"`
  + 保持 apikey 這六個英文字即可
* `"Abp.Mailing.Smtp.Password"`
  + 從 SendGrid 生成 API KEY
  + 使用 ABP 的 ISettingEncryptionService 加密
  + 將加密後的字串填入此設定值
  + appsettings.json:StringEncryption:DefaultPassPhrase 需一致
* `"Abp.Mailing.Smtp.EnableSsl": "true"`
* `"Abp.Mailing.Smtp.UseDefaultCredentials": "false"`
* `"Abp.Mailing.Smtp.Port": "587"`
  + Azure App Service 中只開放 587 port

### 參照

[Emailing | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Emailing#email-settings)

[Sending Email in abp io with SmtpEmailSender throwing The input is not a valid Base-64 string](https://stackoverflow.com/questions/67062083/sending-email-in-abp-io-with-smtpemailsender-throwing-the-input-is-not-a-valid-b)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure](/jakeuj/Tags?qq=Azure)
* [SendGrid](/jakeuj/Tags?qq=SendGrid)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
