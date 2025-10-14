# ABP.IO 批量預賦予 AzureAD User 角色

> **原文發布日期:** 2021-09-08
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/08/Abp-Create-Identity-Users-List
> **標籤:** 無

---

因為 AAD 帳號在使用者登入之前在系統不會有資料

如果要讓新登入的使用者有指定的角色權限

目前思路是預建User並給予對應角色

結論

```
public class CustomIdentityUserCreateDto
{
    [Required]
    [EmailAddress]
    [DynamicStringLength(typeof(IdentityUserConsts), nameof(IdentityUserConsts.MaxEmailLength))]
    public string Email { get; set; }

    [CanBeNull]
    public string[] RoleNames { get; set; }
}
```

```
public class CustomIdentityUserAppService : ApplicationService
{
    private IdentityUserManager UserManager { get; }
    private IOptions<IdentityOptions> IdentityOptions { get; }
    public CustomIdentityUserAppService(
        IdentityUserManager userManager,
        IOptions<IdentityOptions> identityOptions)
    {
        UserManager = userManager;
        IdentityOptions = identityOptions;
    }

    [Authorize(IdentityPermissions.Users.Create)]
    public async Task CreateUsersAsync(
        IEnumerable<CustomIdentityUserCreateDto> inputs)
    {
        foreach (var input in inputs)
        {
            await IdentityOptions.SetAsync();

            var user = new IdentityUser(
                GuidGenerator.Create(),
                input.Email,
                input.Email,
                CurrentTenant.Id
            );

            (await UserManager.CreateAsync(user)).CheckErrors();

            if (input.RoleNames != null)
            {
                (await UserManager.SetRolesAsync(user, input.RoleNames)).CheckErrors();
            }

            (await UserManager.UpdateAsync(user)).CheckErrors();
        }

        await CurrentUnitOfWork.SaveChangesAsync();
    }
}
```

以上是直接新增一個全新服務來放新的 API

下面是用擴充原本模塊的方式來新增新 API

```
public class MyIdentityUserCreateDto
{
    [Required]
    [EmailAddress]
    [DynamicStringLength(typeof(IdentityUserConsts), nameof(IdentityUserConsts.MaxEmailLength))]
    public string Email { get; set; }

    [CanBeNull]
    public string[] RoleNames { get; set; }
}
```

```
[Dependency(ReplaceServices = true)]
[ExposeServices(typeof(IIdentityUserAppService), typeof(IdentityUserAppService), typeof(MyIdentityUserAppService))]
public class MyIdentityUserAppService : IdentityUserAppService
{
    public MyIdentityUserAppService(
        IdentityUserManager userManager,
        IIdentityUserRepository userRepository,
        IIdentityRoleRepository roleRepository,
        IOptions<IdentityOptions> identityOptions) : base(userManager, userRepository, roleRepository,
        identityOptions)
    {
    }

    [Authorize(IdentityPermissions.Users.Create)]
    public async Task CreateUsersAsync(
        IEnumerable<MyIdentityUserCreateDto> inputs)
    {
        foreach (var input in inputs)
        {
            await IdentityOptions.SetAsync();

            var user = new IdentityUser(
                GuidGenerator.Create(),
                input.Email,
                input.Email,
                CurrentTenant.Id
            );

            (await UserManager.CreateAsync(user)).CheckErrors();

            if (input.RoleNames != null)
            {
                (await UserManager.SetRolesAsync(user, input.RoleNames)).CheckErrors();
            }

            (await UserManager.UpdateAsync(user)).CheckErrors();
        }

        await CurrentUnitOfWork.SaveChangesAsync();
    }
}
```

如果原本就有 override `IdentityUserAppService` 某些方法的打算

我覺得放一起比較好

BTW, Swagger 會同時顯示新舊 API

如果要隱藏可以參考另一篇

[ABP.IO WEB應用程式框架 Swagger 隱藏指定 API | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/09/08/Abp-Swagger-Hide-Endpoint)

備註：這邊簡單直接檢查原本的 User.Create 權限，所以記得先登入有該權限的帳號，否則直接到 Swagger 呼叫 API 會報錯

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
