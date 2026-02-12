# accessing-entity-with-query-filter-using-required-navigation

Migration 時跳出警告

## Warning

```
Entity 'xxx' has a global query filter defined and is the required end of a relationship with the entity 'xxx'.
This may lead to unexpected results when the required entity is filtered out.
Either configure the navigation as optional,
or define matching query filters for both entities in the navigation.
See https://go.microsoft.com/fwlink/?linkid=2131316 for more information.
```

## ABP

使用 `ISoftDelete` 實體會使用查詢篩選條件 `IsDeleted=false`
當使用 Include 時，會用 Inner Join 的方式將主副表連結起來
如果其中一張表的紀錄是被刪除的( `IsDeleted=true` )，則可能會導致查詢結果不符合預期

## 說明

這個警告是提醒我們，當使用必要的導覽時，如果有使用查詢篩選條件，可能會導致查詢結果不符合預期

Case 1: 使用必要的導覽並使用查詢篩選條件

```C#
modelBuilder.Entity<Blog>().HasMany(b => b.Posts).WithOne(p => p.Blog).IsRequired();
modelBuilder.Entity<Blog>().HasQueryFilter(b => b.Url.Contains("fish"));
```

Case 2: 使用選擇性的導覽並使用查詢篩選條件

```C#
modelBuilder.Entity<Blog>().HasMany(b => b.Posts).WithOne(p => p.Blog).IsRequired(false);
modelBuilder.Entity<Blog>().HasQueryFilter(b => b.Url.Contains("fish"));
```

Case 3: 使用必要的導覽並使用一致的查詢篩選條件

```C#
modelBuilder.Entity<Blog>().HasMany(b => b.Posts).WithOne(p => p.Blog).IsRequired();
modelBuilder.Entity<Blog>().HasQueryFilter(b => b.Url.Contains("fish"));
modelBuilder.Entity<Post>().HasQueryFilter(p => p.Blog.Url.Contains("fish"));
```

考慮以上篩選方式

```C#
var allPosts = db.Posts.ToList();
var allPostsWithBlogsIncluded = db.Posts.Include(p => p.Blog).ToList();
```

單純讀取 Posts 與使用 Include 來讀取 Posts 並連結 Blog 時，會有不同的結果

Case 1: `Posts.ToList()` 會撈出全部紀錄，`Posts.Include(p => p.Blog).ToList()` 會用 Inner Join 僅撈出 `Url` 包含 `fish` 的 N 筆紀錄

Case 2: `Posts.ToList()` 會撈出全部紀錄，`Posts.Include(p => p.Blog).ToList()` 會用 LEFT JOIN 撈出全部紀錄

Case 3: `Posts.ToList()` 與 `Posts.Include(p => p.Blog).ToList()` 皆僅會撈出 `Url` 包含 `fish` 的 N 筆紀錄

## 官方文件

[使用必要的導覽來存取具有查詢篩選的實體](https://go.microsoft.com/fwlink/?linkid=2131316)

實體定義

```C#
modelBuilder.Entity<Blog>().HasMany(b => b.Posts).WithOne(p => p.Blog).IsRequired();
modelBuilder.Entity<Blog>().HasQueryFilter(b => b.Url.Contains("fish"));
```

Seed Data

```C#
db.Blogs.Add(
    new Blog
    {
        Url = "http://sample.com/blogs/fish",
        Posts = new List<Post>
        {
            new Post { Title = "Fish care 101" },
            new Post { Title = "Caring for tropical fish" },
            new Post { Title = "Types of ornamental fish" }
        }
    });

db.Blogs.Add(
    new Blog
    {
        Url = "http://sample.com/blogs/cats",
        Posts = new List<Post>
        {
            new Post { Title = "Cat care 101" },
            new Post { Title = "Caring for tropical cats" },
            new Post { Title = "Types of ornamental cats" }
        }
    });
```

查詢

```C#
var allPosts = db.Posts.ToList();
var allPostsWithBlogsIncluded = db.Posts.Include(p => p.Blog).ToList();
```

在上述設定中，第一個查詢會傳回所有 6 個 `Post`，但第二個查詢只會傳回 3 個 `Post`。
因為第二個查詢中的 Include 方法會載入相關的 Blog 實體，因此會發生這種不相符的情況。
由於 Post 和 Blog 之間的流覽屬性為必需，所以 EF Core 會使用 INNER JOIN 來建構以下查詢：

```SQL
SELECT [p].[PostId], [p].[BlogId], [p].[Content], [p].[IsDeleted], [p].[Title], [t].[BlogId], [t].[Name], [t].[Url]
FROM [Posts] AS [p]
INNER JOIN (
    SELECT [b].[BlogId], [b].[Name], [b].[Url]
    FROM [Blogs] AS [b]
    WHERE [b].[Url] LIKE N'fish'
) AS [t] ON [p].[BlogId] = [t].[BlogId]
```

使用 INNER JOIN 會過濾掉所有相關 Blog 已被全域查詢篩選器刪除的 Post。

您可以使用選擇性導覽而非必要方式加以定址。 如此一來，第一個查詢會保持不變，不過第二個查詢現在 LEFT JOIN 會產生並傳回 6 個結果。

```C#
modelBuilder.Entity<Blog>().HasMany(b => b.Posts).WithOne(p => p.Blog).IsRequired(false);
modelBuilder.Entity<Blog>().HasQueryFilter(b => b.Url.Contains("fish"));
```

替代方法是在 Post 和 Blog 實體上指定一致的篩選。
如此一來，比對篩選會同時套用至 Blog 和 Post 。
預期外的貼文會被刪除，兩次查詢都會回傳3個結果。

```C#
modelBuilder.Entity<Blog>().HasMany(b => b.Posts).WithOne(p => p.Blog).IsRequired();
modelBuilder.Entity<Blog>().HasQueryFilter(b => b.Url.Contains("fish"));
modelBuilder.Entity<Post>().HasQueryFilter(p => p.Blog.Url.Contains("fish"));
```
