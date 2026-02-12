# Linq 加總兩個欄位

> **原文發布日期:** 2021-07-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/19/LinqSumGroupBy
> **標籤:** 無

---

SQL SUM(A), SUM(B) FROM C

在 Linq 一時之間竟然打不出來..

趕緊筆記一下

直接結論

```
Products
 .GroupBy(p => 1)
 .Select(p => new {
  TotalSid = p.Sum(x => x.SupplierID),
  TotalCid = p.Sum(x => x.CategoryID)
 })
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Linq

- 回首頁

---

*本文章從點部落遷移至 Writerside*
