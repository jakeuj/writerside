# ABP.IO WEB應用程式框架 EF 整合 最佳實踐

> **原文發布日期:** 2023-02-06
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/02/06/abp-Entity-Framework-Core-Integration
> **標籤:** 無

---

EF 整合 最佳實踐的小筆記

## 前言

下面以官方文件 `IdentityDbContext` 與 `IdentityUser` 為例

## DbContext

### 介面

EntityFrameworkCore 層 建立 IIdentityDbContext.cs

```
[ConnectionStringName("AbpIdentity")]
public interface IIdentityDbContext : IEfCoreDbContext
{
    DbSet<IdentityUser> Users { get; set; }
    DbSet<IdentityRole> Roles { get; set; }
}
```

### 類別

EntityFrameworkCore 層 建立 IdentityDbContext.cs

```
[ConnectionStringName("AbpIdentity")]
public class IdentityDbContext : AbpDbContext<IdentityDbContext>, IIdentityDbContext
{
    public static string TablePrefix { get; set; } = YourProjectNameConsts.DbTablePrefix;
    public static string Schema { get; set; } = YourProjectNameConsts.DbSchema;

    public DbSet<IdentityUser> Users { get; set; }
    public DbSet<IdentityRole> Roles { get; set; }

    public IdentityDbContext(DbContextOptions<IdentityDbContext> options)
        : base(options)
    {

    }

    //code omitted for brevity
    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        builder.ConfigureIdentity(options =>
        {
            options.TablePrefix = TablePrefix;
            options.Schema = Schema;
        });
    }
}
```

EntityFrameworkCore 層 建立 IdentityDbContextModelBuilderExtensions.cs

```
public static class IdentityDbContextModelBuilderExtensions
{
    public static void ConfigureIdentity(
        [NotNull] this ModelBuilder builder,
        Action<IdentityModelBuilderConfigurationOptions> optionsAction = null)
    {
        Check.NotNull(builder, nameof(builder));

        var options = new IdentityModelBuilderConfigurationOptions();
        optionsAction?.Invoke(options);

        builder.Entity<IdentityUser>(b =>
        {
            b.ToTable(options.TablePrefix + "Users", options.Schema);
            b.ConfigureByConvention();
            //code omitted for brevity
        });

        builder.Entity<IdentityUserClaim>(b =>
        {
            b.ToTable(options.TablePrefix + "UserClaims", options.Schema);
            b.ConfigureByConvention();
            //code omitted for brevity
        });
        //code omitted for brevity
    }
}
```

EntityFrameworkCore 層 建立 IdentityModelBuilderConfigurationOptions.cs

```
public class IdentityModelBuilderConfigurationOptions : AbpModelBuilderConfigurationOptions
{
    public IdentityModelBuilderConfigurationOptions()
        : base(AbpIdentityConsts.DefaultDbTablePrefix, AbpIdentityConsts.DefaultDbSchema)
    {
    }
}
```

## 倉儲

Domain 層 建立 IIdentityUserRepository.cs

```

public interface IdentityUserRepository

    : IRepository<IdentityUserRepository, Guid>
{

    Task<IdentityUser> FindByNormalizedUserNameAsync(

        string normalizedUserName,
        bool includeDetails = true,
        CancellationToken cancellationToken = default);
}
```

EntityFrameworkCore 層 建立 EfCoreIdentityUserRepository.cs

```
public class EfCoreIdentityUserRepository
    : EfCoreRepository<IIdentityDbContext, IdentityUser, Guid>
    , IIdentityUserRepository
{
    public EfCoreIdentityUserRepository(
        IDbContextProvider<IIdentityDbContext> dbContextProvider)
        : base(dbContextProvider)
    {
    }

    public virtual async Task<IdentityUser> FindByNormalizedUserNameAsync(
        string normalizedUserName,
        bool includeDetails = true,
        CancellationToken cancellationToken = default)
    {
        return await DbSet
            .IncludeDetails(includeDetails)
            .FirstOrDefaultAsync(
                u => u.NormalizedUserName == normalizedUserName,
                GetCancellationToken(cancellationToken)
            );
    }

public override IQueryable<IdentityUser> WithDetails()
    {
        return GetQueryable().IncludeDetails(); // Uses the extension method defined above
    }
}
```

EntityFrameworkCore 層 建立 IdentityExtensions.cs

```
public static class IdentityExtensions
{
    public static IQueryable<IdentityUser> IncludeDetails(
    this IQueryable<IdentityUser> queryable,
    bool include = true)
    {
        if (!include)
        {
            return queryable;
        }

        return queryable
            .Include(x => x.Roles)
            .Include(x => x.Logins)
            .Include(x => x.Claims)
            .Include(x => x.Tokens);
    }
}
```

EntityFrameworkCore 層 AbpIdentityEntityFrameworkCoreModule.cs

```
[DependsOn(
    typeof(AbpIdentityDomainModule),
    typeof(AbpEntityFrameworkCoreModule)
    )]
public class AbpIdentityEntityFrameworkCoreModule : AbpModule
{
    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        context.Services.AddAbpDbContext<IdentityDbContext>(options =>
        {
            options.AddRepository<IdentityUser, EfCoreIdentityUserRepository>();
            options.AddRepository<IdentityRole, EfCoreIdentityRoleRepository>();
        });
    }
}
```

## 參照

[Best Practices/Entity Framework Core Integration | Documentation Center | ABP.IO](https://docs.abp.io/zh-Hans/abp/latest/Best-Practices/Entity-Framework-Core-Integration)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Entity Framework](/jakeuj/Tags?qq=Entity%20Framework)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
