# ABP AAD 選擇帳號

記錄一下登入時可以選擇微軟帳號的情況。

## 1. 問題描述

系統僅允許企業帳號登入，但我在登入流程不小心登入到了個人 hotmail 帳號，即使登出系統重新登入會直接用我 hotmail 帳號登入，導致無法使用企業帳號登入。

## 2. 解決方法

在登入流程加入選擇帳號的參數 `prompt=select_account`。

`AuthServerModule.cs` 中的 `AddMicrosoftAccount` 方法可以設定這個參數。

```C#
.AddMicrosoftAccount(
    MicrosoftAccountDefaults.AuthenticationScheme, options => {
    //Enterprise Microsoft accounts as an example.
    var tenantId = configuration["AzureAd:TenantId"] ?? "consumers";
    options.AuthorizationEndpoint =
        $"https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/authorize";
    options.TokenEndpoint =
        $"https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token";

    options.ClaimActions.MapCustomJson("picture", 
        _ => "https://graph.microsoft.com/v1.0/me/photo/$value");
    options.SaveTokens = true;
    
    // 插入 OAuth events，僅當 AzureAd:Prompt 有值時
    var prompt = configuration["AzureAd:Prompt"];
    if (!string.IsNullOrEmpty(prompt))
    {
        options.Events = 
            new Microsoft.AspNetCore.Authentication.OAuth.OAuthEvents
        {
            OnRedirectToAuthorizationEndpoint = cxt =>
            {
                cxt.HttpContext.Response.Redirect(
                    cxt.RedirectUri + $"&prompt={prompt}"
                );
                return Task.CompletedTask;
            }
        };
    }
})
```

appsettings.json 中加入 `AzureAd:Prompt` 的設定：

```json
{
  "AzureAd": {
    "TenantId": "xxxx-xxxx-xxxx-xxxx-xxxx",
    "Prompt": "select_account"
  }
}
```

## 3. 注意事項

如果 `AzureAd:Prompt` 沒有設定，則不會加入 `prompt=select_account` 參數，這樣就不會影響到正常的企業帳號登入流程。

prompt 選用 表示必要的使用者互動類型。

目前的有效值只有 'login'、'none'、'select_account' 和 'consent'。

- prompt=login 會強制使用者在該要求上輸入認證，否定單一登入。
- prompt=none 相反-它會確保不會對使用者顯示任何互動式提示。 如果要求無法透過單一登入以無訊息方式完成，Microsoft 身分識別平臺將會傳回錯誤。
- prompt=select_account 會將使用者傳送至帳戶選擇器，工作階段中記下的所有帳戶都會出現在當中。
- prompt=consent 會在使用者登入之後觸發 OAuth 同意對話方塊，詢問使用者是否要授與權限給應用程式。

## 4. 參考資料

[AZURE-AD-Prompt-Login](https://dotblogs.com.tw/jakeuj/2021/09/28/AZURE-AD-Prompt-Login)
