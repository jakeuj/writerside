# CI/CD

在部屬中心可以選擇 Github Actions，這樣就可以自動化部屬。

## OpenIddict 憑證問題
OpenIddict 需要使用憑證來簽署 JWT，但 Azure App Service 預設不會讀取專案內的憑證。

目前已知三種方式解決這個問題：
1. 將憑證放在 Azure Key Vault：未研究
2. 將憑證放在 Azure App Service 的憑證中
   - 這要求 App Service Plan 處於基本層或更高層
   - 須設定環境變數：WEBSITE_LOAD_CERTIFICATES=*
3. 將憑證放在專案中，並在 Azure App Service 中指定憑證
   - 應用程式 App Service Plan 位於免費或共享層即可使用
   - 須設定環境變數：WEBSITE_LOAD_USER_PROFILE=1

## 範例
這邊透過修改原本範本處理憑證的程式碼，來支援 Azure App Service 透過指紋來讀取憑證。

原本 AuthServerModule.cs 中的 PreConfigureServices 方法
```C#
serverBuilder.AddProductionEncryptionAndSigningCertificate(
   "openiddict.pfx", "password");
```

建立新擴充方法
```C#
public static class OpenIddictServerBuilderExtensions
{
    public static OpenIddictServerBuilder 
         AddProductionEncryptionAndSigningCertificate(
              this OpenIddictServerBuilder builder,
              string fileName,
              string passPhrase,
              string? certThumbprint)
    {
        var certificate = 
            LoadCertificate(fileName, passPhrase, certThumbprint);

        if (certificate == null)
        {
            throw new FileNotFoundException(
               $"Signing Certificate couldn't be found: {fileName} or with thumbprint {certThumbprint}");
        }

        builder.AddSigningCertificate(certificate);
        builder.AddEncryptionCertificate(certificate);
        return builder;
    }

    private static X509Certificate2? LoadCertificate(
         string fileName, string passPhrase, string? certThumbprint)
    {
        if (!string.IsNullOrEmpty(certThumbprint))
        {
            var certificate = 
               GetCertificateByThumbprint(certThumbprint);
            if (certificate != null)
            {
                return certificate;
            }
        }

        return File.Exists(fileName) ? 
            new X509Certificate2(fileName, passPhrase) : null;
    }

    private static X509Certificate2? GetCertificateByThumbprint(
         string certThumbprint)
    {
        using var certStore = 
            new X509Store(StoreName.My, StoreLocation.CurrentUser);
        certStore.Open(OpenFlags.ReadOnly);

        var certCollection = certStore.Certificates.Find(
            X509FindType.FindByThumbprint,
            certThumbprint,
            validOnly: false);

        return Enumerable.OfType<X509Certificate2>(certCollection)
            .FirstOrDefault();
    }
}
```

修改 AuthServerModule.cs 中的 PreConfigureServices 方法
```C#
serverBuilder.AddProductionEncryptionAndSigningCertificate(
   "openiddict.pfx", "password",
   configuration["OpenIddict:Thumbprint"]);
```

其中 `Thumbprint` 可以透過本地執行產生的 openiddict.pfx 上傳到 Azure App Service 憑證後取得指紋。

之後 Azure App Service 裡面就不需要有 openiddict.pfx 檔案，會透過指紋去找到正確的憑證。

這裡的問題是憑證過期之後，需要重新上傳憑證，並且更新指紋。

可能要改用第三種直接允許讀憑證檔案，然後從程式檢查憑證過期，自動重新產生新憑證。

[configure-ssl-certificate-in-code](https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-certificate-in-code?tabs=windows)

[setting-up-abp-with-openiddict-on-azure-app-services](https://brianmeeker.me/2022/08/29/setting-up-abp-with-openiddict-on-azure-app-services/)

## Github Actions
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

## Auth server 快取版本

```YAML
# Docs for the Azure Web Apps Deploy action: https://github.com/Azure/webapps-deploy
# More GitHub Actions for Azure: https://github.com/Azure/actions

name: Build and deploy ASP.Net Core app to Azure Web App - BookStore

on:
  push:
    branches:
      - cicd/dev/auth
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest

    env:
      PROJECT_PATH: 'src\BookStore.AuthServer'  # 參數化的路徑

    steps:
      - uses: actions/checkout@v4

      - name: Set up .NET Core
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.x'
          cache: true
          cache-dependency-path: '**/package-lock.json'
      - run: dotnet restore --locked-mode

      - name: Install ABP CLI
        run: dotnet tool install -g Volo.Abp.Studio.Cli

      - name: Install ABP libs
        run: abp install-libs -wd ${{ env.PROJECT_PATH }}

      - name: Build with dotnet
        run: dotnet build ${{ env.PROJECT_PATH }} --configuration Release

      - name: dotnet publish
        run: dotnet publish ${{ env.PROJECT_PATH }} -c Release -r win-x86 -o "${{env.DOTNET_ROOT}}/myapp"

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

## Host API
API 不需要 wwwroot libs，所以可以不用安裝 ABP libs。

```YAML
# Docs for the Azure Web Apps Deploy action: https://github.com/Azure/webapps-deploy
# More GitHub Actions for Azure: https://github.com/Azure/actions

name: Build and deploy ASP.Net Core app to Azure Web App - BookStore

on:
  push:
    branches:
      - cicd/dev/api
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest

    env:
      PROJECT_PATH: 'src\BookStore.HttpApi.Host'  # 參數化的路徑

    steps:
      - uses: actions/checkout@v4

      - name: Set up .NET Core
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.x'
          cache: true
          cache-dependency-path: '**/package-lock.json'
      - run: dotnet restore --locked-mode

      - name: Build with dotnet
        run: dotnet build ${{ env.PROJECT_PATH }} --configuration Release

      - name: dotnet publish
        run: dotnet publish ${{ env.PROJECT_PATH }} -c Release -r win-x86 -o "${{env.DOTNET_ROOT}}/myapp"

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