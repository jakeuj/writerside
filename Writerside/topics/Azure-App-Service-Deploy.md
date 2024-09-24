# Azure App Service Deploy

第一次直接從 VS 2022 布署到 Azure App Service 時，會遇到一些問題，這邊做一個紀錄。

## 結論
1. 在 Azure App Service 的 環境變數 中新增 `ASPNETCORE_ENVIRONMENT` = `Dev` ，這樣就可以讓專案知道目前的環境是 `Dev`。
2. 在 Azure App Service 的 環境變數 中新增 `WEBSITE_LOAD_CERTIFICATES` = `*` ，這樣就可以讓 Azure App Service 讀取到該憑證。
3. 找到專案 AuthServer 內的 authserver.pfx 檔案
4. 找到專案 AuthServer 內的 AuthServerModule.cs 的 `GetSigningCertificate` 方法裡面的 `passPhrase` 變數
5. 在 Azure App Service 的 證書 選擇 `攜帶您自己的憑證` 並上傳 `authserver.pfx` 檔案，其中密碼為 `passPhrase` 變數的值

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

## CI/CD
在部屬中心可以選擇 Github Actions，這樣就可以自動化部屬。
其中要注意修改 Github Actions 的設定檔，確保部屬時有正確的設定。
1. 安裝 Volo.Abp.Studio.Cli
2. 安裝 ABP libs
3. 指定 PROJECT_PATH (因為一個方案內包含多個專案)
4. `dotnet build` & `dotnet publish` 指令 (指定 `${{ env.PROJECT_PATH }}`)
5. `dotnet publish -o` 指令須加上雙引號，不然會報錯

   這個錯誤是由於命令行中包含了空格，導致 MSBuild 將 `C:\Program Files\dotnet/myapp` 路徑解析成多個參數。

   MSBuild 無法理解帶有空格的路徑，除非將它們用引號括起來。

branch_project(dev).yml
```YAML
# Docs for the Azure Web Apps Deploy action: https://github.com/Azure/webapps-deploy
# More GitHub Actions for Azure: https://github.com/Azure/actions

name: Build and deploy ASP.Net Core app to Azure Web App - BookStore

on:
  push:
    branches:
      - cicd/dev/web
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest

    env:
      PROJECT_PATH: 'src\BookStore.Web'  # 參數化的路徑

    steps:
      - uses: actions/checkout@v4

      - name: Set up .NET Core
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.x'

      - name: Install ABP CLI
        run: dotnet tool install -g Volo.Abp.Studio.Cli

      - name: Install ABP libs
        run: abp install-libs -wd ${{ env.PROJECT_PATH }}

      - name: Build with dotnet
        run: dotnet build ${{ env.PROJECT_PATH }} --configuration Release

      - name: dotnet publish
        run: dotnet publish ${{ env.PROJECT_PATH }} -c Release -o "${{env.DOTNET_ROOT}}/myapp"

      - name: Upload artifact for deployment job
        uses: actions/upload-artifact@v4
        with:
          name: .net-app
          path: ${{env.DOTNET_ROOT}}/myapp

  deploy:
    runs-on: windows-latest
    needs: build
    environment:
      name: 'dev'
      url: ${{ steps.deploy-to-webapp.outputs.webapp-url }}
    permissions:
      id-token: write #This is required for requesting the JWT

    steps:
      - name: Download artifact from build job
        uses: actions/download-artifact@v4
        with:
          name: .net-app
      
      - name: Login to Azure
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZUREAPPSERVICE_CLIENTID_XXX }}
          tenant-id: ${{ secrets.AZUREAPPSERVICE_TENANTID_XXX }}
          subscription-id: ${{ secrets.AZUREAPPSERVICE_SUBSCRIPTIONID_XXX }}

      - name: Deploy to Azure Web App
        id: deploy-to-webapp
        uses: azure/webapps-deploy@v3
        with:
          app-name: 'BookStore'
          slot-name: 'dev'
          package: .
          
```

## 參照
[Publish-an-abpio-project-to-an-azure-AppServices-Error-OpenIddict](https://abp.io/support/questions/5595/Publish-an-abpio-project-to-an-azure-AppServices-Error-OpenIddict)
