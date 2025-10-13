# Unknown column &#x27;Discriminator&#x27; in &#x27;where clause&#x27;

> **原文發布日期:** 2019-06-10
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/06/10/EfCore
> **標籤:** 無

---

Unknown column 'Discriminator' in 'where clause'

結論是實體裡面設定了關聯性

但實際資料庫中的資料表卻沒有該關聯

檢查巡覽屬性與外部索引鍵

是否與資料庫不一致

修正後可以正常

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Entity Framework
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
