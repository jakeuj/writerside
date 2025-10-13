# ABP.IO EntityFramework Insert 時指定識別欄位 Id 自動增量的值

> **原文發布日期:** 2023-06-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/06/28/ABP-EF-SET-IDENTITY-INSERT-ON
> **標籤:** 無

---

SET IDENTITY\_INSERT ON

## 情境

需要將舊 mysql 資料表匯入到新的 mssql 資料表

## 問題1

ABP 中 `Entity<int>` Id 屬性的 setter 是 private 所以無法指定該值

### 解決方案

改繼承 `Entity`

```
public class User : Entity
{
    public long Id { get; set; }
    public string Name { get; set; }

    public override object[] GetKeys()
    {
        return new object[] { Id };
    }
}
```

## 問題2

自動增量識別欄位於 Insert 資料指定 Id 時會得到例外，錯誤訊息如下

`Cannot insert explicit value for identity column in table 'Users' when IDENTITY_INSERT is set to OFF.`

### 解決方案

SET IDENTITY\_INSERT ON

```
await _repository.InsertAsync(new User
    {
        Id = 8888,
        Name = "Test"
    });

var db = await _repository.GetDbContextAsync();
await db.Database.ExecuteSqlRawAsync("SET IDENTITY_INSERT dbo.NandPackageUsages ON;");
await db.SaveChangesAsync();
await db.Database.ExecuteSqlRawAsync("SET IDENTITY_INSERT dbo.NandPackageUsages OFF;");
```

### 備註

目前是新開分支把 `Entity<int>` 改為 `Entity`

並將邏輯寫在 `DataSeedContributor` 執行 `DbMigrator` 專案

預計僅在系統上線時執行一次

其實資料不複雜可以直接用 csv 匯出匯入

也有其他現成的 migration tools 可以將 mysql 匯入到 mssql

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Entity Framework](/jakeuj/Tags?qq=Entity%20Framework)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
