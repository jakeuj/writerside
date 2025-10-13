# ABP.IO WEB應用程式框架 新手教學 No.07 開發教學 第 6 部分 作者&#xFF1A;領域層 {id="ABP.IO-WEB應用程式框架-新手教學-No.07-開發教學-第-6-部分-作者&#xFF1A;領域層"}

> **原文發布日期:** 2021-07-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/23/ABP-Tutorials-Part-6
> **標籤:** 無

---

使用一些 DDD 最佳實踐來實作 Author 的領域層

## Web 應用程序開發教程 - 第 6 部分：作者：領域層

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
* **第 6 部分：作者：領域層（本部分）**
* [第 7 部分：作者：數據庫集成](https://docs.abp.io/en/abp/latest/Tutorials/Part-7)
* [第 8 部分：作者：應用程序層](https://docs.abp.io/en/abp/latest/Tutorials/Part-8)
* [第 9 部分：作者：用戶界面](https://docs.abp.io/en/abp/latest/Tutorials/Part-9)
* [第 10 部分：書與作者的關係](https://docs.abp.io/en/abp/latest/Tutorials/Part-10)

### 下載源代碼

本教程根據您的**UI**和**數據庫**首選項有多個版本。我們準備了幾個要下載的源代碼組合：

* [帶有 EF Core 的 MVC（Razor Pages）UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Mvc-EfCore)
* [帶有 EF Core 的 Blazor UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Blazor-EfCore)
* [帶有 MongoDB 的 Angular UI](https://github.com/abpframework/abp-samples/tree/master/BookStore-Angular-MongoDb)

## 介紹

在前面的部分中，我們已經使用 ABP 基礎架構輕鬆構建了一些服務；

* 使用[CrudAppService](https://docs.abp.io/en/abp/latest/Application-Services)基類，而不是為標準的創建、讀取、更新和刪除操作手動開發應用程序服務。
* 使用[通用存儲庫](https://docs.abp.io/en/abp/latest/Repositories)來完全自動化數據庫層。

對於“作者”部分；

* 我們將**手動完成一些操作，**以展示您在需要時如何進行操作。
* 我們將實施一些**領域驅動設計 (DDD) 最佳實踐**。

> **開發將逐層進行，以一次集中在單個層上。在實際項目中，您將按功能（垂直）開發應用程序功能，如前幾部分所述。通過這種方式，您將體驗兩種方法。**

## 作者實體

`Authors`在`Acme.BookStore.Domain`項目中創建一個文件夾（命名空間）並在其中添加一個`Author`類：

```
using System;
using JetBrains.Annotations;
using Volo.Abp;
using Volo.Abp.Domain.Entities.Auditing;

namespace Acme.BookStore.Authors
{
    public class Author : FullAuditedAggregateRoot<Guid>
    {
        public string Name { get; private set; }
        public DateTime BirthDate { get; set; }
        public string ShortBio { get; set; }

        private Author()
        {
            /* This constructor is for deserialization / ORM purpose */
        }

        internal Author(
            Guid id,
            [NotNull] string name,
            DateTime birthDate,
            [CanBeNull] string shortBio = null)
            : base(id)
        {
            SetName(name);
            BirthDate = birthDate;
            ShortBio = shortBio;
        }

        internal Author ChangeName([NotNull] string name)
        {
            SetName(name);
            return this;
        }

        private void SetName([NotNull] string name)
        {
            Name = Check.NotNullOrWhiteSpace(
                name,
                nameof(name),
                maxLength: AuthorConsts.MaxNameLength
            );
        }
    }
}
```

* 繼承自`FullAuditedAggregateRoot<Guid>`which 使實體[軟刪除](https://docs.abp.io/en/abp/latest/Data-Filtering)（這意味著當您刪除它時，它不會在數據庫中刪除，而只是標記為已刪除）具有所有[審計](https://docs.abp.io/en/abp/latest/Entities)屬性。
* `private set`因為`Name`屬性限制從這個類中設置這個屬性。有兩種設置名稱的方法（在這兩種情況下，我們都驗證名稱）：
  + 在構造函數中，同時創建一個新作者。
  + `ChangeName`稍後使用該方法更新名稱。
* 的`constructor`和`ChangeName`方法是`internal`迫使僅在域層使用這些方法，使用`AuthorManager`將在後面說明。
* `Check`class 是一個 ABP 框架實用程序類，可幫助您檢查方法參數（它會引發`ArgumentException`無效情況）。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/acc54cd3-0216-4d21-9550-4ccb95e1c2c1/1627027394.png)

`AuthorConsts`是一個簡單的類，位於項目的`Authors`命名空間（文件夾）下`Acme.BookStore.Domain.Shared`：

```
namespace Acme.BookStore.Authors
{
    public static class AuthorConsts
    {
        public const int MaxNameLength = 64;
    }
}
```

在`Acme.BookStore.Domain.Shared`項目內部創建了這個類，因為我們稍後將在[數據傳輸對象](https://docs.abp.io/en/abp/latest/Data-Transfer-Objects)(DTO)上重用它。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/acc54cd3-0216-4d21-9550-4ccb95e1c2c1/1627027510.png)

## AuthorManager：領域服務

`Author`構造函數和`ChangeName`方法是`internal`，因此它們只能在領域層中使用。

在 `Acme.BookStore.Domain` 專案的`Authors`文件夾（命名空間）中創建一個類 `AuthorManager`：

```
using System;
using System.Threading.Tasks;
using JetBrains.Annotations;
using Volo.Abp;
using Volo.Abp.Domain.Services;

namespace Acme.BookStore.Authors
{
    public class AuthorManager : DomainService
    {
        private readonly IAuthorRepository _authorRepository;

        public AuthorManager(IAuthorRepository authorRepository)
        {
            _authorRepository = authorRepository;
        }

        public async Task<Author> CreateAsync(
            [NotNull] string name,
            DateTime birthDate,
            [CanBeNull] string shortBio = null)
        {
            Check.NotNullOrWhiteSpace(name, nameof(name));

            var existingAuthor = await _authorRepository.FindByNameAsync(name);
            if (existingAuthor != null)
            {
                throw new AuthorAlreadyExistsException(name);
            }

            return new Author(
                GuidGenerator.Create(),
                name,
                birthDate,
                shortBio
            );
        }

        public async Task ChangeNameAsync(
            [NotNull] Author author,
            [NotNull] string newName)
        {
            Check.NotNull(author, nameof(author));
            Check.NotNullOrWhiteSpace(newName, nameof(newName));

            var existingAuthor = await _authorRepository.FindByNameAsync(newName);
            if (existingAuthor != null && existingAuthor.Id != author.Id)
            {
                throw new AuthorAlreadyExistsException(newName);
            }

            author.ChangeName(newName);
        }
    }
}
```

* `AuthorManager`強制以受控方式創建作者和更改作者姓名。應用層（後面會介紹）會用到這些方法。

> **DDD 提示**：除非確實需要並執行一些核心業務規則，否則不要引入域服務方法。
>
> 對於這種情況，我們需要此服務能夠強制唯一名稱約束。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/acc54cd3-0216-4d21-9550-4ccb95e1c2c1/1627027935.png)

兩種方法都會檢查是否已經存在具有給定名稱的作者並拋出一個特殊的業務異常，`AuthorAlreadyExistsException`在`Acme.BookStore.Domain`項目（`Authors`文件夾中）中定義，如下所示：

```
using Volo.Abp;

namespace Acme.BookStore.Authors
{
    public class AuthorAlreadyExistsException : BusinessException
    {
        public AuthorAlreadyExistsException(string name)
            : base(BookStoreDomainErrorCodes.AuthorAlreadyExists)
        {
            WithData("name", name);
        }
    }
}
```

`BusinessException`是一種特殊的異常類型。在需要時拋出域相關的異常是一個很好的做法。它由 ABP 框架自動處理，並且可以輕鬆本地化。

`WithData(...)`方法用於向異常對象提供附加數據，這些數據稍後將用於本地化消息或用於其他目的。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/acc54cd3-0216-4d21-9550-4ccb95e1c2c1/1627027997.png)

`BookStoreDomainErrorCodes`在`Acme.BookStore.Domain.Shared`項目中打開，修改如下圖：

```
namespace Acme.BookStore
{
    public static class BookStoreDomainErrorCodes
    {
        public const string AuthorAlreadyExists = "BookStore:00001";
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/acc54cd3-0216-4d21-9550-4ccb95e1c2c1/1627028152.png)

這是一個唯一的字符串，代表您的應用程序拋出的錯誤代碼，可由客戶端應用程序處理。對於用戶，您可能希望對其進行本地化。

打開項目`Localization/BookStore/en.json`內部`Acme.BookStore.Domain.Shared`並添加以下條目：

```
"BookStore:00001": "There is already an author with the same name: {name}"
```

無論何時拋出`AuthorAlreadyExistsException`，最終用戶都會在 UI 上看到一條很好的錯誤消息。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/acc54cd3-0216-4d21-9550-4ccb95e1c2c1/1627028256.png)

## IAuthorRepository

// 這個自訂倉儲的所定義的方法其實直接使用內建的通用倉儲就可以完成，這邊只是為了示範自訂倉儲該如何一步步實現，如果用不到沒必要多此一舉。

`AuthorManager`注入`IAuthorRepository`，所以我們需要定義它。在 `Acme.BookStore.Domain` 項目的`Authors`文件夾（命名空間）中創建這個新接口：

```
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Volo.Abp.Domain.Repositories;

namespace Acme.BookStore.Authors
{
    public interface IAuthorRepository : IRepository<Author, Guid>
    {
        Task<Author> FindByNameAsync(string name);

        Task<List<Author>> GetListAsync(
            int skipCount,
            int maxResultCount,
            string sorting,
            string filter = null
        );
    }
}
```

* `IAuthorRepository`擴展了標準`IRepository<Author, Guid>`接口，因此所有標準[存儲庫](https://docs.abp.io/en/abp/latest/Repositories)方法也可用於`IAuthorRepository`.
* `FindByNameAsync`用於`AuthorManager`按姓名查詢作者。
* `GetListAsync` 將在應用程序層中用於獲取列出、排序和過濾的作者列表以顯示在 UI 上。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/acc54cd3-0216-4d21-9550-4ccb95e1c2c1/1627028426.png)

我們將在下一部分實現這個存儲庫。

// 這邊由於 DDD 領域層不會相依基礎設施層，所以在這邊只定義了介面，至於實作部分因為會使用到 DbContext，所以會放到基礎設施層來進行實作的部分。

> 這兩種方法**似乎都沒有必要，**因為標準存儲庫已經存在`IQueryable`，您可以直接使用它們而不是定義此類自定義方法。
>
> 你是對的，就像在真正的應用程序中一樣。但是，對於這個**“學習”教程**，解釋如何在您真正需要時創建自定義存儲庫方法很有用。

## 結論

這部分涵蓋了書店應用程序作者功能的領域層。在此部分中創建/更新的主要文件在下圖中突出顯示：

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/acc54cd3-0216-4d21-9550-4ccb95e1c2c1/1627029402.png)![書店作者域層](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/bookstore-author-domain-layer.png)

## 下一部分

請參閱本教程的[下一部分](https://docs.abp.io/en/abp/latest/Tutorials/Part-7)。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
