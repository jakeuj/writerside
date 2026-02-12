# Entity Framework Core DB First

> **原文發布日期:** 2021-10-14
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/10/14/Entity-Framework-Core-DB-First
> **標籤:** 無

---

筆記一下將 table 轉成 class 的相關資訊

## 結論

```
cd .\src\MyAPI.EntityFrameworkCore\

dotnet ef dbcontext scaffold "Server=(LocalDb)\MSSQLLocalDB;Database=MyDb;Trusted_Connection=True;" /
Microsoft.EntityFrameworkCore.SqlServer --data-annotations -o D:\Entities
```

### 參數：--data-annotations 您可以使用屬性來設定模型。 如果省略此選項，則只會使用 Fluent API

### 注意

建議使用 Fluent API 來分離 Domain 與基礎設施層的依賴關係

(如果使用屬性，則需要在領域層加入 EF 的抽象類別包)

### 說明

切到 EntityFrameworkCore 的專案

然後提供連接字串並指定輸出目錄給 `dotnet ef dbcontext scaffold`

### 連結字串名稱

也可以指定 `Name=ConnectionStrings:Blogging`

```
dotnet user-secrets set ConnectionStrings:Blogging "Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=Blogging"
dotnet ef dbcontext scaffold Name=ConnectionStrings:Blogging Microsoft.EntityFrameworkCore.SqlServer
```

### 備註

如果沒裝 ef tool 使用以下命令安裝

`dotnet tool install --global dotnet-ef`

如果 tool 過舊，使用以下命令更新

`dotnet tool update --global dotnet-ef`

如果要更新到預覽版

`dotnet tool update --global dotnet-ef --version 6.0.0-rc.2.21480.5`

### 參照

[EF Core 工具參考 ( .NET CLI) -EF Core | Microsoft Docs](https://docs.microsoft.com/zh-tw/ef/core/cli/dotnet#dotnet-ef-dbcontext-scaffold)

MySQL

`dotnet ef dbcontext scaffold "Server=127.0.0.1; Port=3306; Database=jakeuj; Uid=jakeuj; Pwd=jakeuj;" MySql.EntityFrameworkCore -o sakila -f`

參照

[MySQL :: MySQL Connector/NET Developer Guide :: 7.2.2 Scaffolding an Existing Database in EF Core](https://dev.mysql.com/doc/connector-net/en/connector-net-entityframework-core-scaffold-example.html#connector-net-entityframework-core-scaffold-cli)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Entity Framework
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
