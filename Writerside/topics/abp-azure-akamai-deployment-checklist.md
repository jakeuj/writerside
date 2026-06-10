# ABP 分離 Auth/API 專案部署到 Azure 與 Akamai 檢查表

ABP 分離式部署經 Akamai 再回 Azure App Service 時，公開 hostname 要一路對齊到 Akamai、App Service custom domain、TLS/SNI、ABP `SelfUrl`、OpenIddict redirect URI 與前端 OIDC 設定。`*.azurewebsites.net` 只適合作為 Azure origin resolution 或平台預設位址，不應出現在使用者-facing URL、redirect URI 或 cookie domain。

<tldr>
<p>Akamai 到 origin 主建議使用 <code>Forward Host Header = Incoming Host Header</code>。</p>
<p><code>AuthServer</code>、<code>HttpApi.Host</code>、前端 Web/SPA 與 DbMigrator 都要使用公開 hostname。</p>
<p>如果短期必須用 origin hostname，必須另外處理 <code>Forwarded</code> / <code>X-Forwarded-Host</code>、redirect URI、cookie 與 App Service Authentication。</p>
</tldr>

> 本文中的 hostname、App Service 名稱、憑證、client id、connection string 與 Azure 資源皆已去識別化。請把 `<auth-public-host>`、`<api-public-host>`、`<web-public-host>`、`<app-name>.azurewebsites.net` 替換成自己的環境值。

## 建議拓樸

本文假設是 ABP 分離式部署：

- `AuthServer`：登入、OpenIddict issuer、token endpoint、account pages。
- `HttpApi.Host` / API：後端 API 與 Swagger。
- Web / SPA：MVC、Blazor Server、Angular、Blazor WASM 或 React 前端。
- Akamai：公開入口、WAF、edge TLS、origin fetch 到 Azure App Service。
- Azure App Service：各服務的 origin host。

建議公開 URL 長這樣：

```text
https://<auth-public-host>
https://<api-public-host>
https://<web-public-host>
```

避免讓登入流程、OpenIddict discovery document、cookie 或前端設定出現：

```text
https://<app-name>.azurewebsites.net
```

## Akamai 設定

主路線：

| Akamai 欄位 | 建議值 | 注意事項 |
| --- | --- | --- |
| `Forward Host Header` | `Incoming Host Header` | Origin 收到的 HTTP `Host` 會是公開 hostname。 |
| `Cache Key Hostname` | `Incoming Host Header` | 不同公開 hostname 分開快取，避免多站台或多 tenant 混用。 |
| Origin protocol | HTTPS | Akamai 到 App Service 之間也走 TLS。 |
| SNI | 跟 `Forward Host Header` 一致 | Origin TLS 憑證要能對應公開 hostname。 |

Auth / Login / OIDC 相關路徑不要快取，至少檢查：

```text
/.well-known/*
/connect/*
/Account/*
/account/*
/api/account/*
```

另外確認 Akamai 或中間 proxy 是否會保留或注入：

- `X-Forwarded-For`
- `X-Forwarded-Proto`
- `X-Forwarded-Host`

<warning>
<p><code>Forward Host Header = Incoming Host Header</code> 的前提是 Azure App Service 已綁定公開 custom domain，且 origin TLS 憑證 CN/SAN、SNI、App Service custom domain binding 都能接受該公開 hostname。</p>
</warning>

## Azure App Service 設定

每個 App Service 都要綁定自己的 public custom domain：

| App Service | Custom domain | 用途 |
| --- | --- | --- |
| AuthServer | `<auth-public-host>` | OpenIddict issuer 與登入頁。 |
| API | `<api-public-host>` | API、Swagger、remote service。 |
| Web / SPA | `<web-public-host>` | 使用者入口。 |

TLS 憑證要注意兩件事：

- App Service 綁定的 TLS 憑證 CN/SAN 必須包含對應 public hostname。
- 如果公開 DNS 指向 Akamai，免費 App Service Managed Certificate 通常不適合拿來做 Akamai 到 App Service 的 end-to-end TLS；可改用匯入憑證、Key Vault、App Service Certificate 或其他可管理憑證來源。

OpenIddict signing / encryption certificate 是另一件事，不等於 HTTPS 憑證。正式環境不要使用 development certificate；Azure App Service 常見做法是上傳憑證並設定：

```text
WEBSITE_LOAD_CERTIFICATES=*
```

如果用 Azure App Service 環境變數覆寫 ABP 設定，階層式 key 建議用雙底線：

```text
App__SelfUrl
App__CorsOrigins
App__RedirectAllowedUrls
AuthServer__Authority
AuthServer__MetaAddress
AuthServer__RequireHttpsMetadata
OpenIddict__Applications__Web__RootUrl
RemoteServices__Default__BaseUrl
```

部署 slot 使用 swap 時，和環境綁定的值要設成 slot setting，避免正式與測試 URL 被交換。

## ABP 設定矩陣

### AuthServer

`AuthServer` 必須以公開 auth hostname 作為自己的對外 URL。

```json
{
  "App": {
    "SelfUrl": "https://<auth-public-host>",
    "CorsOrigins": "https://<web-public-host>,https://<api-public-host>",
    "RedirectAllowedUrls": "https://<web-public-host>,https://<api-public-host>"
  },
  "AuthServer": {
    "RequireHttpsMetadata": "true"
  }
}
```

檢查重點：

- `App:SelfUrl` 不要放 `*.azurewebsites.net`。
- `App:CorsOrigins` 放前端與 Swagger 會實際呼叫 AuthServer 的 public origin。
- `App:RedirectAllowedUrls` 放前端與 Swagger callback 會回來的 public URL。
- OpenIddict application 的 redirect URI / post logout redirect URI 都必須是公開 hostname。

### HttpApi.Host / API

API 要信任公開 AuthServer authority，並把 CORS 開給公開前端。

```json
{
  "App": {
    "SelfUrl": "https://<api-public-host>",
    "CorsOrigins": "https://<web-public-host>"
  },
  "AuthServer": {
    "Authority": "https://<auth-public-host>",
    "MetaAddress": "https://<auth-public-host>",
    "RequireHttpsMetadata": "true"
  }
}
```

檢查重點：

- `AuthServer:Authority` 必須和 OpenIddict discovery document 的 `issuer` 一致。
- 如果專案使用 `AuthServer:MetaAddress`，也使用公開 auth hostname。
- Swagger OAuth client 的 redirect URL 要使用公開 API hostname。

### Web / SPA

MVC / Blazor Server 類型的前端通常會有後端設定：

```json
{
  "App": {
    "SelfUrl": "https://<web-public-host>"
  },
  "AuthServer": {
    "Authority": "https://<auth-public-host>",
    "RequireHttpsMetadata": "true"
  },
  "RemoteServices": {
    "Default": {
      "BaseUrl": "https://<api-public-host>/"
    },
    "AbpAccountPublic": {
      "BaseUrl": "https://<auth-public-host>/"
    }
  }
}
```

Angular、Blazor WASM 或 React 的 OIDC 設定要對齊：

| 前端設定 | 建議值 |
| --- | --- |
| `issuer` / `authority` | `https://<auth-public-host>` |
| `redirectUri` | `https://<web-public-host>` 或框架實際 callback URL |
| `postLogoutRedirectUri` | `https://<web-public-host>` |
| API base URL | `https://<api-public-host>` |

## DbMigrator / Seed Data

ABP 的 `OpenIddictDataSeedContributor` 會依 `OpenIddict:Applications:*:RootUrl` 建立或更新 client redirect URI、post logout redirect URI 與 CORS origins。正式部署前要把 `DbMigrator` 的設定也改成公開 URL。

```json
{
  "OpenIddict": {
    "Applications": {
      "Web": {
        "RootUrl": "https://<web-public-host>"
      },
      "Swagger": {
        "RootUrl": "https://<api-public-host>"
      }
    }
  }
}
```

部署後要做其中一項：

- 重新執行 DbMigrator，讓 OpenIddict client 設定更新。
- 或直接檢查 OpenIddict DB 內的 redirect URI / post logout redirect URI / CORS origins。

檢查 DB 內不應殘留：

```text
localhost
127.0.0.1
*.azurewebsites.net
舊 domain
```

## Forwarded Headers

AuthServer、API、Web 都要啟用 ASP.NET Core `ForwardedHeadersMiddleware`，而且要在 HSTS、HTTPS redirection、authentication、routing 之前。

基本方向：

```C#
using Microsoft.AspNetCore.HttpOverrides;

public override void ConfigureServices(ServiceConfigurationContext context)
{
    context.Services.Configure<ForwardedHeadersOptions>(options =>
    {
        options.ForwardedHeaders =
            ForwardedHeaders.XForwardedFor |
            ForwardedHeaders.XForwardedProto |
            ForwardedHeaders.XForwardedHost;

        // 建議只信任 Akamai / 內部 proxy / App Service 前方可信來源。
        // 依實際網路補 KnownProxies 或 KnownNetworks。
    });
}

public override void OnApplicationInitialization(ApplicationInitializationContext context)
{
    var app = context.GetApplicationBuilder();

    app.UseForwardedHeaders();

    // app.UseHsts();
    // app.UseHttpsRedirection();
    // app.UseRouting();
    // app.UseAuthentication();
}
```

<warning>
<p>不要無條件信任所有 <code>X-Forwarded-*</code> header。若外部使用者能直接連到 origin，又能自行帶 header，可能造成 spoofing。Origin 應搭配 App Service Access Restrictions 或其他網路控制，只允許可信 proxy 進入。</p>
</warning>

## 例外：不得不用 Origin Hostname

如果短期無法讓 App Service 接受公開 hostname，例如 origin TLS 只能吃 `<app-name>.azurewebsites.net`，可以暫時用：

```text
Forward Host Header = Origin Hostname
```

但這不是正式正解，必須補齊：

- Akamai 注入或保留 `X-Forwarded-Host: <public-hostname>`。
- ABP / ASP.NET Core 正確信任 `X-Forwarded-Host` 與 `X-Forwarded-Proto`。
- App Service Authentication / Easy Auth 若有使用，要確認 `forwardProxy` 設定能尊重 `X-Forwarded-Host`。
- Identity provider 的 redirect URI 仍以公開 hostname 為準。
- 重新驗證 `Location`、`Set-Cookie`、OpenIddict discovery document 與前端登入流程。

## 上線驗證

### OpenIddict discovery

打開：

```text
https://<auth-public-host>/.well-known/openid-configuration
```

確認以下欄位都是公開 hostname：

- `issuer`
- `authorization_endpoint`
- `token_endpoint`
- `jwks_uri`
- `end_session_endpoint`

### 登入流程

從前端開始登入，確認：

- browser request 裡的 `redirect_uri` 是 `https://<web-public-host>` 或實際 callback URL。
- 登入成功後不會跳到 `*.azurewebsites.net`。
- Identity provider 沒有因 redirect URI mismatch 擋下。

### Response header

檢查 AuthServer / Web / API response：

- `Location` 不應出現 origin hostname。
- `Set-Cookie` 的 `Domain` 不應指到 origin hostname。
- Cookie 應有合理的 `Secure` / `SameSite` 設定。

### CORS 與 API auth

確認前端 public host 呼叫 API public host：

- OPTIONS preflight 通過。
- 實際 API request 通過。
- 登入後呼叫 `/api/abp/application-configuration`，`currentUser` 正確帶出。

### Akamai 與 scale-out

確認：

- Auth/OIDC 路徑無快取。
- Akamai 到 origin 的 HTTPS handshake 使用公開 hostname SNI 可通過。
- 多 instance 或 restart 後 token validation 正常。
- 若有多 instance，Data Protection keys、Redis / distributed cache、OpenIddict signing/encryption certificate 都已規劃。

## 相關筆記

- [ABP App Settings](ABP-App-Settings.md)
- [Azure App Service Deploy](Azure-App-Service-Deploy.md)
- [Akamai Forward Host Header 對 App Service redirect 與 cookie 的影響](akamai-origin-host-header-app-service.md)

## 參考資料

- [ABP OpenIddict Deployment](https://abp.io/docs/latest/solution-templates/layered-web-application/deployment/openiddict-deployment)
- [ABP Configuring OpenIddict](https://abp.io/docs/latest/deployment/configuring-openiddict)
- [ABP Forwarded Headers](https://abp.io/docs/latest/deployment/forwarded-headers)
- [Akamai TechDocs - Origin Server](https://techdocs.akamai.com/property-mgr/docs/origin-server)
- [Microsoft Learn - Preserve the original HTTP host name between a reverse proxy and its backend web application](https://learn.microsoft.com/en-us/azure/architecture/best-practices/host-name-preservation)
- [Microsoft Learn - Authentication and authorization in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/overview-authentication-authorization)
