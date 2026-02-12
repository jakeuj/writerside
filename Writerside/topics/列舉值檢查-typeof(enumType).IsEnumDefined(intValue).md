# 列舉值檢查 typeof(enumType).IsEnumDefined(intValue)

> **原文發布日期:** 2019-06-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/06/13/IsEnumDefined
> **標籤:** 無

---

typeof(enumType).IsEnumDefined(intValue)

```

public enum MyEnum
{
    DOG=1,
    CAT,
    Willy
}
void Main()
{
    TestFunction((MyEnum)0);
}
void TestFunction(MyEnum inputEnum)
{
    //會進來不會報錯，API也可以正常Call，監看式這邊inputEnum=0
}
```

所以只好加上一段檢查

```

typeof(MyEnum).IsEnumDefined(inputEnum)
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
