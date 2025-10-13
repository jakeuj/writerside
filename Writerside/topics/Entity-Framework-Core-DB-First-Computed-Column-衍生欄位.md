# Entity Framework Core DB First Computed Column 衍生欄位

> **原文發布日期:** 2023-07-10
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/07/10/computed-columns
> **標籤:** 無

---

計算資料行是一個虛擬資料行，除非資料行標示了PERSISTED，否則，並未實際儲存在資料表中。

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/26095bf3-f412-4159-96eb-8c45ddcb47bf/1688983414.png.png)

## Entity

```
public class Test : FullAuditedAggregateRoot<Guid>
{
    public virtual int Total{ get; set; }
    public virtual int Used { get; set; }
    public virtual int Unused  { get; private set; }
}
```

## DbContext

### 虛擬資料行

```
modelBuilder.Entity<Test>()
    .Property(p => p.Unused)
    .HasComputedColumnSql("([Total] - [Used])");
```

實際上不儲存該值，每次要用的時候即時運算出該欄位

### 實值資料行

```
modelBuilder.Entity<Test>()
    .Property(p => p.Unused)
    .HasComputedColumnSql("([Total] - [Used])", stored: true);
```

每次更新時重新計算，並將結果作為值寫入資料庫

## 參照

[Generated Values - EF Core | Microsoft Learn](https://learn.microsoft.com/en-us/ef/core/modeling/generated-properties?tabs=data-annotations#computed-columns)

### 延伸

[ABP.IO WEB應用程式框架 取得關聯資料 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2022/10/25/abp-ef-With-Details-Async)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Entity Framework](/jakeuj/Tags?qq=Entity%20Framework)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
