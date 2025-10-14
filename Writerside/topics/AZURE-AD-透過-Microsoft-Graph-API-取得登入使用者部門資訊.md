# Azure AD Microsoft Graph API

> **原文發布日期:** 2021-09-16
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/16/AAD-Microsoft-Graph-API
> **標籤:** 無

---

本文說明如何透過 Microsoft Graph API 取得 Azure AD 登入使用者的部門資訊。

紀錄 AAD 取得用戶部門

結論

```
// GET https://graph.microsoft.com/v1.0/me?$select=displayName,jobTitle

var user = await graphClient.Me
    .Request()
    .Select(u => new {
        u.Department
    })
    .GetAsync();
```

其他還有甚麼 `u.DisplayName,u.JobTitle` 自己按需求加

---

範例

[active-directory-aspnetcore-webapp-openidconnect-v2/2-WebApp-graph-user/2-1-Call-MSGraph at master · Azure-Samples/active-directory-aspnetcore-webapp-openidconnect-v2 (github.com)](https://github.com/Azure-Samples/active-directory-aspnetcore-webapp-openidconnect-v2/tree/master/2-WebApp-graph-user/2-1-Call-MSGraph)

摘要

appsetting.json (`DownstreamApi`)

```
"AzureAd": {
  "Instance": "https://login.microsoftonline.com/",
  "Domain": "[Enter the domain of your tenant, e.g. contoso.onmicrosoft.com]",
  "TenantId": "[Enter 'common', or 'organizations' or the Tenant Id (Obtained from the Azure portal. Select 'Endpoints' from the 'App registrations' blade and use the GUID in any of the URLs), e.g. da41245a5-11b3-996c-00a8-4d99re19f292]",
  "ClientId": "[Enter the Client Id (Application ID obtained from the Azure portal), e.g. ba74781c2-53c2-442a-97c2-3d60re42f403]",
  "ClientSecret": "[Copy the client secret added to the app from the Azure portal]",
  "ClientCertificates": [
  ],
  // the following is required to handle Continuous Access Evaluation challenges
  "ClientCapabilities": [ "cp1" ],
  "CallbackPath": "/signin-oidc"
},
"DownstreamApi": {
  /*
   'Scopes' contains space separated scopes of the Web API you want to call. This can be:
    - a scope for a V2 application (for instance api:b3682cc7-8b30-4bd2-aaba-080c6bf0fd31/access_as_user)
    - a scope corresponding to a V1 application (for instance <App ID URI>/.default, where  <App ID URI> is the
      App ID URI of a legacy v1 Web application
    Applications are registered in the https:portal.azure.com portal.
  */
  "BaseUrl": "https://graph.microsoft.com/v1.0",
  "Scopes": "user.read"
}
```

Startup.cs => ConfigureServices (`AddMicrosoftGraph`)

```
string[] initialScopes = Configuration.GetValue<string>("DownstreamApi:Scopes")?.Split(' ');

services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(Configuration)
    .EnableTokenAcquisitionToCallDownstreamApi(initialScopes)
    .AddMicrosoftGraph(Configuration.GetSection("DownstreamApi"))
    .AddInMemoryTokenCaches();
```

API (`HomeController`)

```
private readonly GraphServiceClient _graphServiceClient;

private readonly MicrosoftIdentityConsentAndConditionalAccessHandler _consentHandler;

private string[] _graphScopes = new[] { "user.read" };

public HomeController(ILogger<HomeController> logger,
                    IConfiguration configuration,
                    GraphServiceClient graphServiceClient,
                    MicrosoftIdentityConsentAndConditionalAccessHandler consentHandler)
{
    _logger = logger;
    _graphServiceClient = graphServiceClient;
    this._consentHandler = consentHandler;

    // Capture the Scopes for Graph that were used in the original request for an Access token (AT) for MS Graph as
    // they'd be needed again when requesting a fresh AT for Graph during claims challenge processing
    _graphScopes = configuration.GetValue<string>("DownstreamApi:Scopes")?.Split(' ');
}

[AuthorizeForScopes(ScopeKeySection = "DownstreamApi:Scopes")]
public async Task<string> Profile()
{
    var currentUser = await _graphServiceClient.Me.Request().Select(u=>u.Department).GetAsync();
    return currentUser.Department;
}
```

`currentUser.Department` 就會顯示名稱

參照

[Make API calls using the Microsoft Graph SDKs - Microsoft Graph | Microsoft Docs](https://docs.microsoft.com/zh-tw/graph/sdks/create-requests?view=graph-rest-1.0&tabs=CS#use-select-to-control-the-properties-returned)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Azure AD
{ignore-vars="true"}
* Microsoft Graph
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
