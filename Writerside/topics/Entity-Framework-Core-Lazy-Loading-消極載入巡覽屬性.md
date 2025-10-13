# Entity Framework Core Lazy Loading 消極載入巡覽屬性

> **原文發布日期:** 2021-06-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/06/09/EFCoreLazyLoading
> **標籤:** 無

---

筆記一下 EF Core 消極載入的前世今生

先下結論

* EF Core (.Net Core)
  預設是積極載入，不需要再加 virtaul
  如果特別設定成消極載入，則一樣要補上 virtaul
* EF (.Net Framework)
  預設是消極載入，要啟用需要加 virtaul
  但也可以不加，就不走消極載入

---

遙想當年還沒開始用EF時，問我友人巡覽屬性的事情，他要我不要用

後來查了一下其實是消極載入如果使用不當會造成N+1的查詢效能問題

最後還是用了 virtual 來宣告巡覽屬性，想說注意一下就好了

後來轉到 Dotnet Core 還是習慣把實體的巡覽屬性當加上 virtual

有看到一些程式或文章沒有加也沒特別注意這事情 (沒特別注意是 EF or EFCore)

今天心血來潮查了一下資料才了解了事情原委

就以前 EF 預設是消極載入，需要用 virtual 宣告巡覽屬性

後來到了 EF Core 預設是積極載入，不需要 virtual

並且初期也不支援消極載入，畢竟草創時期缺一堆API

現在 EF Core 也有開始支援延遲載入了

但是需要另外設定 Proxy (不是加了 virtual 就可以完事)

不過官方也警告延遲載入用不好會造成 N+1 效能問題

<https://docs.microsoft.com/zh-tw/ef/core/querying/related-data/lazy#lazy-loading-with-proxies>

> **警告**
>
> 消極式載入可能會導致不必要的額外資料庫往返發生 (所謂的 N + 1 問題) ，而且應該小心避免此情況。 如需詳細資訊，請參閱 [**[效能] 區段**](https://docs.microsoft.com/zh-tw/ef/core/performance/efficient-querying#beware-of-lazy-loading) 。

建議沒特別要求就盡可能使用預設的積極載入就好

<https://docs.microsoft.com/zh-tw/ef/core/performance/efficient-querying#load-related-entities-eagerly-when-possible>

---

至於何時需要用到消極載入

```
    public class Blog
    {
        public int BlogId { get; set; }
        public string Url { get; set; }

        public List<Post> Posts { get; } = new List<Post>();
    }

    public class Post
    {
        public int PostId { get; set; }
        public string Title { get; set; }
        public string Content { get; set; }

        public int BlogId { get; set; }
        public Blog Blog { get; set; }
    }
```

如果想一條 linq 取得100個`Blog.Url`換其中一個 `Blog.Post`

如果直接積極載入 include 全部 Post 就會撈出 100篇部落格文章

但其實只會用到其中一篇

這時候就不適合積極載入

反而比較需要消極載入

或是就不 include

直接分兩個 linq 來查詢

這篇主要不是講這個就這樣帶過

有需要可以自行詢問古哥哥

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Entity Framework](/jakeuj/Tags?qq=Entity%20Framework)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
