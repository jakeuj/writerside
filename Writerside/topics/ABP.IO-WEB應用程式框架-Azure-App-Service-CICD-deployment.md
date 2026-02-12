# ABP.IO Azure App Service CI/CD deployment

> **原文發布日期:** 2022-10-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/21/abp-Azure-App-Service-Github-CICD
> **標籤:** 無

---

筆記下 Azure App Service 部屬中心 CI/CD

## 前言

在 Azure App Service 部屬中心可以選擇部屬方式

- Azure DevOps Repo
  需要在根目錄建立以下檔案來指定起始專案
  .deployment

```
[config]
project = src/TestProject.HttpApi.Host/TestProject.HttpApi.Host.csproj
```

- Github
  需要將自動產生的設定檔案進行以下修改來指定建置專案
  不然會 publish 測試專案導致 appsettings.json 被覆蓋
  - `dotnet build src\MyProject.HttpApi.Host`
  - `dotnet publish src\MyProject.HttpApi.Host`

### yml

```
# Docs for the Azure Web Apps Deploy action: https://github.com/Azure/webapps-deploy
# More GitHub Actions for Azure: https://github.com/Azure/actions

name: Build and deploy ASP.Net Core app to Azure Web App - euorder

on:
  push:
    branches:
      - testing
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up .NET Core
        uses: actions/setup-dotnet@v1
        with:
          dotnet-version: '6.0.x'
          include-prerelease: true

      - name: Build with dotnet
        run: dotnet build src\MyProject.HttpApi.Host --configuration Release

      - name: dotnet publish
        run: dotnet publish src\MyProject.HttpApi.Host -c Release -o ${{env.DOTNET_ROOT}}/myapp

      - name: Upload artifact for deployment job
        uses: actions/upload-artifact@v2
        with:
          name: .net-app
          path: ${{env.DOTNET_ROOT}}/myapp

  deploy:
    runs-on: windows-latest
    needs: build
    environment:
      name: 'testing'
      url: ${{ steps.deploy-to-webapp.outputs.webapp-url }}

    steps:
      - name: Download artifact from build job
        uses: actions/download-artifact@v2
        with:
          name: .net-app

      - name: Deploy to Azure Web App
        id: deploy-to-webapp
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'MyProject'
          slot-name: 'testing'
          publish-profile: ${{ secrets.AZUREAPPSERVICE_PUBLISHPROFILE_ABCDEFG }}
          package: .
```

- DevOps Pipeline
  如果再從 DevOps 設定 CI/CD，則 Azure App Service 部屬中心的設定要拿掉
  統一由 DevOps 這邊的 yaml 檔案來進行 CI/CD 設定

## 錯誤

### Deploy 逾時

```
Command 'starter.cmd "D:\home\site\d ...' was aborted due to no output nor CPU activity for 61 seconds.
You can increase the SCM_COMMAND_IDLE_TIMEOUT app setting
(or WEBJOBS_IDLE_TIMEOUT if this is a WebJob) if needed.
```

[SCM\_COMMAND\_IDLE\_TIMEOUT = 3600](https://www.dotblogs.com.tw/jakeuj/2021/08/30/AzureDevOpsGitRepoCiCdAppService)

### 執行階段錯誤

```
CryptographicException: Access is denied
```

1. 非免費層級 App Service Plan
   [WEBSITE\_LOAD\_USER\_PROFILE=1](https://dotblogs.azurewebsites.net/jakeuj/2022/10/13/OpenIddict-WindowsCryptographicException-Access-is-denied)
2. 免費層級 App Service Plan
   上面那條設定沒用，需要改程式碼 HttpApiHostModule.cs

```
public override void PreConfigureServices(ServiceConfigurationContext context)
{
 // 新增程式碼起始
    var hostingEnvironment = context.Services.GetHostingEnvironment();
    if (hostingEnvironment.IsStaging())
    {
        PreConfigure<AbpOpenIddictAspNetCoreOptions>(options =>
        {
            options.AddDevelopmentEncryptionAndSigningCertificate = false;
        });

        PreConfigure<OpenIddictServerBuilder>(builder =>
        {
            builder.AddEphemeralEncryptionKey();
            builder.AddEphemeralSigningKey();
        });
    }
    // 新增程式碼完成

    PreConfigure<OpenIddictBuilder>(builder =>
    {
        builder.AddValidation(options =>
        {
            options.AddAudiences("TestCiCd");
            options.UseLocalServer();
            options.UseAspNetCore();
        });
    });
}
```

其中 `IsStaging()` 需與 App Service 內的 .Net 環境對應 (或移除此判斷)

## 正規作法

WEBSITE\_LOAD\_CERTIFICATES=\*

大概是設定以上環境變數來允許應用程式訪問到憑證

然後憑證上傳後將指紋複製起來

到程式裡查該指紋的憑證用在原本開發憑證那邊

```
using System;
using System.Linq;
using System.Security.Cryptography.X509Certificates;

string certThumbprint = "E661583E8FABEF4C0BEF694CBC41C28FB81CD870";
bool validOnly = false;

using (X509Store certStore = new X509Store(StoreName.My, StoreLocation.CurrentUser))
{
  certStore.Open(OpenFlags.ReadOnly);

  X509Certificate2Collection certCollection = certStore.Certificates.Find(
                              X509FindType.FindByThumbprint,
                              // Replace below with your certificate's thumbprint
                              certThumbprint,
                              validOnly);
  // Get the first cert with the thumbprint
  X509Certificate2 cert = certCollection.OfType<X509Certificate2>().FirstOrDefault();

  if (cert is null)
      throw new Exception($"Certificate with thumbprint {certThumbprint} was not found");

  // Use certificate
  Console.WriteLine(cert.FriendlyName);

  // Consider to call Dispose() on the certificate after it's being used, available in .NET 4.6 and later
}
```

`cert` 取代下面的 x509

```
public override void PreConfigureServices(ServiceConfigurationContext context)
{
    var hostingEnvironment = context.Services.GetHostingEnvironment();
    var configuration = context.Services.GetConfiguration();

    if (!hostingEnvironment.IsDevelopment())
    {
        PreConfigure<AbpIdentityServerBuilderOptions>(options =>
        {
            options.AddDeveloperSigningCredential = false;
        });

        // add custom signing credential
        var x509 = new X509Certificate2(
            File.ReadAllBytes("openiddict.pfx"),"222d265a-XXXX-XXXX-XXXX-5bf0f201908c");

        PreConfigure<IdentityServerBuilder>(serverBuilder =>
        {
            serverBuilder
                .AddSigningCredential(x509)
                .AddValidationKey(x509);;
        });
    }
}
```

Ref:

- [在代碼中使用 TLS/SSL 證書 - Azure App Service |Microsoft 學習](https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-certificate-in-code#load-certificate-in-windows-apps)
- [OpenIddict WindowsCryptographicException：訪問被拒絕 #3537 |支援中心 |ABP商業 |支援中心](https://support.abp.io/QA/Questions/3537/OpenIddict-WindowsCryptographicException-Access-is-denied)

.NET 環境

```
ASPNETCORE_ENVIRONMENT=Staging
```

[.NET Core 5 Console 泛用主機 依照環境變數讀取對應設定檔 AppSetting | 御用小本本 - 點部落 (dotblogs.azurewebsites.net)](https://dotblogs.azurewebsites.net/jakeuj/2021/06/10/DotNetCoreConsoleAppsettingEnvironment)

### 參照

[Azure 持續部署(CI/CD)至 Azure App Service (DevOps Git Repo) | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/08/30/AzureDevOpsGitRepoCiCdAppService)

[設定連續部署 - Azure App Service | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/app-service/deploy-continuous-deployment?tabs=github)

[Customizing deployments · projectkudu/kudu Wiki (github.com)](https://github.com/projectkudu/kudu/wiki/Customizing-deployments#deploying-a-specific-aspnet-or-aspnet-core-project-file)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- App Service
{ignore-vars="true"}
- Azure
- CI/CD
{ignore-vars="true"}
- deployment
- DevOps
- Github

- 回首頁

---

*本文章從點部落遷移至 Writerside*
