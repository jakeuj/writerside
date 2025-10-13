# ABP.IO WEB應用程式框架 新手教學 No.02 開發教學 第 1 部分 創建服務端

> **原文發布日期:** 2021-07-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/21/abpio02
> **標籤:** 無

---

此開發教學相較上一篇 No.01 [快速開始](https://dotblogs.com.tw/jakeuj/2021/07/20/abpio01) 比較複雜一些

第一次接觸還沒看過快速開始的建議先從上一篇先看

這篇理論上同樣著重在 .Net Core + EF Core 建立 API

前端框架 Angular 的實現不在本次重點會先快速帶過

### [[2021] ABP.IO WEB應用程式框架 新手教學 No.0 全篇索引](https://dotblogs.com.tw/jakeuj/2021/07/15/abpio0)

本篇會以官方文件 [開發教學](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1?UI=NG&DB=EF) 為依據中文化並附圖加以說明的方式進行

---

## Web應用程序開發教程 - 第一章：創建服務端

## 關於本教程

在本系列教程中，您將構建一個名稱`Acme.BookStore`的用於管理書籍及其作者列表的基於 ABP 的程序。是使用以下技術開發的：

* **Entity Framework Core 為**ORM 提供程序。
* **MVC / Razor Pages**做為 UI 框架。

本教程分為以下部分：

* [第 1 部分：創建服務器端](https://docs.abp.io/en/abp/latest/Tutorials/Part-1)
* [第 2 部分：圖書列表頁面](https://docs.abp.io/en/abp/latest/Tutorials/Part-2)
* [第 3 部分：創建、更新和刪除書籍](https://docs.abp.io/en/abp/latest/Tutorials/Part-3)
* [第 4 部分：集成測試](https://docs.abp.io/en/abp/latest/Tutorials/Part-4)
* [第 5 部分：授權](https://docs.abp.io/en/abp/latest/Tutorials/Part-5)
* [第 6 部分：作者：領域層](https://docs.abp.io/en/abp/latest/Tutorials/Part-6)
* [第 7 部分：作者：數據庫集成](https://docs.abp.io/en/abp/latest/Tutorials/Part-7)
* [第 8 部分：作者：應用程序層](https://docs.abp.io/en/abp/latest/Tutorials/Part-8)
* [第 9 部分：作者：用戶界面](https://docs.abp.io/en/abp/latest/Tutorials/Part-9)
* [第 10 部分：圖書到作者的關係](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-10)

## 下載源碼

本教程根據你的**UI**和**數據庫**首選項有多個版本，我們準備了一個模型下載的源碼組件：

* [MVC (Razor Pages) UI 與 EF Core](https://github.com/abpframework/abp-samples/tree/master/BookStore-Mvc-EfCore)
* [Angular UI 與 MongoDB](https://github.com/abpframework/abp-samples/tree/master/BookStore-Angular-MongoDb)

## 創建解決方案

在開始開發之前，請按照[入門教程](https://docs.abp.io/zh-Hans/abp/latest/Getting-Started)創建命名`Acme.BookStore`的新解決方案。

// 這邊我從 <https://abp.io/get-started> 使用以下選項建立

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1626833463.png)

// 這邊可以不要勾最下面的選項，這邊只是我想要分開，但分開真正要跑需要有 Redis，可以安裝 [docker](https://www.docker.com/products/docker-desktop) 後執行，`docker pull redis` & `docker run --name some-redis -d redis -p 6379:6379`

// 因為專案預設會啟用 Redis，如果沒有可以先關閉，在 appsettings.json 中的 Redis 裡面加上 "IsEnabled": "true", 請參考 [Redis 快取設定 說明文件](https://docs.abp.io/en/abp/latest/Redis-Cache#configuration)

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1626834411.png)

## 創建圖書實體

啟動模板中的**領域層**分為兩個項目：

* `Acme.BookStore.Domain`包括你的[實體](https://docs.abp.io/zh-Hans/abp/latest/Entities)、[領域服務](https://docs.abp.io/zh-Hans/abp/latest/Domain-Services)和其他核心對象(例如：倉儲介面)。
* `Acme.BookStore.Domain.Shared`包括可與客戶端共享的所有對象，枚舉或其他域相關。

### BookType 枚舉 (Enum)

下面的項目所產生的`BookType`枚舉，在`Acme.BookStore.Domain.Shared`創建`BookType`。

// 如果有開發過 API 應該遇過給 client 的時候蠻常會用到實體的 enum ，因為 DDD 中領域不會開放給外部(Client)，所以這類東西需要放在領域共用專案，方便到時候 DTO 可以直接使用。

```
namespace Acme.BookStore.Books
{
    public enum BookType
    {
        Undefined,
        Adventure,
        Biography,
        Dystopia,
        Fantastic,
        Horror,
        Science,
        ScienceFiction,
        Poetry
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1626838792.png)

### Book 實體 (Entity)

在解決方案的**領域層**（`Acme.BookStore.Domain`項目）中定義你的實體。

該應用程序的主要實體是`Book`。在`Acme.BookStore.Domain`項目中創建一個`Books`文件夾並在其中添加了一個名稱`Book`的類，如下所示：

```
using System;
using Volo.Abp.Domain.Entities.Auditing;

namespace Acme.BookStore.Books
{
    public class Book : AuditedAggregateRoot<Guid>
    {
        public string Name { get; set; }

        public BookType Type { get; set; }

        public DateTime PublishDate { get; set; }

        public float Price { get; set; }
    }
}
```

* ABP為實體提供了兩個基本的基類：`AggregateRoot`和`Entity`。**Aggregate Root**是[**領域驅動設計**](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Domain-Driven-Design)概念一個。可以直接查詢和處理的根實體（請參閱[實體文檔](https://docs.abp.io/zh-Hans/abp/latest/Entities)）。
  // 同聚合內非根的一般實體可以用 BookCover : Entity<Guid>，因為同聚合內應該只有一個根，DDD不熟暫時不想用也可以直接照你原本開發方式全部用一般實體基類Entity<T>
* `Book`實體繼承了`AuditedAggregateRoot`，`AuditedAggregateRoot`類在`AggregateRoot`類的基礎上添加了一些審計屬性( `CreationTime`, `CreatorId`, `LastModificationTime`)。ABP框架自動為你管理這些屬性。
  // 不用聚合根也不想那麼多審計屬性，[ABP 也提供其他基類](https://docs.abp.io/zh-Hans/abp/latest/Entities#%E5%AE%A1%E8%AE%A1%E5%9F%BA%E7%B1%BB)，比如：CreationAuditedEntity<TKey> ，再少也可以只使用 [ABP 提供的介面](https://docs.abp.io/zh-Hans/abp/latest/Entities#%E5%AE%A1%E8%AE%A1%E6%8E%A5%E5%8F%A3)，例如：IHasCreationTime，優點是可以統一屬性名稱為 `CreationTime`
{ignore-vars="true"}
* `Guid`是`Book`實體的主鍵類型。
  // 主鍵類型也可以自己改，例如：BookPage : Entity<long> ，只是 [ABP 推薦使用 Guid](https://docs.abp.io/zh-Hans/abp/latest/Entities#guid%E4%B8%BB%E9%94%AE%E7%9A%84%E5%AE%9E%E4%BD%93) 就是了
{ignore-vars="true"}

> 為了保持簡單，本教程將實體屬性保留為**public get/set**。如果您想了解 DDD 最佳實踐，請參閱[實體文檔](https://docs.abp.io/zh-Hans/abp/latest/Entities)。

// 這邊引用一下 [ABP 審計基類](https://docs.abp.io/zh-Hans/abp/latest/Entities#%E5%AE%A1%E8%AE%A1%E5%9F%BA%E7%B1%BB) 中關於實體中巡覽屬性的一段敘述給大家參考一下
{ignore-vars="true"}

> 所有這些基類也有`... WithUser`,像`FullAuditedAggregateRootWithUser<TUser>`和`FullAuditedAggregateRootWithUser<TKey, TUser>`.
>
> 這樣就可以將導航屬性添加到你的用戶實體.但在聚合根之間添加導航屬性不是一個好做法,所以這種用法是不建議的
>
> (**除非你使用 EF Core**之類的ORM可以很好地支持這種情況,並且你真的需要它.請記住這種方法不適用於NoSQL數據庫(如MongoDB),你必須真正實現聚合模式）.

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1626838362.png)

最終的文件夾/文件結構應該如下所示：

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1626838911.png)

### 將Book實體添加到DbContext中

EF Core 需要你將實體和`DbContext`建立關聯。最簡單的做法是在`Acme.BookStore.EntityFrameworkCore`項目的`BookStoreDbContext`類中添加`DbSet`屬性。如下所示：

```
public class BookStoreDbContext : AbpDbContext<BookStoreDbContext>
{
    public DbSet<Book> Books { get; set; }
    //...
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1626838226.png)

### 將書實體映射到數據庫表

在`Acme.BookStore.EntityFrameworkCore`項目中打開`BookStoreDbContextModelCreatingExtensions.cs`文件，添加`Book`實體的映射代碼。最終類應為：

```
using Acme.BookStore.Books;
using Microsoft.EntityFrameworkCore;
using Volo.Abp;
using Volo.Abp.EntityFrameworkCore.Modeling;

namespace Acme.BookStore.EntityFrameworkCore
{
    public static class BookStoreDbContextModelCreatingExtensions
    {
        public static void ConfigureBookStore(this ModelBuilder builder)
        {
            Check.NotNull(builder, nameof(builder));

            /* Configure your own tables/entities inside here */

            builder.Entity<Book>(b =>
            {
                b.ToTable(BookStoreConsts.DbTablePrefix + "Books",
                          BookStoreConsts.DbSchema);
                b.ConfigureByConvention(); //auto configure for the base class props
                b.Property(x => x.Name).IsRequired().HasMaxLength(128);
            });
        }
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1626839141.png)

* `ConfigureByConvention()` 方法優雅的配置/歸屬的屬性，應始終對你所有的屬性使用它。
* `BookStoreConsts`包含用於表的架構和表前綴的常量值。你不一定需要使用它，但建議在單點控製表的前綴。
  // 這是定義資料表名稱前綴，用來跟 Abp 開頭的表來做區分，方便辨識哪些是框架用的資料表，哪些是我們自己應用程式用的資料表，或自己定義不同前綴來分類自己的表，
  // 這邊建議統一定義在領域層的一個統一地方，預設是 `BookStoreConsts.cs` ，有其他需要共用的常量 (Const) 也可以繼續統一加在這裡，方便使用與管理。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1626839256.png)

### 添加數據遷移

啟動模板使用[EF Core Code First Migrations](https://docs.microsoft.com/zh-cn/ef/core/managing-schemas/migrations/)創建和維護數據庫架構。我們應該創建一個新的遷移並應用到數據庫。

在`Acme.BookStore.EntityFrameworkCore.DbMigrations`目錄中打開命令行輸入以下命令：

```
dotnet ef migrations add Created_Book_Entity
```

![](https://dotblogsfile.blob.core.windows.net/user/%E5%BE%A1%E6%98%9F%E5%B9%BB/f8aa590e-d43b-4f53-afa6-cea509e45adf/1626682350.png)
{ignore-vars="true"}

它會添加新的遷移類到項目中：

![書店-efcore-遷移](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/Tutorials/images/bookstore-efcore-migration.png)
> 如果你使用Visual Studio 你可能想要在*包授權管理(PMC)中*`Add-Migration Created_Book_Entity -c BookStoreMigrationsDbContext`*和使用*`Update-Database -c BookStoreMigrationsDbContext`*命令。確保*`Acme.BookStore.Web`*是啟動項目並且*`Acme.BookStore.EntityFrameworkCore.DbMigrations`*是 PMC 的默認項目*。

![](https://dotblogsfile.blob.core.windows.net/user/%E5%BE%A1%E6%98%9F%E5%B9%BB/f8aa590e-d43b-4f53-afa6-cea509e45adf/1626682501.png)
{ignore-vars="true"}

#### 添加附加數據 (SeedData)

// 在之後的 整合測試 章節會用到這份資料來做測試，雖然不是必須的流程，但這邊建議可以試著做一遍。

> 在運行應用程序最好之前將詳細數據添加到數據庫中。本節介紹ABP框架的[數據種子系統](https://docs.abp.io/zh-Hans/abp/latest/Data-Seeding)。如果你不想創建數據可以跳過本節，但是你自己會來學習這個建議的 ABP 框架功能。

在`*.Domain`項目下創建派生`IDataSeedContributor`的類，並且拷貝以下代碼：

```
using System;
using System.Threading.Tasks;
using Acme.BookStore.Books;
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Domain.Repositories;

namespace Acme.BookStore
{
    public class BookStoreDataSeederContributor
        : IDataSeedContributor, ITransientDependency
    {
        private readonly IRepository<Book, Guid> _bookRepository;

        public BookStoreDataSeederContributor(IRepository<Book, Guid> bookRepository)
        {
            _bookRepository = bookRepository;
        }

        public async Task SeedAsync(DataSeedContext context)
        {
            if (await _bookRepository.GetCountAsync() <= 0)
            {
                await _bookRepository.InsertAsync(
                    new Book
                    {
                        Name = "1984",
                        Type = BookType.Dystopia,
                        PublishDate = new DateTime(1949, 6, 8),
                        Price = 19.84f
                    },
                    autoSave: true
                );

                await _bookRepository.InsertAsync(
                    new Book
                    {
                        Name = "The Hitchhiker's Guide to the Galaxy",
                        Type = BookType.ScienceFiction,
                        PublishDate = new DateTime(1995, 9, 27),
                        Price = 42.0f
                    },
                    autoSave: true
                );
            }
        }
    }
}
```

* 如果中數據庫沒有當前圖書，則使用`IRepository<Book, Guid>`(默認為[知識庫](https://docs.abp.io/zh-Hans/abp/latest/Repositories))將兩本書插入數據庫。

![](https://dotblogsfile.blob.core.windows.net/user/%E5%BE%A1%E6%98%9F%E5%B9%BB/f8aa590e-d43b-4f53-afa6-cea509e45adf/1626683321.png)
{ignore-vars="true"}

### 更新數據庫

運行`Acme.BookStore.DbMigrator`應用程序來更新數據庫：

![bookstore-dbmigrator-on-solution](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/Tutorials/images/bookstore-dbmigrator-on-solution.png)

`.DbMigrator` 是一個開發使用程序，可以在**開發**和**生產**環境**遷移數據庫**和**初始化數據**。

// 預設連線字串指定的 DB Server 是 LocalDb (裝 VS 預設會有的開發用 DB)，沒有了話需要到 appsettings.json 改連線字串到自己的DB，

// 執行完以上可以用SSMS連到 (LocalDb)\MSSQLLocalDB 看看剛剛建立出來的資料庫與表，確認資料是否有如我們預期正確新建出來

## 創建應用程序

應用程序層由兩個單獨的項目組成：

* `Acme.BookStore.Application.Contracts`包含你的[DTO](https://docs.abp.io/zh-Hans/abp/latest/Data-Transfer-Objects)和[應用服務](https://docs.abp.io/zh-Hans/abp/latest/Application-Services)接口。
* `Acme.BookStore.Application` 包含你的應用服務實現。

在本部分中，您將創建一個應用程序服務，使用 ABP 框架的`CrudAppService`基類來獲取、創建、更新和刪除書籍。

// 這邊教學是使用非常規(ABP內建CRUD)的應用服務基底類別，基本的可以參考上一篇 [快速開始](https://dotblogs.com.tw/jakeuj/2021/07/20/abpio01) 的應用服務部分，

// 這邊主要是了解ABP如何簡化重複的CRUD程式碼，基本的可以不實作任何一行程式，只要定義DTO並繼承ABP的介面與基類就可以提供基本CRUD程作業

### Book Dto

`CrudAppService`基類需要定義實體的基本DTO。在`Acme.BookStore.Application.Contracts`項目中創建一個名稱`BookDto`的 DTO 類：

```
using System;
using Volo.Abp.Application.Dtos;

namespace Acme.BookStore
{
    public class BookDto : AuditedEntityDto<Guid>
    {
        public string Name { get; set; }

        public BookType Type { get; set; }

        public DateTime PublishDate { get; set; }

        public float Price { get; set; }
    }
}
```

* **DTO**類被用來**表示層**和**應用層** **傳遞數據**。查看[DTO 文檔](https://docs.abp.io/zh-Hans/abp/latest/Data-Transfer-Objects)查看更多信息。
* 為了在頁面上展示書籍信息，`BookDto`被將書籍數據傳遞到顯示層。
* `BookDto`繼承自`AuditedEntityDto<Guid>`。跟上面定義的`Book`實體一樣具有一些審計屬性。
  // 這邊為了用來做 CRUD，某些DTO可能需要繼承內鍵含有Id定義的基類，才能正常做Update與Delete，一般DTO則可以不用，可以參考 [快速開始](https://dotblogs.com.tw/jakeuj/2021/07/20/abpio01)

![](https://dotblogsfile.blob.core.windows.net/user/%E5%BE%A1%E6%98%9F%E5%B9%BB/bff36275-1beb-423a-9664-b96e21b3c91c/1626684853.png)
{ignore-vars="true"}

在將書籍返回到表示層時，需要將`Book`實體轉換為`BookDto`對象。[AutoMapper](https://automapper.org/)庫可以在定義正確的映射時自動執行此轉換。

啟動模板配置了AutoMapper，因此你很適合在`Acme.BookStore.Application`項目的`BookStoreApplicationAutoMapperProfile`類中定義映射：

```
using Acme.BookStore.Books;
using AutoMapper;

namespace Acme.BookStore
{
    public class BookStoreApplicationAutoMapperProfile : Profile
    {
        public BookStoreApplicationAutoMapperProfile()
        {
            CreateMap<Book, BookDto>();
        }
    }
}
```

> 參見[對像對對象](https://docs.abp.io/zh-Hans/abp/latest/Object-To-Object-Mapping)文檔了解詳情。

### 創建更新書Dto

在`Acme.BookStore.Application.Contracts`項目中創建一個名稱`CreateUpdateBookDto`的 DTO 類：

```
using System;
using System.ComponentModel.DataAnnotations;

namespace Acme.BookStore.Books
{
    public class CreateUpdateBookDto
    {
        [Required]
        [StringLength(128)]
        public string Name { get; set; }

        [Required]
        public BookType Type { get; set; } = BookType.Undefined;

        [Required]
        [DataType(DataType.Date)]
        public DateTime PublishDate { get; set; } = DateTime.Now;

        [Required]
        public float Price { get; set; }
    }
}
```

* 這個DTO類被用於在創建或更新書籍的時候從用戶界面獲取圖書信息。
* 它定義了數據註釋屬性（如`[Required]`）來定義屬性的驗證。DTO由ABP框架[自動驗證](https://docs.abp.io/zh-Hans/abp/latest/Validation)。

就像上面`BookDto`一樣，創建一個從對像`CreateUpdateBookDto`到`Book`實體的映射，最後一個映射類如下：

```
using Acme.BookStore.Books;
using AutoMapper;

namespace Acme.BookStore
{
    public class BookStoreApplicationAutoMapperProfile : Profile
    {
        public BookStoreApplicationAutoMapperProfile()
        {
            CreateMap<Book, BookDto>();
            CreateMap<CreateUpdateBookDto, Book>();
        }
    }
}
```

### 圖書應用服務介面

下一步是應用程序定義接口，在`Acme.BookStore.Application.Contracts`項目中定義一個未知`IBookAppService`的接口：

```
using System;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;

namespace Acme.BookStore.Books
{
    public interface IBookAppService :
        ICrudAppService< //Defines CRUD methods
            BookDto, //Used to show books
            Guid, //Primary key of the book entity
            PagedAndSortedResultRequestDto, //Used for paging/sorting
            CreateUpdateBookDto> //Used to create/update a book
    {

    }
}
```

* 框架定義應用程序服務的接口**不是必需的**。但是，它被建議為最佳實踐。
* `ICrudAppService`定義了常見的**CRUD**方法：`GetAsync`，`GetListAsync`，`CreateAsync`，`UpdateAsync`和`DeleteAsync`。
  你可以從空的`IApplicationService`接口繼承並手動定義自己的方法（將在下一個領域中完成）。
* `ICrudAppService`有一些變體，你可以在每個方法中單獨使用 DTO，也可以分別單獨指定（例如使用不同的 DTO 進行創建和更新）。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1627018683.png)

### 圖書應用服務

在`Acme.BookStore.Application`項目中命名`BookAppService`的`IBookAppService`實現：

```
using System;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;
using Volo.Abp.Domain.Repositories;

namespace Acme.BookStore.Books
{
    public class BookAppService :
        CrudAppService<
            Book, //The Book entity
            BookDto, //Used to show books
            Guid, //Primary key of the book entity
            PagedAndSortedResultRequestDto, //Used for paging/sorting
            CreateUpdateBookDto>, //Used to create/update a book
        IBookAppService //implement the IBookAppService
    {
        public BookAppService(IRepository<Book, Guid> repository)
            : base(repository)
        {

        }
    }
}
```

* `BookAppService`繼承了`CrudAppService<...>`。它實現了`ICrudAppService`定義的 CRUD 方法。
* `BookAppService`注入`IRepository <Book,Guid>`，這是`Book`實體的默認。ABP自動為每個化根(或實體)創建默認。請參閱[文檔](https://docs.abp.io/zh-Hans/abp/latest/Repositories)
* `BookAppService`使用[`IObjectMapper`](https://docs.abp.io/zh-Hans/abp/latest/Object-To-Object-Mapping)將`Book`對象轉換為`BookDto`對象, 將`CreateUpdateBookDto`對象轉換為`Book`對象。
  啟動模板使用[AutoMapper](http://automapper.org/)庫作為對象映射提供程序。我們之前定義了映射，從而導致方向預期工作。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/09547ec3-aaf1-4f7e-a6f0-91e27d5a7a1f/1627018955.png)

### 自動生成API控制器

通常你創建**控制器**以將應用程序服務公開為**HTTP API**。因此允許瀏覽器或客戶端通過 AJAX 調用他們。

ABP可以[**自動**](https://docs.abp.io/zh-Hans/abp/latest/API/Auto-API-Controllers)為你的應用程序服務配置MVC API控制器。

### Swagger 的用戶界面

啟動模板配置為使用[Swashbuckle.AspNetCore](https://github.com/domaindrivendev/Swashbuckle.AspNetCore)運行[swagger UI](https://swagger.io/tools/swagger-ui/)。運行應用程序並在瀏覽器中輸入`https://localhost:XXXX/swagger/`（用你自己的端口替換XXXX）作為URL。

你會看到一些內置的接口和`Book`接口，它們都是REST風格的：

![書店招搖](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/Tutorials/images/bookstore-swagger.png)

Swagger 有一個很好的 UI 來測試 API。

你可以嘗試執行`[GET] /api/app/book`API來獲取書籍列表，服務端會返回以下JSON結果：

```
{
  "totalCount": 2,
  "items": [
    {
      "name": "The Hitchhiker's Guide to the Galaxy",
      "type": 7,
      "publishDate": "1995-09-27T00:00:00",
      "price": 42,
      "lastModificationTime": null,
      "lastModifierId": null,
      "creationTime": "2020-07-03T21:04:18.4607218",
      "creatorId": null,
      "id": "86100bb6-cbc1-25be-6643-39f62806969c"
    },
    {
      "name": "1984",
      "type": 3,
      "publishDate": "1949-06-08T00:00:00",
      "price": 19.84,
      "lastModificationTime": null,
      "lastModifierId": null,
      "creationTime": "2020-07-03T21:04:18.3174016",
      "creatorId": null,
      "id": "41055277-cce8-37d7-bb37-39f62806960b"
    }
  ]
}
```

這很酷，因為我們沒有寫任何代碼來創建 API 控制器，但是現在我們有了一個可以正常使用的 REST API！

## 下一章

請參閱教程的[下一章](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/part-2)。

---

[ABP.IO WEB應用程式框架 新手教學 No.02 開發教學 Part 2 圖書列表頁面](https://dotblogs.com.tw/jakeuj/2021/07/21/abpio03)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
