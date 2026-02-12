# Dapper Bulk InsertOrUpdate

> **原文發布日期:** 2019-09-29
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/09/29/bulk-merge
> **標籤:** 無

---

Dapper 大量 插入或更新

就丟List<實體>進去，有Id就更新，否則插入

PM > Install-Package Z.Dapper.Plus

```
//Merge a single order.
connection.BulkMerge(order);

//Merge multiple orders.
connection.BulkMerge(order1, order2, order3);
```

<https://dapper-plus.net/bulk-merge>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
{ignore-vars="true"}
- Dapper
- SQL

- 回首頁

---

*本文章從點部落遷移至 Writerside*
