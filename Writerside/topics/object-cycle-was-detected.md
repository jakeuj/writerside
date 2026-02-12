# object cycle was detected

A possible object cycle was detected.

This can either be due to a cycle or if the object depth is larger than the maximum allowed depth of 64.

Consider using ReferenceHandler.Preserve on JsonSerializerOptions to support cycles.

## 翻譯

偵測到可能的物件循環。

這可能是由於週期或物件深度大於允許的最大深度 64。

請考慮在 JsonSerializerOptions 上使用 ReferenceHandler.Preserve 來支援循環。

## 結論

在實體的尋覽屬性加上 `[JsonIgnore]`，避免循環參考。

```C#
using System.Text.Json.Serialization;

[JsonIgnore] public ICollection<OrderLine> Lines { get; set; } //Sub collection
[JsonIgnore] public Order Order { get; set; } //Navigation property
```

## 參考

- [ABP.IO WEB應用程式框架 取得關聯資料 include](https://dotblogs.azurewebsites.net/jakeuj/2022/10/25/abp-ef-With-Details-Async)
- [認識 Entity Framework Core 載入關聯資料的三種方法](https://blog.miniasp.com/post/2022/04/21/Loading-Related-Data-in-EF-Core)
- [Distributed-Event-Bus](https://abp.io/support/questions/7460/VoloAbpAuditingAuditingHelper-warning-in-API-output-logging)
