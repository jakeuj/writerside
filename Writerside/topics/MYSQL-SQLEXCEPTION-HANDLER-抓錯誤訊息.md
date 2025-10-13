# MYSQL SQLEXCEPTION HANDLER 抓錯誤訊息

> **原文發布日期:** 2019-11-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/11/21/MYSQLEXCEPTION
> **標籤:** 無

---

我用MSSQL的SP好像沒這麼多事啊？

筆記下MYSQL搞得我快瘋了的SP例外處理

```

DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN

GET CURRENT DIAGNOSTICS CONDITION 1
code = RETURNED_SQLSTATE,
errno = MYSQL_ERRNO,
msg = MESSAGE_TEXT;

SELECT code,errno,msg;

ROLLBACK;

END
```

注意：ROLLBACK;要放在最後不然先回滾錯例外就跟著沒了！

另外是如果有用 @sqlString 記錄查詢語句，要注意這是全域變數，

也就是說你在A SP紀錄，但是在B SP沒有reset該變數，

B在執行途中輸出 @sqlString 實際上會輸出上A SP裡頭用的查詢語句

讓我好查了老半天...

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [MySql](/jakeuj/Tags?qq=MySql)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
