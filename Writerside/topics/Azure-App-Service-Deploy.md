# Azure App Service Deploy

第一次直接從 VS 2022 布署到 Azure App Service 時，會遇到一些問題，這邊做一個紀錄。

## 結論
1. 找到專案 AuthServer 內的 authserver.pfx 檔案
2. 找到專案 AuthServer 內的 AuthServerModule.cs 的 `GetSigningCertificate` 方法裡面的 `passPhrase` 變數
3. 在 Azure App Service 的 證書 選擇 `攜帶您自己的憑證` 並上傳 `authserver.pfx` 檔案，其中密碼為 `passPhrase` 變數的值
4. 在 Azure App Service 的 環境變數 中新增 `WEBSITE_LOAD_CERTIFICATES` = `*` ，這樣就可以讓 Azure App Service 讀取到該憑證。

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
