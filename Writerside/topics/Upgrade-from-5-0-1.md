# Upgrade from 5.0.1

更新 ABP 到 8.0.0。

## 參照

[官方文件](https://docs.abp.io/en/abp/latest/Migration-Guides/Index)

## 注意

`abp update` 指令都需要於專案根目錄執行

假設切到 `src\web` 內執行則只會更新 web 專案，導致其他專案無法更新 (ex: Domain)

## abp update -v 5.2.0

記得 Add migration

## abp update -v 5.3.0

Test501.Application.Contracts 改成 .Net 6 (standard 2.0)
Test501.Domain.Shared 改成 Microsoft.Extensions.FileProviders.Embedded 6.0.5 (6.0.0)

## abp update -v 6.0.0

記得 Add migration

## abp update -v 7.0.0

專案更新成 .Net 7 (6)
Test501.Application.Contracts 改成 .Net 7 (.Net 6)
Test501.Domain.Shared 改成 .Net 7 (standard 2.0)
Test501.HttpApi.Client 改成 .Net 7 (standard 2.0)
Test501.Domain.Shared 改成 Microsoft.Extensions.FileProviders.Embedded 7.0.0 (6.0.5)
Test501.EntityFrameworkCore 改成 Microsoft.EntityFrameworkCore.Tools 7.0.0 (6.0.0)

`Test501.DbMigrator\DbMigratorHostedService.cs`

新增 `options.AddDataMigrationEnvironment();` 在 `options.Services.AddLogging(c => c.AddSerilog());` 之後

```C#
using (var application = await AbpApplicationFactory.CreateAsync<MyMigratorModule>(options =>
{
    //...
    options.Services.AddLogging(c => c.AddSerilog());
    //...
    options.AddDataMigrationEnvironment();
}))
{
    //...
}
```

`Test501.DbMigrator\Program.cs`

新增 `services.AddDataMigrationEnvironment();` 在 `AddApplicationAsync` 之前

```C#
public static IHostBuilder CreateHostBuilder(string[] args) =>
    Host.CreateDefaultBuilder(args)
        .AddAppSettingsSecretsJson()
        .ConfigureLogging((context, logging) => logging.ClearProviders())
        .ConfigureServices((hostContext, services) =>
        {
            services.AddDataMigrationEnvironment();
            // Call AddDataMigrationEnvironment before AddApplicationAsync
            services.AddHostedService<DbMigratorHostedService>();
        });
```

記得 Add migration

```Shell
cd .\src\Test501.Web\
yarn cache clean
rm -r node_modules
abp install-libs
```

[AbpException: Could not find the bundle file '/libs/bootstrap-daterangepicker/daterangepicker.css' for the bundle 'Basic.Global'!](https://github.com/abpframework/abp/issues/14907)

![libs.png](libs.png){style="block"}

## abp update -v 8.0.0

專案更新成 .Net 8 (7)
Test501.EntityFrameworkCore 改成 Microsoft.EntityFrameworkCore.Tools 8.0.0 (7.0.0)
Test501.Domain.Shared 改成 Microsoft.Extensions.FileProviders.Embedded 8.0.0 (7.0.0)

### 注意：這邊不知道為甚麼官方文件沒有說明要新增，雖然也就是實作介面需要的屬性，但是還是要新增才能正常運作

`Test501.EntityFrameworkCore\Test501DbContext.cs`

加入 `public DbSet<IdentityUserDelegation> UserDelegations { get; }`

```C#
//Identity
public DbSet<IdentityUser> Users { get; set; }
public DbSet<IdentityRole> Roles { get; set; }
public DbSet<IdentityClaimType> ClaimTypes { get; set; }
public DbSet<OrganizationUnit> OrganizationUnits { get; set; }
public DbSet<IdentitySecurityLog> SecurityLogs { get; set; }
public DbSet<IdentityLinkUser> LinkUsers { get; set; }
// 新增以下實作
public DbSet<IdentityUserDelegation> UserDelegations { get; }
```

記得 Add migration

### 注意：不明原因更新後會出現權限問題，需要加入以下程式碼

Test501.HttpApi.Host\Test501HttpApiHostModule.cs

加入 `options.UpdateAbpClaimTypes = false;` 關閉 Claim Type 更新

```C#
public override void PreConfigureServices(ServiceConfigurationContext context)
{
    // disable developer signing credential
    PreConfigure<AbpIdentityServerBuilderOptions>(options =>
    {
        options.AddDeveloperSigningCredential = false;
        // disable claim type update
        options.UpdateAbpClaimTypes = false;
    });
}
```

#### 參照

[v800-Permission-issue](https://support.abp.io/QA/Questions/6432/v800-Permission-issue)
