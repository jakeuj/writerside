# ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.5 建立倉儲 Repository

> **原文發布日期:** 2016-07-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/07/28/abp5
> **標籤:** 無

---

ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.5 建立倉儲 Repository

​[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.0 索引](https://dotblogs.com.tw/jakeuj/2016/07/28/abp0)

---

ABP有內建基本常用的倉儲功能例如CRUD，而我們可以進行擴充

在架構上倉儲的介面與實作是拆開分別在Domain層與基礎設施層的

先說倉儲的介面部分

這裡來做一個用Map的ID來取得對應Player集合的一個倉儲介面

首先一樣按照架構我們在Core專案中開一個IRepositories資料夾來放

MyCompany.MyProject.Core\IRepositories\

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6b10a8cd-2443-44d7-8c9b-c0639abe6c6f/1469674105_26116.png)然後我們新增一個介面 IPlayerRepository.cs

```

using Abp.Domain.Repositories;
using MyCompany.MyProject.Entities;
using System.Collections.Generic;

namespace MyCompany.MyProject.IRepositories
{
    public interface IPlayerRepository : IRepository<Player, long>
    {
        List<Player> GetPlayersWithMap(long mapID);
    }
}
```

這樣我們就完成了倉儲的介面定義

而實作部分我們來到 AbsoluteDuo\_V4.EntityFramework\Repositories\

建立一個類別 PlayerRepository.cs 該類別繼承ABP提供的基底類別 MyProjectRepositoryBase 並且繼承我們剛剛定義的介面 IPlayerRepository

```

using Abp.EntityFramework;
using MyCompany.MyProject.Entities;
using MyCompany.MyProject.IRepositories;
using System.Collections.Generic;
using System.Linq;

namespace MyCompany.MyProject.EntityFramework.Repositories
{
    public class PlayerRepository : MyProjectRepositoryBase<Player, long>, IPlayerRepository
    {
        public PlayerRepository(IDbContextProvider<MyProjectDbContext> dbContextProvider) : base(dbContextProvider)
        {

        }

        public List<Player> GetPlayersWithMap(long mapID)
        {
            // GetAll()返回一個IQueryable<T>，我們可以通過它來查詢
            var query = GetAll();

            // 也可以直接使用EF的DbContext對象
            //var query2 = Context.Players.AsQueryable();

            // 另一種選擇：直接使用Table屬性代替"Context.Players"，都是一樣的。
            //var query3 = Table.AsQueryable();

            if (mapID > 0)
            {
                query = query.Where(c => c.MapID == mapID);
            }
            return query.ToList();
        }

        public async Task<List<Player>> GetPlayersWithMapAsync(long mapID)
        {
            return await GetAllListAsync(c => c.MapID == mapID);
        }
    }
}
```

* GetAll()
  返回 `IQueryable<T>`
  因為有延遲載入(Lazy Loading)的特性，所以實際與資料庫連接是在使用ToList()方法時
* GetAllList()
  返回 `List<T>`
  這個則是在呼叫時就會立即從資料來源取出資料

到這邊倉儲就已經建立完成了

---

下一篇

[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.6 建立應用服務](https://dotblogs.com.tw/jakeuj/2016/07/28/abp6)

參照

[一步一步使用ABP框架搭建正式項目系列教程](http://www.cnblogs.com/farb/p/4849791.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
