# ABP.IO 取得關聯資料 include

> **原文發布日期:** 2022-10-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/25/abp-ef-With-Details-Async
> **標籤:** 無

---

定義關聯屬性來使用倉儲`WithDetailsAsync` 方法取得關聯資料

## 預設載入關聯實體

EntityFrameworkCoreModule

```
Configure<AbpEntityOptions>(options =>
{
    options.Entity<Blog>(orderOptions =>
    {
        orderOptions.DefaultWithDetailsFunc =
            query => query.Include(o => o.Posts);
    });
});
```

BlogAppService

```
var q = await _blogRepository.WithDetailsAsync();

var entity = await AsyncExecuter.FirstAsync(q);
```

這樣使用時就不用再指定 `WithDetailsAsync(x => x.Posts)`

```
var entity = await _blogRepository.GetAsync();
```

使用 `GetAsync` 時會直接包含`Posts`

[Entity Framework Core | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Entity-Framework-Core#defaultwithdetailsfunc)

## 步驟

首先要在 Entity 定義導覽屬性

* Order
  `public ICollection<OrderLine> Lines { get; set; } //Sub collection`
* OrderLine
  `[JsonIgnore] public Order Order { get; set; } //Navigation property`

#### 注意

1. 如果沒加 `[JsonIgnore]` (System.Text.Json.Serialization) ，API 回傳的時候會報錯
2. `[JsonIgnore]` 是 `using System.Text.Json.Serialization;` 而非 `using Newtonsoft.Json;` 否則會吃不到設定

```
JsonException: A possible object cycle was detected.
This can either be due to a cycle or if the object depth
is larger than the maximum allowed depth of 32.
```

如果FK不符合命名原則 (`OrderId`)，則需要在 DbContext 定義關聯

```
//Define the relation
b.HasMany(x => x.Lines)
    .WithOne(x => x.Order)
    .HasForeignKey(x => x.NotOrderIdButIsFkId)
    .IsRequired();
```

最後就可以透過倉儲取得

```
//Get a IQueryable<T> by including sub collections
var queryable = await _orderRepository.WithDetailsAsync(x => x.Lines);

//Apply additional LINQ extension methods
var query = queryable.Where(x => x.Id == id);

//Execute the query and get the result
var order = await AsyncExecuter.FirstOrDefaultAsync(query);
```

沒意外了話，order 裡面會包含 Line 的集合資料

```
[Fact]
public async Task Should_Get_Details_From_A_Order()
{
    var orderManager = GetRequiredService<orderManager>();

    //Act
    var result = await WithUnitOfWorkAsync(async () =>
        await orderManager.WithDetailsAsync()};

    //Assert
    result.ShouldNotBeNull();
    result.Lines.ShouldNotBeNull();
    result.Lines.Count.ShouldBeGreaterThan(0);
}
```

多層關聯 [Include(A).ThenInclude(B)]

```
//Get a IQueryable<T> by including sub collections
var queryable = await _orderRepository.WithDetailsAsync(
    x => x.Lines,
    x => x.Lines.Providers);

//Apply additional LINQ extension methods
var query = queryable.Where(x => x.Id == id);

//Execute the query and get the result
var result = await AsyncExecuter.ToListAsync(query, cancellationToken);
```

複數關聯 [Include(A).Include(C)]

```
//Get a IQueryable<T> by including sub collections
var queryable = await _orderRepository.WithDetailsAsync(
    x => x.Lines,
    x => x.Details);

//Apply additional LINQ extension methods
var query = queryable.Where(x => x.Id == id);

//Execute the query and get the result
var result = await AsyncExecuter.ToListAsync(query, cancellationToken);
```

## 參照

[Entity Framework Core | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Entity-Framework-Core#repository-withdetails)

[認識 Entity Framework Core 載入關聯資料的三種方法 | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2022/04/21/Loading-Related-Data-in-EF-Core)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Entity Framework
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
