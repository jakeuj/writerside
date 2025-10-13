# ABP.IO WEB應用程式框架 屬性注入

> **原文發布日期:** 2023-05-12
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/05/12/ABP-Dependency-Injection
> **標籤:** 無

---

筆記下 ABP 中使用屬性注入

## 結論

TestAppService

```
public class TestAppService : TestDiAppService
{
    private readonly ITestManager _testManager { get; set; }

    public TestAppService(ITestManager TestManager)
    {
        _testManager = TestManager;
    }

    public Task<string> GetAsync()
    {
        return _testManager.GetAsync();
    }
}
```

一般使用建構式注入方式，由建構式參數傳入 `ITestManager TestManager`

屬性注入則不由建構式參數傳入 `ITestManager TestManager`

將 `TestAppService(ITestManager TestManager)` 改為 `TestAppService()`

並將欄位改成屬性 `public ITestManager TestManager { get; set; }`

TestAppService

```
public class TestAppService : TestDiAppService
{
    public ITestManager TestManager { get; set; }

    public TestAppService()
    {
        TestManager = new NullManager();
    }

    public Task<string> GetAsync()
    {
        return TestManager.GetAsync();
    }
}
```

ITestManager

```
public interface ITestManager : IDomainService
{
    Task<string> GetAsync();
}
```

NullManager

```
public class NullManager:ITestManager
{
    public Task<string> GetAsync()
    {
        return Task.FromResult("Null");
    }
}
```

TestManager

```
public class TestManager : DomainService, ITestManager
{
    public Task<string> GetAsync()
    {
        return Task.FromResult("Hello World");
    }
}
```

Swagger

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/8903953f-bfa8-4bdc-b48c-ab305de9ece2/1683864476.png.png)

Hello World

## 參照

[Dependency Injection | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Dependency-Injection)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [DI](/jakeuj/Tags?qq=DI)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
