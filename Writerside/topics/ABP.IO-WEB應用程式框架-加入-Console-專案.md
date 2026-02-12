# ABP.IO WEB應用程式框架 加入 Console 專案

> **原文發布日期:** 2022-02-11
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/02/11/abp-console
> **標籤:** 無

---

筆記將 Console 專案加到原本 ABP WebApplication 解決方案中

這將使 Console 得以呼叫位於應用層中的既有 Application Service

範例步驟大致上是

1. 新增一般 Abp Web 方案
2. 新增 Abp Console 方案
3. 將 Console 專案搬進 Web 方案
4. 於應用層新增一個測試應用服務
5. 於 Console 專案中呼叫應用層的服務

1.2. 首先使用 Abp Cli 建立兩種方案

`abp new MyProject`

`abp new MyProject  -t console`

1. 然後在 Web 方案中新增專案 `MyProject.ConsoleApp`

再把 Console 方案中的檔案複製貼上到新建的 `MyProject.ConsoleApp` 空專案中

編輯 `MyProject.ConsoleApp.csproj` 將 Console 用到的套件貼過去

參照 `MyProject.Web.csproj` 將 `<Import Project="..\..\common.props" />` 也貼過去 `MyProject.ConsoleApp.csproj`

範例：

```
<Project Sdk="Microsoft.NET.Sdk">
    <Import Project="..\..\common.props" />
    <PropertyGroup>
        <OutputType>Exe</OutputType>
        <TargetFramework>net6.0</TargetFramework>
        <ImplicitUsings>enable</ImplicitUsings>
        <Nullable>enable</Nullable>
    </PropertyGroup>
    <ItemGroup>
        <PackageReference Include="Volo.Abp.Autofac" Version="5.1.3" />
    </ItemGroup>

    <ItemGroup>
        <PackageReference Include="Microsoft.Extensions.Hosting" Version="6.0.0" />
        <PackageReference Include="Serilog.Extensions.Hosting" Version="4.1.2" />
        <PackageReference Include="Serilog.Extensions.Logging" Version="3.1.0" />
        <PackageReference Include="Serilog.Sinks.Async" Version="1.5.0" />
        <PackageReference Include="Serilog.Sinks.Console" Version="4.0.0" />
        <PackageReference Include="Serilog.Sinks.File" Version="5.0.0" />
    </ItemGroup>

    <ItemGroup>
        <Content Include="appsettings.json">
            <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
            <CopyToOutputDirectory>Always</CopyToOutputDirectory>
        </Content>
    </ItemGroup>

    <ItemGroup>
      <ProjectReference Include="..\MyProject.Application\MyProject.Application.csproj" />
    </ItemGroup>
</Project>
```

1. 於應用層建立一個應用服務

```
namespace MyProject.Application;

public class HelloWorldAppService : MyProjectAppService,IHelloWorldAppService
{
    public HelloWorldAppService(IAbpLazyServiceProvider lazyServiceProvider)
    {
        LazyServiceProvider = lazyServiceProvider;
    }
    public Task SayHelloAsync()
    {
        Logger.LogInformation("Hello World!");
        return Task.CompletedTask;
    }
}
```

基本跟原本建立應用服務流程一樣，建立Interface並繼承基底 `MyProjectAppService` 與該介面

其中特別注意的是 Logger 是使用消極載入，而其載入方式是由 `LazyServiceProvider` 提供

※ Logger 本身是唯讀，所以即使建構式注入 ILogger 也無法指派給 Logger

```
protected ILoggerFactory LoggerFactory => LazyServiceProvider.LazyGetRequiredService<ILoggerFactory>();
```

而 `LazyServiceProvider` 本身則是使用屬性注入，所以這邊要先在建構式注入 `IAbpLazyServiceProvider` ，再使用屬性注入到基底類別中的 `LazyServiceProvider`

```
public IAbpLazyServiceProvider LazyServiceProvider { get; set; }
```

好處是如果你建的 Sevice 不需要用到 Logger，他就不用建立 Logger 的 Instance，甚至你沒有要用到任何依賴，你也可以直接不注入 `IAbpLazyServiceProvider`

補充：消極載入倉儲，直到你呼叫的 API 裡頭有用到 `Repository` 他才會開始去檢查有沒有該實例，沒有再實例化 `Repository<Book, Guid>`

```
public IRepository<Book, Guid> Repository =>
 LazyServiceProvider.LazyGetRequiredService<IRepository<Book, Guid>>();
```

5.使用應用層中的服務

首先於新增的 ConsoleApp 專案加入參考 Application 專案的依賴

然後於 ConsoleAppHostedService 設定 `IHelloWorldAppService` 的 DI

```
options.Services.AddTransient<IHelloWorldAppService,HelloWorldAppService>();
```

並取得該服務並呼叫方法

```
var helloWorldService = _abpApplication.ServiceProvider.GetRequiredService<IHelloWorldAppService>();
await helloWorldService.SayHelloAsync();
```

範例：

```
public async Task StartAsync(CancellationToken cancellationToken)
{
    _abpApplication =  await AbpApplicationFactory.CreateAsync<ConsoleAppModule>(options =>
    {
        options.Services.ReplaceConfiguration(_configuration);
        options.Services.AddSingleton(_hostEnvironment);

        options.UseAutofac();
        options.Services.AddLogging(loggingBuilder => loggingBuilder.AddSerilog());

        options.Services.AddTransient<IHelloWorldAppService,HelloWorldAppService>();
    });

    await _abpApplication.InitializeAsync();

    var helloWorldService = _abpApplication.ServiceProvider.GetRequiredService<IHelloWorldAppService>();
    await helloWorldService.SayHelloAsync();
}
```

執行 ConsoleApp

```
[16:58:04 INF] Loaded ABP modules:
[16:58:04 INF] - MyProject.ConsoleApp.ConsoleAppModule
[16:58:04 INF]   - Volo.Abp.Autofac.AbpAutofacModule
[16:58:04 INF]     - Volo.Abp.Castle.AbpCastleCoreModule
[16:58:04 INF] MySettingName => MySettingValue
[16:58:04 INF] EnvironmentName => Production
[16:58:04 INF] Initialized all ABP modules.
[16:58:04 INF] Hello World!
[16:58:04 INF] Application started. Press Ctrl+C to shut down.
[16:58:04 INF] Hosting environment: Production
[16:58:04 INF] Content root path: D:\repos\MyAbpProject\src\MyProject.ConsoleApp\bin\Debug\net6.0
[16:58:08 INF] Application is shutting down...
```

正常可以看到 `Hello World!`

### 範例程式碼

[jakeuj/MyAbpProject (github.com)](https://github.com/jakeuj/MyAbpProject)

### 參照

[ABP.IO WEB應用程式框架 ABP Cli | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/11/26/Abp-Cli)

### 延伸閱讀

[.NET Core 5 Console 泛用主機 依照環境變數讀取對應設定檔 AppSetting | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/06/10/DotNetCoreConsoleAppsettingEnvironment)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- Console

- 回首頁

---

*本文章從點部落遷移至 Writerside*
