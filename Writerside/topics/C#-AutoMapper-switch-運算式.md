# C# AutoMapper switch 運算式

> **原文發布日期:** 2023-03-07
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/03/07/CSharp-AutoMapper-Switch
> **標籤:** 無

---

使用 關鍵字比對運算式的 `switch` 模式

### 結論

```
CreateMap<TSource, TDest>()
    .ForMember(dest => dest.SomeDestProp, opt => opt.MapFrom((src, dest) =>
    {
        TSomeDestProp destinationValue;

        // mapping logic goes here

        return destinationValue;
    }));
```

補充

```
.ForMember(dst => dst.DisplayName,
    map => map.MapFrom((src, dst) =>
        src.Detail switch
        {
            var detail when detail.Option == "自訂" => detail.DisplayName,
            var detail when detail.Sex == "男" => detail.Name + "男士",
            var detail when detail.Sex == "女" => detail.Name + "女士",
            _ => default
        }
    ))
```

P.S. 其中 `var detail` 等於 `src.Detail`

### 參照

[c# - Automapper: complex if else statement in ForMember - Stack Overflow](https://stackoverflow.com/questions/32643076/automapper-complex-if-else-statement-in-formember/59329566#59329566)

[switch 運算式 - 使用 'switch' 運算式評估模式比對運算式 | Microsoft Learn](https://learn.microsoft.com/zh-tw/dotnet/csharp/language-reference/operators/switch-expression)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [AutoMapper](/jakeuj/Tags?qq=AutoMapper)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
