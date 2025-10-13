# PowerShell DotNetCore Background Task Queue

> **原文發布日期:** 2021-04-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/04/28/PowerShellNetCoreQueue
> **標籤:** 無

---

* DotnetCore Web API
* Background Queue 背景佇列工作
* PowerShell Script

輸出[結果](https://github.com/jakeuj/PowerShellNetCoreQueue)

```
info: JobAPI.QueuedHostedService[0]
      Queued Hosted Service is running.
info: Microsoft.Hosting.Lifetime[0]
      Now listening on: https://localhost:5001
info: Microsoft.Hosting.Lifetime[0]
      Now listening on: http://localhost:5000
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Development
info: Microsoft.Hosting.Lifetime[0]
      Content root path: JobAPI
info: JobAPI.Controllers.WeatherForecastController[0]
      加入一個 30 秒的 PowerShell 作業
info: JobAPI.Controllers.WeatherForecastController[0]
      開始一個 30 秒的 PowerShell 作業 155e8c0c-13dd-43ff-b506-d09eaf0a0b2b
info: JobAPI.Controllers.WeatherForecastController[0]
      加入一個 25 秒的 PowerShell 作業
info: JobAPI.Controllers.WeatherForecastController[0]
      加入一個 20 秒的 PowerShell 作業
info: JobAPI.Controllers.WeatherForecastController[0]
      完成一個 30 秒的 PowerShell 作業 155e8c0c-13dd-43ff-b506-d09eaf0a0b2b
info: JobAPI.Controllers.WeatherForecastController[0]
      開始一個 25 秒的 PowerShell 作業 c7f00d7c-7fd8-46e4-a777-3a921bf4c25c
info: JobAPI.Controllers.WeatherForecastController[0]
      完成一個 25 秒的 PowerShell 作業 c7f00d7c-7fd8-46e4-a777-3a921bf4c25c
info: JobAPI.Controllers.WeatherForecastController[0]
      開始一個 20 秒的 PowerShell 作業 471b2916-cd4e-4615-a90e-fdfced026ad0
info: JobAPI.Controllers.WeatherForecastController[0]
      完成一個 20 秒的 PowerShell 作業 471b2916-cd4e-4615-a90e-fdfced026ad00
```

---

首先開一個 [WebAPI](https://github.com/jakeuj/PowerShellNetCoreQueue) 專案

參照官方 [MSDN](https://docs.microsoft.com/zh-tw/aspnet/core/fundamentals/host/hosted-services?view=aspnetcore-5.0&tabs=visual-studio#queued-background-tasks) 把 [BackgroundTaskQueue](https://github.com/dotnet/AspNetCore.Docs/blob/main/aspnetcore/fundamentals/host/hosted-services/samples/3.x/BackgroundTasksSample/Services/BackgroundTaskQueue.cs) 與 [QueuedHostedService](https://github.com/dotnet/AspNetCore.Docs/blob/main/aspnetcore/fundamentals/host/hosted-services/samples/3.x/BackgroundTasksSample/Services/QueuedHostedService.cs) 搬進去

[BackgroundTaskQueue.cs](https://github.com/dotnet/AspNetCore.Docs/blob/main/aspnetcore/fundamentals/host/hosted-services/samples/3.x/BackgroundTasksSample/Services/BackgroundTaskQueue.cs)

```
public interface IBackgroundTaskQueue
{
    ValueTask QueueBackgroundWorkItemAsync(Func<CancellationToken, ValueTask> workItem);

    ValueTask<Func<CancellationToken, ValueTask>> DequeueAsync(
        CancellationToken cancellationToken);
}

public class BackgroundTaskQueue : IBackgroundTaskQueue
{
    private readonly Channel<Func<CancellationToken, ValueTask>> _queue;

    public BackgroundTaskQueue(int capacity)
    {
        // Capacity should be set based on the expected application load and
        // number of concurrent threads accessing the queue.
        // BoundedChannelFullMode.Wait will cause calls to WriteAsync() to return a task,
        // which completes only when space became available. This leads to backpressure,
        // in case too many publishers/calls start accumulating.
        var options = new BoundedChannelOptions(capacity)
        {
            FullMode = BoundedChannelFullMode.Wait
        };
        _queue = Channel.CreateBounded<Func<CancellationToken, ValueTask>>(options);
    }

    public async ValueTask QueueBackgroundWorkItemAsync(
        Func<CancellationToken, ValueTask> workItem)
    {
        if (workItem == null)
        {
            throw new ArgumentNullException(nameof(workItem));
        }

        await _queue.Writer.WriteAsync(workItem);
    }

    public async ValueTask<Func<CancellationToken, ValueTask>> DequeueAsync(
        CancellationToken cancellationToken)
    {
        var workItem = await _queue.Reader.ReadAsync(cancellationToken);

        return workItem;
    }
}
```

[QueuedHostedService.cs](https://github.com/dotnet/AspNetCore.Docs/blob/main/aspnetcore/fundamentals/host/hosted-services/samples/3.x/BackgroundTasksSample/Services/QueuedHostedService.cs)

```
public class QueuedHostedService : BackgroundService
{
    private readonly ILogger<QueuedHostedService> _logger;

    public QueuedHostedService(IBackgroundTaskQueue taskQueue,
        ILogger<QueuedHostedService> logger)
    {
        TaskQueue = taskQueue;
        _logger = logger;
    }

    public IBackgroundTaskQueue TaskQueue { get; }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation(
            $"Queued Hosted Service is running.{Environment.NewLine}" +
            $"{Environment.NewLine}Tap W to add a work item to the " +
            $"background queue.{Environment.NewLine}");

        await BackgroundProcessing(stoppingToken);
    }

    private async Task BackgroundProcessing(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var workItem =
                await TaskQueue.DequeueAsync(stoppingToken);

            try
            {
                await workItem(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,
                    "Error occurred executing {WorkItem}.", nameof(workItem));
            }
        }
    }

    public override async Task StopAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Queued Hosted Service is stopping.");

        await base.StopAsync(stoppingToken);
    }
}
```

AppSetting 加入 Queue 容量的設定

AppSetting.json

```
{
  "QueueCapacity": 10,
  // ...
}
```

Startup 設定 DI

Startup.cs

```
public void ConfigureServices(IServiceCollection services)
{
    services.AddHostedService<QueuedHostedService>();
    services.AddSingleton<IBackgroundTaskQueue>(ctx => {
        if (!int.TryParse(Configuration["QueueCapacity"], out var queueCapacity))
            queueCapacity = 100;
        return new BackgroundTaskQueue(queueCapacity);
    });
    // ...
}
```

Controller 注入 IBackgroundTaskQueue

```
private readonly IBackgroundTaskQueue _taskQueue;

public WeatherForecastController(IBackgroundTaskQueue taskQueue)
{
    _taskQueue = taskQueue;
}
```

安裝 PowerShell 套件

```
Install-Package Microsoft.PowerShell.SDK
```

寫一下 API 來新增工作排程

```
[HttpGet]
public async void Get(int sec=15)
{
    await _taskQueue.QueueBackgroundWorkItemAsync(async ct =>
    {
    	(await PowerShell.Create()
                .AddScript($"Start-Sleep -s {sec}")
                .InvokeAsync())
                .ToList()
                .ForEach(Console.WriteLine);
    });
}
```

其中 `Start-Sleep -s 15` 可以改成真正需要執行的 [PowerShell Script](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/start-sleep?view=powershell-7.1)

---

## 同場加映

### 改為呼叫外部 PowerShell Script 並傳遞參數

1.首先準備一個 PowerShell Script

c:\MyScript.ps1

```
param([int] $Sec)
'Waitting for {0} second...' -f $Sec
Start-Sleep -s $Sec
```

2.修改 API

```
[HttpGet]
public async void Get(int sec=15)
{
    await _taskQueue.QueueBackgroundWorkItemAsync(async ct =>
    {
    	(await PowerShell.Create()
                .AddCommand(@"C:\MyScript.ps1")
                .AddParameter("Sec", 10)
                .InvokeAsync())
                .ToList()
                .ForEach(Console.WriteLine);
    });
}
```

* `AddScript` 吃不到 `AddParameter` 所設定的參數
* `AddCommand` 裡面直接寫 Script 會無法執行
* `AddParameter` 可以設定多組 `.AddParameter("p1","1").AddParameter("p2","2")`

---

### 補充：PowerShell 語法範例

* 沒有就建立該資料夾

```
param([string] $Path)
if(-not(Test-Path $Path)) {New-Item $Path -ItemType "directory"}
```

### 桌面建立捷徑執行程式

`C:\Users\jakeu\AppData\Local\Microsoft\WindowsApps\Microsoft.WindowsTerminalPreview_8wekyb3d8bbwe\wt.exe dotnet "D:\Users\jakeu\RiderProjects\src\PowerShellNetCoreQueue\JobAPI\bin\Release\net5.0\publish\JobAPI.dll"`

---

參考 我的 Github Repo

<https://github.com/jakeuj/PowerShellNetCoreQueue>

參考 MSDN 的 Queue

<https://docs.microsoft.com/zh-tw/aspnet/core/fundamentals/host/hosted-services?view=aspnetcore-5.0&tabs=visual-studio#queued-background-tasks>

https://github.com/dotnet/AspNetCore.Docs/blob/main/aspnetcore/fundamentals/host/hosted-services/samples/3.x/BackgroundTasksSample/Program.cs

參考 MSDN 的 PowerShell

<https://docs.microsoft.com/zh-tw/powershell/scripting/learn/deep-dives/everything-about-string-substitutions?view=powershell-7.1#format-string>

Could not load file or assembly 'Microsoft.Management.Infrastructure

http://dog0416.blogspot.com/2020/06/aspnet-core-microsoftpowershellsdk-iis.html

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}
* .Net Core
{ignore-vars="true"}
* PowerShell

* 回首頁

---

*本文章從點部落遷移至 Writerside*
