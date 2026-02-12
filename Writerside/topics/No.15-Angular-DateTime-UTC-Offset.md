# No.15 Angular DateTime UTC Offset

> **原文發布日期:** 2019-09-17
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/09/17/abp15
> **標籤:** 無

---

前後端時間的時區對不起來的問題

Angular 預設使用UTC時間

DotNet 預設使用本地時間

所以造成時間一直錯亂

先下結論：加下面這行到 AbpModule (我是加在Web Project Module)

<https://aspnetboilerplate.com/Pages/Documents/Timing#clock>

```

Clock.Provider = ClockProviders.Utc;
```

Sample

```

public override void Initialize()
{
    Clock.Provider = ClockProviders.Utc;
    IocManager.RegisterAssemblyByConvention(typeof(ObManWebHostModule).GetAssembly());
}
```

如果有用日期時間選擇套件了話注意要設定成 UTC:true

@NgModule > providers

```

{ provide: OWL_MOMENT_DATE_TIME_ADAPTER_OPTIONS, useValue: { useUtc: true }}
```

有使用 NSWang 了話，其實 DateTimeType設成以下兩種都可以

service.config.nswag > codeGenerators

```

"dateTimeType": "MomentJS",
```

```

"dateTimeType": "OffsetMomentJS",
```

只是格式有點差異 UTC V.S. Offset

utc 格式: 2018-12-31T16:30:07.000z

offset 格式: 2018-12-31T16:30:07.000+08:00

參照：<https://www.cnblogs.com/keatkeat/p/9737128.html>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- Angular

- 回首頁

---

*本文章從點部落遷移至 Writerside*
