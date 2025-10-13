# ABP.IO WEB應用程式框架 AzureAD 登入

> **原文發布日期:** 2021-08-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/23/AbpAzureAdLogin
> **標籤:** 無

---

筆記下新增 Azure AD 帳號登入的相關資訊

## 2021-11-3

如果登入後收到以下錯誤訊息

Self-registration is disabled for this application

這邊需要確保 AD User 的 Mail 欄位有值

因為流程上會需要取得使用者信箱來做新增使用者或是關聯使用者

## 2021/9/28

.Net 5 微軟改用 MSAL 來處理 AAD 登入

[重大變更：驗證： AzureAD UI 和 AzureADB2C。 UI Api 和標記為過時的封裝 - .NET | Microsoft Docs](https://docs.microsoft.com/zh-tw/dotnet/core/compatibility/aspnet-core/5.0/authentication-aad-packages-obsolete)

MSAL 的 ABP 請參考

[How to Use the Azure Active Directory Authentication for MVC / Razor Page Applications | ABP Community](https://community.abp.io/articles/how-to-use-the-azure-active-directory-authentication-for-mvc-razor-page-applications-4603b9cf)

範例

PM> Install-Package Microsoft.Identity.Web

MyWebModule.cs (Web層)

```
context.Services.AddAuthentication()
    // ...其他登入方式...
    .AddMicrosoftIdentityWebApp(configuration);

context.Services.Configure<OpenIdConnectOptions>(OpenIdConnectDefaults.AuthenticationScheme, options =>
    {
        options.ResponseType = OpenIdConnectResponseType.CodeIdToken;
        options.GetClaimsFromUserInfoEndpoint = true;
        options.SignInScheme = IdentityConstants.ExternalScheme;
        options.ClaimActions.MapJsonKey(ClaimTypes.NameIdentifier, "sub");
    });
```

appsetting.json

```
"AzureAd": {
  "Instance": "https://login.microsoftonline.com/",
  "Domain": "mydomain.onmicrosoft.com",
  "ClientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "TenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "CallbackPath": "/signin-azuread-oidc",
  "ClientSecret": "set env variables or appsettings.secrets.json"
}
```

這樣就可以用AAD登入了，登入後會在 AbpUserLogins 新增如下資料，來對應至 UserId

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/92c64bf6-3d30-45d8-9d06-6d69039b0e9e/1632815630.png)

如果要改 LoginPovider => AzureAdOpenId 可以用以下方式

.AddMicrosoftIdentityWebApp(configuration,openIdConnectScheme:"AzureAdOpenId");

context.Services.Configure<OpenIdConnectOptions>("AzureAdOpenId", options =>

主要可能會想要有多種外部登入 (GoogleOpenId,FbOpenId,AzureAdOpenId…ETC.) 的情境了話可以參考一下。

## 2021/9/9

自建AAD帳號必須要設定該User的Email，因為ABP會需要拿這個當作帳號來創建或關聯使用者，如果沒有則AAD登入後會導到註冊頁面。

## 2021/9/1

[Azure App Service 存取限制 導致自己Get自己 403 | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/09/01/AzureAppService403)

## 2021/8/31

### appsettings.secrets.json

appsettings.secrets.json  會複寫 Azure App Service 環境變數

因此如果要使用環境變數，則部署時 `AzureAd.ClientSecret` 不能出現在 appsettings.secrets.json

依照部署方式不同，處理方式可能不太一樣，使用 Git 做 CI/CD 可以保持 appsettings.secrets 為空並藉由忽略該檔案來達成

直接從 IDE build & publish 可能要自己清空 appsettings.secrets 或是直接不使用環境變數改由 appsettings.secrets 定義

唯使用 Git 時不可把 `AzureAd.ClientSecret` 寫在 appsettings.secrets 並 push 到 repo 造成資安疑慮

### 500 Server Error (IDX20803: Unable to obtain configuration from)

Identify Server 4 讀不到 configuration 就會報錯誤，原因可能有很多，但錯誤訊息可能都是這條，

因為詳細錯誤紀錄要另外設定 Services.AddAuthentication() 在這上面

加上以下程式碼可以顯示詳細錯誤訊息

IdentityModelEventSource.ShowPII = true;

如果打開後看到SSL錯誤，可能需要加上以下程式碼 (如果你使用 TLS 1.2)

ServicePointManager.SecurityProtocol = SecurityProtocolType.**Tls12**;

以上程式碼都是加在 Startup.cs > ConfigureServices 裡頭

我打開後則是看到 403，才想到我有設定 Azure App Service IP 限制自己 IP

雖然我整個網站都可以成功訪問，但看來內部取得該設定檔卻被擋住，難不成我要開 127.0.0.1 ?

總之打開錯誤訊息之後，就比較方便 Debug，省得繞一大圈

暫時先把 IP 限制拿掉，可以正常訪問 API，不再噴 500 了

[c# - "InvalidOperationException: IDX20803: Unable to obtain configuration from: '[PII is hidden]'" - Stack Overflow](https://stackoverflow.com/questions/54435551/invalidoperationexception-idx20803-unable-to-obtain-configuration-from-pii)

---

## 結論

[How to Setup Azure Active Directory and Integrate Abp Angular Application | ABP Community](https://community.abp.io/articles/how-to-setup-azure-active-directory-and-integrate-abp-angular-application-lyk87w5l)

WebModule.cs

```
.AddOpenIdConnect("AzureOpenId", "Azure AD OpenId", options =>
{
    options.Authority = "https://login.microsoftonline.com/" + configuration["AzureAd:TenantId"] + "/v2.0/";
    options.ClientId = configuration["AzureAd:ClientId"];
    options.ResponseType = OpenIdConnectResponseType.CodeIdToken;
    options.CallbackPath = configuration["AzureAd:CallbackPath"];
    options.ClientSecret = configuration["AzureAd:ClientSecret"];
    options.RequireHttpsMetadata = false;
    options.SaveTokens = true;
    options.GetClaimsFromUserInfoEndpoint = true;

    options.Scope.Add("email");

    options.ClaimActions.MapJsonKey(ClaimTypes.NameIdentifier, "sub");
});
```

appsettings.json

```
"AzureAd": {
  "Instance": "https://login.microsoftonline.com/",
  "TenantId": "<azureAd-tenant-id>",
  "ClientId": "<azureAd-client-id>",
  "Domain": "domain.onmicrosoft.com",
  "CallbackPath": "/signin-azuread-oidc",
  "ClientSecret": "<azureAd-client-secret>"
}
```

## Azure

首先需要到 Azure > Azure Active Directory > **應用程式註冊 > 新增註冊**

參照：[Quickstart: Add sign-in with Microsoft Identity to an ASP.NET Core web app - Microsoft identity platform | Microsoft Docs](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-v2-aspnet-core-webapp?view=aspnetcore-5.0)

其中會需要設定 CallbackURI 需樣與開發/生產環境中的設定一致

例如開發時設定：https://localhost:44375/signin-azuread-oidc

其中 port 需與開發 run 的 port 一樣

而路徑則等等要把一樣的值設定到 appsettings 裡面

路徑 /signin-azuread-oidc 貌似沒甚麼特別意思

可以自訂喜歡的名稱保持 Azure 設定與 appsetting 一致即可

**憑證及祕密**這好像 2.0 要拿 email 需要用到 ClientSecret 最後拿來當作 User 的帳號

## ABP

參照：[How To/Azure Active Directory Authentication MVC | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/2.8/How-To/Azure-Active-Directory-Authentication-MVC)

目前我成功的是照以上這份文件

大概是使用 Microsoft.AspNetCore.Authentication.AzureAD.UI 這個套件安裝到 Web 層

然後提供相關 Azure AD 的設定值

```
"AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "Domain": "xxxx.onmicrosoft.com",
    "ClientId": "30fa3c26-xxxx-4342-8acc-9d3400c28ad5",
    "TenantId": "da99111d-385d-xxxx-b8bf-c06f82284e39",
    "CallbackPath": "/signin-azuread-oidc",
    "ClientSecret": "define.from.appsettings.secrets.json"
  }
```

其中 `ClientSecret` 需要 Azure > Azure Active Directory > **應用程式註冊 > 上面新增的應用 >** **憑證及祕密 裡面去生成**

**並設定到** `appsettings.secrets.json` **如下所示**

```
{
  "AzureAd": {
    "ClientSecret": "xx-xx.x_xxxxxxxxxx-xxxxx"
  }
}
```

當然直接設到 appsettings.json 也不是不行，只是敏感資料建議獨立設定在 secrets，並且不 commit 到 git 裡面

最後在 WebModule 裡面註冊以下服務

```
private void ConfigureAuthentication(ServiceConfigurationContext context, IConfiguration configuration)
{
    JwtSecurityTokenHandler.DefaultInboundClaimTypeMap.Clear();
    JwtSecurityTokenHandler.DefaultInboundClaimTypeMap.Add("sub", ClaimTypes.NameIdentifier);
    context.Services.AddAuthentication()
        .AddJwtBearer(options =>
        {
            options.Authority = configuration["AuthServer:Authority"];
            options.RequireHttpsMetadata = Convert.ToBoolean(configuration["AuthServer:RequireHttpsMetadata"]);
            options.Audience = "MyProjectName";
        })
        .AddAzureAD(options => configuration.Bind("AzureAd", options));
    context.Services.Configure<OpenIdConnectOptions>(AzureADDefaults.OpenIdScheme, options =>
    {
        options.Authority = options.Authority + "/v2.0/";
        options.ClientId = configuration["AzureAd:ClientId"];
        options.CallbackPath = configuration["AzureAd:CallbackPath"];
        options.ResponseType = OpenIdConnectResponseType.CodeIdToken;
        options.RequireHttpsMetadata = false;

        options.TokenValidationParameters.ValidateIssuer = false;
        options.GetClaimsFromUserInfoEndpoint = true;
        options.SaveTokens = true;
        options.SignInScheme = IdentityConstants.ExternalScheme;

        options.Scope.Add("email");
    });
}
```

其中 `options.Audience = "MyProjectName";` 裡面會是專案初始化時預先生成好的專案名稱

總之就是在原本 `context.Services.AddAuthentication` 的後面加上 `.AddAzureAD` 區段

是說用內建的 OpenId 也可以不用額外裝套件

```
private void ConfigureAuthentication(ServiceConfigurationContext context, IConfiguration configuration)
{
    JwtSecurityTokenHandler.DefaultInboundClaimTypeMap.Clear();
    JwtSecurityTokenHandler.DefaultInboundClaimTypeMap.Add("sub", ClaimTypes.NameIdentifier);
    context.Services.AddAuthentication()
        .AddJwtBearer(options =>
        {
            options.Authority = configuration["AuthServer:Authority"];
            options.RequireHttpsMetadata = Convert.ToBoolean(configuration["AuthServer:RequireHttpsMetadata"]);
            options.Audience = "MyProjectName";
        })
        .AddOpenIdConnect("AzureOpenId", "Azure Active Directory OpenId", options =>
        {
            options.Authority = "https://login.microsoftonline.com/" + configuration["AzureAd:TenantId"] + "/v2.0/";
            options.ClientId = configuration["AzureAd:ClientId"];
            options.ResponseType = OpenIdConnectResponseType.CodeIdToken;
            options.CallbackPath = configuration["AzureAd:CallbackPath"];
            options.RequireHttpsMetadata = false;
            options.SaveTokens = true;
            options.GetClaimsFromUserInfoEndpoint = true;

            options.Scope.Add("email");
        });
}
```

據我目前了解，這是比較通用於所有 OpenId 的方式，但反過來說相比專用於 Azure 的專用套件，他可能需要比較多的手動配置。

ま…我肉眼看到的差異目前只有以下這行

```
options.Authority = options.Authority + "/v2.0/";
```

上面是 AzureUI, 下面是 OpenId

```
options.Authority = "https://login.microsoftonline.com/" + configuration["AzureAd:TenantId"] + "/v2.0/";
```

[asp.net 核心 - 微軟帳戶、AzureAD 和 OpenIdConnect 認證有何區別？- 堆疊溢出 (stackoverflow.com)](https://stackoverflow.com/questions/61029365/what-is-the-difference-between-microsoftaccount-azuread-and-openidconnect-authe)

## DEBUG

可以在最後加上一段 code, 然後下中斷點看拿了些甚麼東西(claims)回來

```

options.Scope.Add("email");

options.Events.OnTokenValidated = (async c =>
{
    var claimsFromOidcProvider = c.Principal?.Claims.ToList();
    await Task.CompletedTask;
});
```

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/92c64bf6-3d30-45d8-9d06-6d69039b0e9e/1629785468.png)

## 其他 OpenID 登入

其他諸如 FB, Google, Microsoft….ETC. OpenID 登入請參照以下文檔進行設定

[Modules/Account | Documentation Center | ABP.IO](https://docs.abp.io/en/abp/latest/Modules/Account#social-external-logins)

```
services.AddAuthentication().AddTwitter(twitterOptions =>
    {
        twitterOptions.ConsumerKey = Configuration["Authentication:Twitter:ConsumerAPIKey"];
        twitterOptions.ConsumerSecret = Configuration["Authentication:Twitter:ConsumerSecret"];
        twitterOptions.RetrieveUserDetails = true;
    });
```

最後大概長這樣

```
services.AddAuthentication()
    .AddMicrosoftAccount(microsoftOptions => { ... })
    .AddGoogle(googleOptions => { ... })
    .AddTwitter(twitterOptions => { ... })
    .AddFacebook(facebookOptions => { ... });
```

## 延伸閱讀

略過登入畫面，直接將使用者導向 Azure AD 帳號密碼登入畫面，請參照以下這篇文章

[ABP.IO WEB應用程式框架 關閉本地帳號註冊與登入 | 御用 - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/08/19/AbpAccountIsSelfRegistrationEnabledFalse)

[LDAP Admin & C# .Net Core Identity Server 4 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2021/07/30/LdapAdmin)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure](/jakeuj/Tags?qq=Azure)
* [Azure AD](/jakeuj/Tags?qq=Azure%20AD)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
