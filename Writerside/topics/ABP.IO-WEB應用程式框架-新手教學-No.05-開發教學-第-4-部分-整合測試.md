# ABP.IO WEB應用程式框架 新手教學 No.05 開發教學 第 4 部分 整合測試

> **原文發布日期:** 2021-07-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/23/abpio05
> **標籤:** 無

---

這篇接續上一篇 開發教學 [Part 3 創建、更新和刪除圖書](https://dotblogs.com.tw/jakeuj/2021/07/23/abpio04)

主要針對 ABP 的測試專案說明如何進行測試

對於沒做過測試的建議照著做一次提升程式交付品質

## Web應用程序開發教程 - 第三章：集成測試

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

## 解決方案中的測試項目

這涉及到了**服務器端**測試。解決方案還有很多測試項目：

![bookstore-test-projects-v2](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/Tutorials/images/bookstore-test-projects-angular.png)

各個項目用於測試相關的應用程序項目。測試項目使用以下庫進行測試：

* [xunit](https://xunit.github.io/) 作為主測試框架。
* [Shoudly](http://shouldly.readthedocs.io/en/latest/) 作為斷言庫。
* [NSubstitute](http://nsubstitute.github.io/) 作為模擬庫。

> 測試項目配置為使用**SQLite 內存**作為數據庫。創建一個單獨的數據庫實例並使用數據生成系統進行初始化數據，為每個單獨的數據庫實例準備一個新的數據庫。

## 添加測試數據

如果你已經按照第一個[部分](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1)中的描述創建了數據種子貢獻者，則相同的數據用於測試中可用。因此你可以跳過此部分。如果你還沒有創建數據種子貢獻者(DataSeedContributor)，可以使用`BookStoreTestDataSeedContributor`來為要在以下測試中使用的相同數據提供種子。

## 測試 BookAppService

在`Acme.BookStore.Application.Tests`項目中創建一個有名`BookAppService_Tests`的測試類：

```
using System.Threading.Tasks;
using Shouldly;
using Volo.Abp.Application.Dtos;
using Xunit;

namespace Acme.BookStore.Books
{
    public class BookAppService_Tests : BookStoreApplicationTestBase
    {
        private readonly IBookAppService _bookAppService;

        public BookAppService_Tests()
        {
            _bookAppService = GetRequiredService<IBookAppService>();
        }

        [Fact]
        public async Task Should_Get_List_Of_Books()
        {
            //Act
            var result = await _bookAppService.GetListAsync(
                new PagedAndSortedResultRequestDto()
            );

            //Assert
            result.TotalCount.ShouldBeGreaterThan(0);
            result.Items.ShouldContain(b => b.Name == "1984");
        }
    }
}
```

* 測試方法直接`Should_Get_List_Of_Books`使用`BookAppService.GetListAsync`方法來獲取用戶列表，並執行檢查。
* 我們可以安全地檢查“1984”這本書的名稱，因為我們知道這本書可以在數據庫中找到，我們已經將其添加到衍生數據中。

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f1aefb8a-bd69-4233-ac7c-cd9d986a76f7/1627019102.png)

新增測試方法，創建一個**合法**書籍實體的場景：

```
[Fact]
public async Task Should_Create_A_Valid_Book()
{
    //Act
    var result = await _bookAppService.CreateAsync(
        new CreateUpdateBookDto
        {
            Name = "New test book 42",
            Price = 10,
            PublishDate = System.DateTime.Now,
            Type = BookType.ScienceFiction
        }
    );

    //Assert
    result.Id.ShouldNotBe(Guid.Empty);
    result.Name.ShouldBe("New test book 42");
}
```

新增測試方法，創建一個公開書籍實體失敗的場景：

```
[Fact]
public async Task Should_Not_Create_A_Book_Without_Name()
{
    var exception = await Assert.ThrowsAsync<AbpValidationException>(async () =>
    {
        await _bookAppService.CreateAsync(
            new CreateUpdateBookDto
            {
                Name = "",
                Price = 10,
                PublishDate = DateTime.Now,
                Type = BookType.ScienceFiction
            }
        );
    });

    exception.ValidationErrors
        .ShouldContain(err => err.MemberNames.Any(mem => mem == "Name"));
}
```

* 因為`Name`是空值，ABP 拋出了一個`AbpValidationException`異常。

最終的測試類如下所示：

```
using System;
using System.Linq;
using System.Threading.Tasks;
using Shouldly;
using Volo.Abp.Application.Dtos;
using Volo.Abp.Validation;
using Xunit;

namespace Acme.BookStore.Books
{
    public class BookAppService_Tests : BookStoreApplicationTestBase
    {
        private readonly IBookAppService _bookAppService;

        public BookAppService_Tests()
        {
            _bookAppService = GetRequiredService<IBookAppService>();
        }

        [Fact]
        public async Task Should_Get_List_Of_Books()
        {
            //Act
            var result = await _bookAppService.GetListAsync(
                new PagedAndSortedResultRequestDto()
            );

            //Assert
            result.TotalCount.ShouldBeGreaterThan(0);
            result.Items.ShouldContain(b => b.Name == "1984");
        }

        [Fact]
        public async Task Should_Create_A_Valid_Book()
        {
            //Act
            var result = await _bookAppService.CreateAsync(
                new CreateUpdateBookDto
                {
                    Name = "New test book 42",
                    Price = 10,
                    PublishDate = System.DateTime.Now,
                    Type = BookType.ScienceFiction
                }
            );

            //Assert
            result.Id.ShouldNotBe(Guid.Empty);
            result.Name.ShouldBe("New test book 42");
        }

        [Fact]
        public async Task Should_Not_Create_A_Book_Without_Name()
        {
            var exception = await Assert.ThrowsAsync<AbpValidationException>(async () =>
            {
                await _bookAppService.CreateAsync(
                    new CreateUpdateBookDto
                    {
                        Name = "",
                        Price = 10,
                        PublishDate = DateTime.Now,
                        Type = BookType.ScienceFiction
                    }
                );
            });

            exception.ValidationErrors
                .ShouldContain(err => err.MemberNames.Any(mem => mem == "Name"));
        }
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f1aefb8a-bd69-4233-ac7c-cd9d986a76f7/1627024422.png)

打開**測試資源管理器**(測試 -> Windows -> 測試資源管理器)並**執行**所有測試：

![書店應用服務測試](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/Tutorials/images/bookstore-appservice-tests.png)

恭喜你，**綠色圖標**表示測試已成功通過！

## 下一章

查看本教程的[下一章](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-5)。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
