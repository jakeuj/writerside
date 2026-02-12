# ABP.IO EnableSensitiveDataLogging

> **原文發布日期:** 2021-11-05
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/11/05/Abp-Enable-Sensitive-Data-Logging
> **標籤:** 無

---

本文說明如何在 ABP.IO WEB應用程式框架中啟用敏感資料紀錄（EnableSensitiveDataLogging）。

紀錄 Framework 啟用輸入值顯示在 Log 的設定

Logging 會隱藏 SQL 錯誤的一些敏感資料

可能是實際輸入的值之類的資訊

開發 Debug 需要看了話需要設定一下 `EnableSensitiveDataLogging`

```
options.Configure(configureOptions =>
{
  configureOptions.UseSqlServer();
  configureOptions.DbContextOptions.EnableSensitiveDataLogging();
});
```

參考

Project.EntityFrameworkCore.ProjectEntityFrameworkCoreModule.cs

```
Configure<AbpDbContextOptions>(options =>
{
    /* The main point to change your DBMS.
     * See also PlmAPIMigrationsDbContextFactory for EF Core tooling. */
    options.UseSqlServer();

    //TODO: Debug 用完需註解
    options.Configure(configureOptions =>
    {
        configureOptions.UseSqlServer();
        configureOptions.DbContextOptions.EnableSensitiveDataLogging();
    });
});
```

參照

[DbContextOptionsBuilder.EnableSensitiveDataLogging throws InvalidOperationException · Issue #4557 · abpframework/abp (github.com)](https://github.com/abpframework/abp/issues/4557)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Entity Framework
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
