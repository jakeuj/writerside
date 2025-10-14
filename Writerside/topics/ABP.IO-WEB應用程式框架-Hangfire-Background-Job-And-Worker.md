# ABP.IO Hangfire Background Job And Worker

> **原文發布日期:** 2022-04-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/04/26/abp-Hangfire-Background-Worker
> **標籤:** 無

---

筆記下背景定期執行工作

## 簡介

首先 ABP 有內建基本的 Background Worker 與 Background Job

這邊簡單釐清一下 Job 與 Worker 這兩個東西

* Job: API 觸發一個需要背景執行的作業時，呼叫 Job 來完成
  例如：產生報表 API 觸發一個 Job 後立即返回，該 Job 會花費十分鐘產生報表後，以信件寄出報表
  (連續觸發 Job 會進入 Queue 依序處理報表需求)
* Woker: 程式啟動時就開始按照既定排程來執行特定作業
  例如：定期刪除過期 Log、定期寄信

另外 ABP 有整合 Quartz 與 Hangfire 這兩個套件

功能比較強，內建儀表板，詳細功能請自行到對應官方網站了解

## 安裝

因應以下問題

[如果您決定使用 Hangfire 作為後台 Worker/Job #2940，DbMigrator 將不再起作用|支援中心|總部基地商業 (abp.io)](https://support.abp.io/QA/Questions/2940/DbMigrator-will-not-be-functional-anymore-if-you-decide-to-use-Hangfire-as-Background-WorkerJob)

1. Domain
   * PS> dotnet add package Volo.Abp.BackgroundWorkers.Hangfire
2. Host (Web)
   * PS> dotnet add package Volo.Abp.BackgroundJobs.HangFire
   * PS> dotnet add package [Hangfire.SqlServer](https://www.nuget.org/packages/Hangfire.SqlServer)
   * HostModule > DependsOn
     + typeof(AbpBackgroundWorkersHangfireModule)
     + typeof(AbpBackgroundJobsHangfireModule)
   * HostModule > context.Services.AddHangfire
     + config.UseSqlServerStorage(configuration.GetConnectionString("Default"));

P.S. **Hangfire.SqlServer 版本需與 Volo.Abp.BackgroundJobs.HangFire 中使用的 Hangfire 一致**

### Sample

```
[DependsOn(
    //...other dependencies
    //Add the new module dependency
    typeof(AbpBackgroundJobsHangfireModule),
    typeof(AbpBackgroundWorkersHangfireModule)
    )]
public class YourHostModule : AbpModule
{
  private void ConfigureHangfire(ServiceConfigurationContext context, IConfiguration configuration)
  {
    context.Services.AddHangfire(config =>
    {
        config.UseSqlServerStorage(configuration.GetConnectionString("Default"));
        // 預設任務失敗會自動重試，如果不想要可以用下面這段來設定重試次數
        // config.UseFilter(new AutomaticRetryAttribute { Attempts = 0 });
    });
  }
}
```

這樣 Migratior 可以正常運作，Job 與 Worker 可以寫在 Domain 層

P.S. Job 與 Worker 不需要與表現層互動，放在 Domain

## Volo.Abp.OpenIddict.Domain 目錄結構

GitHub 路徑：
- [Volo.Abp.OpenIddict.Domain](https://github.com/abpframework/abp/tree/dev/modules/openiddict/src/Volo.Abp.OpenIddict.Domain)
- [Volo](https://github.com/abpframework/abp/tree/dev/modules/openiddict/src/Volo.Abp.OpenIddict.Domain/Volo)
- [Abp](https://github.com/abpframework/abp/tree/dev/modules/openiddict/src/Volo.Abp.OpenIddict.Domain/Volo/Abp)
- [OpenIddict](https://github.com/abpframework/abp/tree/dev/modules/openiddict/src/Volo.Abp.OpenIddict.Domain/Volo/Abp/OpenIddict)
- [Tokens](https://github.com/abpframework/abp/tree/dev/modules/openiddict/src/Volo.Abp.OpenIddict.Domain/Volo/Abp/OpenIddict/Tokens)

### 參照

[Background Jobs | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Background-Jobs)

[Background Workers Hangfire | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Background-Workers-Hangfire#using-the-abp-cli)

[abp/TokenCleanupBackgroundWorker.cs at dev · abpframework/abp (github.com)](https://github.com/abpframework/abp/blob/dev/modules/openiddict/src/Volo.Abp.OpenIddict.Domain/Volo/Abp/OpenIddict/Tokens/TokenCleanupBackgroundWorker.cs)

## 實作

參照：[Background Workers Hangfire | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Background-Workers-Hangfire#create-a-background-worker)

實際上要執行的作業需要繼承 HangfireBackgroundWorkerBase 並實作 `DoWorkAsync`

備註：HangfireBackgroundWorkerBase : BackgroundWorkerBase, IHangfireBackgroundWorker

```
public class MyLogWorker : HangfireBackgroundWorkerBase
{
    public MyLogWorker()
    {
        RecurringJobId = nameof(MyLogWorker);
        CronExpression = Cron.Daily();
    }

    public override Task DoWorkAsync()
    {
        Logger.LogInformation("Executed MyLogWorker..!");
        return Task.CompletedTask;
    }
}
```

## 註冊

最後在模塊的應用程式初始化階段加入該背景作業

`context.AddBackgroundWorkerAsync<MyLogWorker>();`

```
[DependsOn(typeof(AbpBackgroundWorkersModule))]
public class MyModule : AbpModule
{
    public override async Task OnApplicationInitializationAsync(
        ApplicationInitializationContext context)
    {
        await base.OnApplicationInitializationAsync(context);
        context.AddBackgroundWorkerAsync<MyLogWorker>();

        //If the interface is defined
        //await context.AddBackgroundWorkerAsync<IMyLogWorker>();

    }
}
```

## Queue

### **注意**

需更新至 ABP 7.0.0 版本才能正常使用 Queue, 之前的版本有 BUG 一律都會跑

[Hangfire background job unable specific queues · Issue #13789 · abpframework/abp (github.com)](https://github.com/abpframework/abp/issues/13789)

### Info

預設 Queue 為 default

可以依照需求

指定 Server 要跑那些 Queue

[abp/AbpHangfireOptions.cs at dev · abpframework/abp (github.com)](https://github.com/abpframework/abp/blob/dev/framework/src/Volo.Abp.HangFire/Volo/Abp/Hangfire/AbpHangfireOptions.cs)

appsettings.json

```
{
  "AbpHangfireOptions" : {
    "ServerOptions": {
      "Queues": [
        "default1"
      ]
    }
  }
}
```

HostModule

```
private void ConfigureAbpHangfire(IConfiguration configuration)
{
    Configure<AbpHangfireOptions>(configuration.GetSection(nameof(AbpHangfireOptions)));
}
```

指定 Worker 跑在哪個 Queue

```
public class QueueWork : HangfireBackgroundWorkerBase
{
    public QueueWork()
    {
        RecurringJobId = nameof(QueueWork);
        CronExpression = Cron.Minutely();
        // 只會由具有以下 Queue 名稱的 Server 執行
        Queue = "queue1";
    }

    public override Task DoWorkAsync(CancellationToken cancellationToken = new CancellationToken())
    {
        Logger.LogInformation("Executed QueueWork..!");
        return Task.CompletedTask;
    }
}
```

P.S. 這邊由於 Woker 指定由 `queue1` Queue執行，而 Server 並無設定要處理此 Queue (`queue1`)，因此不會處理

Job 版本指定 queue

```
public class TestJob
    : AsyncBackgroundJob<TestArgs>, ITransientDependency
{
    [Queue("queue1")]
    public override Task ExecuteAsync(EdiTestArgs args)
    {
        Logger.LogInformation("Do something...");
        return Task.CompletedTask;
    }
}
```

## 例外

參照：[AbpBackgroundWorkersHangfireModule exception without using hangfire configuration](https://support.abp.io/QA/Questions/2795/AbpBackgroundWorkersHangfireModule-exception-without-using-hangfire-configuration-after-upgrade-still-same-issue)

我實際跑的時候會遇到錯誤

```
JobStorage.Current property value has not been initialized.
You must set it before using Hangfire Client or Server API.
```

需要再加上一行 Code

GlobalConfiguration.Configuration.UseSqlServerStorage(configuration.GetConnectionString("Default"));

如下所示

```
private void ConfigureHangfire(ServiceConfigurationContext context, IConfiguration configuration)
{
    context.Services.AddHangfire(config =>
    {
        config.UseSqlServerStorage(configuration.GetConnectionString("Default"));
    });
    GlobalConfiguration.Configuration.UseSqlServerStorage(configuration.GetConnectionString("Default"));
}
```

## 儀錶板

1. UseHangfireDashboard 應該在你的 Startup 類中的認證和授權中間件之後被調用（可能在最後一行）。
   否則，授權將總是失敗。
2. UseHangfireDashboard 應該在 app.UseConfiguredEndpoints() 之前添加到請求管道。

要求登入使用者具有指定權限名稱 `MyHangFireDashboardPermissionName`

```
// ...
app.UseAuthentication();
// ...
app.UseAuthorization();
// ...
app.UseHangfireDashboard("/hangfire", new DashboardOptions
{
    AsyncAuthorization = new[]
    {
        new AbpHangfireAuthorizationFilter(
            requiredPermissionName: "MyHangFireDashboardPermissionName")
    }
});
app.UseConfiguredEndpoints();
```

僅要求登入

```
app.UseHangfireDashboard("/hangfire", new DashboardOptions
{
    AsyncAuthorization = new[] { new AbpHangfireAuthorizationFilter() }
});
```

全開放

```
app.UseHangfireDashboard();
```

## 參照

[Background Jobs Hangfire | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Background-Jobs-Hangfire#abphangfireauthorizationfilter)

[cron - Wikipedia](https://en.wikipedia.org/wiki/Cron#CRON_expression)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Hangfire

* 回首頁

---

*本文章從點部落遷移至 Writerside*
