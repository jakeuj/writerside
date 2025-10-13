# ABP (ASP.NET Boilerplate) 應用程式開發框架 No.12 複數資料庫(DBContext)

> **原文發布日期:** 2019-01-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/01/30/abp12
> **標籤:** 無

---

ABP (ASP.NET Boilerplate) 應用程式開發框架 No.12 複數資料庫(DBContext)

2019/5/7

參照：<https://www.twblogs.net/a/5c23609bbd9eee16b3db438c/>

---

2019/4/30

終於成功呼叫同一支API來使用兩個不同資料庫...

步驟有空再補

總之參考以下範例即可

<https://github.com/aspnetboilerplate/aspnetboilerplate-samples/tree/master/MultipleDbContextEfCoreDemo>

---

今天試了一下兩個資料連接字串

同一個專案分別連到不同資料庫

這邊記錄一下步驟以備不時之需

0.測試環境：

本次專案名稱為PlatRazor

因此預設會有一個DB叫做PlatRazorDb

然後我要加入另一個DB=EventCloudDb

1.建立實體：這部分不變

```

public class Game : Entity
{
    public virtual string Name { get; set; }
}
```

2.建立上下文(DbContext)：

這邊我複製了一份PlatRazorDbContext.cs

重命名PlatRazor=>EventCloud

然後一樣把實體加進去

EventCloudDbContext.cs

```

public class EventCloudDbContext : AbpDbContext
{
    public DbSet<Game> Games { get; set; }
    public EventCloudDbContext(DbContextOptions<EventCloudDbContext> options)
        : base(options)
    {

    }
}
```

這裡就是把你準備要放到另一個資料庫的實體

都加到這個新的DbContext

3.然後是PlatRazorDbContextFactory.cs

這檔案裡面說是用來跑migration指令用的

總之一樣複製後重新命名PlatRazor=>EventCloud

EventCloudDbContextFactory.cs

```

public class EventCloudDbContextFactory : IDesignTimeDbContextFactory<EventCloudDbContext>
{
    public EventCloudDbContext CreateDbContext(string[] args)
    {
        var builder = new DbContextOptionsBuilder<EventCloudDbContext>();
        var configuration = AppConfigurations.Get(WebContentDirectoryFinder.CalculateContentRootFolder());

        DbContextOptionsConfigurer.Configure(
        builder,
        configuration.GetConnectionString(PlatRazorConsts.EventCloudConnectionStringName)
        );

        return new EventCloudDbContext(builder.Options);
    }
}
```

這裡有一個 PlatRazorConsts.EventCloudConnectionStringName

他在核心層的 PlatRazorConsts.cs

就字串常量，把我們的連結字串名稱加進去

public const string EventCloudConnectionStringName = "EventCloud";

```

public class PlatRazorConsts
{
    public const string LocalizationSourceName = "PlatRazor";

    public const string ConnectionStringName = "Default";

    public const string EventCloudConnectionStringName = "EventCloud";
}
```

4.appsettings.json

剛剛既然定義了連接字串的名稱

那當然要用這名子加到連結字串設定裡面

"EventCloudDb": "Server=::1; Database=EventCloudDb;User ID=xxx;Password=xxxxxx;"

```

{
  "ConnectionStrings": {
    "Default": "Server=::1; Database=PlatRazorDb;User ID=xxx;Password=xxxxxx;",
    "EventCloudDb": "Server=::1; Database=EventCloudDb;User ID=xxx;Password=xxxxxx;"
  },
  "Logging": {
    "IncludeScopes": false,
    "LogLevel": {
      "Default": "Debug",
      "System": "Information",
      "Microsoft": "Information"
    }
  }
}
```

上一行最後記得加個逗號

5.Startup.cs

根據官方文件其實要設定資料庫就是要從這檔案來設定

```

//Configure DbContext
services.AddAbpDbContext<PlatRazorDbContext>(options =>
{
    DbContextOptionsConfigurer.Configure(options.DbContextOptions, options.ConnectionString);
});
```

一樣複製原本的重新命名PlatRazor=>EventCloud

```

public IServiceProvider ConfigureServices(IServiceCollection services)
{
    //Configure DbContext
    services.AddAbpDbContext<PlatRazorDbContext>(options =>
    {
        DbContextOptionsConfigurer.Configure(options.DbContextOptions, options.ConnectionString);
    });

    services.AddAbpDbContext<EventCloudDbContext>(options =>
    {
        DbContextOptionsConfigurer.Configure(options.DbContextOptions, options.ConnectionString);
    });

    services.AddMvc(options =>
    {
        options.Filters.Add(new AutoValidateAntiforgeryTokenAttribute());
    });

    //Configure Abp and Dependency Injection
    return services.AddAbp<PlatRazorWebModule>(options =>
    {
        //Configure Log4Net logging
        options.IocManager.IocContainer.AddFacility<LoggingFacility>(
            f => f.UseAbpLog4Net().WithConfig("log4net.config")
        );
    });
}
```

6.DbContextOptionsConfigurer.cs

上一步會發現設定部分會找不到對應型別的設定檔

官方文件其實是長這樣

```

services.AddDbContext<MyDbContext>(options =>
{
    options.UseSqlServer(Configuration.GetConnectionString("Default"));
});
```

但開出來的專案實際是長這樣

```

DbContextOptionsConfigurer.Configure(options.DbContextOptions, options.ConnectionString);
```

總之呢他把原本的設定統一移動到 DbContextOptionsConfigurer.cs 來做設定

 /\* This is the single point to configure DbContextOptions for PlatRazorDbContext \*/

一樣複製裡頭的內容來重新命名PlatRazor=>EventCloud

```

public static class DbContextOptionsConfigurer
{
    public static void Configure(
        DbContextOptionsBuilder<PlatRazorDbContext> dbContextOptions,
        string connectionString
        )
    {
        /* This is the single point to configure DbContextOptions for PlatRazorDbContext */
        dbContextOptions.UseSqlServer(connectionString);
    }

    public static void Configure(
        DbContextOptionsBuilder<EventCloudDbContext> dbContextOptions,
        string connectionString
        )
    {
        dbContextOptions.UseSqlServer("Server=::1; Database=EventCloudDb;User ID=xxx;Password=xxxxxx;");
    }
}
```

這裡我是先寫死連結字串

因為他好像是吃PlatRazorWebModule=>PreInitialize預設的連結字串

```

Configuration.DefaultNameOrConnectionString = _appConfiguration.GetConnectionString(PlatRazorConsts.ConnectionStringName);
```

TODO:DbContextOptionsConfigurer.cs改吃appsettings.json

7.migration

簡單來說就是指令都要指定 DbContext

```

PM> Add-Migration Init -Context PlatRazorDbContext

PM> Update-Database -Context PlatRazorDbContext

PM> Add-Migration Init -Context EventCloudDbContext

PM> Update-Database -Context EventCloudDbContext
```

8.應用服務層

用起來是跟原本一樣的

```

public class GameAppService : PlatRazorAppServiceBase,IGameAppService
{
    private readonly IRepository<Game> _gameRepository;
    public GameAppService(IRepository<Game> gameRepository)
    {
        _gameRepository = gameRepository;
    }
    public void CreateGame()
    {
        _gameRepository.Insert(new Game(){Name = "B"});
    }
}
```

9.動態WebApi或是Controller

如果是WebApi可以直接執行然後訪問測試了

應該是 http://localhost:62114/api/services/app/gameApp/createGame

Controller就要把應用服務注入之後呼叫

```

public class HomeController : PlatRazorControllerBase
{
    private readonly IGameAppService _gameAppService;
    public HomeController(IGameAppService gameAppService)
    {
        _gameAppService = gameAppService;
    }
    public ActionResult Index()
    {
        _gameAppService.CreateGame();
        return View();
    }

    public ActionResult About()
    {
        return View();
    }
}
```

亂打得這樣每次開出首頁就會新增一筆紀錄到資料庫

10.資料庫

沒意外了話到資料庫裡面應該會發現有新資料寫入

原本的DB一樣建立Service來呼叫應該也會正常有資料

11.But,人生中最重要的就是這個But!

在一同一次request調用不同DbContext的service會報錯

`System.InvalidOperationException: 'The specified transaction is not associated with the current connection. Only transactions associated with the current connection may be used.'`

同一個req會共用同一個連線，另外Unit of Work會建立交易，但跨資料庫無法建立交易的樣子

12.TODO

## Add EfCoreTransactionStrategy to share transactions

參考連結：[GitHub PR #1834](https://github.com/aspnetboilerplate/aspnetboilerplate/pull/1834#issuecomment-283948116)

## IConnectionStringResolver

參考文檔：[Entity Framework Core Configuration](https://aspnetboilerplate.com/Pages/Documents/Entity-Framework-Core#configuration)

ABP can use IConnectionStringResolver to determine it. This behaviour can be changed and the connection string can be determined dynamically.

You should implement and replace IConnectionStringResolver. In this custom service you can check dbcontext type (or other logic) to determine connection string dynamically.

[DbPerTenantConnectionStringResolver](https://github.com/aspnetboilerplate/module-zero-forsaken/blob/dev/src/Abp.ZeroCore.EntityFrameworkCore/Zero/EntityFrameworkCore/DbPerTenantConnectionStringResolver.cs)

參照：

[ABP Entity Framework Core](https://aspnetboilerplate.com/Pages/Documents/Entity-Framework-Core#configuration)

[ABP 基礎設施層- 集成Entity Framework Core](https://www.52abp.com/wiki/abp-cn/latest/9.3ABP%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BD%E5%B1%82-%E9%9B%86%E6%88%90EntityFrameworkCore)
{ignore-vars="true"}

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
