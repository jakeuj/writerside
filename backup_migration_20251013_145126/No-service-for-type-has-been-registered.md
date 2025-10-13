# No service for type has been registered

檢查 DbContext 是否有宣告 `DbSet<T>`，並且在 ConfigureServices 中有呼叫 `AddDbContext<T>`。

## Sample

```C#
public virtual DbSet<Product> Products { get; set; }
```