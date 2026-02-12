# ABP.IO WEB應用程式框架 授權

> **原文發布日期:** 2021-07-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/26/ABP-Authorization
> **標籤:** 無

---

搬官方說明文檔來批註

https://docs.abp.io/zh-Hans/abp/latest/Authorization

## 結論

於 Application.Contracts.Permissions.BookStorePermissions 附加

public const string **BookAdd** = **GroupName** + ".BookAdd";

(上面只是用常量定義權限名稱，然後給下面新增權限時使用)

於 Application.Contracts.Permissions.BookStorePermissionDefinitionProvider 附加 Define

myGroup.AddPermission(BookStorePermissions.**BookAdd**);

這樣就完成了！啟動程式到角色賦予權限的畫面就會看到新增的權限！

## 授權

授權用於在應用程序中判斷是否允許用戶執行某些特定的操作.

ABP擴展了 [ASP.NET Core 授权](https://docs.microsoft.com/zh-cn/aspnet/core/security/authorization/introduction), 将 **权限** 添加为自动[策略](https://docs.microsoft.com/zh-cn/aspnet/core/security/authorization/policies)并且使授权系统在 [**应用服务**](https://docs.abp.io/zh-Hans/abp/latest/Application-Services) 同样可用.

所以ASP.NET Core授權的功能特性和它的文檔在基於ABP的應用程序是可用的. 本文中著重介紹在ASP.NET Core授權功能基礎上添加的功能.

## Authorize Attribute

ASP.NET Core 定義了 [**Authorize**](https://docs.microsoft.com/zh-cn/aspnet/core/security/authorization/simple) attribute 用于在控制器,控制器方法以及页面上授权. 现在ABP将它带到了[应用服务](https://docs.abp.io/zh-Hans/abp/latest/Application-Services).

示例:

```
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Volo.Abp.Application.Services;

namespace Acme.BookStore
{
    [Authorize]
    public class AuthorAppService : ApplicationService, IAuthorAppService
    {
        public Task<List<AuthorDto>> GetListAsync()
        {
            ...
        }

        [AllowAnonymous]
        public Task<AuthorDto> GetAsync(Guid id)
        {
            ...
        }

        [Authorize("BookStore_Author_Create")]
        public Task CreateAsync(CreateAuthorDto input)
        {
            ...
        }
    }
}
```

- `Authorize`attribute 使用戶必須登陸到應用程序才可以訪問 `AuthorAppService`中的方法. 所以`GetListAsync` 方法仅可用于通过身份验证的用户.
- `AllowAnonymous`禁用身份驗證. 所以 `GetAsync` 方法任何人都可以访问,包括未授权的用户.
- `[Authorize("BookStore_Author_Create")]`定義了一個策略(参阅 [基于策略的授权](https://docs.microsoft.com/zh-cn/aspnet/core/security/authorization/policies)),它用于检查当前用户的权限.

"BookStore\_Author\_Create" 是一個策略名稱. 如果你想要使用策略的授權方式,需要在ASP.NET Core授權系統中預先定義它.

你可以按照ASP.NET Core文檔進行實施策略授權,但對於簡單的 `true/false` 条件(比如是否授予了用户策略) ABP定义了权限系统,在下一部分中会进行讲解.

## 權限系統

權限系統是為特定用戶,角色或客戶端授權或禁止的簡單策略.

### 定義權限

創建一個繼承自 PermissionDefinitionProvider 的类,如下所示:

Application.Contracts.Permissions.BookStorePermissionDefinitionProvider

```
using Volo.Abp.Authorization.Permissions;

namespace Acme.BookStore.Permissions
{
    public class BookStorePermissionDefinitionProvider : PermissionDefinitionProvider
    {
        public override void Define(IPermissionDefinitionContext context)
        {
            var myGroup = context.AddGroup("BookStore");

            myGroup.AddPermission("BookStore_Author_Create");
        }
    }
}
```

> ABP會自動發現這個類,不需要進行配置!

你需要在 `Define`方法中添加**权限组**或者获取已存在的权限组,并向权限组中添加**权限**.

在定義權限後就可以在ASP.NET Core權限系統中當做**策略**名称使用. 在角色的权限管理模态框中同样可以看到:

![authorization-new-permission-ui](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/images/authorization-new-permission-ui.png)

- 左邊的選項卡顯示了"BookStore" 權限組.
- 右側的"BookStore\_Author\_Create" 是權限名稱,在這裡可以為角色授權或禁止.

保存後更改會持久化到數據庫並在授權系統使用.

> 只有在你安裝了identity模塊時,才會出現上圖中的管理對話框. 該模塊用於用戶和角色的. 啟動模板中已經預裝identity模塊.

#### 本地化權限名稱

"BookStore\_Author\_Create" 名稱對於權限系統來說很適合,但對於UI展示會讓操作人員費解. 幸運的是 `AddPermission` 和 `AddGroup` 方法提供了 `LocalizableString` 参数:

```
var myGroup = context.AddGroup(
    "BookStore",
    LocalizableString.Create<BookStoreResource>("BookStore")
);

myGroup.AddPermission(
    "BookStore_Author_Create",
    LocalizableString.Create<BookStoreResource>("Permission:BookStore_Author_Create")
);
```

然後在本地化文檔中對"BookStore" 和"Permission:BookStore\_Author\_Create" 鍵添加本地化語言:

```
"BookStore": "Book Store",
"Permission:BookStore_Author_Create": "Creating a new author"
```

> 有關更多信息請參閱 [本地化系统文档](https://docs.abp.io/zh-Hans/abp/latest/Localization).

下圖展示了本地化後的效果:

![authorization-new-permission-ui-localized](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/images/authorization-new-permission-ui-localized.png)

#### 多租戶

權限系統同樣支持在ABP中做為一等公民的 [多租户](https://docs.abp.io/zh-Hans/abp/latest/Multi-Tenancy). 在定义新权限时可以设置多租户选项. 有下面三个值:

- **Host**: 权限仅适用于宿主.
- **Tenant**: 权限仅适用于租户.
- **Both**(默认): 权限适用与宿主和租户.

> 如果你的應用程序不是多租戶的,可以忽略這個選項.

`AddPermission` 方法的第三個參數用於設置多租戶選項:

```
myGroup.AddPermission(
    "BookStore_Author_Create",
    LocalizableString.Create<BookStoreResource>("Permission:BookStore_Author_Create"),
    multiTenancySide: MultiTenancySides.Tenant //set multi-tenancy side!
);
```

#### 啟用/禁用權限

權限默認為啟用. 它也可以被禁用,禁用權限所有的用戶將無法使用它. 你仍然可以檢查這個權限,但它總是會返回被禁止.

定義示例:

```
myGroup.AddPermission("Author_Management", isEnabled: false);
```

通常你不需要定義禁用權限(除非你暫時想要禁用應用程序的功能). 無論怎樣,你可能想要禁用依賴模塊中定義的權限,這樣你可以禁用相關的功能. 參閱下面的 "*更改依赖模块的权限定义*" 节,查看示例用法.

> 注意:檢查一個未定義的權限會拋出異常,而被禁用的權限的返回禁止(false).

#### 子權限

權限可以具有子權限,當你想要創建一個層次結構的權限樹時它特別有用. 在這個樹中一個權限可能含有子權限,並且子權限只有在授權父權限時才可用.

定義示例:

```
var authorManagement = myGroup.AddPermission("Author_Management");
authorManagement.AddChild("Author_Management_Create_Books");
authorManagement.AddChild("Author_Management_Edit_Books");
authorManagement.AddChild("Author_Management_Delete_Books");
```

在頁面上如下所示(你可能想要本地化權限名稱):

![authorization-new-permission-ui-hierarcy](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/images/authorization-new-permission-ui-hierarcy.png)

下面的示例代碼是一個典型的應用服務:

```
[Authorize("Author_Management")]
public class AuthorAppService : ApplicationService, IAuthorAppService
{
    public Task<List<AuthorDto>> GetListAsync()
    {
        ...
    }

    public Task<AuthorDto> GetAsync(Guid id)
    {
        ...
    }

    [Authorize("Author_Management_Create_Books")]
    public Task CreateAsync(CreateAuthorDto input)
    {
        ...
    }

    [Authorize("Author_Management_Edit_Books")]
    public Task UpdateAsync(CreateAuthorDto input)
    {
        ...
    }

    [Authorize("Author_Management_Delete_Books")]
    public Task DeleteAsync(CreateAuthorDto input)
    {
        ...
    }
}
```

- 擁有`Author_Management`权限的用户可以访问`GetListAsync`& `GetAsync`方法
- 示例中的其他方法需要額外的權限.

### 自定義策略覆蓋已有權限

有時我們需要擴展擴展應用程序中預構建模塊的權限,可以定義並註冊一個與權限名稱相同的策略到ASP.Net Core授權系統,策略會覆蓋已有權限.

參閱 [基于策略的授权](https://docs.microsoft.com/zh-cn/aspnet/core/security/authorization/policies) 文档了解如何自定义策略.

### 更改依賴模塊的權限定義

從 `PermissionDefinitionProvider`派生的类(就像上面的示例一样) 可以获取现有的权限定义(由依赖[模块](https://docs.abp.io/zh-Hans/abp/latest/Module-Development-Basics)定义)并更改其定义.

示例:

```
context
    .GetPermissionOrNull(IdentityPermissions.Roles.Delete)
    .IsEnabled = false;
```

當你在權限提供程序編寫了這行代碼,它會找到 [身份模块](https://docs.abp.io/zh-Hans/abp/latest/Modules/Identity)的 "role deletion" 权限并且禁用它,因此没有人可以在应用程序中删除角色.

> 提供: 更好的方式應該檢查 `GetPermissionOrNull`返回值,如果权限未定义,它会返回null值.

## IAuthorizationService

ASP.NET Core 提供了 `IAuthorizationService`用于检查权限. 注入后使用它进行条件控制权限.

示例:

```
public async Task CreateAsync(CreateAuthorDto input)
{
    var result = await AuthorizationService
        .AuthorizeAsync("Author_Management_Create_Books");
    if (result.Succeeded == false)
    {
        //throw exception
        throw new AbpAuthorizationException("...");
    }

    //continue to the normal flow...
}
```

> 因為應用服務會經常檢查權限, `ApplicationService` 已经属性注入了`AuthorizationService`, 所有继承自 `ApplicationService` 的类都可以直接使用. 你也可以直接 [注入](https://docs.abp.io/zh-Hans/abp/latest/Dependency-Injection)到类中.

上面的示例代碼是檢查權限的標準代碼,ABP提供了一種簡化的方式來編寫它.

示例:

```
public async Task CreateAsync(CreateAuthorDto input)
{
    await AuthorizationService.CheckAsync("Author_Management_Create_Books");

    //continue to the normal flow...
}
```

如果未授權 `CheckAsync` 扩展方法会抛出 `AbpAuthorizationException` 异常. 还有一个 `IsGrantedAsync` 扩展方法会返回 `true` 或 `false`.

`IAuthorizationService` 中有多个 `AuthorizeAsync` 方法重载. [ASP.NET Core 授权文档](https://docs.microsoft.com/zh-cn/aspnet/core/security/authorization/introduction)中有详细的解释.

> 提示: 盡可能使用聲明式的`Authorize` attribute,因为它比较简单不会侵入方法内部. 如果你需要在业务代码中有条件的检查权限,那么请使用 `IAuthorizationService`.

### 在JavaScript中檢查權限

有時你會需要在客戶端檢查策略/權限. 在ASP.NET Core MVC/Razor頁面應用程序可以使用`abp.auth`API. 示例:

```
abp.auth.isGranted('MyPermissionName');
```

## 權限管理

通常權限管理是管理員用戶使用權限管理模態框進行授權:

![authorization-new-permission-ui-localized](https://raw.githubusercontent.com/abpframework/abp/rel-4.3/docs/zh-Hans/images/authorization-new-permission-ui-localized.png)

如果你想要通過代碼管理權限, 可以注入使用`IPermissionManager`. 如下所示:

```
public class MyService : ITransientDependency
{
    private readonly IPermissionManager _permissionManager;

    public MyService(IPermissionManager permissionManager)
    {
        _permissionManager = permissionManager;
    }

    public async Task GrantPermissionForUserAsync(Guid userId, string permissionName)
    {
        await _permissionManager.SetForUserAsync(userId, permissionName, true);
    }

    public async Task ProhibitPermissionForUserAsync(Guid userId, string permissionName)
    {
        await _permissionManager.SetForUserAsync(userId, permissionName, false);
    }
}
```

`SetForUserAsync`方法用於設置用戶的權限(true/false). 類似的還有 `SetForRoleAsync` 和 `SetForClientAsync` 扩展方法.

`IPermissionManager`由權限管理模塊定義, 更多信息請參閱[权限管理模块文档](https://docs.abp.io/zh-Hans/abp/latest/Modules/Permission-Management).

## 高級主題

### Permission Value Providers

權限檢查是可擴展的. 繼承自`PermissionValueProvider` (或实现 `IPermissionValueProvider`) 的任何类都可以参与权限检查. 有三个预定义的Provider:

- `UserPermissionValueProvider`從當前的聲明中拿到當前用戶ID並檢查用戶授權. 用戶聲明由 `AbpClaimTypes.UserId`静态属性定义.
- `RolePermissionValueProvider`從當前的聲明中拿到授予當前用戶的角色集合併且判斷角色是否具有指定的權限. 角色聲明由 `AbpClaimTypes.Role`静态属性定义.
- `ClientPermissionValueProvider`從當前聲明中拿到當前客戶端並檢查客戶端是否具有指定的權限. 這在沒有當前登錄用戶的客戶端交互特別有用. 客戶端聲明由 `AbpClaimTypes.ClientId`静态属性定义.

你可以定義自己的`PermissionValueProvider`扩展权限检查系统.

示例:

```
public class SystemAdminPermissionValueProvider : PermissionValueProvider
{
    public SystemAdminPermissionValueProvider(IPermissionStore permissionStore)
        : base(permissionStore)
    {
    }

    public override string Name => "SystemAdmin";

    public async override Task<PermissionGrantResult>
           CheckAsync(PermissionValueCheckContext context)
    {
        if (context.Principal?.FindFirst("User_Type")?.Value == "SystemAdmin")
        {
            return PermissionGrantResult.Granted;
        }

        return PermissionGrantResult.Undefined;
    }
}
```

示例`SystemAdminPermissionValueProvider`允许声明`User_Type`值为`SystemAdmin`的用户授予所有权限. 通常在`Provider`中使用当前声明和 `IPermissionStore`.

`PermissionValueProvider`的 `CheckAsync`应该返回下面三个值之一:

- `PermissionGrantResult.Granted`授予用戶權限,如果沒有其他的授權值提供程序返回`Prohibited`, 那么最后会返回 `Granted`.
- `PermissionGrantResult.Prohibited`禁止授權用戶,任何一個授權值提供程序返回了`Prohibited`, 那么其他的提供程序返回的值都不再重要.
- `PermissionGrantResult.Undefined`代表當前無法確定是否授予或禁止權限, 返回`UnDefined`由其他权限值提供程序检查权限.

定義`Provider`后将其添加到 `AbpPermissionOptions`,如下所示:

```
Configure<AbpPermissionOptions>(options =>
{
    options.ValueProviders.Add<SystemAdminPermissionValueProvider>();
});
```

### Permission Store

`IPermissionStore`是唯一需要從持久化源(通常是數據庫)中讀取權限值的接口. 它的實現在權限管理模塊. 參見 [权限管理模块](https://docs.abp.io/zh-Hans/abp/latest/Modules/Permission-Management) 了解更多信息

### AlwaysAllowAuthorizationService

`AlwaysAllowAuthorizationService` 類可以繞過授權服務. 通常用於在需要禁用授權系統的集成測試中.

使用 `IServiceCollection.AddAlwaysAllowAuthorization()` 扩展方法将 `AlwaysAllowAuthorizationService` 注册到 [依赖注入](https://docs.abp.io/zh-Hans/abp/latest/Dependency-Injection) 系统中:

```
public override void ConfigureServices(ServiceConfigurationContext context)
{
    context.Services.AddAlwaysAllowAuthorization();
}
```

啟動模板的集成測試已經禁用了授權服務.

## 接下來

- [權限管理模塊](https://docs.abp.io/zh-Hans/abp/latest/Modules/Permission-Management)
- [ASP.NET Core MVC / Razor 頁面JavaScript Auth API](https://docs.abp.io/zh-Hans/abp/latest/API/JavaScript-API/Auth)
- [Angular界面中的權限管理](https://docs.abp.io/zh-Hans/abp/latest/UI/Angular/Permission-Management)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP

- 回首頁

---

*本文章從點部落遷移至 Writerside*
