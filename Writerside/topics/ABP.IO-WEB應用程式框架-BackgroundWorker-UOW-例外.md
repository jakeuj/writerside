# ABP.IO BackgroundWorker UOW 例外

> **原文發布日期:** 2022-08-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/08/19/abp-Background-Job-uow
> **標籤:** 無

---

紀錄 HangfireBackgroundWorkerBase 的坑

## 徵狀

- Cannot access a disposed context instance
  - 使用 HangfireBackgroundWorkerBase 發生例外
- The Logger object is null
  - 使用介面設定 Hangfire Worker UOW 發生例外
- 資料沒有更新到資料庫
  - 記得 `SaveChanges`
  - 更新資料須將查到的或新增的 Entity 回傳給之後更新用

### 示意圖

![](https://user-images.githubusercontent.com/834156/185554747-f5091008-8fbd-4eb3-ad0a-be47dbb09133.png)

### 結論

Worker.cs

- 使用類別

```
using Hangfire;
using Volo.Abp.BackgroundWorkers.Hangfire;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Uow;

namespace T89NoUi.Workers;

public class UowModifiedWorker : HangfireBackgroundWorkerBase
    , IUowModifiedWorker
{
 private readonly OrderManager _orderManager;
    public UowModifiedWorker(OrderManager orderManager)
    {
        RecurringJobId = nameof(UowModifiedWorker);
        CronExpression = Cron.Minutely();
        _orderManager = orderManager;
    }

    public override async Task DoWorkAsync(
        CancellationToken cancellationToken = new CancellationToken())
    {
     Logger.LogDebug("Executed {@Name} ..!",MethodBase.GetCurrentMethod());
        using var uow = LazyServiceProvider
            .LazyGetRequiredService<IUnitOfWorkManager>().Begin();
        await orderManager.SaveAsync();
        await uow.SaveChangesAsync(cancellationToken);
    }
}
```

- 使用介面

```
using Hangfire;
using Volo.Abp.BackgroundWorkers.Hangfire;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Uow;

namespace T89NoUi.Workers;

public interface IUowModifiedWorker : IHangfireBackgroundWorker
{
}

[ExposeServices(typeof(IUowModifiedWorker), typeof(UowModifiedWorker))]
public class UowModifiedWorker : HangfireBackgroundWorkerBase
    , IUowModifiedWorker
{
    public UowModifiedWorker()
    {
        RecurringJobId = nameof(UowModifiedWorker);
        CronExpression = Cron.Minutely();
    }

    public override Task DoWorkAsync(
        CancellationToken cancellationToken = new CancellationToken())
    {
        using var uow = LazyServiceProvider
            .LazyGetRequiredService<IUnitOfWorkManager>().Begin();
        Logger.LogInformation($"Executed {nameof(UowModifiedWorker)} ..!");
        return Task.CompletedTask;
    }
}
```

Module.cs

```
public override async Task OnApplicationInitializationAsync(
    ApplicationInitializationContext context)
{
    await base.OnApplicationInitializationAsync(context);
    // 使用類別
    await context.AddBackgroundWorkerAsync<UowModifiedWorker>();

    // If the interface is defined
    // await context.AddBackgroundWorkerAsync<IUowModifiedWorker>();
}
```

### Issue

[The Logger object is null · Issue #12339 · abpframework/abp (github.com)](https://github.com/abpframework/abp/issues/12339)

### Doc

[Background Workers Hangfire | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Background-Workers-Hangfire#unitofwork)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP

- 回首頁

---

*本文章從點部落遷移至 Writerside*
