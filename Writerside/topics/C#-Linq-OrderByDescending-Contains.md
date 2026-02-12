# C# Linq OrderByDescending Contains

> **原文發布日期:** 2023-06-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/06/19/CSharp-Linq-OrderByDescending-Contains
> **標籤:** 無

---

筆記下按照某 bool 條件 (Id是否包含在指定清單中) 來排序集合

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/5302d5c5-1820-4f50-8d4e-6d16bf110f1f/1688024053.png.png)

## 情境

一般使用某欄位按大小排序

需求是按照某清單，符合的優先，不符合地次之

### 結論

```
void Main()
{
 List<User> users = new List<User> {
  new User(1),
  new User(2),
  new User(3),
  new User(4),
  new User(5),
 };

 List<int> idList = new List<int> {2,4};

 var newList = users.OrderByDescending(x=>idList.Contains(x.Id)).ToList();

 newList.Dump();
}

// You can define other methods, fields, classes and namespaces here
public class User
{
 public int Id { get; set; }
 public User(int id) {Id = id;}
}
```

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/5302d5c5-1820-4f50-8d4e-6d16bf110f1f/1687164433.png.png)
![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Linq

- 回首頁

---

*本文章從點部落遷移至 Writerside*
