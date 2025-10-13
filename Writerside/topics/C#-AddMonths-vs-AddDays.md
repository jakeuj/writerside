# C# AddMonths vs AddDays

> **原文發布日期:** 2022-05-27
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/05/27/AddMonthsDays
> **標籤:** 無

---

筆記下差異

上個月 vs 過去30天

```
var dat = new DateTime(2015, 3,15);
dat.AddMonths(-1).Dump();
dat.AddDays(-30).Dump();
```

輸出

```
2015/2/15 上午 12:00:00
2015/2/13 上午 12:00:00
```

結論

視情況選擇是否需要精確三十日

例如：每日處理近一個月內尚未處理的東西，這感覺是比較模糊的日數

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* 回首頁

---

*本文章從點部落遷移至 Writerside*
