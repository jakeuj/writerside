# ABP.IO WEB應用程式框架 新手教學 No.09 開發教學 第 8 部分&#xFF1A;作者&#xFF1A;應用服務層

> **原文發布日期:** 2021-07-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/23/ABP-Tutorials-Part-8
> **標籤:** 無

---

主要說明一般常用的API該如何一步一步地完成

包含服務介面(這次使用一般應用介面而非CRUD專用介面)

還有介面實作、權限屬性、AutoMapper、種子資料、測試

## Web 應用程序開發教程 - 第 8 部分：作者：應用程序層

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
* [第 7 部分：作者：數據庫集成](https://docs.abp.io/en/abp/latest/Tutorials/Part-7)
* **第八部分：作者：應用層（本部分）**
* [第 9 部分：作者：用戶界面](https://docs.abp.io/en/abp/latest/Tutorials/Part-9)
* [第 10 部分：書與作者的關係](https://docs.abp.io/en/abp/latest/Tutorials/Part-10)

### 下載源代碼

本教程根據您的**UI**和**數據庫**首選項有多個版本。我們準備了幾個要下載的源代碼組合：

* [帶有 EF Core 的 MVC（Razor Pages）UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Mvc-EfCore)
* [帶有 EF Core 的 Blazor UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Blazor-EfCore)
* [帶有 MongoDB 的 Angular UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Angular-MongoDb)

## 介紹

這部分說明為之前創建的`Author`實體創建一個應用層。

## IAuthorAppService

我們將首先創建[應用服務](https://docs.abp.io/en/abp/latest/Application-Services)接口和相關的[DTO](https://docs.abp.io/en/abp/latest/Data-Transfer-Objects)。在項目`IAuthorAppService`的`Authors`命名空間（文件夾）中創建一個名為 的新接口`Acme.BookStore.Application.Contracts`：

```
using System;
using System.Threading.Tasks;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Application.Services;

namespace Acme.BookStore.Authors
{
    public interface IAuthorAppService : IApplicationService
    {
        Task<AuthorDto> GetAsync(Guid id);

        Task<PagedResultDto<AuthorDto>> GetListAsync(GetAuthorListDto input);

        Task<AuthorDto> CreateAsync(CreateAuthorDto input);

        Task UpdateAsync(Guid id, UpdateAuthorDto input);

        Task DeleteAsync(Guid id);
    }
}
```

* `IApplicationService` 是所有應用服務都繼承的約定俗成的接口，所以ABP框架可以識別服務。
* 定義了對`Author`實體執行 CRUD 操作的標準方法。
* `PagedResultDto`是 ABP 框架中預定義的 DTO 類。它有一個`Items`集合和一個`TotalCount`返回分頁結果的屬性。
* 首選`AuthorDto`從`CreateAsync`方法返回（對於新創建的作者），而此應用程序不使用它 - 只是為了顯示不同的用法。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627030796.png)

此接口使用下面定義的 DTO（為您的項目創建它們）。

### AuthorDto

```
using System;
using Volo.Abp.Application.Dtos;

namespace Acme.BookStore.Authors
{
    public class AuthorDto : EntityDto<Guid>
    {
        public string Name { get; set; }

        public DateTime BirthDate { get; set; }

        public string ShortBio { get; set; }
    }
}
```

* `EntityDto<T>`僅具有`Id`具有給定泛型參數的屬性。您可以`Id`自己創建一個屬性，而不是繼承`EntityDto<T>`.

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627030856.png)

### GetAuthorListDto - 獲取作者列表

```
using Volo.Abp.Application.Dtos;

namespace Acme.BookStore.Authors
{
    public class GetAuthorListDto : PagedAndSortedResultRequestDto
    {
        public string Filter { get; set; }
    }
}
```

* `Filter`用於搜索作者。可以`null`（或空字符串）獲取所有作者。
* `PagedAndSortedResultRequestDto`具有標準的分頁和排序屬性：`int MaxResultCount`,`int SkipCount`和`string Sorting`。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627030919.png)
> ABP 框架有這樣的基本 DTO 類來簡化和標準化你的 DTO。請參閱[DTO 文檔](https://docs.abp.io/en/abp/latest/Data-Transfer-Objects)了解所有信息。

### CreateAuthorDto - 創建作者

```
using System;
using System.ComponentModel.DataAnnotations;

namespace Acme.BookStore.Authors
{
    public class CreateAuthorDto
    {
        [Required]
        [StringLength(AuthorConsts.MaxNameLength)]
        public string Name { get; set; }

        [Required]
        public DateTime BirthDate { get; set; }

        public string ShortBio { get; set; }
    }
}
```

數據註釋屬性可用於驗證 DTO。有關詳細信息，請參閱[驗證文件](https://docs.abp.io/en/abp/latest/Validation)。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627030989.png)

### UpdateAuthorDto - 更新作者

```
using System;
using System.ComponentModel.DataAnnotations;

namespace Acme.BookStore.Authors
{
    public class UpdateAuthorDto
    {
        [Required]
        [StringLength(AuthorConsts.MaxNameLength)]
        public string Name { get; set; }

        [Required]
        public DateTime BirthDate { get; set; }

        public string ShortBio { get; set; }
    }
}
```

> 我們可以在創建和更新操作之間共享（重用）相同的 DTO。雖然你可以做到，但我們更喜歡為這些操作創建不同的 DTO，因為我們看到它們通常隨著時間的推移而不同。因此，與緊耦合設計相比，這裡的代碼重複是合理的。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627031168.png)

## 作者應用服務

是時候實現`IAuthorAppService`接口了。創建一個新的類別，在 `Acme.BookStore.Application` 項目的`Authors`命名空間（文件夾）中命名 `AuthorAppService`：

```
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Acme.BookStore.Permissions;
using Microsoft.AspNetCore.Authorization;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Domain.Repositories;

namespace Acme.BookStore.Authors
{
    [Authorize(BookStorePermissions.Authors.Default)]
    public class AuthorAppService : BookStoreAppService, IAuthorAppService
    {
        private readonly IAuthorRepository _authorRepository;
        private readonly AuthorManager _authorManager;

        public AuthorAppService(
            IAuthorRepository authorRepository,
            AuthorManager authorManager)
        {
            _authorRepository = authorRepository;
            _authorManager = authorManager;
        }

        //...SERVICE METHODS WILL COME HERE...
    }
}
```

* `[Authorize(BookStorePermissions.Authors.Default)]`是一種檢查權限（策略）以授權當前用戶的聲明性方式。詳見[授權文件](https://docs.abp.io/en/abp/latest/Authorization)。`BookStorePermissions`類將在下面更新，現在不要擔心編譯錯誤。
* 派生自`BookStoreAppService`，它是啟動模板附帶的一個簡單基類。它派生自標準`ApplicationService`類。
* 實現了`IAuthorAppService`上面定義的。
* 注入`IAuthorRepository`和`AuthorManager`以在服務方法中使用。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627031311.png)

現在，我們將一一介紹服務方法。將解釋的方法複製到`AuthorAppService`類中。

### GetAsync

// 這邊主要展示如何利用 ABP 進行 AutoMapper 的自動映射

```
public async Task<AuthorDto> GetAsync(Guid id)
{
    var author = await _authorRepository.GetAsync(id);
    return ObjectMapper.Map<Author, AuthorDto>(author);
}
```

這個方法簡單地通過`Author`實體獲取實體`Id`，轉換為`AuthorDto`使用對[像到對象映射器](https://docs.abp.io/en/abp/latest/Object-To-Object-Mapping)。這需要配置AutoMapper，後面會解釋。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627031430.png)

### GetListAsync

// 這主要展示取得集合時的分頁，排序，篩選，可以如何利用 ABP 進行實作

```
public async Task<PagedResultDto<AuthorDto>> GetListAsync(GetAuthorListDto input)
{
    if (input.Sorting.IsNullOrWhiteSpace())
    {
        input.Sorting = nameof(Author.Name);
    }

    var authors = await _authorRepository.GetListAsync(
        input.SkipCount,
        input.MaxResultCount,
        input.Sorting,
        input.Filter
    );

    var totalCount = input.Filter == null
        ? await _authorRepository.CountAsync()
        : await _authorRepository.CountAsync(
            author => author.Name.Contains(input.Filter));

    return new PagedResultDto<AuthorDto>(
        totalCount,
        ObjectMapper.Map<List<Author>, List<AuthorDto>>(authors)
    );
}
```

* 默認排序是“按作者姓名”，它在方法的開頭完成，以防它不是由客戶端發送的。
* 用於`IAuthorRepository.GetListAsync`從數據庫中獲取分頁、排序​​和過濾的作者列表。我們已經在本教程的前一部分中實現了它。同樣，實際上不需要創建這樣的方法，因為我們可以直接查詢存儲庫，但想演示如何創建自定義存儲庫方法。
* 直接從`AuthorRepository`獲取作者計數的同時查詢。如果發送了過濾器，那麼我們將在獲取計數時使用它來過濾實體。
* 最後，通過將`Author`列表映射到 `AuthorDto` 列表來返回分頁結果。

### CreateAsync

// 這邊主要展示如何使用屬性的方式來設定權限

```
[Authorize(BookStorePermissions.Authors.Create)]
public async Task<AuthorDto> CreateAsync(CreateAuthorDto input)
{
    var author = await _authorManager.CreateAsync(
        input.Name,
        input.BirthDate,
        input.ShortBio
    );

    await _authorRepository.InsertAsync(author);

    return ObjectMapper.Map<Author, AuthorDto>(author);
}
```

* `CreateAsync`需要`BookStorePermissions.Authors.Create`權限（除了`BookStorePermissions.Authors.Default`為`AuthorAppService`類聲明的）。
* 使用`AuthorManager`（域服務）創建新作者。
* 用於`IAuthorRepository.InsertAsync`將新作者插入到數據庫中。
* 使用`ObjectMapper`返回一個`AuthorDto`代表新創建的作者。

> **DDD 提示**：一些開發人員可能會發現將新實體插入到`_authorManager.CreateAsync`. 我們認為將它留給應用層是一個更好的設計，因為它更好地知道什麼時候將它插入到數據庫中（也許它需要在插入之前對實體進行額外的工作，如果我們在域服務）。但是，這完全取決於您。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627031565.png)

### UpdateAsync

// 這邊主要展示如何在更新時透過領域服務來套用業務邏輯 (DDD)

```
[Authorize(BookStorePermissions.Authors.Edit)]
public async Task UpdateAsync(Guid id, UpdateAuthorDto input)
{
    var author = await _authorRepository.GetAsync(id);

    if (author.Name != input.Name)
    {
        await _authorManager.ChangeNameAsync(author, input.Name);
    }

    author.BirthDate = input.BirthDate;
    author.ShortBio = input.ShortBio;

    await _authorRepository.UpdateAsync(author);
}
```

* `UpdateAsync`需要額外的`BookStorePermissions.Authors.Edit`權限。
* 用於`IAuthorRepository.GetAsync`從數據庫中獲取作者實體。如果沒有給定 id 的作者，則`GetAsync`拋出異常`EntityNotFoundException`，這會導致`404`Web 應用程序中的HTTP 狀態代碼。始終使實體進行更新操作是一種很好的做法。
* `AuthorManager.ChangeNameAsync`如果客戶端要求更改作者姓名，則使用（域服務方法）更改作者姓名。
* 直接更新`BirthDate`並且`ShortBio`由於沒有任何業務規則來更改這些屬性，因此它們接受任何值。
* 最後，調用`IAuthorRepository.UpdateAsync`方法更新數據庫上的實體。

> **EF Core 提示**：Entity Framework Core 具有**更改跟踪**系統，並在工作單元結束時**自動保存**對實體的任何更改（您可以簡單地認為 ABP 框架會`SaveChanges`在方法結束時自動調用）。因此，即使您沒有`_authorRepository.UpdateAsync(...)`在方法的末尾調用 ，它也會按預期工作。如果您以後不考慮更改 EF Core，則可以刪除此行。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627032142.png)

### DeleteAsync

```
[Authorize(BookStorePermissions.Authors.Delete)]
public async Task DeleteAsync(Guid id)
{
    await _authorRepository.DeleteAsync(id);
}
```

* `DeleteAsync`需要額外的`BookStorePermissions.Authors.Delete`權限。
* 它只是使用`DeleteAsync`存儲庫的方法。

## 權限定義

您無法編譯代碼，因為它需要在`BookStorePermissions`類中聲明一些常量。

打開 `Acme.BookStore.Application.Contracts` 專案裡面的類 `BookStorePermissions`（在`Permissions`文件夾中），修改內容如下圖：

```
namespace Acme.BookStore.Permissions
{
    public static class BookStorePermissions
    {
        public const string GroupName = "BookStore";

        public static class Books
        {
            public const string Default = GroupName + ".Books";
            public const string Create = Default + ".Create";
            public const string Edit = Default + ".Edit";
            public const string Delete = Default + ".Delete";
        }

        // *** ADDED a NEW NESTED CLASS ***
        public static class Authors
        {
            public const string Default = GroupName + ".Authors";
            public const string Create = Default + ".Create";
            public const string Edit = Default + ".Edit";
            public const string Delete = Default + ".Delete";
        }
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627032305.png)

然後`BookStorePermissionDefinitionProvider`在同一個項目中打開 並在`Define`方法的末尾添加以下幾行：

```
var authorsPermission = bookStoreGroup.AddPermission(
    BookStorePermissions.Authors.Default, L("Permission:Authors"));

authorsPermission.AddChild(
    BookStorePermissions.Authors.Create, L("Permission:Authors.Create"));

authorsPermission.AddChild(
    BookStorePermissions.Authors.Edit, L("Permission:Authors.Edit"));

authorsPermission.AddChild(
    BookStorePermissions.Authors.Delete, L("Permission:Authors.Delete"));
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627032454.png)

最後，將以下條目添加到 `Acme.BookStore.Domain.Shared`項目`Localization/BookStore/en.json`內部，以本地化權限名稱：

```
"Permission:Authors": "Author Management",
"Permission:Authors.Create": "Creating new authors",
"Permission:Authors.Edit": "Editing the authors",
"Permission:Authors.Delete": "Deleting the authors"
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627032509.png)

## 對像到對象映射

`AuthorAppService`正在使用`ObjectMapper`將`Author`對象轉換為`AuthorDto`對象。所以，我們需要在 AutoMapper 配置中定義這個映射。

打開 `Acme.BookStore.Application` 項目中的`BookStoreApplicationAutoMapperProfile`類並將以下行添加到構造函數中：

```
CreateMap<Author, AuthorDto>();
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627032622.png)

## 數據播種機 (Seed Data Contributor)

正如之前對書籍所做的那樣，最好在數據庫中包含一些初始作者實體。這在第一次運行應用程序時會很好，但對於自動化測試也非常有用。

`BookStoreDataSeederContributor`在`Acme.BookStore.Domain`項目中，打開並使用以下代碼更改文件內容：

```
using System;
using System.Threading.Tasks;
using Acme.BookStore.Authors;
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
        private readonly IAuthorRepository _authorRepository;
        private readonly AuthorManager _authorManager;

        public BookStoreDataSeederContributor(
            IRepository<Book, Guid> bookRepository,
            IAuthorRepository authorRepository,
            AuthorManager authorManager)
        {
            _bookRepository = bookRepository;
            _authorRepository = authorRepository;
            _authorManager = authorManager;
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

            // ADDED SEED DATA FOR AUTHORS

            if (await _authorRepository.GetCountAsync() <= 0)
            {
                await _authorRepository.InsertAsync(
                    await _authorManager.CreateAsync(
                        "George Orwell",
                        new DateTime(1903, 06, 25),
                        "Orwell produced literary criticism and poetry, fiction and polemical journalism; and is best known for the allegorical novella Animal Farm (1945) and the dystopian novel Nineteen Eighty-Four (1949)."
                    )
                );

                await _authorRepository.InsertAsync(
                    await _authorManager.CreateAsync(
                        "Douglas Adams",
                        new DateTime(1952, 03, 11),
                        "Douglas Adams was an English author, screenwriter, essayist, humorist, satirist and dramatist. Adams was an advocate for environmentalism and conservation, a lover of fast cars, technological innovation and the Apple Macintosh, and a self-proclaimed 'radical atheist'."
                    )
                );
            }
        }
    }
}
```

現在，您可以運行`.DbMigrator`控制台應用程序**遷移**的**數據庫架構**和**種子**的初始數據。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627032845.png)

## 測試作者申請服務

最後，我們可以為`IAuthorAppService`. 添加一個新類，`AuthorAppService_Tests`在 `Acme.BookStore.Application.Tests` 項目的`Authors`命名空間（文件夾）中命名：

```
using System;
using System.Threading.Tasks;
using Shouldly;
using Xunit;

namespace Acme.BookStore.Authors
{
    public class AuthorAppService_Tests : BookStoreApplicationTestBase
    {
        private readonly IAuthorAppService _authorAppService;

        public AuthorAppService_Tests()
        {
            _authorAppService = GetRequiredService<IAuthorAppService>();
        }

        [Fact]
        public async Task Should_Get_All_Authors_Without_Any_Filter()
        {
            var result = await _authorAppService.GetListAsync(new GetAuthorListDto());

            result.TotalCount.ShouldBeGreaterThanOrEqualTo(2);
            result.Items.ShouldContain(author => author.Name == "George Orwell");
            result.Items.ShouldContain(author => author.Name == "Douglas Adams");
        }

        [Fact]
        public async Task Should_Get_Filtered_Authors()
        {
            var result = await _authorAppService.GetListAsync(
                new GetAuthorListDto {Filter = "George"});

            result.TotalCount.ShouldBeGreaterThanOrEqualTo(1);
            result.Items.ShouldContain(author => author.Name == "George Orwell");
            result.Items.ShouldNotContain(author => author.Name == "Douglas Adams");
        }

        [Fact]
        public async Task Should_Create_A_New_Author()
        {
            var authorDto = await _authorAppService.CreateAsync(
                new CreateAuthorDto
                {
                    Name = "Edward Bellamy",
                    BirthDate = new DateTime(1850, 05, 22),
                    ShortBio = "Edward Bellamy was an American author..."
                }
            );

            authorDto.Id.ShouldNotBe(Guid.Empty);
            authorDto.Name.ShouldBe("Edward Bellamy");
        }

        [Fact]
        public async Task Should_Not_Allow_To_Create_Duplicate_Author()
        {
            await Assert.ThrowsAsync<AuthorAlreadyExistsException>(async () =>
            {
                await _authorAppService.CreateAsync(
                    new CreateAuthorDto
                    {
                        Name = "Douglas Adams",
                        BirthDate = DateTime.Now,
                        ShortBio = "..."
                    }
                );
            });
        }

        //TODO: Test other methods...
    }
}
```

為應用服務方法創建了一些測試，應該很容易理解。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f2f20135-b3fd-4c0d-843e-dd74ccc5877a/1627033014.png)

## 下一部分

請參閱本教程的[下一部分](https://docs.abp.io/en/abp/latest/Tutorials/Part-9)。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
