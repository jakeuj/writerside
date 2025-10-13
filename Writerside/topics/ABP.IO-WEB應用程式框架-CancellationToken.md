# ABP.IO WEB應用程式框架 CancellationToken

> **原文發布日期:** 2023-05-11
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/05/11/ABP-Cancellation-Token-Provider
> **標籤:** 無

---

筆記下 CancellationToken 的一些東西

## 介紹

### ICancellationTokenProvider

使用 ABP 提供的 `ICancellationTokenProvider`

```
public class TestAppService : ProjectNameAppService
{
    private readonly TestManager _manager;
    private readonly ICancellationTokenProvider _cancellationTokenProvider;

    public TestAppService(TestManager manager, ICancellationTokenProvider cancellationTokenProvider)
    {
        _manager = manager;
        _cancellationTokenProvider = cancellationTokenProvider;
    }

    public async Task<int> GetAsync()
    {
        return await _manager.GetTestDataAsync(cancellationToken: _cancellationTokenProvider.Token);
    }
}
```

通常，應將 `CancellationToken` 傳遞給方法的參數以使用它。

有了 `ICancellationTokenProvider` 您無需為每種方法傳遞。

可以使用依賴項注入進行注入，並從其來源提供令牌。

P.S. 例如 API 則為 `Request.HttpContext.RequestAborted`

[Cancellation Token Provider | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Cancellation-Token-Provider)

### CancellationToken

原本每個 API 方法要傳入 `CancellationToken`

```
public class TestAppService : ProjectNameAppService
{
    private readonly TestManager _manager;

    public TestAppService(TestManager manager)
    {
        _manager = manager;
    }

    public async Task<int> GetAsync(CancellationToken cancellationToken = default)
    {
        return await _manager.GetTestDataAsync(cancellationToken: cancellationToken);
    }
}
```

[[ASP.NET Web API 2] 通過 CancellationToken 取消非同步請求 | 余小章 @ 大內殿堂 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/yc421206/2019/09/05/webapi_via_cancellationtokens_cancel_asyn_request)

### Request.HttpContext.RequestAborted

.Net 本身有個 `Request.HttpContext.RequestAborted` 可以用

```
public class TestAppService : ProjectNameAppService
{
    private readonly TestManager _manager;

    public TestAppService(TestManager manager)
    {
        _manager = manager;
    }

    public async Task<int> GetAsync()
    {
        return await _manager.GetTestDataAsync(cancellationToken: Request.HttpContext.RequestAborted);
    }
}
```

[ASP.NET 與 ASP․NET Core 偵測用戶端已斷線並自動取消非同步方法執行 | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2021/08/14/How-to-Cancel-a-Task-when-Client-Disconnected-in-ASPNET-Core)

### 測試

模擬一項作業預計花費一分鐘完成

```
public async Task<int> GetAsync()
{
    const int max = 60;
    var curr = 0;
    for (; curr < max; curr++)
    {
        if (_cancellationTokenProvider.Token.IsCancellationRequested)
        {
            Console.WriteLine("IsCancellationRequested {0}", curr);
            break;
        }

        await Task.Delay(1000);
    }
    Console.WriteLine("Current: {0}", curr);
    return curr;
}
```

假設有 `if (_cancellationTokenProvider.Token.IsCancellationRequested)`

使用 Swagger 呼叫該 API 9s 後將該頁面關閉

會發現的 LOG 顯示該 Request 費時約 9s

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/f150ebac-fe2a-4144-9a4c-c6af94a2ba53/1683798997.jpg.jpg)

反之即使提前關閉畫面還是需要消耗 60s 來完成該 API 呼叫

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/f150ebac-fe2a-4144-9a4c-c6af94a2ba53/1683799086.jpg.jpg)

## 結論

由此可知如果有將 CancellationToken 傳遞給該 API 所使用的非同步方法

EF ToListAsync, HttpClinet RequestAsync, Stream ReadAsync, Blob SaveAsync…ETC.

則可以在使用者提前取消 Request 時，節省消耗資源並提前完成該要求

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ASYNC
* 非同步
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
