# MSSQL取得UnixTime時間戳記

> **原文發布日期:** 2012-09-10
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2012/09/10/74694
> **標籤:** 無

---

MSSQL取得UnixTime時間戳記

找了半天好像沒有內建日期函數可以直接取得UnixTime

於是乎只好用別的方法來取得

其實也沒甚麼複雜的

就簡單一行即可取得

SELECT DATEDIFF(SS,'1970-01-01',GETUTCDATE())

這行意思是取得目前時間與1970/01/01 00:00:00的差異秒數

也就是UnixTime時間戳記所定義的內容

有更好的方法可以再分享給我

微軟跟Uinx有這麼不友好嗎@@?

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [MSSQL](/jakeuj/Tags?qq=MSSQL)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
