# ABP.IO WEB應用程式框架 新手教學 No.08 開發教學 第 7 部分&#xFF1A;作者&#xFF1A;數據庫集成

> **原文發布日期:** 2021-07-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/23/ABP-Tutorials-Part-7
> **標籤:** 無

---

主要說明如何實現自定義倉儲

其他之前已說明過的部分則快速帶過

## 關於本教程

在本系列教程中，您將構建一個名為`Acme.BookStore`. 此應用程序用於管理書籍及其作者的列表。它是使用以下技術開發的：

* **Entity Framework Core**作為 ORM 提供者。
* **Angular**作為 UI 框架。

本教程分為以下幾個部分；

* [第 1 部分：創建服務器端](https://docs.abp.io/en/abp/latest/Tutorials/Part-1)
* [第 2 部分：圖書列表頁面](https://docs.abp.io/en/abp/latest/Tutorials/Part-2)
* [第 3 部分：創建、更新和刪除書籍](https://docs.abp.io/en/abp/latest/Tutorials/Part-3)
* [第 4 部分：集成測試](https://docs.abp.io/en/abp/latest/Tutorials/Part-4)
* [第 5 部分：授權](https://docs.abp.io/en/abp/latest/Tutorials/Part-5)
* [第 6 部分：作者：領域層](https://docs.abp.io/en/abp/latest/Tutorials/Part-6)
* **第 7 部分：作者：數據庫集成（本部分）**
* [第 8 部分：作者：應用程序層](https://docs.abp.io/en/abp/latest/Tutorials/Part-8)
* [第 9 部分：作者：用戶界面](https://docs.abp.io/en/abp/latest/Tutorials/Part-9)
* [第 10 部分：書與作者的關係](https://docs.abp.io/en/abp/latest/Tutorials/Part-10)

### 下載源代碼

本教程根據您的**UI**和**數據庫**首選項有多個版本。我們準備了幾個要下載的源代碼組合：

* [帶有 EF Core 的 MVC（Razor Pages）UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Mvc-EfCore)
* [帶有 EF Core 的 Blazor UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Blazor-EfCore)
* [帶有 MongoDB 的 Angular UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Angular-MongoDb)

## 介紹

這一部分解釋瞭如何為上一部分介紹的`Author`實體配置數據庫集成。

## 數據庫上下文

`BookStoreDbContext`在`Acme.BookStore.EntityFrameworkCore`項目中打開並添加以下`DbSet`屬性：

```
public DbSet<Author> Authors { get; set; }
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/0b114430-3502-4bef-8e26-932b0b23dd3e/1627029766.png)

然後`BookStoreDbContextModelCreatingExtensions`在同一個項目中打開類，在`ConfigureBookStore`方法的末尾添加以下幾行：

```
builder.Entity<Author>(b =>
{
    b.ToTable(BookStoreConsts.DbTablePrefix + "Authors",
        BookStoreConsts.DbSchema);

    b.ConfigureByConvention();

    b.Property(x => x.Name)
        .IsRequired()
        .HasMaxLength(AuthorConsts.MaxNameLength);

    b.HasIndex(x => x.Name);
});
```

這就像`Book`之前對實體所做的一樣，因此無需再次解釋。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/0b114430-3502-4bef-8e26-932b0b23dd3e/1627029930.png)

## 創建新的數據庫遷移

啟動解決方案配置為使用[Entity Framework Core Code First Migrations](https://docs.microsoft.com/en-us/ef/core/managing-schemas/migrations/)。由於我們已經更改了數據庫映射配置，我們應該創建一個新的遷移並將更改應用於數據庫。

在`Acme.BookStore.EntityFrameworkCore.DbMigrations`項目目錄中打開命令行終端並鍵入以下命令：

```
dotnet ef migrations add Added_Authors
```

這將向項目添加一個新的遷移類：

![bookstore-efcore-migration-authors](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/bookstore-efcore-migration-authors.png)

您可以在同一命令行終端中使用以下命令對數據庫應用更改：

```
dotnet ef database update
```

> 如果您使用的是 Visual Studio，您可能需要在*包管理器控制台 (PMC) 中*使用`Add-Migration Added_Authors -c BookStoreMigrationsDbContext`和`Update-Database -c BookStoreMigrationsDbContext`命令。在這種情況下，請確保是啟動項目並且是PMC 中的*默認項目*。`Acme.BookStore.HttpApi.HostAcme.BookStore.EntityFrameworkCore.DbMigrations`

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/0b114430-3502-4bef-8e26-932b0b23dd3e/1627030142.png)

## 實現 IAuthorRepository

創建一個新類，`EfCoreAuthorRepository`在`Acme.BookStore.EntityFrameworkCore`項目內部（`Authors`文件夾中）命名並粘貼以下代碼：

```
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Dynamic.Core;
using System.Threading.Tasks;
using Acme.BookStore.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Volo.Abp.Domain.Repositories.EntityFrameworkCore;
using Volo.Abp.EntityFrameworkCore;

namespace Acme.BookStore.Authors
{
    public class EfCoreAuthorRepository
        : EfCoreRepository<BookStoreDbContext, Author, Guid>,
            IAuthorRepository
    {
        public EfCoreAuthorRepository(
            IDbContextProvider<BookStoreDbContext> dbContextProvider)
            : base(dbContextProvider)
        {
        }

        public async Task<Author> FindByNameAsync(string name)
        {
            var dbSet = await GetDbSetAsync();
            return await dbSet.FirstOrDefaultAsync(author => author.Name == name);
        }

        public async Task<List<Author>> GetListAsync(
            int skipCount,
            int maxResultCount,
            string sorting,
            string filter = null)
        {
            var dbSet = await GetDbSetAsync();
            return await dbSet
                .WhereIf(
                    !filter.IsNullOrWhiteSpace(),
                    author => author.Name.Contains(filter)
                 )
                .OrderBy(sorting)
                .Skip(skipCount)
                .Take(maxResultCount)
                .ToListAsync();
        }
    }
}
```

* 繼承自`EfCoreRepository`，因此它繼承了標準存儲庫方法實現。
* `WhereIf`是 ABP 框架的快捷擴展方法。`Where`僅當第一個條件滿足時才添加條件（它按名稱過濾，僅當提供了過濾器時）。你可以自己做同樣的事情，但這些類型的快捷方法讓我們的生活更輕鬆。
* `sorting`可以是像`Name`,`Name ASC`或 之類的字符串`Name DESC`。可以使用[System.Linq.Dynamic.Core](https://www.nuget.org/packages/System.Linq.Dynamic.Core) NuGet 包。

> 有關基於 EF Core 的存儲庫的更多信息，請參閱[EF Core 集成文檔](https://docs.abp.io/en/abp/latest/Entity-Framework-Core)。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/0b114430-3502-4bef-8e26-932b0b23dd3e/1627030341.png)

## 下一部分

請參閱本教程的[下一部分](https://docs.abp.io/en/abp/latest/Tutorials/Part-8)。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
