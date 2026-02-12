# ABP 改用 MySql

> **原文發布日期:** 2017-09-08
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2017/09/08/abp_mysql
> **標籤:** 無

---

ASP.NET Boilerplate 改用 MySql 操作步驟

安裝 .Net Core 2.0

https://github.com/dotnet/core/blob/master/release-notes/download-archives/2.0.0-download.md

下載 ABP Startup Templates

https://aspnetboilerplate.com/

開啟專案 > NGProject.EntityFrameworkCore > NuGet 套件管理 >

1. 移除套件 > Microsoft.EntityFrameworkCore.SqlServer
2. 安裝套件 > Pomelo.EntityFrameworkCore.MySql

修改 NGProject.EntityFrameworkCore/EntityFrameworkCore/NGProjectDbContextConfigurer.cs

```

builder.UseSqlServer(connectionString);
```

改為

```

builder.UseMySql(connectionString);
```

移除原有的Migration資料夾 > NGProject.EntityFrameworkCore/Migration

修改連結字串：NGProject.Web.Host/appsettings.json  與 NGProject.Migrator/appsettings.json

```

"Default": "Server=localhost; Database=NGProjectDb; Trusted_Connection=True;"
```

改為

```

"Default": "Server=localhost; Database=NGProjectDb; userid=root;pwd=;port=3306;sslmode=none;"
```

設定方案的起始專案為 > NGProject.Web.Host

開啟套件管理主控台 > 預設專案設定為 > NGProject.EntityFrameworkCore >

執行命令 > Add-Migration "AbpZero\_Initial" > Update-Database "AbpZero\_Initial"

設定方案的起始專案為 > NGProject.Migrator > 執行

設定方案的起始專案為 > NGProject.Web.Host > 執行

完成

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
