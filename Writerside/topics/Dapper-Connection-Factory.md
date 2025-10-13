# Dapper Connection Factory

> **原文發布日期:** 2021-12-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/12/30/Dapper-Connection-Factory
> **標籤:** 無

---

筆記下 Dapper 建立連線

`IConnectionFactory`

```
public interface IConnectionFactory
{
    IDbConnection GetConnection(string dbSettingName);
}
```

`ConnectionFactory`

```
public class ConnectionFactory : IConnectionFactory, ITransientDependency
{
    private readonly IConfiguration _configuration;

    public ConnectionFactory(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public IDbConnection GetConnection(string dbSettingName)
    {
        var connectionString = GetConnectionString(dbSettingName);
        return new SqlConnection(connectionString);
    }

    // Dapper
    public string GetConnectionString(string connectStringName)
    {
        var connectionString = _configuration.GetConnectionString(connectStringName);

        if (!string.IsNullOrWhiteSpace(connectionString))
	    {
        return connectionString;
        }

        throw new UserFriendlyException("Could not find a connection string definition for the application.
        Set IAbpStartupConfiguration.DefaultNameOrConnectionString or add a 'Default' connection string to application .config file.");
    }
}
```

`TestAppService`

```
public class TestAppService : BaseAppService
{
    private readonly IConnectionFactory _connectionFactory;
    public TestAppService(IConnectionFactory connectionFactory)
    {
        _connectionFactory = connectionFactory;
    }
    public async Task TestInsert()
    {
        using var dbConnection = _connectionFactory.GetConnection("TestDb");
        const string sql = @"SELECT * FROM TABLE";

        // No need to use using statement. Dapper will automatically
        // open, close and dispose the connection for you.
        return await dbConnection.QueryAsync<Diameter>(sql);
    }
}
```

BJ4

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP
* Dapper

* 回首頁

---

*本文章從點部落遷移至 Writerside*
