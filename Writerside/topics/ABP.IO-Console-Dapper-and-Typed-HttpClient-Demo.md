# ABP.IO Console Dapper and Typed HttpClient Demo

> **原文發布日期:** 2022-10-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/21/ABP-Console-Dapper-Typed-HttpClient-Demo
> **標籤:** 無

---

筆記下簡單的 Console 連資料庫並發送 API

## 參照

[Startup Templates/Console | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Startup-Templates/Console)

## 指令

* `dotnet tool install -g Volo.Abp.Cli`
* `abp new Acme.MyConsoleApp -t console -csf`
* `dotnet add Volo.Abp.Dapper`
* `dotnet add Microsoft.Data.SqlClient`
* `dotnet add Microsoft.Extensions.Http`

## Dapper

Entity

```
public class Order
{
    public Guid Id { get; set; }
    public string OrderNumber { get; set; }
}
```

Query

```
using var conn = new SqlConnection("connectionString");
var sql = "SELECT TOP 5 * FROM AppOrders";
var results = conn.Query<Order>(sql).ToList();
```

P.S. MySql 要用 Nuget 改裝 `MySql.Data` 然後改用 `MySqlConnection`

## Typed HttpClient

Test Client

```
public class TestClient
{
    private readonly HttpClient _client;
    public TestClient(HttpClient client)
    {
        _client = client;
    }
    public async Task<string>GetAccountAsync(string name)
    {
        var response = await _client.GetAsync($"/api/abp/multi-tenancy/tenants/by-name/{name}");
        return response.IsSuccessStatusCode ? response.Content.ReadAsStringAsync().Result : null;
    }
}
```

Module

```
private void ConfigureHttpClient(ServiceConfigurationContext context, IConfiguration configuration)
{
    context.Services.AddHttpClient<TestClient>(opt =>
    {
        if (Uri.TryCreate(configuration["BaseAddress"], UriKind.Absolute, out var uri))
        {
            opt.BaseAddress = uri;
        }
    });
}
```

Service

```
public class HelloWorldService : ITransientDependency
{
    public ILogger<HelloWorldService> Logger { get; set; }
    private readonly TestClient _client;

    public HelloWorldService(TestClient client)
    {
        _client = client;
        Logger = NullLogger<HelloWorldService>.Instance;
    }

    public async Task SayHelloAsync()
    {
        var response = await _client.GetAccountAsync("HelloWorld");
        Logger.LogDebug("Response: {@Response}",response);
    }
}
```

appsettings.secrets.json

```
{
  "ConnectionStrings": {
    "Default": "Server=(LocalDb)\\MSSQLLocalDB;Database=TestDb;Trusted_Connection=True"
  },
  "BaseAddress": "https://test-api-dev.azurewebsites.net"
}
```

## 結論

```
public class HelloWorldService : ITransientDependency
{
    public ILogger<HelloWorldService> Logger { get; set; }
    private readonly TestClient _client;
    private readonly IConfiguration _configuration;

    public HelloWorldService(TestClient client, IConfiguration configuration)
    {
        _client = client;
        _configuration = configuration;
        Logger = NullLogger<HelloWorldService>.Instance;
    }

    public async Task SayHelloAsync()
    {
        Logger.LogInformation("Hello World!");
        var connectionString = _configuration.GetConnectionString("Default");
        using var conn = new SqlConnection(connectionString);
        var sql = "SELECT TOP 5 * FROM AppOrders";
        var results = conn.Query<Order>(sql).ToList();
        Logger.LogDebug("{@Orders}",results);
        var orderNumber = results.FirstOrDefault()?.OrderNumber;
        Logger.LogDebug("Number: {@Number}",orderNumber);
        var response = await _client.GetAccountAsync(orderNumber);
        Logger.LogDebug("Response: {@Response}",response);
        Logger.LogInformation("Finish {@Method}!",nameof(SayHelloAsync));
    }
}
```

範例程式碼

[jakeuj/abp-console-samples: Abp console Dapper and HttpClient samples (github.com)](https://github.com/jakeuj/abp-console-samples)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Console
* Dapper
* HttpClinet

* 回首頁

---

*本文章從點部落遷移至 Writerside*
