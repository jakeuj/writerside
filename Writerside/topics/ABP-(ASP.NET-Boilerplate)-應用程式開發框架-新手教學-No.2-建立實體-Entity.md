# ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.2 建立實體 Entity

> **原文發布日期:** 2016-07-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/07/26/abp2
> **標籤:** 無

---

ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.2 建立實體 Entity

​[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.0 索引](https://dotblogs.com.tw/jakeuj/2016/07/28/abp0)

---

1.延續上篇建立專案後，接著是建立實體的部分，這邊先稍微解說一下目前的分層結構

分層簡介

* MyCompany.MyProject.Application
  應用服務層：給表現層調用的服務與資料傳輸物件(DTO)
* MyCompany.MyProject.Core
  領域核心層：領域驅動設計(DDD)核心，內含實體(Entity)、倉儲介面(Repository)、領域事件、工作單元與領域服務
* MyCompany.MyProject.EntityFramework
  基礎設施層：EF框架、DbContext、實作倉儲介面、Migration資料庫遷移內含Seed預設資料列產生作業
* MyCompany.MyProject.Web
  表現層：視覺前端網站
* MyCompany.MyProject.WebApi
  表現層：將應用層服務生成Web API
* Test
  單元測試資料夾：建立基於記憶體的測試資料庫，利用基礎設施的Seed產生基本資料，在自定義測試資料來驗證應用服務結果是否符合預期

2.簡單了解基本分層後，開始著手實體的建立，依照架構應該將實體放在Core專案

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/214c215c-1e80-4ac1-8e0a-bec8ad05535b/1469594040_81626.png)

先不考慮聚合，在Core裡面簡單建立一個Entities資料夾來放我們的實體

3.開始建立實體

建立一個類別，這邊我建立一個地圖類別 Map.cs

```

using Abp.Domain.Entities;
using Abp.Domain.Entities.Auditing;
using System;
using System.Collections.Generic;

namespace MyCompany.MyProject.Entities
{
    public class Map : Entity<long>, IHasCreationTime
    {
        public const string DefaultMapName = "DefaultMap";

        public virtual string MapName { get; set; }

        public virtual DateTime CreationTime { get; set; }

        public virtual ICollection<Player> Player { get; set; }

        public Map()
        {
            CreationTime = DateTime.Now;
        }
    }
}
```

類別Entity繼承後會自動含有一個資料型態為int的ID屬性，該類別還有一個泛型版本Entity<T>可以繼承，這邊我ID是long所以繼承Entity<long>

```

public class Map : Entity<long>, IHasCreationTime
```

ABP還提供了IHasCreationTime這個介面來讓我們統一所有會使用到建立時間這個屬性的實體，藉此統一該屬性名稱為CreationTime

```

public const string DefaultMapName = "DefaultMap";
```

DefaultMapName是用在做Migration的Seed的時候所使用的預設值

```

public virtual string MapName { get; set; }
```

MapName則是相當於資料庫欄位的宣告方式，CreationTime同理

```

public virtual ICollection<Player> Player { get; set; }
```

Player這行則是代表此表(Map)為Player的外部索引鍵，一個Map可能會對應多個Player所以是用Player集合

```

public Map()
{
    CreationTime = DateTime.Now;
}
```

預設CreationTime使用系統目前時間，到這裡Map這個實體就建立好了，再來我在建立一個Player實體

```

using Abp.Domain.Entities;
using Abp.Domain.Entities.Auditing;
using System;

namespace MyCompany.MyProject.Entities
{
    public class Player : Entity<long>, IHasCreationTime
    {
        public const string DefaultPlayerName = "DefaultPlayer";

        public virtual string PlayerName { get; set; }

        public virtual long MapID { get; set; }

        public virtual DateTime CreationTime { get; set; }

        public virtual Map Map { get; set; }
        public Player()
        {
            CreationTime = DateTime.Now;
            MapID = 1;
        }
    }
}
```

Player有個MapID對應至Map實體的ID並且有預設值為1

```

public virtual long MapID { get; set; }

public virtual Map Map { get; set; }
```

至此我們建立了兩個實體，地圖和玩家。

---

下一篇

[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.3 建立DbContext](https://dotblogs.com.tw/jakeuj/2016/07/27/abp3)

參照

[一步一步使用ABP框架搭建正式項目系列教程](http://www.cnblogs.com/farb/p/4849791.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [C#](/jakeuj/Tags?qq=C%23)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
