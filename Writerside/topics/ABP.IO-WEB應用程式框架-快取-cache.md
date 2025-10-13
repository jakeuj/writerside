# ABP.IO WEB應用程式框架 快取 cache

> **原文發布日期:** 2023-08-29
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/08/29/ABP-Caching
> **標籤:** 無

---

筆記下 `IDistributedCache<TCacheItem>`

## 必要知識

[ASP.NET Core 中的分散式快取 | Microsoft Learn](https://learn.microsoft.com/zh-tw/aspnet/core/performance/caching/distributed?view=aspnetcore-7.0)

### 優點

利用 `IDistributedCache` 可以快速在 in-memory 與 Redis 間切換

### .Net 問題

* 它使用 **byte arrays**而不是 .NET 物件。因此，您需要對需要緩存的物件進行 **序列化/反序列化**。
* 它為所有緩存項目提供了一個單一的鍵池，因此； 您需要使用鍵來區分不同類型的對象。 在多租戶系統中，您需要關注不同租戶的緩存項。

### ABP 增強

* 它在內部對緩存對象進行序列化/解序列化。默認使用 JSON 序列化，但可通過替換依賴注入系統中的 `IDistributedCacheSerializer` 服務來重載。
* 它會根據緩存中存儲的對像類型，自動為緩存鍵添加緩存名稱前綴。默認的緩存名稱是緩存項類的全名（如果緩存項類以 `CacheItem` 後綴結尾，則去掉 `CacheItem` 後綴）。
  您可以使用緩存項類上的 `CacheName` 屬性來設置緩存名稱。
* 它會自動將當前租戶 ID 添加到緩存密鑰中，以區分不同租戶的緩存項（如果您的應用程序是多租戶的）。
  如果想在多租戶應用程序中的所有租戶之間共享緩存對象，可在緩存項類上定義 `IgnoreMultiTenancy` 屬性來禁用此功能。
* 允許為每個應用程序定義一個全局緩存密鑰前綴，這樣不同的應用程序就可以在共享的分佈式緩存服務器中使用各自獨立的密鑰池。
* 它可以盡可能容忍錯誤，並繞過緩存。這在緩存服務器出現臨時問題時非常有用。
* 它擁有 `GetManyAsync` 和 `SetManyAsync` 等方法，能顯著提高批處理操作的性能。

### 範例

`CacheItem`

```
namespace MyProject
{
    public class BookCacheItem
    {
        public string Name { get; set; }

        public float Price { get; set; }
    }
}
```

`Service`

```
using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Caching.Distributed;
using Volo.Abp.Caching;
using Volo.Abp.DependencyInjection;

namespace MyProject
{
    public class BookService : ITransientDependency
    {
        private readonly IDistributedCache<BookCacheItem> _cache;

        public BookService(IDistributedCache<BookCacheItem> cache)
        {
            _cache = cache;
        }

        public async Task<BookCacheItem> GetAsync(Guid bookId)
        {
            return await _cache.GetOrAddAsync(
                bookId.ToString(), //Cache key
                async () => await GetBookFromDatabaseAsync(bookId),
                () => new DistributedCacheEntryOptions
                {
                    AbsoluteExpiration = DateTimeOffset.Now.AddHours(1)
                }
            );
        }

        private Task<BookCacheItem> GetBookFromDatabaseAsync(Guid bookId)
        {
            //TODO: get from database
        }
    }
}
```

### 參照

[Caching | Documentation Center | ABP. IO](https://docs.abp.io/zh-Hans/abp/latest/Caching)

[ASP.NET Core 中的分散式快取 | Microsoft Learn](https://learn.microsoft.com/zh-tw/aspnet/core/performance/caching/distributed?view=aspnetcore-7.0)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
