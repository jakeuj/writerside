# SQL 臨時表 定序衝突 (COLLATE)

> **原文發布日期:** 2021-12-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/12/20/SQL-TempTable-COLLATE
> **標籤:** 無

---

Cannot resolve the collation conflict between "SQL\_Latin1\_General\_CP1\_CI\_AS" and "Chinese\_Taiwan\_Stroke\_CI\_AS" in the equal to operation.

建立臨時表時會以資料庫伺服器預設定序來建立

當伺服器(比如 LocalDb or Azure SQL)預設定序(SQL\_Latin1\_General\_CP1\_CI\_AS)

與當前資料庫(資料表或預存程序)不一致(Chinese\_Taiwan\_Stroke\_CI\_AS)時，就會報錯

```
CREATE TABLE #tmplist (
name nvarchar(15),
desc nvarchar(128));
```

需要將原本每個 nvarchar 後面都加上要使用的定序 (`COLLATE Chinese_Taiwan_Stroke_CI_AS`)

```
CREATE TABLE #tmplist (
name nvarchar(15) COLLATE Chinese_Taiwan_Stroke_CI_AS,
desc nvarchar(128) COLLATE Chinese_Taiwan_Stroke_CI_AS);
```

結論

新專案請使用 Code First

參照

[SQL Server的 排序规则(collation)冲突和解决方案 - LanceZhang - 博客园 (cnblogs.com)](https://www.cnblogs.com/blodfox777/archive/2010/01/21/sqlserver-collation-conflict-and-solutions.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [MSSQL](/jakeuj/Tags?qq=MSSQL)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
