# Mock

在測試中，我們有時候會遇到一些服務是需要遠端資料庫或 API 來取得資訊，但是這樣的服務在測試中會變得很困難，因為我們無法控制遠端服務的狀態，也無法確保遠端服務的可用性。

## 重點
- 要模擬的服務需要是介面 (IDomainManager) 而不是實現類 (DomainManager)
- 實際要測試的方法裡頭，需透過介面 (IDomainManager) 來注入該服務 (DomainManager)

## 情境
要測試 `_appService.GetAsync` 方法，而該方法裡頭會使用 `DemoManager.GetUser` 來呼叫遠端 API 來取得資訊，但該 API 限制只有正式環境可以訪問，所以我需要 MOCK 該方法，而不必實際呼叫該 API。

## Mock
Abp 提供了一個簡單的方法來模擬服務，這樣我們就可以在測試中使用模擬的服務，而不是真實的服務。
這樣我們就可以專注於測試我們的代碼，而不是依賴的服務。

```C#
protected override void AfterAddApplication(
    IServiceCollection services)
{
    var mockUser = new DemoUserObject { 
        Name = DemoConsts.DefaultName, 
        Ext = DemoConsts.DefaultExt 
    };
    
    var mockDemoManager = Substitute.For<IDemoManager>();
    
    // Mock GetUserExtAsync 方法
    mockDemoManager
        .GetUser(Arg.Any<string>())
        .Returns(mockUser);
    
    services.AddSingleton(mockDemoManager);
}
```

- 使用 `Substitute.For<IDemoManager>()` 來模擬服務
- 使用 `Arg.Any<string>()` 來模擬任何字串參數
- 使用 `Returns(mockUser)` 來模擬該方法的回傳值
- 使用 `services.AddSingleton(mockDemoManager)` 來注入模擬的服務

## Demo
完整範例如下：
```C#
using Microsoft.Extensions.DependencyInjection;
using NSubstitute;
using Shouldly;
using Volo.Abp;
using Volo.Abp.Json;
using Volo.Abp.Modularity;
using Xunit;
using Xunit.Abstractions;

namespace Demo;

/* This is just an example test class.
 * _testOutputHelper.WriteLine() is used to log the result of the test
 */
public abstract class DemoAppServiceTests<TStartupModule> 
    : DemoApplicationTestBase<TStartupModule>
        where TStartupModule : IAbpModule
{
    private readonly IDemoAppService _appService;

    private readonly ITestOutputHelper _testOutputHelper;

    protected NandPackageAppServiceTests(
            ITestOutputHelper testOutputHelper
        )
    {
        _testOutputHelper = testOutputHelper;
        _appService = GetRequiredService<IDemoAppService>();
    }

    protected override void AfterAddApplication(
            IServiceCollection services
        )
    {
        var mockUser = new DemoUserObject { 
                Name = DemoConsts.DefaultName, 
                Ext = DemoConsts.DefaultExt 
        };
            
        var mockDemoManager = Substitute.For<IDemoManager>();

        // Mock GetUserExtAsync 方法
        mockDemoManager
            .GetUser(Arg.Any<string>())
            .Returns(mockUser);
        
        services.AddSingleton(mockDemoManager);
    }

    [Fact]
    public async Task Should_Get_A_Demo()
    {
        // Arrange
        var req = new GetDemoRequest
        {
            Demo = NandConsts.TestDemo
        };

        // Act
        var result = await _appService.GetAsync(req);

        // Assert
        result.ShouldNotBeNull();
        result.Name.ShouldBe(NandConsts.DefaultName);
        result.Ext.ShouldBe(NandConsts.DefaultExt);

        // Log
        _testOutputHelper.WriteLine(
            GetRequiredService<IJsonSerializer>().Serialize(result));
    }
}
```