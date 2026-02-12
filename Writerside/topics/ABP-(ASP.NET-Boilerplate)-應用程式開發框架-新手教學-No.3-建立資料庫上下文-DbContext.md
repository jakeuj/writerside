# ABP 新手教學 No.3 建立資料庫上下文 DbContext

> **原文發布日期:** 2016-07-27
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/07/27/abp3
> **標籤:** 無

---

ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.3 建立資料庫上下文 DbContext

​[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.0 索引](https://dotblogs.com.tw/jakeuj/2016/07/28/abp0)

---

建立實體之後就來建立 資料庫上下文 DbContext

DbContext處理資料庫連接字串還有可以設定實體要建立的資料表名稱和關聯性...等等

首先按照前篇的分層架構，DbContext應該放在基礎設施層也就是MyCompany.MyProject.EntityFramework專案

切確位置是在MyCompany.MyProject.EntityFramework專案內的EntityFramework資料夾

ABP已經有建立了專案預設的 DbContext 在 EntityFramework資料夾內的 MyProjectDbContext.cs

```

using System.Data.Common;
using Abp.Zero.EntityFramework;
using MyCompany.MyProject.Authorization.Roles;
using MyCompany.MyProject.MultiTenancy;
using MyCompany.MyProject.Users;
using System.Data.Entity;
using MyCompany.MyProject.Entities;

namespace MyCompany.MyProject.EntityFramework
{
    public class MyProjectDbContext : AbpZeroDbContext<Tenant, Role, User>
    {
        //TODO: Define an IDbSet for your Entities...
        public virtual IDbSet<Player> Players { set; get; }
        public virtual IDbSet<Map> Maps { set; get; }

        /* NOTE:
         *   Setting "Default" to base class helps us when working migration commands on Package Manager Console.
         *   But it may cause problems when working Migrate.exe of EF. If you will apply migrations on command line, do not
         *   pass connection string name to base classes. ABP works either way.
         */
        public MyProjectDbContext()
            : base("Default")
        {

        }

        /* NOTE:
         *   This constructor is used by ABP to pass connection string defined in MyProjectDataModule.PreInitialize.
         *   Notice that, actually you will not directly create an instance of MyProjectDbContext since ABP automatically handles it.
         */
        public MyProjectDbContext(string nameOrConnectionString)
            : base(nameOrConnectionString)
        {

        }

        //This constructor is used in tests
        public MyProjectDbContext(DbConnection connection)
            : base(connection, true)
        {

        }

        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Player>().HasRequired(p => p.Map);
        }
    }
}
```

下面這個建構函式會在Web專案內的Web.config裡面去找名稱為Default的connectionStrings來建立資料庫連線

```

/* NOTE:
*   Setting "Default" to base class helps us when working migration commands on Package Manager Console.
*   But it may cause problems when working Migrate.exe of EF. If you will apply migrations on command line, do not
*   pass connection string name to base classes. ABP works either way.
*/
public MyProjectDbContext()
    : base("Default")
{

}
```

我們在開頭註解 //TODO: Define an IDbSet for your Entities... 下方增加我們要用實體建立資料表的Code

```

//TODO: Define an IDbSet for your Entities...
public virtual IDbSet<Player> Players { set; get; }
public virtual IDbSet<Map> Maps { set; get; }
```

這裡我用Player實體建立了名稱為Players的資料表，Map同理，加上s實際建立資料表時資料表名稱就會有s

然後再最後加上 在建立模型時增加關聯性 Player->Map

```

protected override void OnModelCreating(DbModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    modelBuilder.Entity<Player>().HasRequired(p => p.Map);
}
```

這樣就會有條件約束 Player內的MapID 必須在 Map 內可以找到對應的 ID

到這邊基本 DbContext 就建立完成了

再來是資料庫遷移 Migration

---

下一篇

[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.4 資料庫遷移 Migration](https://dotblogs.com.tw/jakeuj/2016/07/27/abp4)

參照

[一步一步使用ABP框架搭建正式項目系列教程](http://www.cnblogs.com/farb/p/4849791.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
