# MSSQL text 請改用 varchar(max)

> **原文發布日期:** 2021-10-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/10/21/MSSQL-Text-Varchar
> **標籤:** 無

---

提醒自己 ntext、text 及 image 已過時

## 結論

請改用 nvarchar(max)、 varchar(max)和 varbinary(max) 。

### 說明

> 重要！ SQL Server 的未來版本將會移除 ntext、text 及 image 資料類型。
>
> 請避免在新的開發工作中使用這些資料類型，並規劃修改目前在使用這些資料類型的應用程式。
>
> 請改用 nvarchar(max)、 varchar(max)和 varbinary(max) 。

### 參照

[ntext、text 和 image (Transact-SQL) - SQL Server | Microsoft Docs](https://docs.microsoft.com/zh-tw/sql/t-sql/data-types/ntext-text-and-image-transact-sql?view=sql-server-ver15)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [MSSQL](/jakeuj/Tags?qq=MSSQL)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
