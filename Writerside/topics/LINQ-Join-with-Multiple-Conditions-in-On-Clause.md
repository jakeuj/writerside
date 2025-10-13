# LINQ Join with Multiple Conditions in On Clause

> **原文發布日期:** 2021-09-01
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/01/LinqJoinMultipleConditions
> **標籤:** 無

---

摘錄一下 Join On 多條件的寫法

結論

```
var dnrs = context.participants.GroupJoin(
    context.prereg_participants,
    x => new { JoinCol1 = x.barcode, JoinCol2 = x.event_id }, // Left table join key
    y => new { JoinCol1 = y.barcode, JoinCol2 = y.event_id }, // Right table join key
    ...
```

上面是 lamba 語法

```
from a in db.Students
join b in db.Schools on
new { SchoolId = a.SchoolId, IsMale = a.IsMale } equals
new { SchoolId = b.Id, IsMale = true }
```

參照

[LINQ Join with Multiple Conditions in On Clause - Stack Overflow](https://stackoverflow.com/questions/7664727/linq-join-with-multiple-conditions-in-on-clause)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Linq

* 回首頁

---

*本文章從點部落遷移至 Writerside*
