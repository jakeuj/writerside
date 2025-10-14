# ABP.IO WEB應用程式框架 新手教學 No.16 建立應用服務 Application Service

> **原文發布日期:** 2021-07-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/19/abpio5
> **標籤:** 無

---

[ABP.IO WEB應用程式框架 新手教學 No.0 索引](https://dotblogs.com.tw/jakeuj/2021/07/15/abpio0)

最後是應用服務層，這邊寫完就可以呼叫 API 了，這邊先來引用官方說明

應用程序層由兩個分離的項目組成:

* `Acme.BookStore.Application.Contracts`包含你的[DTO](https://docs.abp.io/zh-Hans/abp/latest/Data-Transfer-Objects)和[應用服務](https://docs.abp.io/zh-Hans/abp/latest/Application-Services)接口.
* `Acme.BookStore.Application` 包含你的應用服務實現.

總之呢，上面那個合約是實際 client 所關心的，包含服務介面與DTO，

至於怎麼實作外部是不需要知道的，所以如果有公開dll給clinet使用基本上只會包含 `Application.Contracts`

## DTO

首先呢我們需要先定義與client溝通的資料傳輸物件 DTO

所以在`Acme.BookStore.Application.Contracts`項目中創建 Books 資料夾並新增一個名為`BookDto`的DTO類

* **DTO**類被用來在**表示層**和**應用層** **傳遞數據**.查看[DTO文檔](https://docs.abp.io/zh-Hans/abp/latest/Data-Transfer-Objects)查看更多信息.
* 為了在頁面上展示書籍信息,`BookDto`被用來將書籍數據傳遞到表示層.
* `BookDto`繼承自`AuditedEntityDto<Guid>`.跟上面定義的`Book`實體一樣具有一些審計屬性.

```
namespace Acme.BookStore.Books
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

※ 官方教學是沒有 Books 資料夾，但實戰上建議全部專案的Book相關東西都先建立一個Books資料夾，再把東西建在裡面，不然東西一多想像一下…

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bff36275-1beb-423a-9664-b96e21b3c91c/1626684853.png)

這邊 Dto 基類可以自己換別的，比如只有Id的 `EntityDto<T>`

```
namespace AbpDemo
{
    public class ProductDto : EntityDto<Guid>
    {
        public string Name { get; set; }
        //...
    }
}
```

<https://docs.abp.io/zh-Hans/abp/latest/Data-Transfer-Objects#%E5%AE%9E%E4%BD%93%E7%9B%B8%E5%85%B3dto>
{ignore-vars="true"}

## AutoMapper

有用過應該不是很陌生，這邊要在 profile 裡面加上 Dto 的映射，樣板內建好的 Profile 檔案

在`Acme.BookStore.Application`項目的`BookStoreApplicationAutoMapperProfile`類中定義

```
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

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bff36275-1beb-423a-9664-b96e21b3c91c/1626685149.png)

## Application Service

官方範例是使用 CRUD 基底類別，我這邊打算先用比較一般的 API 來做說明

參照：<https://docs.abp.io/zh-Hans/abp/latest/Application-Services>

首先定義介面 IBookAppService 必須繼承 IApplicationService ，雖然沒有介面也可以跑，但最佳實踐建議每個服務都有自己的介面

```
namespace Acme.BookStore.Books
{
    public interface IBookAppService: IApplicationService
    {
        Task<List<BookDto>> GetListAsync();
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bff36275-1beb-423a-9664-b96e21b3c91c/1626686760.png)

然後實作該介面，必須繼承樣板內建的 BookStoreAppService，還有剛剛新增好的 IBookAppService

```
namespace Acme.BookStore.Books
{
    public class BookAppService:BookStoreAppService, IBookAppService
    {
        private readonly IRepository<Book, Guid> _bookRepository;

        public BookAppService(IRepository<Book, Guid> bookRepository)
        {
            _bookRepository = bookRepository;
        }

        public async Task<List<BookDto>> GetListAsync()
        {
            var entities = await _bookRepository.GetListAsync();
            return ObjectMapper.Map<List<Book>, List<BookDto>>(entities);
        }
    }
}
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bff36275-1beb-423a-9664-b96e21b3c91c/1626686900.png)

## **Redis**

參考文件：[**Redis**](https://docs.abp.io/en/abp/latest/Redis-Cache)

預設 Redis 是打開的，如果開發環境沒有 redis 可以關閉。

Acme.BookStore.HttpApi.Host appsettings.Development.json

```
{
  "Redis": {
    "IsEnabled": "false"
  }
}
```

當然你要用 docker 起一個 redis container 也是可以，或是改到你 redis 開發機的位址去。

到這邊就可以執行 Acme.BookStore.HttpApi.Host 了，會跑出 Swagger Page，然後可以試著呼叫 API

### CrudAppService

參考文件：[CrudAppService](https://docs.abp.io/zh-Hans/abp/latest/Application-Services#crud%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1)
{ignore-vars="true"}

官方原教學：https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#ibookappservice

有內建快速 Crud 讓你不需要實作甚麼程式就可以擁有基本 CRUD 功能

包含分頁、排序與篩選…等等常用功能。

參考：https://docs.abp.io/zh-Hans/abp/latest/Application-Services#crud%E5%BA%94%E7%94%A8%E6%9C%8D%E5%8A%A1

### 自動生成API Controllers

參考文件：[自動生成API Controllers](https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1#%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90api-controllers)
{ignore-vars="true"}

Abp 是不用自己再去寫薄博的控制器的，它會自動將 AppService 公開 API

你通常創建**Controller**以將應用程序服務公開為**HTTP API**端點.因此允許瀏覽器或第三方客戶端通過AJAX調用它們.

ABP可以[**自動**](https://docs.abp.io/zh-Hans/abp/latest/API/Auto-API-Controllers)按照慣例將你的應用程序服務配置為MVC API控制器.

### Swagger UI

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/bff36275-1beb-423a-9664-b96e21b3c91c/1626690589.png)
![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
