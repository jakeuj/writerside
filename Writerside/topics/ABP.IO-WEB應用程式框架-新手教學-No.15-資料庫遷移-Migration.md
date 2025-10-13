# ABP.IO WEB應用程式框架 新手教學 No.15 資料庫遷移 Migration

> **原文發布日期:** 2021-07-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/19/abpio4
> **標籤:** 無

---

[ABP.IO WEB應用程式框架 新手教學 No.0 索引](https://dotblogs.com.tw/jakeuj/2021/07/15/abpio0)

參照官方教學

<https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E6%B7%BB%E5%8A%A0%E6%95%B0%E6%8D%AE%E8%BF%81%E7%A7%BB>
{ignore-vars="true"}

這邊使用 [Entity Framework Core 的 Code First Migrations](https://docs.microsoft.com/zh-cn/ef/core/managing-schemas/migrations/?tabs=dotnet-core-cli) 來操作資料庫

包含建立資料庫、新增修改刪除表(這邊是可以進版退版的)，Insert Seed Data…等等。

首先要先打開終端機到 Acme.BookStore.EntityFrameworkCore.DbMigrations 目錄

然後執行命令 dotnet ef migrations add Created\_Book\_Entity 建立資料庫版本

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f8aa590e-d43b-4f53-afa6-cea509e45adf/1626682350.png)

執行成功會跑出 migrations 資料夾

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f8aa590e-d43b-4f53-afa6-cea509e45adf/1626682501.png)

裡面會定義要新增表，還是修改裡面甚麼欄位，或是移除某某東西之類的，這也可以生出SQL指令，有興趣可以去看MSDN

---

## No. 4.5 SeedData

到這邊其實可以去執行Acme.BookStore.DbMigrator 或 PM> dotnet ef update database 就可以產生資料庫跟表了

不過這邊先進行 SeedData 相關作業來說明如何建立初始資料，這有利於初次部屬或進行單元測試，如果沒有需求可以看看先，說不定哪天會用得上

這邊 SeedData 是定義在 Domain 層

然後他必須繼承 IDataSeedContributor

類別名稱預設是 BookStoreDataSeederContributor

但這東西樣板專案裡面沒有所以需要自己手動新增

```
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

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/f8aa590e-d43b-4f53-afa6-cea509e45adf/1626683321.png)

這邊如果你要拿上一個新增的 Id 去當下一個新增的某欄位值，自己 var 變數去接 Insert 回傳的實體，下面就可以用 entity.Id 當作 value

最後執行 Acme.BookStore.DbMigrator 這專案就會用 appsetting 裡面的連線字串去建立資料庫與資料表並匯入 SeedData

預設是 localdb 裝 vs 預設會有的 db ，沒有了話自己改連線字串到開發用的db，這邊就不多做解釋了

---

### [ABP.IO WEB應用程式框架 新手教學 No.5 建立應用服務 Application Service](https://dotblogs.com.tw/jakeuj/2021/07/19/abpio5)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
