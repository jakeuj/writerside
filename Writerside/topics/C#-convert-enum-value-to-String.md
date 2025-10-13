# C# convert enum value to String

> **原文發布日期:** 2022-10-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/26/143813
> **標籤:** 無

---

筆記下列舉值轉成字串形式的對應數字

## 結論

`.ToString("D")`

## 範例

### Enum

```
public enum Urgency
{
    VeryHigh = 1,
    High = 2,
    Low = 4
}
```

### WriteLine

```
Console.WriteLine(Urgency.High.ToString("D"));
```

### Output

```
"2"
```

### 參照

[C# numeric enum value as string - Stack Overflow](https://stackoverflow.com/questions/3444699/c-sharp-numeric-enum-value-as-string)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
