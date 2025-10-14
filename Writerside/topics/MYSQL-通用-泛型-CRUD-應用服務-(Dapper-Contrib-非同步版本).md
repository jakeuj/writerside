# MYSQL Dapper CRUD

> **原文發布日期:** 2019-09-06
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/09/06/CrudAppService
> **標籤:** 無

---

ServerId是業務邏輯需自行移除

含分頁與自動生成建立時間功能

Override GetList 方法實作篩選

用起來像這樣

```

public class PrizeWheelAppService:ObManAsyncCrudAppService<
    Master_PrizeWheel,
    PrizeWheelDto,
    PrizeWheelDto,
    int,
    GetAllPrizeWheelsInput,
    CreatePrizeWheelDto,
    PrizeWheelDto>,IPrizeWheelAppService
{
    public PrizeWheelAppService(IConnectionFactory connectionFactory)
        : base(connectionFactory)
    {
    }
}
```

實作基底參照：[aspnetboilerplate/src/Abp/Application/Services/AsyncCrudAppService.cs](https://github.com/aspnetboilerplate/aspnetboilerplate/blob/dev/src/Abp/Application/Services/AsyncCrudAppService.cs?fbclid=IwAR2g5MJuHiNHPvFsAdBcdg9hcVV4PoY7hoxBTW-AvHaaHpqCdaJcublkXOM)

```

public abstract class ObManAsyncCrudAppService<TEntity, TGetOutputDto, TGetListOutputDto, TKey, TGetListInput, TCreateInput, TUpdateInput>
    : ObManAppServiceBase,IObManAsyncCrudAppService<TGetOutputDto, TGetListOutputDto, TKey, TGetListInput, TCreateInput, TUpdateInput>
    where TEntity : class, I`Entity<TKey>`, new()
    where TGetListInput :IPagedAndSortedResultRequest,IHasServerId
    where TGetOutputDto : IEntityDto<TKey>
    where TGetListOutputDto : IEntityDto<TKey>
{
    protected readonly IConnectionFactory ConnectionFactory;

    protected ObManAsyncCrudAppService(IConnectionFactory connectionFactory)
    {
        ConnectionFactory = connectionFactory;
    }

    public virtual async Task<TGetOutputDto> GetAsync(TKey id, uint serverId)
    {
        TEntity result;
        using (var connection = ConnectionFactory.GetConnection(serverId))
        {
            result = await connection.GetAsync<TEntity>(id);
        }
        return ObjectMapper.Map<TGetOutputDto>(result);
    }

    public virtual async Task<PagedResultDto<TGetListOutputDto>> GetListAsync(TGetListInput input)
    {
        int count;
        List<TEntity> result;
        var tableName = typeof(TEntity).Name;
        var query = CreateFilteredQuery(input);
        using (var connection = ConnectionFactory.GetConnection(input.ServerId))
        {
            count = await connection.ExecuteScalarAsync<int>($"SELECT COUNT(*) FROM {tableName} {query}", input);
            result = (await connection.QueryAsync<TEntity>($"SELECT * FROM {tableName} {query} LIMIT @SkipCount, @MaxResultCount", input)).ToList();
        }
        var mapping = ObjectMapper.Map<List<TGetListOutputDto>>(result);
        var output = new PagedResultDto<TGetListOutputDto>(count, mapping);
        return output;
    }

    protected virtual string CreateFilteredQuery(TGetListInput input)
    {
        return null;
    }

    public virtual async Task<int> CreateAsync(uint serverId, TCreateInput input)
    {
        var entity= ObjectMapper.Map<TEntity>(input);

        if (typeof(IHasCreationTime).IsAssignableFrom(typeof(TEntity)))
        {
            ((IHasCreationTime)entity).CreationTime=DateTime.Now;
        }

        int result;
        using (var connection = ConnectionFactory.GetConnection(serverId))
        {
            result = await connection.InsertAsync(entity);
        }
        return result;
    }

    public virtual async Task<bool> UpdateAsync(TKey id, uint serverId, TUpdateInput input)
    {
        var entity = ObjectMapper.Map<TEntity>(input);
        bool isSuccess ;
        using (var connection = ConnectionFactory.GetConnection(serverId))
        {
            isSuccess = await connection.UpdateAsync(entity);
        }
        return isSuccess;
    }

    public virtual async Task<bool> DeleteAsync(TKey id, uint serverId)
    {
        var entity = new TEntity{Id = id};
        bool isSuccess;
        using (var connection = ConnectionFactory.GetConnection(serverId))
        {
            isSuccess = await connection.DeleteAsync(entity);
        }
        return isSuccess;
    }
}
```

```

public interface ILimitedResultRequest
{
    /// <summary>
    /// Max expected result count.
    /// </summary>
    int MaxResultCount { get; set; }
}
public interface IPagedResultRequest : ILimitedResultRequest
{
    /// <summary>
    /// Skip count (beginning of the page).
    /// </summary>
    int SkipCount { get; set; }
}
public interface IPagedAndSortedResultRequest : IPagedResultRequest, ISortedResultRequest
{

}
```

```

/// <summary>
/// A shortcut of <see cref="IEntityDto{TPrimaryKey}"/> for most used primary key type (<see cref="int"/>).
/// </summary>
public interface IEntityDto : IEntityDto<int>
{

}

/// <summary>
/// Defines common properties for entity based DTOs.
/// </summary>
/// <typeparam name="TPrimaryKey"></typeparam>
public interface IEntityDto<TPrimaryKey>
{
    /// <summary>
    /// Id of the entity.
    /// </summary>
    TPrimaryKey Id { get; set; }
}
```

```

public interface IHasCreationTime
{
    /// <summary>
    /// Creation time of this entity.
    /// </summary>
    DateTime CreationTime { get; set; }
}
```

```

public interface IHasServerId
{
    uint ServerId { get; set; }
}
```

GetAllList Filter

```

public static class StringBuilderCrudExtensions
{
    public static StringBuilder WhereIf(this StringBuilder query, bool condition, string predicate)
    {
        return condition ? query.AppendFormat(query.Length == 0 ? "WHERE {0}=@{0}" : " {0}=@{0}", predicate) : query;
    }
}
```

```

public class ActivityAppService : ObManAsyncCrudAppService<
        Master_Activity,
        ActivityDto,
        ActivityDto,
        int,
        GetAllActivitiesInput,
        CreateActivityDto,
        ActivityDto>,
    IActivityAppService
{
    public ActivityAppService(IConnectionFactory connectionFactory)
        : base(connectionFactory)
    {
    }
    protected override string CreateFilteredQuery(GetAllActivitiesInput input)
    {
        var query = new StringBuilder();
        query.WhereIf(input.Type.HasValue, nameof(input.Type))
            .WhereIf(input.StartTime.HasValue, nameof(input.StartTime))
            .WhereIf(input.EndTime.HasValue, nameof(input.EndTime))
            .WhereIf(input.CreationTime.HasValue, nameof(input.CreationTime));
        return query.ToString();
    }
}
```

```

public class GetAllActivitiesInput : ObManPagedAndSortedResultRequestDto
{
    public ActivityTypeEnum? Type { get; set; }
    public DateTime? StartTime { get; set; }
    public DateTime? EndTime { get; set; }
    public DateTime? CreationTime { get; set; }
}
```

參照

[AbstractKeyReadOnlyAppService](https://github.com/abpframework/abp/blob/276a48a240a62a53bccba60ba7ef08c0439ca5ba/framework/src/Volo.Abp.Ddd.Application/Volo/Abp/Application/Services/AbstractKeyReadOnlyAppService.cs)

[AbstractKeyCrudAppService](https://github.com/abpframework/abp/blob/276a48a240a62a53bccba60ba7ef08c0439ca5ba/framework/src/Volo.Abp.Ddd.Application/Volo/Abp/Application/Services/AbstractKeyCrudAppService.cs)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP
* C#
{ignore-vars="true"}
* Dapper
* MySql
* SQL
* CRUD

* 回首頁

---

*本文章從點部落遷移至 Writerside*
