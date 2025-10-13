# Entity Framework Core Migrations

> **原文發布日期:** 2019-07-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/07/23/EFCoreMigrations
> **標籤:** 無

---

Rider 與 VS 皆可用的 PowerShell 的 migrations 指令筆記

## migrations add

1. 結論：(以下為同一行)
   dotnet-ef migrations add 'Initial'
       -s .\src\MyProject.HttpApi.Host
       -p .\src\MyProject.EntityFrameworkCore
       -c MyProjectDbContext
2. 基本新增資料庫版本 (須從dbContext專案位置執行以下命令)
   `dotnet ef migrations add newMigrationName`
3. 當有複數DbContext時需要指定context
   `dotnet ef migrations add newMigrationName -c mySecondDbContext`
4. 當DbContext目錄位置與appsetting.json位置不同導致找不到該檔案時(通常為了找連結字串)
   `dotnet ef migrations add newMigrationName -s ./myStartupProject`
5. 當出現請安裝 Microsoft.EntityFrameworkCore.Design 請用nuget安裝該套件至dbContext專案
   `PM> Install Microsoft.EntityFrameworkCore.Design`
6. 當你需要不同環境變數來讀取對應appsetting.{env}.json (dbContext專案必須先實作該功能)
   1. CMD
      `set ASPNETCORE_ENVIRONMENT=Production`
   2. PowerShell
      `$env:ASPNETCORE_ENVIRONMENT='Production'`

## database update

1. 基本更新資料庫版本
   `dotnet ef database update`
2. 當有複數DbContext時需要指定context
   `dotnet ef database update -c myDbContext`
3. 復原資料庫到特定版本 (複數DbContext時參照第2點)
   `dotnet ef database update myMigrationName`

## migrations script

1. 產生SQL語法 (從一開始(0)到myMigrationName之間)
   `dotnet ef migrations script 0 myMigrationName`
2. 產生SQL語法 (從myMigrationName到最新)
   `dotnet ef migrations script myMigrationName`
3. 當有複數DbContext時需要指定context
   `dotnet ef migrations script myMigrationName -c myDbContext`
4. 指定輸出路徑
   `dotnet ef migrations script myMigrationName -o .\Sql\myMigrationName.sql`

## migrations remove

1. 移除上一個版本
   `dotnet ef migrations remove`
2. 當有複數DbContext時需要指定context
   `dotnet ef migrations remove -c myDbContext`

> 因為找不到指定的命令或檔案，所以無法執行。
> 可能的原因包括:
>   \* 內建 dotnet 命令拼寫錯誤。
>   \* 您預計要執行 .NET 程式，但不存在 dotnet-ef。
>   \* 您預計要執行全域工具，但在 PATH 上找不到此名稱且開頭為 dotnet 的可執行檔。

`dotnet tool install --global dotnet-ef`

## 備註

* 多DB時
  所有在 Startup 內有用到的 DBContext ConnectionStrings
  都要正確定義在對應環境變數的 appsetting 內
  (即使 migrations 只指定某一個 DBContext)
  因為 migrations 實際上會執行一次 Startup
  導致裡面有用到某連線字串卻又找不到時會報錯
* 承上
  因為 migrations 實際上會執行一次 Startup
  debug 時可以在 startup 內印出 連接字串、環境變數…等等
  執行 migrations 時觀察 log 方便 Debug
* 執行以上命令時須先把執行中的程式停止

## .Net 5 vs .Net Core 3 指令多了一個連字號

* Dotnet Core 5
  `dotnet-ef database update`
* Dotnet Core 3
  `dotnet ef database update`

But, 人生中最重要的就是這個 But！

新版好像兩種都可以用…

---

參照：[Migrations](https://docs.microsoft.com/en-us/ef/core/managing-schemas/migrations/)

參照：[Running Entity Framework (Core) commands in Rider](https://blog.jetbrains.com/dotnet/2017/08/09/running-entity-framework-core-commands-rider/)

參照：[EF Core MySql Integration](https://aspnetboilerplate.com/Pages/Documents/EF-Core-MySql-Integration)

參照：[dotnet ef 找不到指定的命令](https://blog.darkthread.net/blog/dotnet-ef-not-found/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Entity Framework](/jakeuj/Tags?qq=Entity%20Framework)
* [Migrations](/jakeuj/Tags?qq=Migrations)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
