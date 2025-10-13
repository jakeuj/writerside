# ABP.IO WEB應用程式框架 JSON

> **原文發布日期:** 2023-01-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/01/13/ABP-JSON
> **標籤:** 無

---

簡介 ABP JSON

## 結論

```
public class ProductManager
{
    public IJsonSerializer JsonSerializer { get; }

    public ProductManager(IJsonSerializer jsonSerializer)
    {
        JsonSerializer = jsonSerializer;
    }

    public void SendRequest(Product product)
    {
        var json=  JsonSerializer.Serialize(product);
        // Left blank intentionally for demo purposes...
    }
}
```

ABP框架提供了一個使用JSON的抽象.擁有這樣的抽象有一些好處;

* 您可以編寫獨立於庫的代碼。因此，您可以以最少的工作量和代碼更改來更改基礎庫。
* 您可以使用ABP中定義的預訂轉換器，而無需擔心底層庫的內部細節.

> JSON 序列化系統使用 Volo.Abp.Json NuGet 包實現
>
> （[Volo.Abp.Json.SystemTextJson](https://www.nuget.org/packages/Volo.Abp.Json.SystemTextJson) 是預設實現）。
>
> 大多數情況下，您不需要手動[安裝它](https://abp.io/package-detail/Volo.Abp.Json)，因為它預裝了[應用程式啟動範本](https://docs.abp.io/zh-Hans/abp/latest/Startup-Templates/Application)。

### 參照

[JSON |文檔中心|總部基地。IO (abp.io)](https://docs.abp.io/zh-Hans/abp/latest/JSON)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* JSON

* 回首頁

---

*本文章從點部落遷移至 Writerside*
