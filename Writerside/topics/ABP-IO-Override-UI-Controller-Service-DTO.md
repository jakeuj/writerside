# ABP.IO WEB應用程式框架 Override UI&#x3001;控制器&#x3001;服務&#x3001;DTO {id="ABP-IO-Override-UI-Controller-Service-DTO"}

> **原文發布日期:** 2021-07-27
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/27/ABP-Override-Controller
> **標籤:** 無

---

找了老半天怎麼 override 模塊的控制器

這邊筆記一下網址順便先機翻一下

2021/8/23 補充

跟登入有關的程式碼如下

* [Volo.Abp.Account.Web.Areas.Account.Controllers.AccountController](https://github.com/abpframework/abp/blob/dev/modules/account/src/Volo.Abp.Account.Web/Areas/Account/Controllers/AccountController.cs#L51)
* [Volo.Abp.Account.Web.Pages.Account.LoginModel](https://github.com/abpframework/abp/blob/dev/modules/account/src/Volo.Abp.Account.Web/Pages/Account/Login.cshtml.cs#L85)
* [Volo.Abp.Account.Web.Pages.Account.IdentityServerSupportedLoginModel](https://github.com/abpframework/abp/blob/dev/modules/account/src/Volo.Abp.Account.Web.IdentityServer/Pages/Account/IdentityServerSupportedLoginModel.cs#L104)

其中的關係是

[AccountController](https://github.com/abpframework/abp/blob/dev/modules/account/src/Volo.Abp.Account.Web/Areas/Account/Controllers/AccountController.cs#L51) 提供 API 呼叫，但 Account 模塊不會呼叫這支 API，估計給你自己呼叫用的

[IdentityServerSupportedLoginModel](https://github.com/abpframework/abp/blob/dev/modules/account/src/Volo.Abp.Account.Web.IdentityServer/Pages/Account/IdentityServerSupportedLoginModel.cs#L104) 繼承 [LoginModel](https://github.com/abpframework/abp/blob/dev/modules/account/src/Volo.Abp.Account.Web/Pages/Account/Login.cshtml.cs#L85) 並替換，實際上專案跑的是以這段程式為主

而如果我們要修改原本專案的登入流程則是要

新增自訂 LoginModel 繼承自 [IdentityServerSupportedLoginModel](https://github.com/abpframework/abp/blob/dev/modules/account/src/Volo.Abp.Account.Web.IdentityServer/Pages/Account/IdentityServerSupportedLoginModel.cs#L104) 並替換掉 [LoginModel](https://github.com/abpframework/abp/blob/dev/modules/account/src/Volo.Abp.Account.Web/Pages/Account/Login.cshtml.cs#L85)

結論

```
namespace MyProjectName.Web.Pages.Account
{
    [Dependency(ReplaceServices = true)]
    [ExposeServices(typeof(LoginModel))]
    public class CustomLoginModel : IdentityServerSupportedLoginModel
    {
        private readonly ILogger<CustomLoginModel> _logger;

        public CustomLoginModel(
            IAuthenticationSchemeProvider schemeProvider,
            `IOptions<AbpAccountOptions>` accountOptions,
            IIdentityServerInteractionService interaction,
            IClientStore clientStore,
            IEventService identityServerEvents,
            `IOptions<IdentityOptions>` identityOptions,
            ILogger<CustomLoginModel> logger) : base(
            schemeProvider,
            accountOptions,
            interaction,
            clientStore,
            identityServerEvents,
            identityOptions)
        {
            _logger = logger;
        }

        public override async Task<IActionResult> OnGetAsync()
        {
            _logger.LogDebug("Test...........");

            return await base.OnGetAsync();
        }
    }
}
```

以自訂登入類別繼承自 `IdentityServerSupportedLoginModel` 並取代原本的 `LoginModel` 才是正確姿勢

參照 [UI/AspNetCore/Customization User Interface | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/UI/AspNetCore/Customization-User-Interface)

---

官方文件的 menu 找不到這篇

他其實在架構>模塊化>自訂模塊>覆蓋服務與組件>覆蓋服務 [連結](https://docs.abp.io/en/abp/latest/Customizing-Application-Modules-Guide#overriding-services-components)

就一個超連結，並且切中文了話會跟你說覆蓋控制器同上 (覆蓋服務)

總之如果要修改模塊的控制器或服務請參照以下連結

<https://docs.abp.io/en/abp/latest/Customizing-Application-Modules-Overriding-Services#example-overriding-a-controller>

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/e1b140f8-1c76-4157-a679-ff0de2c89ca0/1627460788.png)

我以為成功了，結果 override Login 還是跑回原本的控制器？最後又改了一下才成功…

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/e1b140f8-1c76-4157-a679-ff0de2c89ca0/1627638136.png)

---

## 自定義應用程序模塊：覆蓋服務

您可能需要**更改**應用程序依賴模塊的**行為（業務邏輯）**。在這種情況下，您可以利用[依賴注入系統](https://docs.abp.io/en/abp/latest/Dependency-Injection)的強大功能，通過您自己的實現來替換依賴模塊的服務、控制器甚至頁面模型。

註冊到依賴注入的任何類型的類都可以**替換服務**，包括 ABP 框架的服務。

您可以根據自己的要求使用不同的選項，這些選項將在下一節中解釋。

> 請注意，某些服務方法可能不是虛擬的，因此您可能無法覆蓋。我們通過設計使所有虛擬化。如果您發現任何不可覆蓋的方法，請[創建一個問題](https://github.com/abpframework/abp/issues/new)或自己完成並在 GitHub 上發送**拉取請求**。

## 更換接口

如果給定的服務定義了一個接口，就像`IdentityUserAppService`類實現了`IIdentityUserAppService`，您可以重新實現相同的接口並用您的類替換當前實現。例子：

```
public class MyIdentityUserAppService : IIdentityUserAppService, ITransientDependency
{
    //...
}
```

`MyIdentityUserAppService`用`IIdentityUserAppService`命名約定替換 the （因為兩個都以 結尾`IdentityUserAppService`）。如果您的類名不匹配，則需要手動公開服務接口：

```
[ExposeServices(typeof(IIdentityUserAppService))]
public class TestAppService : IIdentityUserAppService, ITransientDependency
{
    //...
}
```

依賴注入系統允許為同一個接口註冊多個服務。注入接口時使用最後註冊的一個。明確替換服務是一種很好的做法。

例子：

```
[Dependency(ReplaceServices = true)]
[ExposeServices(typeof(IIdentityUserAppService))]
public class TestAppService : IIdentityUserAppService, ITransientDependency
{
    //...
}
```

這樣，`IIdentityUserAppService`接口的實現將是單一的，而不會改變這種情況下的結果。也可以通過代碼替換服務：

```
context.Services.Replace(
    ServiceDescriptor.Transient<IIdentityUserAppService, MyIdentityUserAppService>()
);
```

你可以在`ConfigureServices`你的[模塊](https://docs.abp.io/en/abp/latest/Module-Development-Basics)的方法中寫這個。

## 覆蓋服務類

在大多數情況下，您會希望更改服務當前實現的一種或幾種方法。在這種情況下，重新實現完整的接口效率不高。作為更好的方法，從原始類繼承並覆蓋所需的方法。

### 示例：覆蓋應用程序服務

```
[Dependency(ReplaceServices = true)]
[ExposeServices(typeof(IIdentityUserAppService), typeof(IdentityUserAppService), typeof(MyIdentityUserAppService))]
public class MyIdentityUserAppService : IdentityUserAppService
{
    //...
    public MyIdentityUserAppService(
        IdentityUserManager userManager,
        IIdentityUserRepository userRepository,
        IGuidGenerator guidGenerator
    ) : base(
        userManager,
        userRepository,
        guidGenerator)
    {
    }

    public async override Task<IdentityUserDto> CreateAsync(IdentityUserCreateDto input)
    {
        if (input.PhoneNumber.IsNullOrWhiteSpace())
        {
            throw new AbpValidationException(
                "Phone number is required for new users!",
                new List<ValidationResult>
                {
                    new ValidationResult(
                        "Phone number can not be empty!",
                        new []{"PhoneNumber"}
                    )
                }
            );        }

        return await base.CreateAsync(input);
    }
}
```

這個類**覆蓋**了[應用服務](https://docs.abp.io/en/abp/latest/Application-Services)的`CreateAsync`方法來檢查電話號碼。然後調用基方法繼續**底層業務邏輯**。通過這種方式，您可以在基本邏輯**之前**和**之後**執行額外的業務邏輯。`IdentityUserAppService`

您可以完全**重寫**用戶創建的整個業務邏輯，而無需調用基本方法。

### 示例：覆蓋域服務

```
[Dependency(ReplaceServices = true)]
[ExposeServices(typeof(IdentityUserManager))]
public class MyIdentityUserManager : IdentityUserManager
{
        public MyIdentityUserManager(
            IdentityUserStore store,
            IIdentityRoleRepository roleRepository,
            IIdentityUserRepository userRepository,
            `IOptions<IdentityOptions>` optionsAccessor,
            IPasswordHasher<IdentityUser> passwordHasher,
            IEnumerable<IUserValidator<IdentityUser>> userValidators,
            IEnumerable<IPasswordValidator<IdentityUser>> passwordValidators,
            ILookupNormalizer keyNormalizer,
            IdentityErrorDescriber errors,
            IServiceProvider services,
            ILogger<IdentityUserManager> logger,
            ICancellationTokenProvider cancellationTokenProvider) :
            base(store,
                roleRepository,
                userRepository,
                optionsAccessor,
                passwordHasher,
                userValidators,
                passwordValidators,
                keyNormalizer,
                errors,
                services,
                logger,
                cancellationTokenProvider)
        {
        }

    public async override Task<IdentityResult> CreateAsync(IdentityUser user)
    {
        if (user.PhoneNumber.IsNullOrWhiteSpace())
        {
            throw new AbpValidationException(
                "Phone number is required for new users!",
                new List<ValidationResult>
                {
                    new ValidationResult(
                        "Phone number can not be empty!",
                        new []{"PhoneNumber"}
                    )
                }
            );
        }

        return await base.CreateAsync(user);
    }
}
```

此示例類繼承自`IdentityUserManager` [域服務](https://docs.abp.io/en/abp/latest/Domain-Services)並覆蓋`CreateAsync`方法以執行上面實現的相同電話號碼檢查。結果是一樣的，但這次我們在域服務中實現了它，假設這是我們系統的**核心域邏輯**。

> `[ExposeServices(typeof(IdentityUserManager))]` 屬性在這裡是**必需的**，因為`IdentityUserManager`它沒有定義接口（如`IIdentityUserManager`），並且依賴注入系統不會按照約定為繼承的類公開服務（就像它為實現的接口所做的那樣）。

檢查[本地化系統](https://docs.abp.io/en/abp/latest/Localization)以了解如何本地化錯誤消息。

### 示例：覆蓋控制器

```
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Volo.Abp.Account;
using Volo.Abp.DependencyInjection;

namespace MyProject.Controllers
{
    [Dependency(ReplaceServices = true)]
    [ExposeServices(typeof(AccountController))]
    public class MyAccountController : AccountController
    {
        public MyAccountController(IAccountAppService accountAppService)
            : base(accountAppService)
        {

        }

        public async override Task SendPasswordResetCodeAsync(
            SendPasswordResetCodeDto input)
        {
            Logger.LogInformation("Your custom logic...");

            await base.SendPasswordResetCodeAsync(input);
        }
    }
}
```

此示例替換了`AccountController`（[帳戶模塊中](https://docs.abp.io/en/abp/latest/Modules/Account)定義的 API 控制器）並覆蓋了該`SendPasswordResetCodeAsync`方法。

`[ExposeServices(typeof(AccountController))]`在這裡**是必不可少的**，因為它`AccountController`在依賴注入系統中註冊了這個控制器。`[Dependency(ReplaceServices = true)]`也建議清除舊的註冊（即使是ASP.NET Core DI系統也會選擇最後註冊的）。

此外，`MyAccountController`將被刪除，[`ApplicationModel`](https://docs.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.mvc.applicationmodels.applicationmodel.controllers)因為它定義了`ExposeServicesAttribute`。

如果`IncludeSelf = true`指定，即`[ExposeServices(typeof(AccountController), IncludeSelf = true)]`，`AccountController`則將被刪除。這對於**擴展**控制器很有用。

如果您不想刪除任一控制器，您可以配置`AbpAspNetCoreMvcOptions`：

```
Configure<AbpAspNetCoreMvcOptions>(options =>
{
    options.IgnoredControllersOnModelExclusion.AddIfNotContains(typeof(MyAccountController));
});
```

### 覆蓋其他類

覆蓋控制器、框架服務、視圖組件類和任何其他類型的註冊到依賴注入的類都可以像上面的例子一樣被覆蓋。

## 擴展數據傳輸對象

**擴展**[**實體**](https://docs.abp.io/en/abp/latest/Entities)是可能的，如[擴展實體文檔中所述](https://docs.abp.io/en/abp/latest/Customizing-Application-Modules-Extending-Entities)。通過這種方式，您可以向實體添加**自定義屬性**並通過覆蓋上述相關服務來執行**其他業務邏輯**。

還可以擴展應用程序服務使用的數據傳輸對象 ( **DTO** )。通過這種方式，您可以從 UI（或客戶端）獲取額外的屬性並從服務返回額外的屬性。

### 例子

假設你已經添加了`SocialSecurityNumber`作為中描述的[擴展實體文檔](https://docs.abp.io/en/abp/latest/Customizing-Application-Modules-Extending-Entities)，並希望包括此信息，而從獲得的用戶列表`GetListAsync` 的方法`IdentityUserAppService`。

您可以使用[對象擴展系統](https://docs.abp.io/en/abp/latest/Object-Extensions)將屬性添加到`IdentityUserDto`. `YourProjectNameDtoExtensions`在應用啟動模板自帶的類裡面寫這段代碼：

```
ObjectExtensionManager.Instance
    .AddOrUpdateProperty<IdentityUserDto, string>(
        "SocialSecurityNumber"
    );
```

此代碼定義一個`SocialSecurityNumber`到`IdentityUserDto`類作為`string`類型。就這樣。現在，如果您從 REST API 客戶端調用`/api/identity/users`HTTP API（在`IdentityUserAppService`內部使用），您將`SocialSecurityNumber`在`extraProperties`部分中看到該值。

```
{
    "totalCount": 1,
    "items": [{
        "tenantId": null,
        "userName": "admin",
        "name": "admin",
        "surname": null,
        "email": "admin@abp.io",
        "emailConfirmed": false,
        "phoneNumber": null,
        "phoneNumberConfirmed": false,
        "twoFactorEnabled": false,
        "lockoutEnabled": true,
        "lockoutEnd": null,
        "concurrencyStamp": "b4c371a0ab604de28af472fa79c3b70c",
        "isDeleted": false,
        "deleterId": null,
        "deletionTime": null,
        "lastModificationTime": "2020-04-09T21:25:47.0740706",
        "lastModifierId": null,
        "creationTime": "2020-04-09T21:25:46.8308744",
        "creatorId": null,
        "id": "8edecb8f-1894-a9b1-833b-39f4725db2a3",
        "extraProperties": {
            "SocialSecurityNumber": "123456789"
        }
    }]
}
```

現在手動將`123456789`值添加到數據庫中。

所有預構建的模塊都在其 DTO 中支持額外的屬性，因此您可以輕鬆配置。

### 定義檢查

當您為實體[定義](https://docs.abp.io/en/abp/latest/Customizing-Application-Modules-Extending-Entities)額外的屬性時，出於安全考慮，它不會自動出現在所有相關的 DTO 中。額外的屬性可能包含敏感數據，默認情況下您可能不想將其公開給客戶端。

因此，如果要使其可用於 DTO（如上所述），則需要為相應的 DTO 顯式定義相同的屬性。如果您想允許在用戶創建時設置它，您還需要為`IdentityUserCreateDto`.

如果財產不是那麼安全，這可能會很乏味。對象擴展系統允許您忽略對所需屬性的此定義檢查。請參閱下面的示例：

```
ObjectExtensionManager.Instance
    .AddOrUpdateProperty<IdentityUser, string>(
        "SocialSecurityNumber",
        options =>
        {
            options.MapEfCore(b => b.HasMaxLength(32));
            options.CheckPairDefinitionOnMapping = false;
        }
    );
```

這是為實體定義屬性的另一種方法（`ObjectExtensionManager`更多，請參閱[其文檔](https://docs.abp.io/en/abp/latest/Object-Extensions)）。這一次，我們設置`CheckPairDefinitionOnMapping`為 false 以跳過定義檢查，同時將實體映射到 DTO，反之亦然。

如果您不喜歡這種方法，但想更輕鬆地將單個屬性添加到多個對象 (DTO)，`AddOrUpdateProperty`可以獲取類型數組以添加額外的屬性：

```
ObjectExtensionManager.Instance
    .AddOrUpdateProperty<string>(
        new[]
        {
            typeof(IdentityUserDto),
            typeof(IdentityUserCreateDto),
            typeof(IdentityUserUpdateDto)
        },
        "SocialSecurityNumber"
    );
```

### 關於用戶界面

該系統允許您向實體和 DTO 添加額外的屬性並執行自定義業務代碼，但它與用戶界面無關。

請參閱[覆蓋](https://docs.abp.io/en/abp/latest/Customizing-Application-Modules-Overriding-User-Interface)UI 部分[的用戶界面](https://docs.abp.io/en/abp/latest/Customizing-Application-Modules-Overriding-User-Interface)指南。

## 如何找到服務？

[模塊文檔](https://docs.abp.io/en/abp/latest/Modules/Index)包括它們定義的主要服務的列表。此外，您可以調查[他們的源代碼](https://github.com/abpframework/abp/tree/dev/modules)以探索所有服務。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
