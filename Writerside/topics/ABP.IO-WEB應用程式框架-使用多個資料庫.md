# ABP.IO WEB應用程式框架 使用多個資料庫

> **原文發布日期:** 2021-10-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/10/04/Abp-Using-Multiple-Databases
> **標籤:** 無

---

主要紀錄將 ABP 與 IS4 相關實體搬到另一個 DB 的坑

## 引導

[Entity Framework Core Migrations | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/5.0/Entity-Framework-Core-Migrations#using-multiple-databases)

首先跟著官方文件步驟走，這邊補充一些個人見解

## 連結字串

如果把原本資料都改到另一個 DB，那麼需要在 API.Host 與 API.DbMigrator 的 appsettings.json 加入以下設定

```
"ConnectionStrings": {
  "Default": "Server=(LocalDb)\\MSSQLLocalDB;Database=BookStore_MainDb;Trusted_Connection=True",
  "AbpAuditLogging": "Server=(LocalDb)\\MSSQLLocalDB;Database=BookStore_SecondDb;Trusted_Connection=True",
  "AbpFeatureManagement": "Server=(LocalDb)\\MSSQLLocalDB;Database=BookStore_SecondDb;Trusted_Connection=True",
  "AbpPermissionManagement": "Server=(LocalDb)\\MSSQLLocalDB;Database=BookStore_SecondDb;Trusted_Connection=True",
  "AbpSettingManagement": "Server=(LocalDb)\\MSSQLLocalDB;Database=BookStore_SecondDb;Trusted_Connection=True",
  "AbpIdentityServer": "Server=(LocalDb)\\MSSQLLocalDB;Database=BookStore_SecondDb;Trusted_Connection=True",
  "AbpBackgroundJobs": "Server=(LocalDb)\\MSSQLLocalDB;Database=BookStore_SecondDb;Trusted_Connection=True",
  "AbpTenantManagement": "Server=(LocalDb)\\MSSQLLocalDB;Database=BookStore_SecondDb;Trusted_Connection=True"
}
```

> 如果採用 IS4 分離專案，則需要將以上加到 API.IdentityServer 專案
>
> - API.IdentityServer 不需要連結字串 `AbpBackgroundJobs`
> - API.Host 不需要連結字串 `AbpIdentityServer`

主要是這邊需要指定各模組的連線字串，不然他會使用 Default 去找 table，然後找不到就會報錯

如有遺漏需要去官方文件找該模組的連線字串名稱，如果沒交代要去 github 找該模組源碼

比如 [Modules/Feature Management | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Modules/Feature-Management)

官方文件沒有描述則要去 github 找該模組的連線字串名稱，位置如下

[abp/FeatureManagementDbProperties.cs at dev · abpframework/abp (github.com)](https://github.com/abpframework/abp/blob/dev/modules/feature-management/src/Volo.Abp.FeatureManagement.Domain/Volo/Abp/FeatureManagement/FeatureManagementDbProperties.cs#L11)

其他模組理論上都在同樣的路徑可以找到對應的程式碼

---

## Migrator

### 結論

MyProject.EntityFrameworkCore 必須有 migrations 資料夾

(以下為同一行)
dotnet-ef migrations add 'Initial'
    -s .\src\MyProject.HttpApi.Host
    -p .\src\MyProject.EntityFrameworkCore
    -c MyProjectSecondDbContext
    -o Migrations\secondDb

- 要馬先不指定 -o 跑一次預設的 migrations add (會建立 migrations folder)
- 不然就要將第二個 db 建立在 migrations 路徑下 (指定 -o Migrations\xxxx)

### 原因

主要是 DbMigrationService.MigrationsFolderExists 是這樣寫的

```
private bool MigrationsFolderExists()
{
    var dbMigrationsProjectFolder = GetEntityFrameworkCoreProjectFolderPath();

    return Directory.Exists(Path.Combine(dbMigrationsProjectFolder, "Migrations"));
}
```

所以只要沒有 Migrations 這個資料夾，他就不做事

### 說明

如果原本或其他 DB 有建出 Migrations 資料夾，那應該會正常

但假設想要先把全部 ABP 既有的資料都先搬到另一個 DB

建立遷移時又不是 output 到 Migrations 資料夾

那使用 DbMigrator 時就會因為檢查 Migrations 不存在

就當作你沒有東西要做遷移直接結束

雖然直接 dotnet ef database update 也可以建出資料庫

但是 SeedData 就會跑不出來了

### 參照

[Entity Framework Core Migrations | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2019/07/23/EFCoreMigrations)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- Entity Framework
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
