# MSSQL 抓半年內的資料

> **原文發布日期:** 2022-10-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/04/MSSQL-DateDiff
> **標籤:** 無

---

筆記下

結論

```
SELECT * FROM USERS WHERE DateDiff(MM,[CreationTime],GETDATE()) < 7
```

參考

```
SELECT * FROM USERS WHERE [CreationTime] > DATEADD(MONTH,-6,GETDATE())
```

參照

[SQL日期查詢-SQL查詢今天、昨天、7天內、30天，年 - 程式人生 (796t.com)](https://www.796t.com/content/1543417684.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* MSSQL

* 回首頁

---

*本文章從點部落遷移至 Writerside*
