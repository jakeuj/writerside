# ABP.IO WEB應用程式框架 新手教學 No.06 開發教學  第 5 部分 授權

> **原文發布日期:** 2021-07-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/23/ABP-Tutorials-Part-5
> **標籤:** 無

---

這篇主要說明 ABP 內建的授權系統

使用  RBAC ([以角色為基礎的存取控制](https://zh.wikipedia.org/zh-tw/%E4%BB%A5%E8%A7%92%E8%89%B2%E7%82%BA%E5%9F%BA%E7%A4%8E%E7%9A%84%E5%AD%98%E5%8F%96%E6%8E%A7%E5%88%B6))
{ignore-vars="true"}

## Web應用程序開發教程 - [第五部分：授權](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-5)

## 關於本教程

在本系列教程中，您將構建一個名稱`Acme.BookStore`的用於管理書籍及其作者列表的基於 ABP 的程序。是使用以下技術開發的：

* **Entity Framework Core 為**ORM 提供程序。
* **Angular**做為 UI 框架。

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

---

## 權限

ABP Framework 提供了一個基於 ASP.NET Core 的[授權基礎架構](https://docs.microsoft.com/en-us/aspnet/core/security/authorization/introduction)的[授權系統](https://docs.abp.io/en/abp/latest/Authorization)。在標準授權基礎架構之上添加的一項主要功能是**權限系統**，它允許定義權限並啟用/禁用每個角色、用戶或客戶端。

### 權限名稱

權限必須具有唯一的名稱 (一個 `string`)。最好的方法是將其定義為 一個 `const`，這樣我們就可以重用權限名稱。

打開 `Acme.BookStore.Application.Contracts`專案裡面的`BookStorePermissions`類（在`Permissions`文件夾中），修改內容如下圖：

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
    }
}
```

這是定義權限名稱的分層方式。例如，“創建書”權限名稱定義為`BookStore.Books.Create`。ABP 不會強迫您使用結構，但我們發現這種方式很有用。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/13c109ab-9312-4d96-a13f-58ec30b74fc5/1627025316.png)

### 權限定義

您應該在使用它們之前定義權限。

打開 `Acme.BookStore.Application.Contracts` 專案裡面的`BookStorePermissionDefinitionProvider`類（在`Permissions`文件夾中），修改內容如下圖：

```
using Acme.BookStore.Localization;
using Volo.Abp.Authorization.Permissions;
using Volo.Abp.Localization;

namespace Acme.BookStore.Permissions
{
    public class BookStorePermissionDefinitionProvider : PermissionDefinitionProvider
    {
        public override void Define(IPermissionDefinitionContext context)
        {
            var bookStoreGroup = context.AddGroup(BookStorePermissions.GroupName, L("Permission:BookStore"));

            var booksPermission = bookStoreGroup.AddPermission(BookStorePermissions.Books.Default, L("Permission:Books"));
            booksPermission.AddChild(BookStorePermissions.Books.Create, L("Permission:Books.Create"));
            booksPermission.AddChild(BookStorePermissions.Books.Edit, L("Permission:Books.Edit"));
            booksPermission.AddChild(BookStorePermissions.Books.Delete, L("Permission:Books.Delete"));
        }

        private static LocalizableString L(string name)
        {
            return LocalizableString.Create<BookStoreResource>(name);
        }
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/13c109ab-9312-4d96-a13f-58ec30b74fc5/1627025548.png)

這個類定義了一個**權限組**（在 UI 上對權限進行分組，將在下面看到）和這個組內的**4 個權限**。

此外，**Create**、**Edit**和**Delete**是`BookStorePermissions.Books.Default`權限的子級。**只有**選擇**了父**權限，才能選擇子權限。

最後，編輯本地化文件（`en.json`在項目`Localization/BookStore`文件夾下`Acme.BookStore.Domain.Shared`）定義上面使用的本地化鍵：

```
"Permission:BookStore": "Book Store",
"Permission:Books": "Book Management",
"Permission:Books.Create": "Creating new books",
"Permission:Books.Edit": "Editing the books",
"Permission:Books.Delete": "Deleting the books"
```

> 本地化鍵名是任意的，沒有強制規則。但我們更喜歡上面使用的約定。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/13c109ab-9312-4d96-a13f-58ec30b74fc5/1627025741.png)

### 權限管理界面

// 這邊是 Angular 前端畫面，這裡先快速帶過

定義權限後，您可以在**權限管理模式中**看到它們。

進入*Administration -> Identity -> Roles*頁面，選擇admin 角色的*Permissions*操作，打開權限管理模式：

![書店權限-ui](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/bookstore-permissions-ui.png)

授予您想要的權限並保存模態。

> **提示**：如果您運行`Acme.BookStore.DbMigrator`應用程序，新的權限會自動授予管理員角色。

## 授權

現在，您可以使用權限來授權圖書管理。

### 應用層 & HTTP API

打開`BookAppService`類並將策略名稱添加為上面定義的權限名稱：

```
using System;
using Acme.BookStore.Permissions;
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
            GetPolicyName = BookStorePermissions.Books.Default;
            GetListPolicyName = BookStorePermissions.Books.Default;
            CreatePolicyName = BookStorePermissions.Books.Create;
            UpdatePolicyName = BookStorePermissions.Books.Edit;
            DeletePolicyName = BookStorePermissions.Books.Delete;
        }
    }
}
```

向構造函數添加了代碼。Base 會`CrudAppService`自動對 CRUD 操作使用這些權限。

這使**應用程序服務**安全，但也使**HTTP API**安全，因為此服務自動用作 HTTP API，如前所述（請參閱[自動 API 控制器](https://docs.abp.io/en/abp/latest/API/Auto-API-Controllers)）。

// 一般 API 使用聲明授權，使用 `[Authorize(BookStorePermissions.Books.Create)]` 屬性，如下所示會在稍後的章節中提及。

> `[Authorize(...)]`稍後在開發作者管理功能時，您將看到使用屬性的聲明性授權。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/13c109ab-9312-4d96-a13f-58ec30b74fc5/1627026014.png)

### Angular 防護配置

// 這邊是 Angular 前端畫面，這裡先快速帶過

UI的第一步是防止未經授權的用戶看到“圖書”菜單項並進入圖書管理頁面。

打開`/src/app/book/book-routing.module.ts`並替換為以下內容：

```
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard, PermissionGuard } from '@abp/ng.core';
import { BookComponent } from './book.component';

const routes: Routes = [
  { path: '', component: BookComponent, canActivate: [AuthGuard, PermissionGuard] },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class BookRoutingModule {}
```

* 進口`AuthGuard`和`PermissionGuard`從`@abp/ng.core`。
* 添加`canActivate: [AuthGuard, PermissionGuard]`到路由定義。

打開`/src/app/route.provider.ts`並添加`requiredPolicy: 'BookStore.Books'`到`/books`路由。該`/books`路線區塊應該是以下幾點：

```
{
  path: '/books',
  name: '::Menu:Books',
  parentName: '::Menu:BookStore',
  layout: eLayoutType.application,
  requiredPolicy: 'BookStore.Books',
}
```

### 隱藏新書按鈕

圖書管理頁面有一個*新建圖書*按鈕，如果當前用戶沒有*圖書創建*權限，該按鈕應該是不可見的。

![書店-新書-按鈕-小](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/bookstore-new-book-button-small.png)

打開`/src/app/book/book.component.html`文件，替換創建按鈕的HTML內容如下圖：

```
<!-- Add the abpPermission directive -->
<button *abpPermission="'BookStore.Books.Create'" id="create" class="btn btn-primary" type="button" (click)="createBook()">
  <i class="fa fa-plus mr-1"></i>
  <span>{{ '::NewBook' | abpLocalization }}</span>
</button>
```

* 剛剛添加`*abpPermission="'BookStore.Books.Create'"`，如果當前用戶沒有權限，則隱藏按鈕。

### 隱藏編輯和刪除操作

圖書管理頁面中的圖書表每行都有一個操作按鈕。操作按鈕包括*編輯*和*刪除*操作：

![書店編輯刪除操作](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/en/Tutorials/images/bookstore-edit-delete-actions.png)

如果當前用戶沒有授予相關權限，我們應該隱藏一個動作。

打開`/src/app/book/book.component.html`文件並替換編輯和刪除按鈕的內容如下：

```
<!-- Add the abpPermission directive -->
<button *abpPermission="'BookStore.Books.Edit'" ngbDropdownItem (click)="editBook(row.id)">
  {{ '::Edit' | abpLocalization }}
</button>

<!-- Add the abpPermission directive -->
<button *abpPermission="'BookStore.Books.Delete'" ngbDropdownItem (click)="delete(row.id)">
  {{ '::Delete' | abpLocalization }}
</button>
```

* `*abpPermission="'BookStore.Books.Edit'"`如果當前用戶沒有編輯權限，則添加隱藏編輯操作。
* `*abpPermission="'BookStore.Books.Delete'"`如果當前用戶沒有刪除權限，則添加隱藏刪除操作。

## 下一部分

請參閱本教程的[下一部分](https://docs.abp.io/en/abp/latest/Tutorials/Part-6)。

---

### [[2021] ABP.IO WEB應用程式框架 新手教學 No.0 全篇索引](https://dotblogs.com.tw/jakeuj/2021/07/15/abpio0)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
