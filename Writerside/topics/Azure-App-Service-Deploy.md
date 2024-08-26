# Azure App Service Deploy

第一次直接從 VS 2022 布署到 Azure App Service 時，會遇到一些問題，這邊做一個紀錄。

## 結論
1. 找到專案 AuthServer 內的 authserver.pfx 檔案
2. 找到專案 AuthServer 內的 AuthServerModule.cs 的 `GetSigningCertificate` 方法裡面的 `passPhrase` 變數
3. 在 Azure App Service 的 證書 選擇 `攜帶您自己的憑證` 並上傳 `authserver.pfx` 檔案，其中密碼為 `passPhrase` 變數的值
4. 在 Azure App Service 的 環境變數 中新增 `WEBSITE_LOAD_CERTIFICATES` = `*` ，這樣就可以讓 Azure App Service 讀取到該憑證。

## 其他
修改對應設定，尤其 DbMigrator 的設定，確保執行 Seed Data 時， DB 是正確的值，不然可能要手動修正 DB 與 Redis 的資料。

1. Azure App Service 環境變數 (**部署位置設定** 記得勾起來)
    - ASPNETCORE_ENVIRONMENT (Production, Staging, Dev)
    - Redis:Configuration
    - ConnectionStrings:Default
2. appsetting.{ENVIRONMENT}.json
   - App:SelfUrl
   - App:CorsOrigins
   - App:RedirectAllowedUrls
   - AuthServer:Authority
   - OpenIddict:Applications:{App}:RootUrl
   - RemoteServices:Default:BaseUrl
   - RemoteServices:AbpAccountPublic:BaseUrls

**部署位置設定** 意思是在 Azure App Service 做 Swap 時，設定值會固定在原本的網站，反過來說就是如果沒有打勾，Swap 後設定值會跟著移動。

## 範例
- authserver.pfx
- passPhrase = "xxxxxxxxxxxx"

### AuthServerModule.cs
```C#
private X509Certificate2 GetSigningCertificate(IWebHostEnvironment hostingEnv)
    {
        var fileName = "authserver.pfx";
        var passPhrase = "xxxxxxxxxxxx";
        var file = Path.Combine(hostingEnv.ContentRootPath, fileName);

        if (!File.Exists(file))
        {
            throw new FileNotFoundException($"Signing Certificate couldn't found: {file}");
        }

        return new X509Certificate2(file, passPhrase);
    }
```

## 錯誤訊息
500.30 - ANCM In-Process Start Failure

## 原因
在 Azure App Service 上，OpenIddict 需要使用憑證來簽署 JWT，但 Azure App Service 預設不會讀取專案內的憑證。

## Log
原始程式碼會看不到錯誤 Log，可以修改 Program.cs 來看到詳細錯誤訊息。

```C#
public async static Task<int> Main(string[] args)
    {
    // 新增這段程式碼
        Log.Logger = new LoggerConfiguration()
#if DEBUG
        .MinimumLevel.Debug()
#else
        .MinimumLevel.Information()
#endif
        .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
        .MinimumLevel.Override("Microsoft.EntityFrameworkCore", 
            LogEventLevel.Information)
        .Enrich.FromLogContext()
        .WriteTo.Async(c => c.File("Logs/logs.txt", 
            rollingInterval: RollingInterval.Day))
        .WriteTo.Async(c => c.Console())
        .CreateLogger();

try
        {
            Log.Information("Starting AuthServer.");
// ...
```

利用以上程式碼防止主程序啟動失敗時，連帶 Log 也無法正常輸出。

## 參照
[Publish-an-abpio-project-to-an-azure-AppServices-Error-OpenIddict](https://abp.io/support/questions/5595/Publish-an-abpio-project-to-an-azure-AppServices-Error-OpenIddict)
