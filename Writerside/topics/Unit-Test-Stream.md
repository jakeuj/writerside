# Unit Test Stream

> **原文發布日期:** 2022-10-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/13/Unit-Test-Stream
> **標籤:** 無

---

筆記下單元測試遇到 Stream 時的測試方式

## 結論

```
using var stream = new MemoryStream();
stream.Write(Encoding.Default.GetBytes("Hello world."));
//stream.Position = 0;
```

其實只是 Stream 怎麼 New 並寫值進去而已

其中 `Position` 在進行 Storage 上傳之前必須歸零

不然會出現甚麼 資料位置需小於資料長度 的例外

這邊我把這動作統一在該服務內處理掉

省得每次呼叫前都要再歸零一次

因此在這邊測試程式碼就註解掉了

### 參照

```
using System.IO;
using System.Text;
using System.Threading.Tasks;
using EuOrder.AzureStorage.Excertis;
using Shouldly;
using Xunit;

namespace Order.AzureStorage;

public class AzureStorageDomainTest: OrderDomainTestBase
{
    private readonly PoContainerManager _manager;

    public AzureStorageDomainTest()
    {
        _manager = GetRequiredService<PoContainerManager>();
    }

    [Fact]
    public async Task Should_Get_Order()
    {
        // Arrange
        using var stream = new MemoryStream();
        stream.Write(Encoding.Default.GetBytes("Hello world."));
        //stream.Position = 0;

        //Act
        var result = await _manager.SaveAsync("test", stream);

        //Assert
        result.ShouldNotBeNull();
    }
}
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [UnitTest](/jakeuj/Tags?qq=UnitTest)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
