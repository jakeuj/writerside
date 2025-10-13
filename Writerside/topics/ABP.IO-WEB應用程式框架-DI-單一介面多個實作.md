# ABP.IO WEB應用程式框架 DI 單一介面多個實作

> **原文發布日期:** 2023-03-03
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/03/03/abp-dealing-with-multiple-implementations
> **標籤:** 無

---

簡單筆記下如何統一呼叫共用介面的複數實作 (class)

結論

`ITestManager`

```
public interface ITestManager
{
    string GetString();
}
```

`OneManager`

```
public class OneManager : ITestManager
{
    public string GetString() => "One";
}
```

`TwoManager`

```
public class TwoManager : ITestManager
{
    public string GetString() => "Two";
}
```

`TestDomainModule`

```
public class TestDomainModule : AbpModule
{
    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        // 手動新增 DI 設定
        context.Services.AddTransient<ITestManager, OneManager>();
        context.Services.AddTransient<ITestManager, TwoManager>();
    }
}
```

`TestDomainTests`

```
[Fact]
public async Task Should_Get_Two_Results_From_ITestManager()
{
    var managers = GetRequiredService<IEnumerable<ITestManager>>();
    var results = managers.Select(manager => manager.GetString()).ToList();

    results.Count.ShouldBeGreaterThan(1);

    _testOutputHelper.WriteLine(string.Join(",",results));
}
```

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/613502e6-c51a-4cb0-b1c8-aaf784120550/1677825290.png.png)

重點

1. 手動註冊每個實作到該介面
2. 改取得 IEnumerable 該介面

參照

[依賴注入 |文檔中心 |總部基地。IO (abp.io)](https://docs.abp.io/en/abp/latest/Dependency-Injection#dealing-with-multiple-implementations)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* 回首頁

---

*本文章從點部落遷移至 Writerside*
