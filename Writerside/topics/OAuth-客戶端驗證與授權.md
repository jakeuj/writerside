# OAuth 客戶端驗證與授權
OAuth 是一種開放標準，用於授權第三方應用程式訪問用戶的資源，而不需要直接分享用戶的憑證。

## 概述
OAuth 客戶端驗證與授權通常涉及以下幾個步驟：
1. **註冊應用程式**：建立新的客戶端，設定 ClientId 和 ClientSecret，允許客戶端驗證流程與相應授權範圍。
![oauth-client.png](oauth-client.png){style="auto"}
2. **新增Policy**：
   在 `ConfigureServices` 方法中新增授權策略，指定使用 JWT Bearer 認證。

   ```C#
   services.AddAuthorization(options =>
   {
       options.AddPolicy("ClientPolicy", policy =>
           policy.RequireAuthenticatedUser()
                 .RequireClaim("scope", "api1"));
   });
   ```
   P.S. 這通常位於 Host 專案的 `Module` 類別中。
3. **設定 API 授權規則**：
   在需要授權的 API 控制器或方法上使用 `[Authorize]` 屬性，並指定使用的認證方案和授權策略。

```C#
[Authorize( AuthenticationSchemes = 
    JwtBearerDefaults.AuthenticationScheme, Policy = "ClientPolicy")]
```

4. IgnoreAntiforgeryToken
    在 API 方法中忽略 CSRF 防護，因為 OAuth 客戶端通常不需要 CSRF 保護。
    
    ```C#
    [IgnoreAntiforgeryToken]
    ```

## 使用範例
以下是一個簡單的範例，展示如何在 ASP.NET Core 中實現 OAuth 客戶端驗證與授權：

`TestProjHttpApiHostModule.cs`
```C#
private void ConfigureAuthorization(
    ServiceConfigurationContext context, 
    IConfiguration configuration)
 {
     context.Services.AddAuthorization(options =>
     {
         // 若是使用 client_credentials flow，會沒有 "sub"，但有 "client_id"
         options.AddPolicy("ClientPolicy", policy =>
         {
             policy.RequireAuthenticatedUser();
             policy.RequireAssertion(context =>
             {
                 var hasClientId = 
                     context.User.HasClaim(c => c.Type == "client_id");
                 var hasScope = 
                     context.User.HasClaim("scope", "TestProj");

                 return hasClientId && hasScope;
             });
         });
     });
 }
```
`TestAppService.cs`
```C#
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace TestProj.Tests;

[IgnoreAntiforgeryToken]
public class TestAppService(ICurrentUser currentUser) 
    : TestProjAppService
{
    [Authorize(AuthenticationSchemes = 
            JwtBearerDefaults.AuthenticationScheme, 
            Policy = "ClientPolicy")]
    public List<string> Get()
    {
        var claims = currentUser.GetAllClaims()
            .Select(c => $"{c.Type}: {c.Value}")
            .ToList();

        return claims;
    }
}
```
test.http
```http
### Authentication Request
POST https://{{authBaseUrl}}/connect/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic {{basicAuth}}

grant_type=client_credentials&scope=TestProj
> {%
    client.log(jsonPath(response.body, "$.access_token",));
    client.global.set("auth_token", response.body.access_token);
%}

### 驗證 Request
GET https://{{apiBaseUrl}}/api/app/test
Authorization: Bearer {{auth_token}}

> {%
    client.test("Request executed successfully 200", function () {
        client.assert(response.status === 200, "Response status is not 200");
    });
    client.log(jsonPath(response.body, "$",));
%}

### 未驗證 Request
GET https://{{apiBaseUrl}}/api/app/test

> {%
    client.test("Request executed successfully 401", function () {
        client.assert(response.status === 401, "Response status is not 401");
    });
%}
```
P.S. 其中 `basicAuth` 是 Base64 編碼的 `ClientId:ClientSecret`，
例如：`Y2xpZW50SWQ6Y2xpZW50U2VjcmV0`