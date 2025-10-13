# ABP.IO WEB應用程式框架 Background Job

> **原文發布日期:** 2022-04-27
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/04/27/abp-Background-Job
> **標籤:** 無

---

筆記下射後不理背景執行工作

## 簡介

ABP 預設已經啟用內建的 Job 機制

直接使用可以參照官方文件 (摘錄在下方)

這邊主要提的是可以透過禁用 Job 來達到某些需求

※ 禁用 Job 只是不處理 Job，但是還是可以發布 Job

## 情境

雲端 API 提供上傳影片到 Storage 功能，另一方面需要進行後製並存到地端

此時可以透過 API 於作業完成時觸發後續處理的 Job 並立即返回成功上傳的訊息

因為後製與轉存到地端需要花費較長時間，為了避免佔用 API 伺服器資源，所以可以禁用 Job (參考下方摘錄)

另一方面於地端將站台架起來並將 Job 開啟 (因為地端不對外服務所以也可以改成 Console 來處理 Jobs)

這樣就可以利用地端服務器資源，將影片下載到地端並進行後製處理再存到地端存放區

如此達到雲端 API 射後不理，地端分散負載的目的

## 禁用

[Background Jobs | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Background-Jobs#disable-job-execution)

```
[DependsOn(typeof(AbpBackgroundJobsModule))]
public class MyModule : AbpModule
{
    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        Configure<AbpBackgroundJobOptions>(options =>
        {
            options.IsJobExecutionEnabled = false; //Disables job execution
        });
    }
}
```

## 使用

[Background Jobs | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Background-Jobs#queue-a-job-item)

1. 定義 Job 所需參數 class

```
public class EmailSendingArgs
{
  public string EmailAddress { get; set; }
  public string Subject { get; set; }
  public string Body { get; set; }
}
```

    2. 定義 Job (需繼承 `AsyncBackgroundJob` & `ITransientDependency` ) 並實作 `ExecuteAsync`

```
public class EmailSendingJob:
  AsyncBackgroundJob<EmailSendingArgs>,
  ITransientDependency
{
  private readonly IEmailSender _emailSender;

  public EmailSendingJob(IEmailSender emailSender)
  {
    _emailSender = emailSender;
  }

  public override async Task ExecuteAsync(EmailSendingArgs args)
  {
    await _emailSender.SendAsync(
      args.EmailAddress,
      args.Subject,
      args.Body
      );
   }
}
```

    3. 於 ApplicationService 在需要時呼叫 `IBackgroundJobManager.EnqueueAsync` 將作業加入

```
public class RegistrationService : ApplicationService
{
    private readonly IBackgroundJobManager _backgroundJobManager;

    public RegistrationService(IBackgroundJobManager backgroundJobManager)
    {
        _backgroundJobManager = backgroundJobManager;
    }

    public async Task RegisterAsync(string userName, string emailAddress, string password)
    {
        //TODO: Create new user in the database...

        await _backgroundJobManager.EnqueueAsync(
            new EmailSendingArgs
            {
                EmailAddress = emailAddress,
                Subject = "You've successfully registered!",
                Body = "..."
            }
        );
    }
}
```

## 延伸

[ABP.IO WEB應用程式框架 Hangfire Background Worker | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2022/04/26/abp-Hangfire-Background-Worker)

## 補充

可以藉由將 `AbpBackgroundJobOptions` 的 `IsJobExecutionEnabled` 改由 appsettings 設定

並利用 launchSettings 新增一個啟動專案的組態來複寫 `IsJobExecutionEnabled` 與 Port

來達到同時啟動兩個站台，其中一個不處理 Job 僅用來呼叫 API，同時另一個接收 Job 進行後續處理

來模擬運行在不同實體 (例如：雲端與地端)

appsettings.json

```
"Abp": {
  "IsJobExecutionEnabled": false
}
```

YourWebModule.cs

```
Configure<AbpBackgroundJobOptions>(options =>
{
    options.IsJobExecutionEnabled =
    Convert.ToBoolean(configuration["Abp:IsJobExecutionEnabled"]);
});
```

launchSettings.json

```
"TestHang.Web4Job": {
  "commandName": "Project",
  "launchBrowser": true,
  "environmentVariables": {
    "ASPNETCORE_ENVIRONMENT": "Development",
    "App__SelfUrl": "https://localhost:44383",
    "AuthServer__Authority": "https://localhost:44383",
    "Abp__IsJobExecutionEnabled": "true"
  },
  "applicationUrl": "https://localhost:44383/"
}
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
