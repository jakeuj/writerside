# ABP.IO 同時使用 MSSQL 與 MySQL

> **原文發布日期:** 2023-06-27
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/06/27/abp-MSSQL-MySQL
> **標籤:** 無

---

筆記下關於 `Option 'trusted_connection' not supported.` 的坑

## 例外

`MYSQL Option 'trusted_connection' not supported.`

## 結論

總之改用下面這段就可以了

```
Server=127.0.0.1;Port=3306;Uid=root;Pwd=;Database=Csharp_Hotel_DB
```

於原本比較一下應該是不能有空格？

```
Server=127.0.0.1; Database=Csharp_Hotel_DB; Port=3306; Uid=root; Pwd=
```

## 補充

1. 基本參照官方多資料庫的說明文件 [Entity Framework Core](https://docs.abp.io/en/abp/5.0/Entity-Framework-Core-Migrations#using-multiple-databases)
2. 需額外安裝套件 `Volo.Abp.EntityFrameworkCore.MySQL`
3. `DbContextFactory` 裡面改用 `UseMySql` 並提供 MySql 版本參數 ( `Select Version();` )
   `UseMySql(configuration.GetConnectionString("Hotel"), ServerVersion.Parse("8.0.33-0ubuntu0.22.04.2"));`
4. `EntityFrameworkCoreModule` 裡面加上 `options.Configure<HotelDbContext>(o => { o.UseMySQL(); });`

`DbContextFactory`

```
public HotelDbContext CreateDbContext(string[] args)
{
    var configuration = BuildConfiguration();
    var builder = new DbContextOptionsBuilder<HotelDbContext>()
        .UseMySql(configuration.GetConnectionString("Hotel"), ServerVersion.Parse("8.0.33-0ubuntu0.22.04.2"));
    return new HotelDbContext(builder.Options);
}
```

`EntityFrameworkCoreModule`

```
context.Services.AddAbpDbContext<HotelDbContext>(options =>
{
    options.AddDefaultRepositories(includeAllEntities: true);
});

Configure<AbpDbContextOptions>(options =>
{
    /* The main point to change your DBMS.
     * See also TestMigrationsDbContextFactory for EF Core tooling. */
    options.UseSqlServer();

    // for MySql DbContext
    options.Configure<HotelDbContext>(o => { o.UseMySQL(); });
});
```

## 參照

[Entity Framework Core MySQL | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Entity-Framework-Core-MySQL)

[How To Check MySQL Version: 5 Easy Commands {Ubuntu, Linux} (phoenixnap.com)](https://phoenixnap.com/kb/how-to-check-mysql-version)

[ABP.IO WEB應用程式框架 使用多個資料庫 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/10/04/Abp-Using-Multiple-Databases)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Entity Framework](/jakeuj/Tags?qq=Entity%20Framework)
{ignore-vars="true"}
* [MSSQL](/jakeuj/Tags?qq=MSSQL)
* [MySql](/jakeuj/Tags?qq=MySql)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
