# Linq Left Join (GroupJoin &#x2B; SelectMany) Repository

> **原文發布日期:** 2019-06-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/06/19/LinqJoin
> **標籤:** 無

---

Repository Linq LeftJoin (GroupJoin + SelectMany) and Join

假設有兩個倉儲 A,B

要用A.bId去跟B.Id為依據

去拿B.Name欄位

最後合併 A.Id與B.Name

成為 cDto 作為資料傳輸物件輸出

* Left Join (GroupJoin + Select) 子集合選擇特定欄位

```
var joinQuery = order
	.GroupJoin(orderStatus,
		o => o.Id,
		s => s.Id,
		(o, s) => new {
			o.Id,
			data = s.Select(x => new {
				x.Item,
				x.Qty
				}
			)
		}
	)
	.Where(x => x.data.Any())
	.ToList();
```

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/573d0ae9-3423-4102-b172-e3e56367dd3b/1665481478.png.png)

* Left Join (GroupJoin + SelectMany) 攤平子集合

```
var joinQuery = _aRepository.GetAll()
    .GroupJoin(_bRepository.GetAll(),
    a => a.bId,
    b => b.Id,
    (a,b) => new{a,b})
    .SelectMany(result => result.b.DefaultIfEmpty(),
    (x, y) => new cDto{
        Id = x.a.Id,
        Name = y.Name ?? "N/A"
    });
```

* Join  (innerJoin)

```
var joinQuery = _aRepository.GetAll()
    .Join(_bRepository.GetAll(),
    a=>a.bId,
    b=>b.Id,
    (a,b)=>new cDto{
        Id = a.Id,
        Name = b.Name
    });
```

B倉儲只要沒有A的bID，該筆資料就不會出現在結果

參照：[LINQ學習筆記(7)實作Left join(1) Join與Group join](https://medium.com/@ad57475747/linq%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-7-%E5%AF%A6%E4%BD%9Cleft-join-1-join%E8%88%87group-join-47e187d80894)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Join](/jakeuj/Tags?qq=Join)
* [Linq](/jakeuj/Tags?qq=Linq)
* [Repository](/jakeuj/Tags?qq=Repository)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
