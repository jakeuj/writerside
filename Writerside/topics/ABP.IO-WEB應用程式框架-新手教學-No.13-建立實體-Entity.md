# ABP.IO 新手教學 No.13 建立實體 Entity

> **原文發布日期:** 2021-07-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/19/aaboio2
> **標籤:** 無

---

[ABP.IO WEB應用程式框架 新手教學 No.0 索引](https://dotblogs.com.tw/jakeuj/2021/07/15/abpio0)

建完專案之後呢，都說領域驅動了，先將領域層處理一下

架構上領域層不相依其他層，所以可以先不管資料怎麼存，要不要建立索引…等等基礎設施層做的事情。

如此一來讓我們可以專注於領域模型，將實體之間的關係、方法、屬性…等等，先定義出來，然後與領域專家討論並修正。

這邊就先照文件來建立Book好了，一時我也沒其他例子的想法，反正都是Demoま

原本的 Domain 裡面長這樣

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/87bcc78e-ff0f-4121-8da5-3e2426d8cc84/1626666566.png)

* Data：處理 SeedData 的東西
* Identity Server：身分驗證服務器的 SeedData
* Settings：定義設定值的地方，印象中應該是會存在DB的那種設定值
* Users：使用者實體
* BookStoreConsts：預設裡面有表名稱前綴(App)，領域其他常值可以集中新增在這裡
* BookStoreDomainModule：Abp 每個專案都會有這個 xxxxModule，用來引入相依模組並進行一些設定
  例如：下面第一段會使用 Domain.Share 層的 MultiTenancyConsts 裡面的 IsEnabled 來決定是否啟用多租戶
  最下面則會在DEBUG的時候把Mail的DI注入一個空的實作Null，不會真的發信但也不會報錯，有利於做單元測試

```
Configure<AbpMultiTenancyOptions>(options =>
{
    options.IsEnabled = MultiTenancyConsts.IsEnabled;
});
#if DEBUG
context.Services.Replace(ServiceDescriptor.Singleton<IEmailSender, NullEmailSender>());
#endif
```

以上我這邊就先不動，只是稍微說明一下，這邊先專注於建立我們自己新的實體

https://docs.abp.io/zh-Hans/abp/latest/Tutorials/Part-1?UI=NG&DB=EF#%E5%88%9B%E5%BB%BAbook%E5%AE%9E%E4%BD%93
{ignore-vars="true"}

官方教學是開一個 Books 資料夾然後放入 Book.cs 實體

我先用一個基本的例子

```
namespace Acme.BookStore.Books
{
    public class Book:`Entity<int>`
    {
        public string Name { get; set; }

        public BookType Type { get; set; }

        public DateTime PublishDate { get; set; }

        public float Price { get; set; }
    }
}
```

其中 ``Entity<T>``是 Abp 提供的基底類別，主要就是定義實體要有個 Id 欄位，其中 T 是主鍵的型別，可以是 Guid,int,long…ETC.

另外也有提供 AggregateRoot 這個基底類別，這是DDD概念，大概是把同質性高的東西聚在一起，統一由 根 進行操作，避免直接操作其下的實體

比如你跟你的好友，首先要有你存在才會有你的好友，如果直接新增你的好友，但是你並不存在與使用者資料表，那資料會有問題。

所以要由使用者操作，新增你的好友這個動作，如果你不存在，則先新增你到使用者表，然後再新增你的好友到好友資料表，如此可以確保資料完整性。

又或者訂單與訂單明細，這兩個東西應該將訂單當作聚合根，然後將明細放到其下面，不應該存在只有明細卻沒有訂單本體的這種情況。

這邊有個概念是，當根不存在時，其下的實體也沒有存在的必要，刪除時應該一併刪除。

詳細請參閱官方關於實體的說明 <https://docs.abp.io/zh-Hans/abp/latest/Entities>

再說說官方範例

```
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

PK 目前官方是推薦用 Guid，然後基底類別這邊使用審計聚合根(`AuditedAggregateRoot`)，

其實就是在 `AggregateRoot` 加上了 `CreationTime`, `CreatorId`, `LastModificationTime` 等等審計欄位

關於審計 Abp 定義了很多介面，比如 IHasCreationTime，這可以統一全部實體的欄位名稱，避免有些人叫 CreationTime 有些人取 CreateTime，但其實是同一個東西。

也有內建好的基底類別，比如 CreationAudited`Entity<TKey>` 可以直接拿來當作實體的基底類別，當然你想自己時做也是可以。

另外這裡的欄位都是 public set ，如果遵照 DDD 這裡應該不能直接開放 set ，但這裡重點不放太多在 DDD ，所以大概知道一下就好，跑反正都是可以跑得。

這邊提供官方聚合根的某程度DDD最佳實作以供參考，看不懂可以先跳過

```
public class Order : AggregateRoot<Guid>
{
    public virtual string ReferenceNo { get; protected set; }

    public virtual int TotalItemCount { get; protected set; }

    public virtual DateTime CreationTime { get; protected set; }

    public virtual List<OrderLine> OrderLines { get; protected set; }

    protected Order()
    {

    }

    public Order(Guid id, string referenceNo)
    {
        Check.NotNull(referenceNo, nameof(referenceNo));

        Id = id;
        ReferenceNo = referenceNo;

        OrderLines = new List<OrderLine>();
    }

    public void AddProduct(Guid productId, int count)
    {
        if (count <= 0)
        {
            throw new ArgumentException(
                "You can not add zero or negative count of products!",
                nameof(count)
            );
        }

        var existingLine = OrderLines.FirstOrDefault(ol => ol.ProductId == productId);

        if (existingLine == null)
        {
            OrderLines.Add(new OrderLine(this.Id, productId, count));
        }
        else
        {
            existingLine.ChangeCount(existingLine.Count + count);
        }

        TotalItemCount += count;
    }
}

public class OrderLine : Entity
{
    public virtual Guid OrderId { get; protected set; }

    public virtual Guid ProductId { get; protected set; }

    public virtual int Count { get; protected set; }

    protected OrderLine()
    {

    }

    internal OrderLine(Guid orderId, Guid productId, int count)
    {
        OrderId = orderId;
        ProductId = productId;
        Count = count;
    }

    internal void ChangeCount(int newCount)
    {
        Count = newCount;
    }

    public override object[] GetKeys()
    {
        return new Object[] {OrderId, ProductId};
    }
}
```

大概意思是DDD不是用貧血模型，在聚合根中提供了操作其下子集合的相關方法，並且讓其欄位都無法直接set，來達到強制只能由 根來統一操作聚合的目的。

最後是 enum ，Book 中的 BookType 是一個列舉，以前版本還不知道放哪就隨便亂擺，現在新版終於有個好歸宿了

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

各實體會用到的 enum 移駕到 Domain.Shared ，所以最後長這樣

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/60153255-a148-491d-a092-bf8a0f9e7b90/1626677558.png)

如果你書還有其他相關實體，比如甚麼書的附件啦，圖片啦，就應該都放在Books這個資料夾內，

這樣有個好處是哪天你系統不需要書了，你只要把Books資料夾砍了，省得東找西找還怕砍錯。

這也是聚合的概念，當主要的書沒有存在的必要了，書的圖片附件等等也沒有單獨存在的必要。

---

No 2.5 [領域服務 Domain Service](https://docs.abp.io/en/abp/latest/Domain-Services) 與 [倉儲介面 IRepository](https://docs.abp.io/zh-Hans/abp/latest/Repositories)

※ 新手教學流程上並不會使用到領域服務，這邊只是稍微提一下

在順序上領域層還可以做的是領域服務跟自訂倉儲介面

利用通用倉儲介面與自訂倉儲介面和上面定義好的實體

就可以開始建立領域服務並實作裡面的領域邏輯

這樣好處是可以最快跟領域專家持續同步並修正模型

這也是領域驅動導向的概念實踐，領域層可以不依賴其他層就把重要的東西都寫出來，然後快速跟領域專家討論

※ 新手教學流程上建完實體會直接到基礎設施準備建立資料庫

---

[ABP.IO WEB應用程式框架 新手教學 No.3 建立資料庫上下文 DbContext](https://dotblogs.com.tw/jakeuj/2021/07/19/abpio3)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
