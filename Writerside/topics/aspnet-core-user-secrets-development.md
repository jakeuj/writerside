# ASP.NET Core User Secrets 只在 Development 載入

ASP.NET Core Web App 使用 `WebApplication.CreateBuilder(args)` 時，

預設組態會在 `EnvironmentName` 為 `Development` 時呼叫 `AddUserSecrets`。

所以一般 Web 專案的重點不是把秘密寫進 `appsettings.json`，

而是先建立 `UserSecretsId`，再用 `dotnet user-secrets` 管理本機開發秘密。

<warning>
永遠不要將密碼或其他敏感資料儲存在原始程式碼或組態檔中。<br/>生產秘密不應該用於開發或測試<br/>不應將秘密與應用程式一起部署<br/>生產秘密應該透過 Azure Key Vault 這類受控制的秘密保存庫來存取。
</warning>

## 重點判斷

- `User Secrets` 適合本機開發，不適合測試、Staging 或 Production。
- 使用 `Microsoft.NET.Sdk.Web` 的 ASP.NET Core Web 專案，通常不需要在 `Program.cs` 手動補 `AddUserSecrets`。
- 如果是 Console App、Worker Service、自訂 `ConfigurationBuilder`，或你覆寫了預設設定載入流程，才需要自己判斷環境後呼叫 `AddUserSecrets`。
- `User Secrets` 不會加密，只是把本機開發用秘密放在使用者設定檔底下，避免簽入 Git。

## 建立 User Secrets

先在專案目錄初始化 `UserSecretsId`：

```bash
dotnet user-secrets init
```

這會在 `.csproj` 加入類似下列設定：

```xml
<PropertyGroup>
  <UserSecretsId>aspnet-core-user-secrets-demo</UserSecretsId>
</PropertyGroup>
```

再把本機開發用的秘密寫進 Secret Manager：

```bash
dotnet user-secrets set "Movies:ServiceApiKey" "<api-key>"
dotnet user-secrets set "ConnectionStrings:Default" "<local-development-connection-string>"
```

確認目前專案底下有哪些秘密：

```bash
dotnet user-secrets list
```

## 一般 Web 專案不必手動加

Minimal API 或 ASP.NET Core Web 專案常見的啟動程式如下：

```C#
var builder = WebApplication.CreateBuilder(args);

var apiKey = builder.Configuration["Movies:ServiceApiKey"];

var app = builder.Build();

app.MapGet("/", () => apiKey);

app.Run();
```

只要目前環境是 `Development`，`WebApplication.CreateBuilder(args)` 預設會把 User Secrets 加進組態來源。也就是說，開發機讀得到 `dotnet user-secrets set` 寫入的值，但部署到非 Development 環境時不會自動讀取同一份 User Secrets。

## 何時需要手動呼叫 AddUserSecrets {#when-to-call-addusersecrets}

預設 Web 專案不必重複註冊。只有在你自己建立 `ConfigurationBuilder`，或在 Console App、Worker Service 等非預設 Web 組態流程中使用 User Secrets 時，才需要把判斷寫清楚：

```C#
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;

var environmentName = Environment.GetEnvironmentVariable("DOTNET_ENVIRONMENT")
    ?? Environments.Production;

var configurationBuilder = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .AddJsonFile($"appsettings.{environmentName}.json", optional: true, reloadOnChange: true)
    .AddEnvironmentVariables();

if (environmentName == Environments.Development)
{
    configurationBuilder.AddUserSecrets<Program>();
}

var configuration = configurationBuilder.Build();
```

這段的重點是：只有 `EnvironmentName` 等於 `Development` 時才呼叫 `AddUserSecrets`，避免其他環境意外依賴開發機上的秘密。

非 `Microsoft.NET.Sdk.Web` 專案如果找不到 `AddUserSecrets`，先安裝 User Secrets 組態套件：

```bash
dotnet add package Microsoft.Extensions.Configuration.UserSecrets
```

## 讀取設定值

User Secrets 進入組態系統後，讀法和 `appsettings.json`、環境變數相同：

```C#
var apiKey = builder.Configuration["Movies:ServiceApiKey"];
var connectionString = builder.Configuration.GetConnectionString("Default");
```

如果要綁定成 options 類別，也可以照一般 Options pattern 寫法處理：

```C#
builder.Services.Configure<MovieOptions>(
    builder.Configuration.GetSection("Movies"));
```

## 補充說明

- Production 建議改用環境變數、部署平台的 secret 管理功能，或 Azure Key Vault 這類受控秘密保存庫。
- `dotnet user-secrets` 的值跟專案的 `UserSecretsId` 綁定；不同專案如果需要共用同一組開發秘密，可以使用相同的 `UserSecretsId`，但要刻意管理，避免混淆。

## Rider

![rider_user_secrets.png](rider_user_secrets.png)
## 參考資料

- [在 ASP.NET Core 的開發中安全儲存應用程式秘密](https://learn.microsoft.com/zh-tw/aspnet/core/security/app-secrets?view=aspnetcore-10.0&tabs=windows)
- [Rider .NET User Secrets](https://blog.jetbrains.com/dotnet/2023/01/17/securing-sensitive-information-with-net-user-secrets/)
