# 將 nullable DateTime? 轉成指定格式字串

> **原文發布日期:** 2023-02-01
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/02/01/how-to-parse-nullable-datetime-object-in-c-sharp
> **標籤:** 無

---

筆記一下 DateTime?.ToString("yyyyMMdd") 的問題

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/c3279c50-9617-4e1a-b488-8eed81047d83/1675303184.png.png)

結論

`GetValueOrDefault()`

```
DateTime? youWinDate = null;
var yyyyMMdd = youWinDate.GetValueOrDefault().ToString("yyyyMMdd");
yyyyMMdd.Dump();
```

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/c3279c50-9617-4e1a-b488-8eed81047d83/1675303258.png.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/c3279c50-9617-4e1a-b488-8eed81047d83/1675303117.png.png)

參照

[How to parse nullable DateTime object in C# - Stack Overflow](https://stackoverflow.com/questions/19152764/how-to-parse-nullable-datetime-object-in-c-sharp)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* 回首頁

---

*本文章從點部落遷移至 Writerside*
