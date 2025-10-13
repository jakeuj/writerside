# AZURE AD 每次登入都要打帳號密碼

> **原文發布日期:** 2021-09-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/28/AZURE-AD-Prompt-Login
> **標籤:** 無

---

預設是使用單一單入

但有時需求是每次都要重新登入

## 結論

登入時加上 prompt=login

以 dotnet core `OpenIdConnect` 為例，加上以下設定

`options.Prompt = configuration["AzureAd:Prompt"];`

### 範例程式碼

```
private void ConfigureAuthentication(ServiceConfigurationContext context,
    IConfiguration configuration)
{
    context.Services.AddAuthentication()
        .AddJwtBearer(options =>
        {
            options.Authority = configuration["AuthServer:Authority"];
            options.RequireHttpsMetadata =
                Convert.ToBoolean(configuration["AuthServer:RequireHttpsMetadata"]);
            options.Audience = "PlmAPI";
        })
        .AddOpenIdConnect("AzureAdOpenId", "Azure AD OpenId", options =>
        {
            options.Authority = "https://login.microsoftonline.com/" +
                configuration["AzureAd:TenantId"] + "/v2.0/";
            options.ClientId = configuration["AzureAd:ClientId"];
            options.ResponseType = OpenIdConnectResponseType.CodeIdToken;
            options.CallbackPath = configuration["AzureAd:CallbackPath"];
            options.ClientSecret = configuration["AzureAd:ClientSecret"];
            options.RequireHttpsMetadata = false;
            options.SaveTokens = true;
            options.GetClaimsFromUserInfoEndpoint = true;
            options.Prompt = configuration["AzureAd:Prompt"];

            options.Scope.Add("email");

            options.ClaimActions.MapJsonKey(ClaimTypes.NameIdentifier, "sub");
        });
}
```

### prompt

選用

表示必要的使用者互動類型。

目前的有效值只有 'login'、'none'、'select\_account' 和 'consent'。

* prompt=login 會強制使用者在該要求上輸入認證，否定單一登入。
* prompt=none 相反-它會確保不會對使用者顯示任何互動式提示。
  如果要求無法透過單一登入以無訊息方式完成，Microsoft 身分識別平臺將會傳回錯誤。
* prompt=select\_account 會將使用者傳送至帳戶選擇器，工作階段中記下的所有帳戶都會出現在當中。
* prompt=consent 會在使用者登入之後觸發 OAuth 同意對話方塊，詢問使用者是否要授與權限給應用程式。

### 參照

[OAuth 2.0 隱含授與流程-Microsoft 身分識別平臺 | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/active-directory/develop/v2-oauth2-implicit-grant-flow#send-the-sign-in-request)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure AD](/jakeuj/Tags?qq=Azure%20AD)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
