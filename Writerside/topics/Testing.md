# Testing

筆記下整合測試

```C#
using System.Linq;
using System.Threading.Tasks;
using Shouldly;
using Volo.Abp.Json;
using Xunit;
using Xunit.Abstractions;

namespace MyProject.MyAppServie;

public class MyAppServieTests: MyProjectApplicationTestBase
{
    private readonly ITestOutputHelper _testOutputHelper;

    public MyAppServieTests(ITestOutputHelper testOutputHelper)
    {
        _testOutputHelper = testOutputHelper;
    }

    [Fact]
    public async Task Initial_Data_Should_Be_9()
    {
        // Arrange
        var testAppService = GetRequiredService<IMyAppServie>();

        // Act
        var result = await WithUnitOfWorkAsync(async () => await testAppService.GetListAsync());

        // Assert
        result.Count().ShouldBe(9);

        // Log
        _testOutputHelper.WriteLine(GetRequiredService<IJsonSerializer>().Serialize(result));
    }
}
```

ITestOutputHelper 只能用建構式注入

IMyAppServie 可以整到建構式裡面取得 (如果多個方法會重複使用到該服務)

```C#
public class MyAppServieTests: MyProjectApplicationTestBase
{
    private readonly IMyAppServie _testAppService;
    
    private readonly ITestOutputHelper _testOutputHelper;

    public MyAppServieTests(ITestOutputHelper testOutputHelper)
    {
        _testAppService = GetRequiredService<IMyAppServie>();
    
        _testOutputHelper = testOutputHelper;
    }

    [Fact]
    public async Task Initial_Data_Should_Be_9()
    {
        // Arrange
        // var testAppService = GetRequiredService<IMyAppServie>();

        // Act
        var result = await WithUnitOfWorkAsync(async () => await _testAppService.GetListAsync());

        // Assert
        result.Count().ShouldBe(9);

        // Log
        _testOutputHelper.WriteLine(GetRequiredService<IJsonSerializer>().Serialize(result));
    }
}
```

## REF
[Testing](https://docs.abp.io/en/abp/latest/Testing)