# ABP.IO CrudAppService 自訂 Header 驗證

> **原文發布日期:** 2022-09-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/09/30/abp-CrudAppService-CheckGetPolicyAsync-Header
> **標籤:** 無

---

於應用服務中取得 header 值作為自訂驗證依據

### 結論

```
public class OrderAppService : CrudAppService<Order, OrderDto, Guid>
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public OrderAppService(
        IRepository<Order, Guid> repository,
        IHttpContextAccessor httpContextAccessor)
        : base(repository)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public override async Task<OrderDto> GetAsync(Guid id)
    {
        await CheckGetPolicyAsync();
        return new OrderDto();
    }

    protected override Task CheckGetPolicyAsync()
    {
        var authorization = _httpContextAccessor?.HttpContext?
            .Request.Headers.Authorization.FirstOrDefault();
        if (authorization == "P@ssw0rd")
            return Task.CompletedTask;

        throw new AbpAuthorizationException(code: AbpAuthorizationErrorCodes.
                    GivenPolicyHasNotGrantedWithPolicyName)
            .WithData("Authorization", authorization);
    }
}
```

### 原由

內建 CrudAppService 基底類別中定義

Get 方法的輸入參數是 TKey Id

`public override async Task<OrderDto> GetAsync(Guid id)`

但方法需要額外參數來進行自訂授權驗證

因此打算由 header 傳入驗證用餐數來進行檢查

### 參照

[Application Services | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Application-Services#authorization-for-crud-app-services)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- 回首頁

---

*本文章從點部落遷移至 Writerside*
